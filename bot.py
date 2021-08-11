#Pacotes
from typing import Counter
import discord
from discord.ext import commands
from datetime import datetime
from discord.utils import get
import random
from PIL import Image,ImageFont,ImageDraw
import string
import os
import time
import asyncio

# Permissão para O bot receber as informações de quem entra e sai do server
intents = discord.Intents.default()
intents.members = True

#client
client = commands.Bot(command_prefix="!", intents=intents)

# Evento quando o bot fica online
@client.event
async def on_ready():
    print('Online!')
#Evento quando o bot fica offiline
@client.event
async def on_disconnect():
    print('Offline!')

#Comando Ping
@client.command(name='ping')
async def ping(context):
    if context.author.bot:
        return
    await context.send(f"**Pong!** {context.author.mention} `{round(client.latency * 1000)}ms`")
    await context.message.delete()
#Comando Versão
@client.command(name='Info')
async def Info(context):
    embed = discord.Embed(title='Informações sobre o Bot', description=f'O Bot Cubo Captcha é um bot de Captcha Simples em Pyhton', color=0xe91e63, timestamp=datetime.utcnow())
    embed.add_field(name='Qual a versão do Bot?', value='Versão 1.5.0', inline=True)
    embed.add_field(name='Qual linguagem voce usa no bot?', value='Discord.py/Discord Pyhton')
    embed.set_footer(text='Cubo Captcha ©2021')
    await context.send(embed=embed)
    await context.message.delete()
#Captcha
@client.event
async def on_member_join(context):
    if context.bot:
        return
    #Variaveis
    id_member = context.id
    user = await client.fetch_user(id_member)
    numero_random = random.randint(4,7)
    #autorole
    autorole = discord.utils.get(context.guild.roles, name= 'indefinido')
    autorole2 = discord.utils.get(context.guild.roles, name= 'verificado')
    await context.add_roles(autorole)
    #Numeros e Letras
    letras = string.ascii_letters
    numeros = string.digits
    lenght = numero_random
    #printable
    printavel = f'{letras}{numeros}'

    #printable2
    printavel = list(printavel)
    random.shuffle(printavel)

    #senha
    senha_aleatoria = random.choices(printavel, k=lenght)
    senha_aleatoria = ''.join(senha_aleatoria)


    img = Image.open('captchabase.png')
    font = ImageFont.truetype('arial.ttf', 24)
    draw = ImageDraw.Draw(img)
    text = senha_aleatoria
    draw.text((156,42), text, (0,0,0), font=font)
    nome = f'{senha_aleatoria}.png'
    print(nome)
    img.save(nome)
    await user.send('Olá! Tera 1 min para terminar o Captcha!',file = discord.File(nome))
    def check(m):
        return m.content == senha_aleatoria
    try:
        msg = await client.wait_for('message',timeout=60, check=check)
    except asyncio.TimeoutError:
        await user.send('O Tempo acabou! Tente entrar no server denovo para refazer!')
        os.remove(nome)
    else:
        await user.send('Verificado! de uma olhada no servidor')
        await context.add_roles(autorole2)
        await context.remove_roles(autorole)
        os.remove(nome)
        msg

    
    
 


        



    

    









client.run('TOKENDOBOT')
