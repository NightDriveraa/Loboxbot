import json
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.adapters import Event



jj_cx = on_command("cx",rule=to_me(),priority=1)

@jj_cx.handle()
async def handle1(bot: Bot,event: Event,state:T_State):
    userid = str(event.get_user_id())
    jjcx = await read_data(userid)
    await jj_cx.finish(jjcx)



async def read_data(userid):
    data_file = "/root/testbot/testbot/plugins/jjconfig/"
    data_file = data_file + userid + '/data.json'
    with open(data_file,encoding='utf-8') as f:
        data = json.load(f)
    return data





