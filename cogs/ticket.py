import discord
from discord.ext import commands
import asyncio

from discord.ui import Button, button, View
from helpers import checks


class CreateButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="Crie um Ticket",style=discord.ButtonStyle.blurple, emoji="🎫",custom_id="ticketopen")
    async def ticket(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        category: discord.CategoryChannel = discord.utils.get(interaction.guild.categories, id=1139673442380152922)
        for ch in category.text_channels:
            if ch.topic == f"{interaction.user.id} Não selecione o topico nesse canal!":
                await interaction.followup.send("Você ja tem um ticket aberto em {0}".format(ch.mention), ephemeral=True)
                return
            
        r1: discord.Role = interaction.guild.get_role(1064393279682129960)
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            r1: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True),
            interaction.user: discord.PermissionOverwrite(read_messages = True, send_messages=True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages = True, send_messages=True)
        }
        channel = await category.create_text_channel(
            name=str(interaction.user),
            topic=f"{interaction.user.id} Não selecione o topico nesse canal!",
            overwrites=overwrites
        )
        await channel.send(
            embed=discord.Embed(
                title="ticket test",
                description="Esse e somente o teste",
                color = discord.Color.green()
            ),
            view = CloseButton()
        )
        await interaction.followup.send(
            embed= discord.Embed(
                description = "Ticket criado em {0}".format(channel.mention),
                color = discord.Color.blurple()
            )
        )

class CloseButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="close the ticket",style=discord.ButtonStyle.red,custom_id="closeticket",emoji="🔒")
    async def close(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)

        await interaction.channel.send("fechando o ticket em 3 segundos")

        await asyncio.sleep(3)
        
        category: discord.CategoryChannel = discord.utils.get(interaction.guild.categories, id = 1139673442380152922)
        r1: discord.Role = interaction.guild.get_role(1064393279682129960)
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            r1: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True),
            interaction.user: discord.PermissionOverwrite(read_messages = True, send_messages=True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages = True, send_messages=True)
        }

        await interaction.channel.edit(category=category)
        await interaction.channel.send(
            embed = discord.Embed(
                description="Ticket fechado!",
                color= discord.Color.red()
            ),
            view = TrashButton()
        )

class TrashButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="delete o ticket", style=discord.ButtonStyle.red, emoji="🗑️", custom_id="trash")
    async def trash(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()
        await interaction.channel.send("Deletando o ticket em 3 segundos")
        await asyncio.sleep(3)

        await interaction.channel.delete()

class Ticket(commands.Cog, name="ticket"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
            name="ticket",
            description="Pelo amor o nome e auto explicativo.",
        )
    @checks.not_blacklisted()
    @checks.is_owner()
    async def ticket(self, ctx):
        await ctx.send(
            embed = discord.Embed(
                description="Aperta no botão para criar o ticket cabeça de vento"
            ),
            view = CreateButton()
        )

async def setup(bot):
    await bot.add_cog(Ticket(bot))
