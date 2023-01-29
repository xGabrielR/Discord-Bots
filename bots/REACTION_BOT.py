import discord
from os import getenv
from datetime import datetime
from discord.ext import commands

TOKEN = getenv('REACTION_ROLE_BOT_TOKEN')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    on_reaction_add
    print('\nOnline\n')

@bot.event
async def on_reaction_add(reaction, user):
    if reaction.emoji == "🔖":
        channel = bot.get_channel(reaction.message.channel.id)
        msg = f">>> **Link da Mensagem no Discord**: {reaction.message.jump_url}"

        embed_msg = discord.Embed(
            title=f"Bookmark Criado em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            description=reaction.message.content
        )
        embed_msg.set_author(
            name=reaction.message.author,
            icon_url=reaction.message.author.avatar_url
        )
        try:
            user_ = await bot.fetch_user(str(user.id))
            await user_.send(msg, embed=embed_msg)

        except:
            await channel.send(f'**<@{user.id}>** Por favor, habilite as mensagens privadas do Bot!')
        
bot.run(TOKEN)
