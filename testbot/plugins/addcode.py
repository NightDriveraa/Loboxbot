from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.adapters import Event
import json

data_file = "/root/testbot/testbot/plugins/config.json"
data = None

add_jj = on_command("add",rule=to_me(),priority=5)

@add_jj.handle()
async def handle1(bot: Bot,event: Event,state:T_State):
    args = str(event.message).split(" ")
    if 1<len(args):
        if args[0]=="":
            state["code"] = args[1]
            state["quantity"] = args[2]
            state["price"] = args[3]
        else:
            state["code"] = args[0]
            state["quantity"] = args[1]
            state["price"] = args[2]
        
    userid = event.get_user_id()
    state["userid"] = str(userid)
        
@add_jj.got("code",prompt="你要绑定哪个基金?")
async def handle2(bot: Bot,event: Event,state:T_State):
    code = state["code"]
    userid = state["userid"]
    global data
    with open(data_file,"r",encoding='utf-8') as f:
        config: dict = json.load(f)
    data = config
    if userid not in data:
        data[userid]={}
        data[userid]["codes"] = {}
        data[userid]["codes"][code] = [0,0]
    elif code not in data[userid]["codes"]:
        data[userid]["codes"][code] = [0,0]
    else:
        await add_jj.finish("该基金已存在")

@add_jj.got("quantity",prompt="你所持有的基金份额是？")
async def handle3(bot: Bot,event: Event,state:T_State):
    quantity = state["quantity"]
    userid = state["userid"]
    code = state["code"]
    global data
    data[userid]["codes"][code][0] = quantity

@add_jj.got("price",prompt="你的购入单价是？")
async def handle4(bot: Bot,event: Event,state:T_State):
    price = state["price"]
    userid = state["userid"]
    code = state["code"]
    global data
    data[userid]["codes"][code][1] = price
    savefile = await save_file(data)
    await add_jj.finish(savefile)        
    
async def save_file(data_dict):
    with open(data_file,"w",encoding='utf-8') as f:
        json.dump(data_dict,f)
        return "添加成功"
        