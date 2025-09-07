import discord
import asyncio
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta

class Moderacao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    #Checa o nível do cargo da pessoa
    async def tem_role_maior(self, interaction: discord.Interaction, target: discord.Member = None):
        #Pega o cargo mais alto do bot
        bot_membro = interaction.guild.get_member(self.bot.user.id)
        bot_maior_cargo = bot_membro.top_role if bot_membro else None

        #Pega o cargo mais alto do usuário
        user_maior_cargo = interaction.user.top_role

        #Checa se o user tem cargo superior ao bot
        if not bot_maior_cargo or user_maior_cargo.position <= bot_maior_cargo.position:
            await interaction.response.send_message('❌ Você não tem permissão para utilizar esse comando', ephemeral=True)
            return False
        
        #Se um alvo for especificado, verifica hierarquia
        if target:
            #Previne auto-punição
            if target == interaction.user:
                await interaction.response.send_message('❌ Você não pode se punir', ephemeral=True)
                return False
            
            #Previne moderar o dono do server
            if target == interaction.guild.owner:
                await interaction.response.send_message('❌ Não posso moderar o dono do servidor!', ephemeral=True)
                return False
            
            #Previne moderar outros bots
            if target.bot:
                await interaction.response.send_message('❌ Não posso moderar outros bots!', ephemeral=True)
                return False
            
            #Previne moderar usuários com cargo igual ou maior
            if user_maior_cargo.position <= target.top_role.position:
                await interaction.response.send_message('❌ Você não pode moderar alguém com o cargo igual ou superior ao seu!', ephemeral=True)
                return False
            
        return True

    #Comando /clear
    @app_commands.command(name='clear', description='⟦Moderação⟧ Limpa mensagens do chat')
    @app_commands.describe(quantidade='Número de mensagens para limpar')
    async def clear(self, interaction: discord.Interaction, quantidade: int):

        #Checa hierarquia dos cargos
        if not await self.tem_role_maior(interaction):
            return
        
        #Limpa as mensagens do canal atual
        if quantidade < 1:
            await interaction.response.send_message('❌ Escolha um número maior do que 0', ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        deletado = await interaction.channel.purge(limit=quantidade)
        if len(deletado) == 1:
            await interaction.followup.send(f'✅ {len(deletado)} mensagem deletada!', ephemeral=True)
        else:
            await interaction.followup.send(f'✅ {len(deletado)} mensagens deletadas!', ephemeral=True)

    #Comando /mute
    @app_commands.command(name='mute', description='⟦Moderação⟧ Silencia um usuário temporariamente')
    @app_commands.describe(
        usuario = 'Usuário para silenciar',
        tempo = 'Tempo de mute (ex: 10m, 1h, 2d) - LIMITE DE 28 DIAS',
        motivo = 'Motivo do mute'
    )

    async def mute(self, interaction: discord.Interaction, usuario: discord.Member, tempo: str, motivo:str = 'Não especificado'):

        #Checa hierarquia dos cargos
        if not await self.tem_role_maior(interaction, usuario):
            return
        
        conversao_tempo = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
        quantidade = int(tempo[:-1])
        unidade = tempo[-1].lower()

        if unidade not in conversao_tempo:
            await interaction.response.send_message('❌ Unidade de tempo inválida! Use s, m, h ou d', ephemeral=True)
            return
        
        duracao_segundos = quantidade * conversao_tempo[unidade]

        #Verifica se o tempo de mute é maior que 28 dias
        limite_28_dias = 28 * 86400
        if duracao_segundos > limite_28_dias:
            await interaction.response.send_message('❌ O tempo máximo do mute é de **28 dias**!', ephemeral=True)
            return
        
        if duracao_segundos < 60:
            await interaction.response.send_message('❌ O tempo mínimo de mute é **1 minuto**!', ephemeral=True)
            return
        
        #Aplica o mute
        duracao_mute = discord.utils.utcnow() + timedelta(seconds=duracao_segundos)
        await usuario.timeout(duracao_mute, reason=motivo)

        #Mensagem de confirmação
        await interaction.response.send_message(
            f'✅ O usuário {usuario.mention} foi silenciado por {tempo}!\n'
            '**Motivo:** {motivo}'
        )

    #Comando /unmute
    @app_commands.command(name='unmute', description='⟦Moderação⟧ Remove o mute de um usuário')
    @app_commands.describe(
        usuario = 'Usuário para tirar o mute'
    )
    async def unmute(self, interaction: discord.Integration, usuario: discord.Member):

        #Checa hierarquia dos cargos
        if not await self.tem_role_maior(interaction, usuario):
            return
        
        #Caso o user não esteja mutado
        if not usuario.is_timed_out():
            await interaction.response.send_message('❌ Este usuário não está mutado', ephemeral=True)
            return
        
        #Remove o mute e adiciona o motivo no registro de auditoria
        await usuario.timeout(None, reason='Remoção de mute realizada por um moderador')
        await interaction.response.send_message(f'O usuário {usuario} foi desmutado')

    #Comando /kick
    @app_commands.command(name='kick', description='⟦Moderação⟧ Expulsa um usuário do servidor')
    @app_commands.describe(
        usuario = 'Usuário para expulsar',
        motivo = 'Motivo da expulsão'
    )
    async def kick(self, interaction: discord.Interaction, usuario: discord.Member, motivo: str = 'Não especificado'):
        #Checa hierarquia dos cargos
        if not await self.tem_role_maior(interaction, usuario):
            return
        
        await usuario.kick(reason=motivo)
        await interaction.response.send_message(
            f' O usuário {usuario} foi expulso!\n'
            f'**Motivo:** {motivo}'
        )

    #Comando /ban
    @app_commands.command(name='ban', description='⟦Moderação⟧ Bane um usuário do servidor')
    @app_commands.describe(
        usuario = 'Usuário para banir',
        motivo = 'Motivo do banimento'
    )
    async def ban(self, interaction:discord.Interaction, usuario: discord.Member, motivo: str = 'Não especificado'):
        #Checa hierarquia com o user alvo
        if not await self.tem_role_maior(interaction, usuario):
            return
        
        await usuario.ban(reason=motivo)
        await interaction.response.send_message(
            f'O usuário {usuario} foi banido!\n'
            f'**Motivo:** {motivo}'
        )

    #Comando /warn
    @app_commands.command(name='warn', description='⟦Moderação⟧ Adverte um usuário')
    @app_commands.describe(
        usuario = 'Usuário para advertir',
        motivo = 'Motivo da advertência'
    )
    async def warn(self, interaction: discord.Interaction, usuario: discord.Member, motivo: str = 'Não especificado'):
        #Checa hierarquia dos cargos
        if not await self.tem_role_maior(interaction, usuario):
            return
        
        #Tenta enviar DM para o usuário advertido
        try:
            embed = discord.Embed(
                title='⚠️ Advertência',
                description=f'Você foi advertido no servidor **{interaction.guild.name}**',
                color=0xffcc00,
                timestamp=datetime.now()
            )
            embed.add_field(name='Motivo', value=motivo, inline=False)
            embed.add_field(name='Moderador', value=interaction.user.mention, inline=False)
            embed.set_footer(text='Mais advertências podem resultar em punições mais severas')

            await usuario.send(embed=embed)
        except:
            #User tem DM fechada
            pass

        await interaction.response.send_message(
            f'⚠️ Usuário {usuario.mention} advertido!\n'
            f'**Motivo:** {motivo}'
        )

    #Comando /slowmode
    @app_commands.command(name='slowmode', description='⟦Moderação⟧ Define o Slow Mode no chat')
    @app_commands.describe(
        tempo = 'Tempo para o Slow Mode - Ex: 10s, 5m, 2h (0 para desativar o Slow Mode)'
    )
    async def slowmode(self, interaction: discord.Interaction, tempo: str):
        #Checa hierarquia dos cargos
        if not await self.tem_role_maior(interaction):
            return
        
        if tempo == '0':
            await interaction.channel.edit(slowmode_delay=0)
            await interaction.response.send_message('✅ Slow Mode desativado')
            return
        
        conversao_tempo = {'s': 1, 'm': 60, 'h': 3600}

        try:
            #Tenta converter | '10s' -> quantidade = 10, unidade = 's'
            quantidade = int(tempo[:-1])
            unidade = tempo[-1].lower()
        except (ValueError, IndexError):
            await interaction.response.send_message('❌ Unidade de tempo inválida! Exemplos: 10s, 5m, 2h ou 0 para desativar', ephemeral=True)
            return
        
        #Checagem para ver se a unidade é válida
        if unidade not in conversao_tempo:
            await interaction.response.send_message('❌ Unidade de tempo inválida! Use s (segundos), m (minutos) ou h (horas)', ephemeral=True)
            return
        
        #Calcula os segundos
        segundos = quantidade * conversao_tempo[unidade]

        #Checa o limite máximo de Slow Mode
        if segundos > 21600:
            await interaction.response.send_message('❌ O tempo máximo de slow mode é 6 horas', ephemeral=True)
            return
        
        #Checa o limite mínimo de Slow Mode
        if segundos < 0:
            await interaction.response.send_message('❌ O tempo não pode ser negativo! Use 0 para desativar ou tente outro valor', ephemeral=True)
            return
        
        #Slow Mode
        try:
            await interaction.channel.edit(slowmode_delay=segundos)

            tempo_formatado = self.formatar_tempo_slowmode(segundos)
            await interaction.response.send_message(f'✅ Slow Mode definido para **{tempo_formatado}**')

        except discord.Forbidden:
            await interaction.response.send_message('❌ Não tenho permissão para alterar o slow mode nesse canal', ephemeral=True)

        except discord.HTTPException as e:
            await interaction.response.send_message(f'❌ Erro ao definir modo lento: {str(e)}', ephemeral=True)

    def formatar_tempo_slowmode(self, segundos: int) -> str:
        #Converte segundos para horas, minutos e segundos
        horas = segundos // 3600
        minutos = (segundos % 3600) // 60
        segundos_restantes = segundos % 60

        partes = []

        if horas > 0:
            partes.append(f'{horas} hora{'s' if horas != 1 else ''}')
        if minutos > 0:
            partes.append(f'{minutos} minuto{'s' if minutos != 1 else ''}')
        if segundos_restantes > 0:
            partes.append(f'{segundos_restantes} segundo{'s' if segundos_restantes != 1 else ''}')

        if len(partes) == 0:
            return '0 segundos'
        elif len(partes) == 1:
            return partes[0]
        else:
            if len(partes) == 2:
                return f'{partes[0]} e {partes[1]}'
            else:
                return f'{", ".join(partes[:-1])} e {partes[-1]}'
    
async def setup(bot):
    await bot.add_cog(Moderacao(bot))