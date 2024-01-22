import random

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks


class Choice(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Cara", style=discord.ButtonStyle.blurple)
    async def confirm(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        self.value = "cara"
        self.stop()

    @discord.ui.button(label="Coroa", style=discord.ButtonStyle.blurple)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = "coroa"
        self.stop()


class RockPaperScissors(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Tesoura", description="Você escolheu tesoura.", emoji="✂"
            ),
            discord.SelectOption(
                label="Pedra", description="Você escolheu pedra.", emoji="🪨"
            ),
            discord.SelectOption(
                label="Papel", description="Você escolheu papel.", emoji="🧻"
            ),
        ]
        super().__init__(
            placeholder="Choose...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        choices = {
            "pedra": 0,
            "papel": 1,
            "tesoura": 2,
        }
        user_choice = self.values[0].lower()
        user_choice_index = choices[user_choice]

        bot_choice = random.choice(list(choices.keys()))
        bot_choice_index = choices[bot_choice]

        result_embed = discord.Embed(color=0x9C84EF)
        result_embed.set_author(
            name=interaction.user.name, icon_url=interaction.user.avatar.url
        )

        if user_choice_index == bot_choice_index:
            result_embed.description = f"**Uau um empate!**\nVocê escolheu {user_choice} e eu escolhi {bot_choice}."
            result_embed.colour = 0xF59E42
        elif user_choice_index == 0 and bot_choice_index == 2:
            result_embed.description = f"**Você ganhou!**\nVocê escolheu {user_choice} e eu escolhi {bot_choice}."
            result_embed.colour = 0x9C84EF
        elif user_choice_index == 1 and bot_choice_index == 0:
            result_embed.description = f"**Você ganhou!**\nVocê escolheu {user_choice} e eu escolhi {bot_choice}."
            result_embed.colour = 0x9C84EF
        elif user_choice_index == 2 and bot_choice_index == 1:
            result_embed.description = f"**Você ganhou!**\nVocê escolheu {user_choice} e eu escolhi {bot_choice}."
            result_embed.colour = 0x9C84EF
        else:
            result_embed.description = (
                f"**Eu ganhei!**\nVocê escolheu {user_choice} e eu escolhi {bot_choice}."
            )
            result_embed.colour = 0xE02B2B
        await interaction.response.edit_message(
            embed=result_embed, content=None, view=None
        )


class RockPaperScissorsView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(RockPaperScissors())


class Fun(commands.Cog, name="fun"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="randomfact", description="Ganhe um fato aleatorio.")
    @checks.not_blacklisted()
    async def randomfact(self, context: Context) -> None:
        """
        Get a random fact.

        :param context: The hybrid command context.
        """
        # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://uselessfacts.jsph.pl/random.json?language=en"
            ) as request:
                if request.status == 200:
                    data = await request.json()
                    embed = discord.Embed(description=data["text"], color=0xD75BF4)
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B,
                    )
                await context.send(embed=embed)

    @commands.hybrid_command(
        name="coinflip", description="Famoso coinflip."
    )
    @checks.not_blacklisted()
    async def coinflip(self, context: Context) -> None:
        """
        Make a coin flip, but give your bet before.

        :param context: The hybrid command context.
        """
        buttons = Choice()
        embed = discord.Embed(description="What is your bet?", color=0x9C84EF)
        message = await context.send(embed=embed, view=buttons)
        await buttons.wait()  # We wait for the user to click a button.
        result = random.choice(["cara", "coroa"])
        if buttons.value == result:
            embed = discord.Embed(
                description=f"Correto! você escolheu `{buttons.value}` e a moeda caiu em `{result}`.",
                color=0x9C84EF,
            )
        else:
            embed = discord.Embed(
                description=f"Woops! não foi dessa vez você escolheu `{buttons.value}` e a moeda girou para `{result}`, boa sorte na proxima!",
                color=0xE02B2B,
            )
        await message.edit(embed=embed, view=None, content=None)

    @commands.hybrid_command(
        name="rps", description="Pedra papel tesoura contra o bot."
    )
    @checks.not_blacklisted()
    async def rock_paper_scissors(self, context: Context) -> None:
        """
        Play the rock paper scissors game against the bot.

        :param context: The hybrid command context.
        """
        view = RockPaperScissorsView()
        await context.send("Porfavor, faça tua escolha", view=view)


async def setup(bot):
    await bot.add_cog(Fun(bot))
