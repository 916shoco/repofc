import discord
from discord.ext import commands

id_cargos = {
    "comprar": 1198347965920706678,  # ID do cargo para compras
    "duvidas": 1198347965920706672,  # ID do cargo para dúvidas
    "denunciar": 1198347965920706674,  # ID do cargo para denúncias
    "parceria": 1198347965912330274,  # ID do cargo para parcerias
    "patrocinio": 1198347965920706678  # ID do cargo para patrocínios
}

class Dropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(value="comprar", label="Comprar", emoji="👋"),
            discord.SelectOption(value="duvidas", label="Duvidas", emoji="❓"),
            discord.SelectOption(value="denunciar", label="Denunciar", emoji="👮"),
            discord.SelectOption(value="parceria", label="Parcerias", emoji="🤝"),
            discord.SelectOption(value="patrocinio", label="Patrocinio", emoji="🚀"),
        ]
        super().__init__(
            placeholder="Selecione uma opção...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="persistent_view:dropdown_help"
        )

    async def callback(self, interaction: discord.Interaction):
        option = self.values[0]

        if option not in id_cargos:
            return

        category = option.capitalize()
        cargo_id = id_cargos[option]

        thread_name = f"{interaction.user.name} - {category}"
        thread = await interaction.channel.create_thread(
            name=thread_name,
            reason=f"Thread criada por {interaction.user.name} ({interaction.user.id})",
            auto_archive_duration=1440  # 24 horas
        )

        await interaction.response.send_message(
            f"Olá {interaction.user.mention}, seu ticket foi aberto em {thread.mention}! Cargo correspondente: <@&{cargo_id}>",
            ephemeral=True
        )

        await thread.send(f"Ticket criado por {interaction.user.mention} na categoria {category}. Aguarde atendimento! Cargo correspondente: <@&{cargo_id}>")
        await thread.send(view=CloseTicket(cargo_id, interaction.user.id))  # Passa o ID do criador da thread

class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Dropdown())

class CloseTicket(discord.ui.View):
    def __init__(self, cargo_id, thread_creator_id):
        super().__init__(timeout=None)
        self.cargo_id = cargo_id
        self.thread_creator_id = thread_creator_id

    @discord.ui.button(label="Fechar Ticket", style=discord.ButtonStyle.red, emoji="🔒", custom_id='CloseTicket')
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.thread_creator_id or any(role.id == self.cargo_id for role in interaction.user.roles):
            await interaction.response.send_message(f"O ticket foi arquivado por {interaction.user.mention}, obrigado por entrar em contato!")
            await interaction.channel.edit(archived=True, locked=True)
        else:
            await interaction.response.send_message("Isso não pode ser feito aqui...")

class Ticket(commands.Cog, name="ticket"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="painel",
        description="Ticket painel."
    )
    @commands.is_owner()
    async def painel(self, ctx: commands.Context):
        embed = discord.Embed(
            colour=discord.Color.dark_blue(),
            title="Suporte Ticket",
            description="Boas vindas ao nosso suporte! Neste chat você pode solicitar seu atendimento rápido e eficaz.\n\nEntão clique abaixo na categoria desejada e aguarde nosso suporte!"
        )
        embed.set_image(url="https://media.discordapp.net/attachments/1191599069102092389/1203380243843252284/Suporte.png?ex=65d0e22f&is=65be6d2f&hm=46c7622f6bd3cd278cb30a7c506d245c6c1503c5ee94b345e9e1d51bbf6d394a&=&format=webp&quality=lossless&width=1440&height=480")
        await ctx.send(embed=embed)
        await ctx.send(view=DropdownView())

async def setup(bot):
    bot.add_view(DropdownView())
    await bot.add_cog(Ticket(bot))
