# 🤖 M8 - Seu amigo multidimensional pessoal

[![Python](https://img.shields.io/badge/Python-3.13.7-blue)](https://python.org)
[![Discord.py](https://img.shields.io/badge/Discord.py-2.6.3-green)](https://discordpy.readthedocs.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Um bot para discord, com **arquitetura modular e open source**, desenvolvido em Python, oferecendo diversas funcionalidades úteis e divertidas para o seu servidor.

## **✨ Funcionalidades**

### Vantagens
- **Personalização**: Use apenas os módulos que precisa
- **Manutenção**: Atualize um módulo sem afetar os outros
- **Expansão**: Adicione novos módulos facilmente
- **Performance**: Carregue apenas o necessário

### Códigos
- **`/userinfo`** - Informações detalhadas de usuários
- **`/wiki`** - Pesquisa na Wikipedia
- **`/ping`** - Mostra o ping do bot

## **🚀 Instalação**
### Pré-requisitos
- Python 3.8 ou superior
- API [discord.py](https://discordpy.readthedocs.io/en/stable/)
- Token de bot Discord ([Como obter](https://discord.com/developers/applications))

### Passo a Passo
1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/m8-bot.git
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Configure as variáveis do arquivo .env**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

4. **Edite o bot**
- Utilize a IDE favorita para editar os arquivos do bot


5. **Execute o bot**
```
Diretamente pela IDE
```
Ou
```bash
python main.py
```

## **⚙️ Configuração**
### Arquivo .env
```
TOKEN=seu_token_do_bot_aqui
Exemplo: TOKEN=1234567890
```

## **Cogs disponíveis**
| Cog | Descrição | Status |
| ---------- | ------------------------------------------------------ | -- |
| `userinfo`| Comando para puxar algumas informações sobre o usuário | ✅ |
| `wiki`   | Comando para fazer pesquisa no wikipedia diretamente do discord | ✅ |
| `random` | Comando com diversas funcionalidades baseados em RNG | 🚧 |
| `dado` | Comando que simula dados de RPG de mesa (D4, D6, D8, D12, D20...) | 🚧 |

## **🏗️ Estrutura do Projeto**
```
m8-bot/
├── main.py              # Ponto de entrada
├── requirements.txt     # Dependências
├── .env.example        # Template de configuração
├── .gitignore          # Arquivos ignorados
└── cogs/               # Módulos do bot
    ├── userinfo.py     # Informações do usuário
    └── wiki.py         # Wikipedia
    ...
```

## 📜 Licença
Este projeto está sob licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## **🏆 Créditos**
Desenvolvido por [Gabe Morais](https://github.com/gabemorais)
Duvidas? Entre em contato comigo pelo discord: g_guerra