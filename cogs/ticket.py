import discord
from discord.ext import commands

from helpers import checks, db_manager

id_cargo_atendente = 1198347965920706672

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
        if self.values[0] == "comprar":
            await interaction.response.send_message("Compre cargos e vip", ephemeral=True, view=CreateTicket())
        elif self.values[0] == "parceria":
            await interaction.response.send_message("Faça parceria com nosso servidor", ephemeral=True, view=CreateTicket())
        elif self.values[0] == "patrocinio":
            await interaction.response.send_message("Solicite esse ticket para fazer seu patrocinio", ephemeral=True, view=CreateTicket())
        elif self.values[0] == "duvidas":
            await interaction.response.send_message("Tire sua duvida sobre qualquer coisa aqui", ephemeral=True, view=CreateTicket())
        elif self.values[0] == "denunciar":
            await interaction.response.send_message("Solicite esse ticket para fazer uma denuncia", ephemeral=True, view=CreateTicket())

class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Dropdown())

class CreateTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.value = None

    @discord.ui.button(label="Abrir Ticket", style=discord.ButtonStyle.blurple, emoji="➕")
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        self.stop()

        ticket = None
        for thread in interaction.channel.threads:
            if f"{interaction.user.id}" in thread.name:
                if thread.archived:
                    ticket = thread
                else:
                    await interaction.response.send_message(ephemeral=True, content=f"Você já tem um atendimento em andamento!")
                    return

        async for thread in interaction.channel.archived_threads(private=True):
            if f"{interaction.user.id}" in thread.name:
                if thread.archived:
                    ticket = thread
                else:
                    await interaction.edit_original_response(content=f"Você já tem um atendimento em andamento!", view=None)
                    return
        
        if ticket is not None:
            await ticket.edit(archived=False, locked=False)
            await ticket.edit(name=f"{interaction.user.name} ({interaction.user.id})", auto_archive_duration=10080, invitable=False)
            # Adiciona o botão "Fechar Ticket" diretamente à vista
        else:
            ticket = await interaction.channel.create_thread(name=f"{interaction.user.name} ({interaction.user.id})", auto_archive_duration=10080)
            await ticket.edit(invitable=False)

        await interaction.response.send_message(ephemeral=True, content=f"Criei um ticket para você! {ticket.mention}")
        await ticket.send(f"📩  **|** || {interaction.user.mention} <@&1198347965920706672> ||  Ticket criado com sucesso! Envie todas as informações possíveis sobre o seu caso e aguarde até que um atendente responda.\n\n Após a sua questão ser resolvida, clique em ""Fechar Ticket"" para encerrar o atendimento!")
        await ticket.send(view=Close_Ticket())

class Close_Ticket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Fechar Ticket", style=discord.ButtonStyle.red, emoji="🔒", custom_id='Close_Ticket')
    async def close_ticket(self, interaction:discord.Interaction, button:discord.ui.Button):
        mod = interaction.guild.get_role(id_cargo_atendente)
        if str(interaction.user.id) in interaction.channel.name or mod in interaction.author.roles:
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
    @checks.is_owner()
    async def painel(self, ctx: commands.Context):
        embed = discord.Embed(
            colour=discord.Color.pink(),
            title="Suporte Ticket",
            description="Boas vindas ao nosso suporte! Neste chat você pode solicitar seu atendimento rápido e eficaz.\n\nEntão clique abaixo na categoria desejada e aguarde nosso suporte!"
        )
        embed.set_image(url="https://media.discordapp.net/attachments/1162586160934158376/1165362186772824216/569_Sem_Titulo_20230817224211.png?format=webp")
        await ctx.send(embed=embed)
        await ctx.send(view=DropdownView())

async def setup(bot):
    bot.add_view(DropdownView())
    bot.add_view(Close_Ticket())
    await bot.add_cog(Ticket(bot))