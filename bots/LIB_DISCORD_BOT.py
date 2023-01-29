import discord
import PySimpleGUI as sg
from os import getenv
from time import sleep
from datetime import datetime
from discord.ext import commands

# Lib Discord Bot Ver 0.2
# Last Update: 2022-12-19 
RUNDATE = datetime.now()
GUILD_NAME = 'Legião Imperial Brasileira'

PREF = getenv('LIB_DISCORD_BOT_PREFIX')
TOKEN = getenv('LIB_DISCORD_BOT_TOKEN')
GUILD_ID = getenv('LIB_DISCORD_GUILD_ID')
LIB_ROLE_ID = getenv('LIB_DISCORD_ROLE_ID')
LIB_ROLE_NAME = getenv('LIB_DISCORD_ROLE_NAME')
CHANNEL_ID_AVISOS = getenv('LIB_DISCORD_CHANNEL_AVISOS')

sg.theme("Black")
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=PREF, intents=intents)

def get_main_layout():
    main_layout = [
        [sg.Text('▃▃▃▃▃▃ ▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃\n\n▃   Discord Bot\n\n▃   Bot Para Mensagens da LIB!\n\n▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃ ▃▃▃▃▃▃')], 
        [sg.Text(' ')],
        [sg.Button('Ligar o Bot'), sg.Button('Info')],
        [sg.Multiline(key="msg_input_user", size=(40,10), pad=(10,10))],
        [sg.Button('Enviar Mensagem no PV')],
        [sg.Text(' ')]
    ]

    return main_layout

def get_info_date(bot_on):
    txt = """
    ================== BOT INFO ===================

        Ligado á: {}

        Butanos:
        
            "Enviar Mensagem no PV"
            Providencie uma mensagem na caixa acima
            do botão, após isso, clique no botão. A
            mensagem vai ser enviada a todos que 
            possuem a ROLE/CARGO: {}.

        OBS:

            Caso o App ""pare de funcionar"",
            chame o cT (Gabriel). =D

    ==============================================
    """

    if bot_on: txt = txt.format(str(datetime.now() - RUNDATE)[:7]+'s', LIB_ROLE_NAME)
    
    else: txt = txt.format('BOT AINDA NÃO ESTA LIGADO', LIB_ROLE_NAME)
    
    return txt

def clean_app_message(message):
    msg = message.strip()
    if len(msg) <= 15: return False
    else: return msg

def get_base_window():
    main_layout = get_main_layout()

    base_window = sg.Window(
            layout=main_layout, 
            title='LIB - Mensagens', 
            element_justification='c'
        )

    return base_window

@bot.event
async def on_ready():
    base_window = get_base_window()
    while True:
        event, values = base_window.read()

        if event == 'Ligar o Bot': # Waiting local discord bot start
            bot_on = True
            sleep(2)
            sg.popup('Bot está Ligado!')

        if event == 'Info':
            try:
                if bot_on: sg.popup(get_info_date(bot_on=True))
            
            except: 
                sg.popup(get_info_date(bot_on=False))

        if event == 'Enviar Mensagem no PV':
                input_msg = values['msg_input_user']

                if input_msg:
                    start_message = f"INICIO - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    print(start_message, file=open('../logs.txt', 'a'))

                    for guild in bot.guilds:
                        if GUILD_NAME == guild.name:
                            sg.popup('Iniciando os envios das msg!')
                            for member in guild.members:
                                if LIB_ROLE_ID in [role.id for role in member.roles]:
                                    user = await bot.fetch_user(member.id)
                                    try:
                                        await user.send(input_msg)
                                        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Mensagem ENVIADA para: {member.name} -> {member.id}")
                                        sleep(7)
                                    except:
                                        try:
                                            print(f"Mensagem Nao Enviada ao: {str(member.name)} -> <@{str(member.id)}>", file=open('../logs.txt', 'a'))
                                            print(f"{datetime.now().strftime('%H:%M:%S')} | Mensagem NAO ENVIADA para: {member.name} -> {member.id}")
                                        except:
                                            print(f"Error Interno")

                    end_message = f"\nFIM - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    print(end_message, file=open('../logs.txt', 'a'))
                    
                    sg.popup('Mensagem Enviada a todos os players da LIB!')

                else:
                    sg.popup('Providêncie uma mensagem!') 
         
        if event == sg.WIN_CLOSED or event == 'Exit':
            exit()

bot.run(TOKEN)
