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
log_dir = os.path.join(main_dir, 'log')

import sys
sys.path.append(module_dir)
sys.path.append(token_dir)
import table
import pandas as pd

import time
import datetime
import random

import numpy as np



'''
 @bot.command()
 async def example(ctx) :
 async def example2(ctx, *, arg) :
 
     await ctx.send('message')
     await ctx.send
     await ctx.send(file = discord.File(os.path.join(watchdir, 'watchdog_show.txt')))
     await asyncio.sleep(int(1))
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


# ----------------------------------------------------------------
# init functions
# ----------------------------------------------------------------


def read_excel(excel) :
    df = pd.read_excel(excel)
    if 'Unnamed: 0' in df.columns :
        df.drop('Unnamed: 0', axis = 1, inplace = True)

    if 'Unnamed: 0.1' in df.columns :
        df.drop('Unnamed: 0.1', axis = 1, inplace = True)

    return df

def double_size(string) :
    string = str(string)

    if len(string) == 1 :
        return '0' + string
    else :
        return string

def four_size(string) :
    string = str(string)

    if len(string) == 3 :
        return '0' + string
    else :
        return string

def get_date() :
    d = datetime.datetime.now()
    return d

def elapsed_time(date1, date2) :
    elapsed = date2 - date1
    hour = elapsed.hour
    minute = elapsed.minute

    return hour, minute


def now_date() :
    d = datetime.datetime.now()
    year = d.year
    month = double_size(d.month)
    day = double_size(d.day)

    return str(year) + str(month) + str(day) 

def random_item(list1) :
    return random.choice(list1)


def timedelta_to_info(td) :
    # day, hour, minute

    days = td.days
    hours = td.seconds//3600
    minutes = (td.seconds//60)%60

    if days == -1 :
        days = 0
        hours = 23 - hours
        minutes = 60 - minutes

    return days, hours, minutes

def timedelta_to_string(td) :
    days, hours, minutes = timedelta_to_info(td)

    send_time = ''
    if days == 0 :
        if hours == 0 :
            send_time += f'{minutes}분'
        else :
            send_time += f'{hours}시간 {minutes}분'
    else :
        send_time += f'{days}일 {hours}시간 {minutes}분'

    return send_time

# ----------------------------------------------------------------
# log.xlsx dataframe
# ----------------------------------------------------------------

def usr_list() :
    return ['승현', '한주', '지인']

# 출근도장과 퇴근도장
def whole_add_date(usr, status, date) :
    os.chdir(log_dir)
    log_df = read_excel('log.xlsx')

    log_df.reset_index(drop = True, inplace = True)
    size = log_df.shape[0]

    # set online/offline status on st.
    onoff_set(usr, status)

    if status == 'on' :
        next_index = size
        log_df.loc[next_index, :] = 0
        log_df.loc[next_index, usr + '_출근'] = date

    else :
        target_series = log_df.loc[:, usr + '_출근' : usr + '_퇴근']

        next_index = -1
        for index in range(target_series.shape[0]) :
            if target_series.loc[index, usr + '_출근'] != 0 :
                if target_series.loc[index, usr + '_퇴근'] == 0 :
                    next_index = index

        if next_index != -1 :
            log_df.loc[next_index, usr + '_퇴근'] = date
        else :
            log_df.loc[log_df.shape[0] - 1, usr + '_퇴근'] = date


    
    os.chdir(log_dir)
    log_df.to_excel('log.xlsx')
    whole_to_string()
    print(log_df)

# 이미 퇴근했는지 확인
def check_if_offed(usr) :
    os.chdir(log_dir)
    log_df = read_excel('log.xlsx')

    log_df.reset_index(drop = True, inplace = True)
    size = log_df.shape[0]

    start_usr = usr + '_출근'
    end_usr = usr + '_퇴근'

    target_series = log_df.loc[:, [start_usr, end_usr]]

    for index in range(target_series.shape[0]) :
        if target_series.loc[index, start_usr] != 0 :
            target_index = index
    
    if target_series.loc[target_index, end_usr] == 0 :
        return True

    else :
        return False



# 한 번동안 일한 시간 확인
def whole_elapsed(usr) :
    os.chdir(log_dir)
    log_df = read_excel('log.xlsx')

    log_df.reset_index(drop = True, inplace = True)
    size = log_df.shape[0]

    target_index = -1
    for index in range(log_df.shape[0]) :
        if log_df.loc[index, usr + '_출근'] != 0 :
            target_index = index

    if target_index != -1 :

        off_date = log_df.loc[target_index, usr + '_퇴근']
        on_date = log_df.loc[target_index, usr + '_출근']

    else :
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n' * 100)
    os.chdir(log_dir)
    log_df.to_excel('log.xlsx')

    return on_date - off_date
    
def whole_to_string() :
    os.chdir(log_dir)
    log_df = read_excel('log.xlsx')

    for index in range(log_df.shape[0]) :
        for col in log_df.columns :
            log_df.loc[index, col] = str(log_df.loc[index, col])

    log_df.to_excel('log_str.xlsx')


# 지금까지 기록상 총 얼마나 일했어?
def whole_time(usr) :
    os.chdir(log_dir)
    log_df = read_excel('log.xlsx')
    

    target_col = [usr + '_출근', usr + '_퇴근']
    target_series = log_df[target_col].copy()

    drop_index = []
    for index in range(target_series.shape[0]) :
        check = 0
        for col in target_col :
            if target_series.loc[index, col] == 0 :
                check = 1
        if check == 1 :
            drop_index.append(index)

    target_series.drop(drop_index, inplace = True)
    target_series.reset_index(drop = True, inplace = True)

    start_num = 0
    
    check = 0
    for index in range(target_series.shape[0]) :
        for col in target_series.columns :
            if target_series.loc[index, col] != 0 :
                check = 1

    if check == 0 :
        elapsed = datetime.timedelta(hours = 0)

    else :

        for num_index, index in enumerate(range(target_series.shape[0])) :
            start_time = target_series.loc[index, usr + '_퇴근']
            end_time = target_series.loc[index, usr + '_출근']
            
            print(start_time, end_time)
            print(type(start_time), type(end_time))
            
            if (str(start_time) != 'nan') & (str(end_time) != 'nan') :
                if start_num == 0 :
                    elapsed = end_time - start_time
                    start_num += 1
                    print('elapsed type is')
                    print(type(elapsed))

                else :
                    elapsed += end_time - start_time

            else :
                print('####')
                print(start_time, end_time)
                print(type(start_time), type(end_time))
                print('nan!')
                print('$$$$')
    print(elapsed, '\n')
    print(elapsed, '\n')
    print(elapsed, '\n')
    print(elapsed, '\n')
    print(elapsed, '\n')
    return elapsed


# 마지막 접속으로부터 얼마나 지났어?
def whole_last_on(usr) :
    os.chdir(log_dir)
    log_df = read_excel('log.xlsx')

    target_col = usr + '_퇴근'

    for index in range(log_df.shape[0]) :
        if log_df.loc[index, target_col] != 0 :
            last_on = log_df.loc[index, target_col]

    now_date = get_date()
    send_time = timedelta_to_string(now_date - last_on)

    return send_time
    

# 오늘 얼마동안 일했어?
def whole_last_on(usr) :
    os.chdir(log_dir)
    log_df = read_excel('log.xlsx')

    target_col = usr + '_퇴근'

    for index in range(log_df.shape[0]) :
        if log_df.loc[index, target_col] != 0 :
            last_on = log_df.loc[index, target_col]

    now_date = get_date()
    send_time = timedelta_to_string(now_date - last_on)

    return send_time

# 누가 일하고 있어?
def get_online_usr() :
    os.chdir(log_dir)
    st = read_excel('on_or_of_status.xlsx')

    on_usr = []
    for usr in usr_list() :
        if st.loc[0, usr] == 1 :
            on_usr.append(usr)

    return on_usr


def get_online_usr_string(on_usr) :
    return str(on_usr).replace('[', '').replace(']', '').replace("'", "")

       

# 일하는 상태 변경
def onoff_set(name, status) :
    os.chdir(log_dir)
    if 'on_or_of_status.xlsx' not in os.listdir(log_dir) :
        st = pd.DataFrame(columns = usr_list())
        st.loc[0, :] = 0
        st.to_excel('on_or_of_status.xlsx')

    st = read_excel('on_or_of_status.xlsx')

    if status == 'on' :
        st.loc[0, name] = 1

    if status == 'off' :
        st.loc[0, name] = 0

    st.to_excel('on_or_of_status.xlsx')

def weekday_str(weekday) :
    weekday_list = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']

    return weekday_list[weekday]

def check_last_off(usr) :
    os.chdir(log_dir)
    log_df = read_excel('log.xlsx')

    target_col = usr + '_퇴근'

    check = 0
    for index in range(log_df.shape[0]) :
        if log_df.loc[index, target_col] != 0 :
            check = 1


    if check == 0 :
        return False
    else :
        return True

    

# 수기로 작성
def add_on_usr_unit(usr, hour, minute) :
    os.chdir(log_dir)
    log_df = read_excel('log.xlsx')

    start_col = usr + '_출근'
    end_col = usr + '_퇴근'

    last_index = log_df.shape[0]

    log_df.loc[last_index, :] = 0

    log_df.loc[last_index, start_col] = get_date()
    log_df.loc[last_index, end_col] = get_date() + datetime.timedelta(hours = hour, minutes = minute)

    log_df.to_excel('log.xlsx')

@bot.command()
async def add_on_usr(ctx, name_pre, arg_time) :
    arg_hour = int(arg_time[ : 2])
    arg_minute = int(arg_time[2 :])

    arg_list = ['일했지?', '일했어?', '일했나?', '일했지', '일했어', '일했나']
    
    seodo_name = ['한지인', '지인', '서도', '한 지인', ' 한지인', '한지인 ']
    hanjoo_name = ['한주', 'faff', '김한주', '오무']
    seonghyun_name = ['승현', '이승현', '리솝', 'lisop']
    
    check = 0

    if name_pre in seodo_name :
        name = '지인'
        check = 1

    elif name_pre in seonghyun_name :
        name = '승현'
        check = 1

    elif name_pre in hanjoo_name :
        name = '한주'
        check = 1

    else :
        await ctx.send(f'unknown user {name_pre}')

    if check == 1 :
        add_on_usr_unit(name, arg_hour, arg_minute)
        await ctx.send(f'{arg_hour}h {arg_minute}m added to {name}')


@bot.command()
async def subtract_from_usr(ctx, name_pre, arg_time) :
    arg_hour = -1 * int(arg_time[ : 2])
    arg_minute = -1 * int(arg_time[2 :])

    arg_list = ['일했지?', '일했어?', '일했나?', '일했지', '일했어', '일했나']
    
    seodo_name = ['한지인', '지인', '서도', '한 지인', ' 한지인', '한지인 ']
    hanjoo_name = ['한주', 'faff', '김한주', '오무']
    seonghyun_name = ['승현', '이승현', '리솝', 'lisop']
    
    check = 0

    if name_pre in seodo_name :
        name = '지인'
        check = 1

    elif name_pre in seonghyun_name :
        name = '승현'
        check = 1

    elif name_pre in hanjoo_name :
        name = '한주'
        check = 1

    else :
        await ctx.send(f'unknown user {name_pre}')

    if check == 1 :
        add_on_usr_unit(name, arg_hour, arg_minute)
        await ctx.send(f'{arg_hour}h {arg_minute}m added to {name}')
# ----------------------------------------------------------------
# authorized functions
# ----------------------------------------------------------------

@bot.command()
async def reset_log(ctx) :
    a = input('make new log? (y/n)')
     
    if a == 'y' :
        col_list = []
        user_list = ['승현', '한주', '지인']
        for item in user_list :
            col_list.append(item + '_출근')
            col_list.append(item + '_퇴근')

        log_df = pd.DataFrame(columns = col_list)
        for col in log_df.columns :
            if '_출근' in col :
                log_df.loc[0, col] = 0
            else :
                log_df.loc[0, col] = 0

        os.chdir(log_dir)
        log_df.to_excel('log.xlsx')
        await ctx.send('new log has made')


@bot.command()
async def show_log(ctx) :
    os.chdir(log_dir)
    log_df = read_excel('log.xlsx')

    table_log = table.Table(log_df, 'log')
    table_string = table_log.make()
    await ctx.send(table_string)


@bot.command()
async def archive_log(ctx) :
    os.chdir(log_dir)
    log_df = read_excel('log.xlsx')
    log_df.to_excel('archived_log.xlsx')

    now_date = get_date()

    await ctx.send(f'log.xlsx archived to archived_log.xlsx at {now_date}')

# ----------------------------------------------------------------
# on and off functions
# ----------------------------------------------------------------

@bot.command(aliases = ['얼마동안'])
async def 얼마나 (ctx, *, arg) :
    #await ctx.send(file = discord.File(os.path.join(log_dir, 'log.xlsx')))
    name_pre = ctx.message.author.name
    arg_list = ['일했지?', '일했어?', '일했나?', '일했지', '일했어', '일했나']
    
    seodo_name = ['한지인', '지인', '서도', '한 지인', ' 한지인', '한지인 ']
    hanjoo_name = ['한주', 'faff', '김한주', '오무']
    seonghyun_name = ['승현', '이승현', '리솝', 'lisop']
    
    check = 0

    if arg in arg_list :
        if name_pre in seodo_name :
            name = '지인'
            check = 1

        elif name_pre in seonghyun_name :
            name = '승현'
            check = 1

        elif name_pre in hanjoo_name :
            name = '한주'
            check = 1

        else :
            await ctx.send(f'{name_pre}? 너 누구야?')

        if check == 1 :
            elapsed = whole_time(name)
            send_time = timedelta_to_string(elapsed)

            await ctx.send(f'{name}님 께서는 지금까지 총 {send_time}동안 일하셨어요!')


    else :
        await ctx.send(f'무슨 말씀이신지 이해하지 못했어요! {arg_list}처럼 대답해주세요!')

@bot.command(aliases = ['전체다'])
async def 전부다 (ctx, *, arg) :
    #await ctx.send(file = discord.File(os.path.join(log_dir, 'log.xlsx')))
    name_pre = ctx.message.author.name
    arg_list = ['알려줘', '알려줘!', '얼마야', '얼마야?']
    
    all_usr_list = usr_list()

    elapsed_list = []
    elapsed_notice_string = '각자 얼마나 일했는지 말씀드릴게요!\n'

    for num_name, name in enumerate(all_usr_list) :
        elapsed = whole_time(name)
        send_time = timedelta_to_string(elapsed)

        elapsed_notice_string += f'{name}님 께서는 총 \t{send_time}\t동안 일하셨어요!'

        if num_name != len(all_usr_list) - 1 :
            elapsed_notice_string += '\n'


    await ctx.send(elapsed_notice_string)





@bot.command(aliases=['출근할게', '출석했어', '출석할게'])
async def 출근했어(ctx) :

    # 마지막 접속이 하루 이상이면 50% 확률로 오랜만이야,
    # 마지막 접속이 하루가 안 되었으면 50% 확률로 벌써 왔구나!

    hi_list = ['안녕!',' 일해!', '반가워', '오랜만이야', '벌써 왔구나!']
    served_list = ['오셨네요', '꺅', '어서오세요', '기다렸어요']
    random_hi = random_item(hi_list)
    random_served = random_item(served_list)
    check = 0

    name_pre = ctx.message.author.name
    
    seodo_name = ['한지인', '지인', '서도', '한 지인', ' 한지인', '한지인 ']
    hanjoo_name = ['한주', 'faff', '김한주', '오무']
    seonghyun_name = ['승현', '이승현', '리솝', 'lisop']

    if name_pre in seodo_name :
        name = '지인'
        check = 1

    elif name_pre in seonghyun_name :
        name = '승현'
        check = 1

    elif name_pre in hanjoo_name :
        name = '한주'
        check = 1

    else :
        await ctx.send(f'{name_pre}? 너 누구야?')


    if check == 1 :
        now_date = get_date()
        whole_add_date(name, 'on', now_date) 
        await ctx.send(f'{name}, {random_hi}!')

        # who's on?
        on_usr = get_online_usr() 
        print(on_usr)
        on_usr.remove(name)
        on_usr_string = get_online_usr_string(on_usr)

        # send whole time

        await asyncio.sleep(1)

        check_last = check_last_off(name)

        if check_last == True : 
            last_on = whole_last_on(name)
            elapsed = whole_time(name)
            send_time = timedelta_to_string(elapsed)
            await ctx.send(f'{last_on}만에 찾으셨네요!\n{name}님 께서는 지금까지 총 {send_time}동안 일하셨어요!')
        else :
            await ctx.send(f'{name}님의 첫 출근이에요! 반겨주세요!')
        if len(on_usr) == 0 :
            await ctx.send('아직 아무도 출근하지 않았어요!')
        else :
            await ctx.send(f'{on_usr_string}님이 출근했네요!')



        
@bot.command(aliases=['퇴근할게', '이제갈게'])
async def 퇴근했어(ctx) :

    bye_list = ['잘가,', '고생했어', '열심히 했네']
    served_list = ['가지 마세요..', '더 있으면 안돼요..?', '잘 가요']
    worked_list = ['동안 일하셨네요!', '동안 고생했어요', '동안 일하신거에요!']

    random_worked = random_item(worked_list)
    random_bye = random_item(bye_list)
    random_served = random_item(served_list)
    check = 0

    name_pre = ctx.message.author.name
    print(f'\n_{name_pre}_\n')
    
    seodo_name = ['한지인', '지인', '서도', '한 지인', ' 한지인', '한지인 ']
    hanjoo_name = ['한주', 'faff', '김한주', '오무']
    seonghyun_name = ['승현', '이승현', '리솝', 'lisop']

    if name_pre in seodo_name :
        name = '지인'
        check = 1

    elif name_pre in seonghyun_name :
        name = '승현'
        check = 1

    elif name_pre in hanjoo_name :
        name = '한주'
        check = 1

    else :
        await ctx.send(f'{name_pre}? 너 누구야?')

    if check == 1 :
        if not check_if_offed(name) :
            await ctx.send(f'{name}님은 이미 퇴근하셨어요!')

        else :
            now_date = get_date()
            whole_add_date(name, 'off', now_date) 

            # send whole time
            elapsed = whole_elapsed(name)
            send_time = timedelta_to_string(elapsed)

            # added - whole worktime
            elapsed_whole = whole_time(name)
            send_time_whole = timedelta_to_string(elapsed_whole)

            await asyncio.sleep(1)

            await ctx.send(f'{name}님 오늘은 {send_time}동안 일하셨네요!')
            await ctx.send(f'이제 총 {send_time_whole}동안 일하셨어요!')
            

            if name == '지인' :
                await ctx.send(f'{random_served} 주인님..')

            else :
                await ctx.send(f'{random_bye} {name}!')
    



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


@bot.command()
async def alarm(ctx) :
    await ctx.send('alarm starts')

    while True :
        date = get_date()
        weekday = weekday_str(date.weekday())

        sample_hour = 21
        sample_minute = 3
        print(date.minute)
        print(type(date.minute))

        if (weekday == '토요일') | (weekday == '일요일') :
            if date.minute == 0 :
                if (date.hour == 13) | (date.hour == 19) :
                    await ctx.send(f'지금은 오후 {date.hour}시에요!\n주중에도 일을 안 하는데 주말에는 좀 해보세요')
                    print('alarm sent')

            if date.minute == sample_minute :
                if date.hour == sample_hour :
                    await ctx.send('sample alarm')

        else :
            if date.minute == 0 :
                if (date.hour == 19) :
                    await ctx.send('퇴근하셨나요?\n오늘도 일 안하면 내년 말에 책이 나올텐데요')
                    print('alarm sent')
               
                if (date.hour == 23) :
                    await ctx.send('주중에는 밤 시간이 가장 일하기 좋아요,\n책을 낼 생각이 있는 거에요?')
                    print('alarm sent')

        print(f'last check is {weekday}, {date.hour} : {date.minute}')
        await asyncio.sleep(60)

def alarm_static_item() :
    date = get_date()
    weekday = weekday_str(date.weekday())

    sample_hour = 21
    sample_minute = 3
    string = 'x'

    if (weekday == '토요일') | (weekday == '일요일') :
        if date.minute == 0 :
            if (date.hour == 13) | (date.hour == 19) :
                string = f'지금은 오후 {date.hour}시에요!\n주중에도 일을 안 하는데 주말에는 좀 해보세요'
                print('alarm sent')

#            if date.minute == sample_minute :
#                if date.hour == sample_hour :
#                    string = 'sample alarm'
#
    else :
        if date.minute == 0 :
            if (date.hour == 19) :
                string = '퇴근하셨나요?\n오늘도 일 안하면 내년 말에 책이 나올텐데요'
                print('alarm sent')
           
            if (date.hour == 23) :
                string = '주중에는 밤 시간이 가장 일하기 좋아요,\n책을 낼 생각이 있는 거에요?'
                print('alarm sent')

    print(f'last check is {weekday}, {date.hour} : {date.minute}')

    return string



def update_on_check() :
    os.chdir(log_dir)
    log = read_excel('log.xlsx')
    all_usr_list = usr_list()
    on_usr_list = get_online_usr()


    # update setups for on_check dataframe
    on_check = pd.DataFrame(columns = all_usr_list)
    on_check.loc[0, :] = 0
    for name in all_usr_list :
        if name in on_usr_list :
            on_check.loc[0, name] = 1


    # check latest on date 
    for name in all_usr_list :
        if name in on_usr_list :
            for index in range(log.shape[0]) :
                if log.loc[index, name + '_출근'] != 0 :
                    on_check.loc[1, name] = log.loc[index, name + '_출근']
    
    return on_check


def elapsed_time_60() :
    # basic informations
    all_usr_list = usr_list()
    on_usr_list = get_online_usr()
    date_now = get_date()
    weekday = weekday_str(date_now.weekday())

    # make on_elapsed dataframe
    # shows each online usr's elapsed time for every minute
    on_elapsed = pd.DataFrame(columns = all_usr_list)
    on_elapsed.loc[0, :] = 0

    # update on_check dataframe
    on_check = update_on_check()

    # update on_elapsed with on_check
    for on_name in on_usr_list :
        elapsed_date = date_now - on_check.loc[1, on_name]
        on_elapsed.loc[0, on_name] = elapsed_date

    print(on_elapsed)

    on_name_all = []
    check = 0
    actual_elapsed_time = datetime.timedelta(hours = 0)
    # alarm if elapsed hour is 1 hour, 2 hour, etc.
    for on_name in on_usr_list :
        actual_elapsed_time = timedelta_to_string(on_elapsed.loc[0, on_name])

        print(f'{on_name}, {(on_elapsed.loc[0, on_name].seconds // 60) % 60}')
        if (on_elapsed.loc[0, on_name].seconds // 60) % 60 == 0 :
            check = 1
            on_name_all.append(on_name)

    return check, on_name_all, actual_elapsed_time


@bot.command()
async def watchdog(ctx) :
    await ctx.send('watchdog starts')
    happy = ['잘 하고 있어요!', '벌써 한시간이 또 지났어요!', '잘 할 수 있어요!']

    while True :
        date_now = get_date()
        weekday = weekday_str(date_now.weekday())

        # notice in every 60 minutes
        on_60_check, all_60_usr, actual_elapsed_time = elapsed_time_60()

        if on_60_check == 1 :
            for name in all_60_usr :
                random_carrot = random_item(happy)
                await ctx.send(f'{name}님, {actual_elapsed_time}만큼 일하셨어요. {random_carrot}')

        # alarm static
        alarm_string = alarm_static_item() 

        if alarm_string != 'x' :
            await ctx.send(alarm_string)


        print(date_now)
        await asyncio.sleep(60)




@bot.command()
async def force_set(ctx, arg_name, arg_status) :
    check = 0
    name_pre = arg_name

    # random hi
    hi_list = ['안녕!',' 일해!', '반가워', '오랜만이야', '벌써 왔구나!']
    served_list = ['오셨네요', '꺅', '어서오세요', '기다렸어요']
    random_hi = random_item(hi_list)
    random_served = random_item(served_list)

    # random bye
    bye_list = ['잘가,', '고생했어', '열심히 했네']
    served_list = ['가지 마세요..', '더 있으면 안돼요..?', '잘 가요']
    worked_list = ['동안 일하셨네요!', '동안 고생했어요', '동안 일하신거에요!']


    # random items
    random_worked = random_item(worked_list)
    random_bye = random_item(bye_list)
    random_served = random_item(served_list)
    

    # available name list
    seodo_name = ['한지인', '지인', '서도', '한 지인', ' 한지인', '한지인 ']
    hanjoo_name = ['한주', 'faff', '김한주', '오무']
    seonghyun_name = ['승현', '이승현', '리솝', 'lisop']

    if name_pre in seodo_name :
        name = '지인'
        check = 1

    elif name_pre in seonghyun_name :
        name = '승현'
        check = 1

    elif name_pre in hanjoo_name :
        name = '한주'
        check = 1

    else :
        await ctx.send(f'{name_pre} not in list')


    if check == 1 :
        await ctx.send('force set status')
        if arg_status == 'on' :
            now_date = get_date()
            whole_add_date(name, 'on', now_date) 
            await ctx.send(f'{name}, {random_hi}!')

            # who's on?
            on_usr = get_online_usr() 
            print(on_usr)
            on_usr.remove(name)
            on_usr_string = get_online_usr_string(on_usr)

            # send whole time

            await asyncio.sleep(1)

            check_last = check_last_off(name)

            if check_last == True : 
                last_on = whole_last_on(name)
                elapsed = whole_time(name)
                send_time = timedelta_to_string(elapsed)
                await ctx.send(f'{last_on}만에 찾으셨네요!\n{name}님 께서는 지금까지 총 {send_time}동안 일하셨어요!')
            else :
                await ctx.send(f'{name}님의 첫 출근이에요! 반겨주세요!')
            if len(on_usr) == 0 :
                await ctx.send('아직 아무도 출근하지 않았어요!')
            else :
                await ctx.send(f'{on_usr_string}님이 출근했네요!')


        elif arg_status == 'off' :
            if not check_if_offed(name) :
                await ctx.send(f'{name}님은 이미 퇴근하셨어요!')

            else :
        
                now_date = get_date()
                whole_add_date(name, 'off', now_date) 

                # send whole time
                elapsed = whole_elapsed(name)
                print(elapsed)
                send_time = timedelta_to_string(elapsed)

                # added - whole worktime
                elapsed_whole = whole_time(name)
                send_time_whole = timedelta_to_string(elapsed_whole)

                await asyncio.sleep(1)

                await ctx.send(f'{name}님 오늘은 {send_time}동안 일하셨네요!')
                await ctx.send(f'이제 총 {send_time_whole}동안 일하셨어요!')
                

                if name == '지인' :
                    await ctx.send(f'{random_served} 주인님..')

                else :
                    await ctx.send(f'{random_bye} {name}!')


# ----------------------------------------------------------------
# GREETINGS !
# ----------------------------------------------------------------

@bot.command(aliases=['hi'])
async def 안녕(ctx):
    await ctx.send(f'안녕하세요!')


@bot.command(aliases = ['잘가'])
async def 잘있어(ctx, *, arg):
    temp_list = ['갈게', '잘게', '간다', '잔다']
    bye_list = ['잘자요,', '잘가요!', '안녕히 주무세요']

    random_bye = random_item(bye_list)

    for item in temp_list :
        if item in arg :
            arg = arg[ : arg.index(item)]

    await ctx.send(f'{random_bye} {arg}님')

@bot.command(aliases = ['고마워요', '감사합니다', '땡큐'])
async def 고마워(ctx):
    name_pre = ctx.message.author.name
    print(f'\n_{name_pre}_\n')
    
    seodo_name = ['한지인', '지인', '서도', '한 지인', ' 한지인', '한지인 ']
    hanjoo_name = ['한주', 'faff', '김한주', '오무']
    seonghyun_name = ['승현', '이승현', '리솝', 'lisop']

    if name_pre in seodo_name :
        name = '지인'
        check = 1

    elif name_pre in seonghyun_name :
        name = '승현'
        check = 1

    elif name_pre in hanjoo_name :
        name = '한주'
        check = 1

    else :
        await ctx.send(f'{name_pre}? 너 누구야?')

    if check == 1 :
        await ctx.send(f'제가 더 감사하죠, {name}님!')

@bot.command(aliases = ['꺼져!'])
async def 꺼져(ctx):
    name_pre = ctx.message.author.name
    print(f'\n_{name_pre}_\n')
    
    seodo_name = ['한지인', '지인', '서도', '한 지인', ' 한지인', '한지인 ']
    hanjoo_name = ['한주', 'faff', '김한주', '오무']
    seonghyun_name = ['승현', '이승현', '리솝', 'lisop']

    if name_pre in seodo_name :
        name = '지인'
        check = 0

    elif name_pre in seonghyun_name :
        name = '승현'
        check = 0

    elif name_pre in hanjoo_name :
        name = '한주'
        check = 1


    if check == 1 :
        await ctx.send(f'그래요! 둘다 꺼지세요!')

    else :
        await ctx.send(f'너나 꺼져!')


# ----------------------------------------------------------------
# run bot
# ----------------------------------------------------------------

bot.run(to)
