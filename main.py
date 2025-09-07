"""
M8 Bot - Um bot para Discord open source
Desenvolvido por Gabe Morais - https://github.com/gabemorais
Licença: MIT
"""

import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

#Carrega variáveis em outro arquivo
#Crie um arquivo .env (apenas ".env") - O arquivo deve conter: TOKEN=Token_bot
#Exemplo: TOKEN=1234567890
load_dotenv()

#Configura as intents(permissões) do bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix='!!', #Prefixo do bot, por exemplo: !!ajuda
    intents = intents
)

async def carregar_cogs():
    #Carrega automaticamente as cogs da pasta 'cogs/'
    for arquivo in os.listdir('cogs'):
        if arquivo.endswith('.py'):
            await bot.load_extension(f'cogs.{arquivo[:-3]}')

@bot.event
#Evento quando o bot se conecta ao Discord
async def on_ready():
    #Carrega todas as cogs da pasta 'cogs/'
    await carregar_cogs()

    #Define o status do bot, nesse caso, vai aparecer como: "Jogando !!ajuda para ver todos os comandos"
    await bot.change_presence(activity = discord.Game(name = '!!ajuda para ver todos os comandos'))

    #Sincroniza os slash commands com o Discord
    sincs = await bot.tree.sync()

    #Exibe algumas informações no terminal
    print('══════════════════════════════════')
    print(f'✅ {bot.user.name} inicializado!')
    print(f'🎯 {len(sincs)} comandos sincronizados')
    print(f'🆔 ID do bot: {bot.user.id}')
    print(f'👥 Servidores: {len(bot.guilds)}')
    print(f'👤 Usuários: {sum(g.member_count for g in bot.guilds)}')
    print('══════════════════════════════════')

@bot.command()
@commands.is_owner() #Restringe esse comando apenas ao dono do bot
async def sync(ctx):    
    #Comando para recarregar as cogs e comandos sem precisar reiniciar o bot
    mensagem = await ctx.reply('Carregando as novas configurações...', mention_author = False)
    for arquivo in os.listdir('cogs'):
        if arquivo.endswith('.py'):
            nome_cog = arquivo[:-3]
            try:
                await bot.reload_extension(f'cogs.{nome_cog}')
            except commands.ExtensionNotLoaded:
                await bot.load_extension(f'cogs.{nome_cog}')
            except Exception as e:
                print(f'Falha na cog "{nome_cog}": {e}')
    await bot.tree.sync()
    await mensagem.edit(content='✅ Todas as cogs e comandos foram sincronizados!')

@bot.tree.command(name = 'ping', description = '⟦Utilidade⟧ Verifique o ping do bot')
async def latencia(interaction: discord.Interaction):
    #Slash command que verifica o ping do bot
    latencia = round(bot.latency * 1000)
    await interaction.response.send_message(f'Pong! 🏓 - **{latencia}ms**')

if __name__ == '__main__':
    #Inicia o bot usando o token no arquivo .env
    bot.run(os.getenv('TOKEN'))