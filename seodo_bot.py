import discord
from discord.ext import commands

import asyncio
import nest_asyncio
import os
import time
from PIL import Image

main_dir = os.getcwd()
module_dir = os.path.join(main_dir, 'module')
token_dir = os.path.join(module_dir, 'token')
watchdir = os.path.join(main_dir, 'log')
workflow_dir = os.path.join(main_dir, 'workflow')
message_dir = os.path.join(main_dir, 'message')

import sys
sys.path.append(module_dir)
sys.path.append(token_dir)
import table
import pandas as pd

import time


'''
 @bot.command()
 async def example(ctx) :
 async def example2(ctx, *, arg) :
 
     await ctx.send('message')
     await ctx.send
     await ctx.send(file = discord.File(os.path.join(watchdir, 'watchdog_show.txt')))
'''

# ----------------------------------------------------------------
# start SEODO
# ----------------------------------------------------------------

# read token
os.chdir(token_dir)
tk_f = open('token.txt', 'r')
to = tk_f.readline()
tk_f.close()

# prefix $
bot = commands.Bot(command_prefix='$')
print('SEODO awaking')


@bot.event
async def on_ready() :
    print("SEODO WHIPPING MACHINE!")
    await bot.change_presence(status = discord.Status.online, activity = None)
    #await watchdog()


# ----------------------------------------------------------------
# init functions
# ----------------------------------------------------------------

def get_time(time) :
    pass


def make_schedule() :
    user_list = ['승현', '한주', '지인']
    index_list = ['start_time', 'time_elapsed']

    schedule = pd.DataFrame(columns = user_list, index = index_list)
    

    pass
    
class random() :
    pass

@bot.command(aliases=['출근할게', '출석했어', '출석할게'])
async def 출근했어(ctx, *, arg) :
    if (arg == '지인') or (arg == '서도') :
        name = '지인'
        await ctx.send(f'오셨어요 주인님!')

    elif (arg == '승현') or (arg == '리솝') or (arg == '이승현') :
        name = '승현'
        await ctx.send(f'일해! {name}!')

    elif (arg == '한주') or (arg == '김한주'):
        name = '한주'
        await ctx.send(f'잘했어, {name}!')
    else :
        await ctx.send('너 누구야')
    



# ----------------------------------------------------------------
# message
# ----------------------------------------------------------------

def time_keeper_msg(gap) :
    set_time = 10 * 60 # watchdog sleeptime = 1 if gap < 10min
    
    if gap < set_time :
        stime = 3

    else :
        stime = 10

    return stime
 


# ----------------------------------------------------------------
# ETC.
# ----------------------------------------------------------------










# ----------------------------------------------------------------
# GREETINGS !
# ----------------------------------------------------------------

@bot.command(aliases=['hi'])
async def 안녕(ctx):
    await ctx.send(f'안녕하세요!')


@bot.command(aliases = ['잘가'])
async def 잘있어(ctx, *, arg):
    temp_list = ['갈게', '잘게', '간다', '잔다']

    for item in temp_list :
        if item in arg :
            arg = arg[ : arg.index(item)]

    await ctx.send(f'잘자요, {arg}')




# ----------------------------------------------------------------
# run bot
# ----------------------------------------------------------------

bot.run(to)
