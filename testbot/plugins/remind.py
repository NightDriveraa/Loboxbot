from nonebot import require
import nonebot
import json

scheduler = require('nonebot_plugin_apscheduler').scheduler

@scheduler.scheduled_job('cron', minute='*/15',hour='21-23',day_of_week='1-5', id='test')
async def remind():
    data_file1 = "/root/testbot/testbot/plugins/config.json"
    with open(data_file1,encoding='utf-8') as f:
        userid_data = json.load(f)
    for userid in userid_data:
        data_file2 = "/root/testbot/testbot/plugins/jjconfig/" + userid + '/update.json'
        with open(data_file2,'r',encoding='utf-8') as f:
            update_data = json.load(f)
        if 'remind' not in update_data:
            update_data['remind'] = 0
        if update_data['remind'] == 1:
            continue
        if update_data['flag'] == 1:
            update_data['remind'] = 1
            with open(data_file2,'w',encoding='utf-8') as f:
                json.dump(update_data,f)
            bot = nonebot.get_bots()['80303142']
            message = '[CQ:at,qq=' + userid + ']' + '今日净值全部已更新'
            await bot.call_api('send_group_msg',**{
                'group_id':'235498647',
                'message':message
                })
    return 0