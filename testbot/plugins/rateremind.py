import json
import requests
import os
import time
from nonebot import require
import nonebot

scheduler = require('nonebot_plugin_apscheduler').scheduler

@scheduler.scheduled_job('cron', minute='*/30',hour='9-15',day_of_week='1-5', id='test2')
async def remind2():
    data_file1 = "/root/testbot/testbot/plugins/config.json"
    with open(data_file1,encoding='utf-8') as f:
        userid_data = json.load(f)
    for userid in userid_data:
        dict = {}
        data_file2 = "/root/testbot/testbot/plugins/jjconfig/" + userid + '/rate.json'
        test_file(data_file2)
        with open(data_file2,encoding='utf-8') as f:
            rate_data = json.load(f)
        for code in userid_data[userid]['codes']:
            result = get_jjcx(code)
            if code not in rate_data:
                rate_data[code] = ['','']
                rate_data[code][0] = result['名称']
                rate_data[code][1] = result['估算涨跌']
                with open(data_file2,'w',encoding='utf-8') as f:
                    json.dump(rate_data,f)
                continue
            old_rate = float(rate_data[code][1])
            new_rate = float(result['估算涨跌'])
            name = result['名称']
            
            if (new_rate > 0) and (old_rate > 0):
                diff = new_rate - old_rate
                if diff > 0:
                    flag = '基金<{}>估值再次增长了{}%,现估算涨跌为{}%'.format(name,str(diff),str(new_rate))
                else:
                    flag = 0
            if (new_rate > 0) and (old_rate < 0):
                diff = new_rate
                flag = '基金<{}>实现翻红，现估算涨跌为{}%'.format(name,str(round(diff,3)))
            if (new_rate < 0) and (old_rate > 0):
                diff = old_rate
                flag = '基金<{}>绿了，现估算涨跌为{}%'.format(name,str(round(diff,3)))
            if (new_rate < 0) and (old_rate < 0):
                diff = new_rate - old_rate
                if diff < -1:
                    flag = '基金<{}>又双叒叕跌了{}%,现估算涨跌为{}%'.format(name,str(round(diff,3)),str(new_rate))
                else:
                    flag = 0
            rate_data[code][0] = name
            rate_data[code][1] = result['估算涨跌']
            with open(data_file2,'w',encoding='utf-8') as f:
                json.dump(rate_data,f)
            dict[code] = flag
        strs = ''
        send = 0
        for code in dict:
            if dict[code] != 0:
                send = 1
                strs = strs + dict[code] + '\n' + "--------------------\n"
        if send == 1:
            message = '[CQ:at,qq=' + userid + ']' + '\n' + strs
            bot = nonebot.get_bots()['80303142']
            await bot.call_api('send_group_msg',**{
                'group_id':'235498647',
                'message':message
                })
    return 0
            
        
def test_file(path):
    try:
        with open(path,'r',encoding='utf-8') as f:
            return 0
    except:
        data = {}
        with open(path,'w',encoding='utf-8') as f:
            json.dump(data,f)
        return 0


def get_jjcx(code):

    headers = {
        'User-Agent': 'EMProjJijin/6.2.8 (iPhone; iOS 13.6; Scale/2.00)',
        'GTOKEN': '98B423068C1F4DEF9842F82ADF08C5db',
        'clientInfo': 'ttjj-iPhone10,1-iOS-iOS13.6',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'fundmobapi.eastmoney.com',
        'Referer': 'https://mpservice.com/516939c37bdb4ba2b1138c50cf69a2e1/release/pages/FundHistoryNetWorth',
    }

    '''获取基金实时预期涨跌幅度'''
    codes = ['']
    codes[0] = code
    data = {
        'pageIndex': '1',
        'pageSize': '300',
        'Sort': '',
        'Fcodes': ",".join(codes),
        'SortColumn': '',
        'IsShowSE': 'false',
        'P': 'F',
        'deviceid': '3EA024C2-7F22-408B-95E4-383D38160FB3',
        'plat': 'Iphone',
        'product': 'EFund',
        'version': '6.2.8',
    }

    json_response = requests.get(
        'https://fundmobapi.eastmoney.com/FundMNewApi/FundMNFInfo', headers=headers, data=data).json()
    data_list = json_response['Datas']
    columns = ['估算涨跌','名称']
    for fund in data_list:
        code = fund['FCODE']
        try:
            rate = float(fund['GSZZL'])
        except:
            rate = 0
        name = fund['SHORTNAME']
        row = [rate,name]
        temp = dict(zip(columns, row))
        rows = temp.copy()
    return rows
    
    
