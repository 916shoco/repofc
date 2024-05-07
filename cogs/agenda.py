import discord
from discord.ext import commands

class Agenda(commands.Cog, name="agenda"):
    def __init__(self, bot):
        self.bot = bot
        self.agendas = {}

    @commands.hybrid_command()
    async def agenda(self, ctx, *, conteudo):
        if ctx.author.id in self.agendas: 
            agenda_atual = self.agendas[ctx.author.id]
        else:
            agenda_atual = " "

        agenda_atual += conteudo + "\n"
        self.agendas[ctx.author.id] = agenda_atual

        await ctx.send(f"Conteudo adicionado a sua agenda: \n{conteudo}")

    @commands.hybrid_command()
    async def ver_agenda(self, ctx):
        if ctx.author.id in self.agendas:
            agenda_atual = self.agendas[ctx.author.id]
            await ctx.send(f"Sua agenda atual: \n{agenda_atual}")
        else:
            await ctx.send("Voce ainda nao possui uma agenda.")
        
async def setup(bot):
    await bot.add_cog(Agenda(bot))