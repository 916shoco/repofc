import os
import discord
from discord.ext import commands
import json

from helpers import checks

class Loja(commands.Cog, name="loja"):
    def __init__(self, bot):
        self.bot = bot
        self.button_to_role = {
            "Ajhin_icon": 1198347965841014906,
            "DrawSword_icon": 1198347965828444252,
            "Fame_icon": 1198347965828444251,
            "Fiend_icon": 1198347965828444253,
            "Hunters_icon": 1198347965828444254,
            "Knight_icon": 1198347965828444259,
            "Scavenger_icon": 1198347965811671049,
            "Whitetiger_icon": 1198347965811671048,
            "Kuromi_icon": 1198347965857808396,
            "MyMelody_icon": 1198347965857808395,
            "Cinnamonroll_icon": 1198347965857808394,
            "HelloKitty_icon": 1198347965841014913,
            "Pompompurin_icon": 1198347965857808397
        }
        self.embed_message_id = None

    async def create_embed(self):
        embed = discord.Embed(title="Loja de Cargos", description="Reaja aos ícones abaixo para obter os cargos correspondentes.", color=0x9C84EF)
        embed.add_field(name="Ícones Solo Levelling", value="<:Ajhin_icon:1206984941385158707> <@&1198347965841014906>\n<:DrawSword_icon:1206984933084766218> <@&1198347965828444252>\n<:Fame_icon:1206984929901285466> <@&1198347965828444251>\n<:Fiend_icon:1206986114523463790> <@&1198347965828444253>\n<:Hunters_icon:1206984935722713150> <@&1198347965828444254>\n<:Knight_icon:1206984938751004752> <@&1198347965828444259>\n<:Scavenger_icon:1206984926747037796> <@&1198347965811671049>\n<:Whitetiger_icon:1206984923194597417> <@&1198347965811671048>", inline=False)
        embed.add_field(name="Ícones Sanrio", value="<:Kuromi_icon:1206984853351047228> <@&1198347965857808396>\n<:MyMelody_icon:1206984855674683452> <@&1198347965857808395>\n<:Cinnamonroll_icon:1206984782081429589> <@&1198347965857808394>\n<:HelloKitty_icon:1206984536991203408> <@&1198347965841014913>\n<:Pompompurin_icon:1206984857746677810> <@&1198347965857808397>", inline=False)
        return embed

    @commands.command(
    name="embed_loja",
    description="Cria e envia a embed da loja de cargos.",
    )
    @checks.is_owner()
    async def embed_loja(self, ctx):
        if self.embed_message_id is None:
            embed = await self.create_embed()
            message = await ctx.send(embed=embed)
            self.embed_message_id = message.id
            for emoji in self.button_to_role.keys():
                emoji_object = discord.utils.get(self.bot.emojis, name=emoji)
                if emoji_object is not None:
                    await message.add_reaction(emoji_object)
            
            # Salva o ID da mensagem da embed no arquivo
            with open("embed_message_id.json", "w") as file:
                data = {"message_id": self.embed_message_id}
                json.dump(data, file)
        else:
            # Carrega a mensagem da embed existente
            message = await ctx.fetch_message(self.embed_message_id)
            await message.edit(embed=await self.create_embed())

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload, interaction: discord.Interaction):
        if payload.message_id == self.embed_message_id:
            guild = self.bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if member is None:
                member = await guild.fetch_member(payload.user_id)
            if member is None:
                return

            if payload.user_id == self.bot.user.id:  # Verifica se o autor da reação é o próprio bot
                return

            role_id = self.button_to_role.get(payload.emoji.name)
            if role_id is None:
                return

            role = guild.get_role(role_id)
            if role is None:
                return

            try:
                with open("loja.json", "r") as file:
                    data = json.load(file)
            except json.decoder.JSONDecodeError:
                data = {"users": {}}

            user_id = str(member.id)
            if user_id not in data["users"]:
                data["users"][user_id] = []

            # Remove todos os cargos anteriores da loja
            for old_role_id in data["users"][user_id]:
                old_role = guild.get_role(old_role_id)
                if old_role is not None:
                    await member.remove_roles(old_role)

            # Adiciona o novo cargo
            if role not in member.roles:  # Verifica se o usuário não possui o cargo no perfil
                if role_id in data["users"][user_id]:  # Verifica se o usuário comprou o cargo na loja.json
                    await member.add_roles(role)
                    await interaction.response.send_message(f"Você recebeu o cargo {role.name} da loja!", ephemeral=True)
                else:
                    await interaction.response.send_message("Você ainda não comprou esse cargo da loja.", ephemeral=True)
            else:
                await interaction.response.send_message("Você já possui esse cargo.", ephemeral=True)

            with open("loja.json", "w") as file:
                json.dump(data, file, indent=4)

    @commands.hybrid_command(
        name="add_cargo",
        description="Adiciona um cargo a um usuário.",
    )
    @checks.is_owner()
    async def add_cargo(self, ctx, user: discord.Member, cargo: discord.Role):
        try:
            with open("loja.json", "r") as file:
                data = json.load(file)
        except json.decoder.JSONDecodeError:
            data = {"users": {}}

        user_id = str(user.id)
        if user_id not in data["users"]:
            data["users"][user_id] = []

        if cargo.id not in data["users"][user_id]:
            await user.add_roles(cargo)
            data["users"][user_id].append(cargo.id)
            await ctx.send(f"Você adicionou o cargo {cargo.name} para {user.name}!")
        else:
            await ctx.send(f"{user.name} já possui esse cargo.")

        with open("loja.json", "w") as file:
            json.dump(data, file, indent=4)


    @commands.Cog.listener()
    async def on_ready(self):
        try:
            with open("embed_message_id.json", "r") as file:
                data = json.load(file)
                self.embed_message_id = data["message_id"]
        except FileNotFoundError:
            self.embed_message_id = None
# Concertar o ephemeral das linha 89 e 92

async def setup(bot):
    await bot.add_cog(Loja(bot))
