import discord
import asyncio
from os import environ
from discord.ext import commands
from types import SimpleNamespace

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = environ.get('D_TOKEN')

def try_cast(var, dtype):
    try: return dtype(var)
    except: return var 
    
async def add_member_role(ctx, member, role):
    # Can be name or Id
    _role = try_cast(role, int)

    if isinstance(_role, int):
        role_object = discord.utils.get(ctx.message.guild.roles, id=_role)
        
    else:
        role_object = discord.utils.get(ctx.message.guild.roles, name=_role)

    if role_object:
        await member.add_roles(role_object)

    else:
        await ctx.send(f'Cannot find role: {role}')

@bot.command(name='give_role_by_name')
async def give_role_by_name(ctx):
    message_content = ctx.message.content.replace('!give_role_by_name ', '').replace(' ', '')

    # Without "Snowflake" Discord Object.
    role_id = [role.id for role in ctx.message.guild.roles if role.name == message_content]

    if role_id:
        # Add role to discord.member.Member Object.
        await ctx.message.author.add_roles(SimpleNamespace(**{'id': role_id[0]}))

    else:
        await ctx.send(f'Cannot Find Role: "{message_content}"')

@bot.command(name='give_role_to_member')
async def give_role_to_member(ctx):
    message_content = ctx.message.content.replace('!give_role_to_member ', '').replace(' ', '')

    # Give to myself :p
    await add_member_role(ctx, ctx.message.author, message_content)

@bot.command(name='give_multiple_roles_by_id')
async def give_multiple_roles_by_id(ctx):
    message_content = ctx.message.content.replace('!give_multiple_roles_by_id ', '').replace(' ', '').split(',')

    try:
        # Without "Snowflake" Discord Object.
        roles = [SimpleNamespace(**{'id': int(role.strip())}) for role in message_content]

        await asyncio.gather(*[ctx.message.author.add_roles(role) for role in roles])

    except Exception as e:
        await ctx.send(f'Invalid Format. \nTry: !give_multiple_roles_by_id role_id_1, role_id_2.\nException:\n{e}')

    await ctx.send(f'All {len(roles)} Roles Gived.')

@bot.command(name='give_role_to_user')
async def give_role_to_user(ctx):
    message_content = ctx.message.content.replace('!give_role_to_user ', '').strip().split(',')
    role, user = [k.strip() for k in message_content]

    # Can be user nick or id.
    role, user = try_cast(role, int), try_cast(user, int)
    guild_roles, guild_members = ctx.message.guild.roles, ctx.message.guild.members

    if isinstance(role, int):
        role_object = discord.utils.get(guild_roles, id=role)

    else:
        role_object = discord.utils.get(guild_roles, name=role)

    if isinstance(user, int):
        user_object = discord.utils.get(guild_members, id=user)

    else:
        user_object = discord.utils.get(guild_members, nick=user)

    try:
        await user_object.add_roles(role_object)
        await ctx.send(f'Role Added to user "{user_object.nick}"')

    except Exception as e:
        await ctx.send(f'Cannot Find User: {user} or Role: {role}.\nExecp:\n{e}')
    

bot.run(TOKEN)