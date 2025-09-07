"""
Cog: UserInfo - Sistema de informações de usuários
Comando /userinfo <id ou @>
Por exemplo: /userinfo 1234567890 ou /userinfo @me
"""

import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timezone

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name='userinfo', description='⟦Utilidade⟧ Mostra informações completas de qualquer usuario do Discord')
    @app_commands.describe(user='ID ou menção do usuário (deixe vazio para ver seu proprio perfil)')
    async def userinfo(self, interaction: discord.Interaction, user: discord.User = None):
        await interaction.response.defer()

        try:
            #Usuário alvo, se nenhum for especificado, usa quem mandou o comando
            if user is None:
                user_obj = interaction.user
            else:
                user_obj = user

            #Pega a data de criação da conta e calcula a idade em dias
            conta_criada = user_obj.created_at
            dias_conta = (datetime.now(timezone.utc) - conta_criada).days
            idade_conta = f'{dias_conta} dias ({conta_criada.strftime("%d/%m/%Y")})'

            #Verifica se a conta é bot
            is_bot = '✅ Sim' if user_obj.bot else '❌ Não'

            #Cor aleatória para a embed
            cor = discord.Colour.random()

            embed = discord.Embed(
                title=f'👤 Informações de {user_obj.name}',
                color=cor,
                timestamp=datetime.now(timezone.utc)
            )

            embed.set_thumbnail(url=user_obj.display_avatar.url)

            #Campo 1: Informações básicas
            embed.add_field(
                name='📋 Identificação',
                value=f'**Nick:** {user_obj.name}\n'
                f'**ID:** `{user_obj.id}`\n'
                f'**É bot?** {is_bot}',
                inline=True
            )

            #Campo 2: Informações da conta
            embed.add_field(
                name='📅 Conta',
                value=f'**Criada em:** {conta_criada.strftime("%d/%m/%Y %H:%M")}\n'
                f'**Idade da conta:** {dias_conta} dias\n'
                f'**Avatar URL:** [Clique aqui]({user_obj.display_avatar.url})',
                inline=True
            )

            #Campo 3: Informações especificas do servidor (caso o usuário não esteja no servidor, vai ignorar essa parte)
            if hasattr(user_obj, 'guild') and user_obj.guild is not None:
                joined_at = user_obj.joined_at.strftime("%d/%m/%Y %H:%M") if user_obj.joined_at else "Desconhecido"
                embed.add_field(
                    name='🏰 No Servidor',
                    value=f'**Apelido:** {user_obj.nick or "Nenhum"}\n'
                    f'**Entrou em:** {joined_at}\n'
                    f'**Cargo mais alto:** {user_obj.top_role.mention}',
                    inline=False
                )

            embed.set_footer(
                text=f'Requisitado por {interaction.user}',
                icon_url=interaction.user.display_avatar.url
            )

            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(f'❌ Erro ao buscar informações: {str(e)}')

async def setup(bot):
    await bot.add_cog(UserInfo(bot))