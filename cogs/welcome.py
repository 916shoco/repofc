import discord
from discord.ext import commands

class Welcome(commands.Cog, name="welcome"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Cria uma embed de boas-vindas com a cor branca
        embed = discord.Embed(title="<:W_HashtagBranca:1130946547203457045> BEM-VINDO",
                              description="<a:B_BlueLacoGif:1198123120628867183> Oba! Membro novo na área! <a:B_BlueLacoGif:1198123120628867183>",
                              color=0xFFFFFF)
        embed.set_footer(text=f"Novo membro: {member.display_name}", icon_url=member.avatar_url)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1068578811345637486/1206738008485793863/718_Sem_Titulo4_20240212200524.png?ex=65dd1959&is=65caa459&hm=ad63e9716bf24516713e96e2590f76f7d5630838f2d5abcc3df19fdc41f4208d&")

        # Encontra o canal de boas-vindas pelo nome (substitua "boas-vindas" pelo nome do seu canal)
        channel = discord.utils.get(member.guild.text_channels, name="💭・chat-geral")
        if channel is not None:
            await channel.send(embed=embed)
        else:
            print("Canal 'boas-vindas' não encontrado!")

async def setup(bot):
    await bot.add_cog(Welcome(bot))