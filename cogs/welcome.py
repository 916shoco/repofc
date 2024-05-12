import discord
import random
import request
from discord.ext import commands
from PIL import Image
from io import BytesIO
import PIL 

messages = [
    "Olá, {mention}! Seja bem-vindo(a) ao servidor! || <#1198347966646321299> ||",
    "Bem-vindo(a), {mention}! Esperamos que você se divirta aqui!",
    "E aí, {mention}! Que bom ter você no nosso servidor!",
    "Seja bem-vindo, {mention}! don`t look here || <#1198347966646321299> ||",
    "**Bem-vindo ao servidor!** {mention}",
    "Seja bem-vindo, {mention}! Esperamos que você se sinta em casa no nosso servidor.",
    "Olá, {mention}! Bem-vindo(a) ao nosso incrível servidor!",
    "Bem-vindo(a), {mention}! Estamos muito felizes em te ver por aqui!",
    "E aí, {mention}! Que bom que você decidiu se juntar a nós. Bem-vindo(a)!",
    "Seja bem-vindo(a), {mention}! Esperamos que você se divirta e faça novos amigos aqui!"
]

image_urls = [
    "https://media1.tenor.com/images/410102eb20e24e2ecb0c0889ed7dd288/tenor.gif?itemid=15974218",
    "https://images-ext-1.discordapp.net/external/IAw9G-WvGFvPm_85AGzKzOqJXDcSz1dImwoEtl0uw-Q/https/rrp-production.loritta.website/img/43885fc9554a8cc3fb96568e9a6ac79604810677.gif",
    "https://media1.tenor.com/m/P7hCyZlzDH4AAAAC/wink-anime.gif"
]

def get_average_color(image_url):
    try:
        response = requests.get(image_url, timeout=5)
        image = Image.open(BytesIO(response.content))
    except PIL.UnidentifiedImageError:
        return None
    width, height = image.size
    pixels = image.getdata()
    total_r = total_g = total_b = 0
    for pixel in pixels:
        if isinstance(pixel, int):
            r = g = b = pixel
        else:
            r, g, b = pixel
        total_r += r
        total_g += g
        total_b += b
    average_r = total_r // (width * height)
    average_g = total_g // (width * height)
    average_b = total_b // (width * height)
    return (average_r, average_g, average_b)

class Welcome(commands.Cog, name="welcome"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel_id = 1198347966646321304
        channel = discord.utils.get(member.guild.text_channels, id=channel_id)

        if channel is not None:
            message_content = random.choice(messages).format(mention=member.mention)
            image_url = random.choice(image_urls)

            average_color = get_average_color(image_url)
            if average_color is None:
                print(f"Erro ao processar a imagem: {image_url}")
                return

            embed_color = discord.Color.from_rgb(*average_color)

            # Envio do GIF como um arquivo
            response = requests.get(image_url)
            gif_file = discord.File(BytesIO(response.content), filename="welcome.gif")

            embed = discord.Embed(title="Bem-vindo ao Nosso Servidor!",
                                description=f"Que tal dar uma olhadinha nesses canais?\n <#1198347966352736328> \n <#1209212839781208164> \n <#1198347966352736330> \n <#1198347966352736332>",
                                color=embed_color)
            embed.set_image(url="attachment://welcome.gif")
            embed.set_footer(text="Sinta-se à vontade para explorar os canais e interagir com a comunidade!")

            await channel.send(message_content, embed=embed, file=gif_file)
        else:
            print("Canal 'boas-vindas' não encontrado!")


async def setup(bot):
    await bot.add_cog(Welcome(bot))
