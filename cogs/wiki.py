"""
Cog: Wiki - Sistema de pesquisa pela Wikipedia
Comando /wiki <termo>
Por exemplo: /wiki Naruto
"""

import discord
import aiohttp
import urllib.parse
from discord import app_commands
from discord.ext import commands

class Wiki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name='wiki', description='⟦Utilidade⟧ Pesquise um termo na Wikipedia')
    @app_commands.describe(termo='O que você quer pesquisar?')
    async def wikipedia(self, interaction: discord.Interaction, termo: str):
        #Adia a resposta pois a pesquisa pode demorar
        #Caso o bot demore um tempo X, o discord mostra que o bot não obteve resposta
        #Defer é para ignorar esse tempo
        await interaction.response.defer()
        
        try:
            #Formata o termo para url (remove espaços, capitaliza, etc.)
            termo_formatado = urllib.parse.quote(termo.strip().title().replace(' ', '_'))
            
            #Cria sessão HTTP para fazer requisições
            async with aiohttp.ClientSession() as sessao:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                #Tenta acesso direto ao artigo
                async with sessao.get(
                    f'https://pt.wikipedia.org/api/rest_v1/page/summary/{termo_formatado}',
                    headers=headers
                ) as response:
                    
                    if response.status == 200:
                        #Artigo encontrado diretamente
                        data = await response.json()
                        await self.send_wiki_embed(interaction, data, termo)
                    
                    elif response.status == 404:
                        #Artigo não encontrato, tenta pesquisa
                        await self.search_wiki(interaction, termo, sessao, headers)
                    
                    else:
                        await interaction.followup.send('❌ Erro ao acessar a Wikipedia. Tente novamente.')
        
        except Exception as e:
            #Tratamento de erro genérico
            await interaction.followup.send(f'❌ Erro inesperado: {str(e)}')

    async def search_wiki(self, interaction, termo, sessao, headers):
        try:
            async with sessao.get(
                'https://pt.wikipedia.org/w/api.php',
                params={
                    'action': 'query',
                    'format': 'json',
                    'list': 'search',
                    'srsearch': termo,
                    'utf8': 1,
                    'srlimit': 1
                },
                headers=headers
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    
                    #Verifica se há resultados de pesquisa
                    if not data.get('query', {}).get('search', []):
                        await interaction.followup.send(f'❌ Não encontrei "{termo}" na Wikipedia.')
                        return
                    
                    #Pega o título do primeiro resultado
                    titulo = data['query']['search'][0]['title']
                    #Codifica o título para URL
                    titulo_codificado = urllib.parse.quote(titulo.replace(' ', '_'))
                    
                    #Busca o sumário do artigo
                    async with sessao.get(
                        f'https://pt.wikipedia.org/api/rest_v1/page/summary/{titulo_codificado}',
                        headers=headers
                    ) as summary_response:
                        
                        if summary_response.status == 200:
                            data = await summary_response.json()
                            await self.send_wiki_embed(interaction, data, termo)
                        else:
                            await interaction.followup.send('❌ Erro ao buscar o artigo.')
                
                else:
                    await interaction.followup.send('❌ Erro na pesquisa da Wikipedia.')
        
        except Exception as e:
            await interaction.followup.send(f'❌ Erro na pesquisa: {str(e)}')

    #Cria e envia a embed
    async def send_wiki_embed(self, interaction, data, termo_original):
        try:
            #Pega o resumo do artigo ou usa uma mensagem padrão
            extract = data.get('extract', 'Nenhuma informação encontrada.')
            
            #Verifica se "pode referir-se a:"
            if 'pode referir-se a:' in extract:
                await interaction.followup.send(
                    f'🔍 Termo muito amplo. Tente ser mais específico.\n'
                    f'Exemplo: "/wiki Rio de Janeiro (cidade)" em vez de "/wiki Rio de Janeiro"'
                )
                return
            
            embed = discord.Embed(
                title=f'Wikipedia: {data.get("title", termo_original)}',
                description=extract[:2000] + '...' if len(extract) > 2000 else extract,
                color=discord.Colour.random(),
                url=data.get('content_urls', {}).get('desktop', {}).get('page', '')
            )
            
            if 'thumbnail' in data:
                embed.set_thumbnail(url=data['thumbnail']['source'])
            
            if 'description' in data:
                embed.set_footer(text=data['description'])
            
            await interaction.followup.send(embed=embed)
        
        except Exception as e:
            await interaction.followup.send(f'❌ Erro ao criar embed: {str(e)}')

async def setup(bot):
    await bot.add_cog(Wiki(bot))