from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.adapters import Event
import nonebot
import json
data_file = "/root/testbot/testbot/plugins/config.json"

cx_trend = on_command("走势",rule=to_me(),priority=5)

@cx_trend.handle()
async def handle1(bot: Bot,event: Event,state:T_State):
    args = str(event.get_message()).strip()
    id = event.get_session_id()
    print(id)    
    if args:
        state['code']

@cx_trend.got("code",prompt="你要查询哪个基金?")        
async def handle2(bot: Bot,event: Event,state:T_State):
    code = state['code']
    message = '[CQ:image,file=http://j4.dfcfw.com/charts/pic6/' + code + '.png]'
    return await bot.call_api('send_group_msg',**{
        'group_id':'235498647',
        'message':message
        })