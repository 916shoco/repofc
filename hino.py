import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="general")
    if channel is not None:
        message_content = (f"{member.mention}")

        embed = discord.Embed(title="<:W_HashtagBranca:1130946547203457045> BEM-VINDO",
                              description="<a:B_BlueLacoGif:1198123120628867183> Oba! Membro novo na área! <a:B_BlueLacoGif:1198123120628867183>",
                              color=0xFFFFFF)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1068578811345637486/1206738008485793863/718_Sem_Titulo4_20240212200524.png?ex=65dd1959&is=65caa459&hm=ad63e9716bf24516713e96e2590f76f7d5630838f2d5abcc3df19fdc41f4208d&")
        await channel.send(message_content, embed=embed)
    else:
        print("Chat nao encontrado")

bot.run('MTIzNzQ0NjMwNzI3OTU0MDMzNA.GeJiBZ.7Nuwa4UmVfTdIr7IcZmp9vKKsQPFCl9wVcBUzY')  # Substitua 'TOKEN' pelo seu token de bot