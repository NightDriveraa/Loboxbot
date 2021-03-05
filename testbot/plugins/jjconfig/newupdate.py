import json
import requests
import os
import time

def get_time_now(fmt: str = '%Y-%m-%d %H:%M:%S'):
    ts = int(time.time())
    ta = time.localtime(ts)
    now = time.strftime(fmt, ta)
    return now

def test_file(path):
    try:
        with open(path,'r',encoding='utf-8') as f: 
            data = json.load(f)
        return 0
    except FileNotFoundError:
        data = {}
        data['flag'] = 0
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
    columns = ['代码', '更新时间']
    for fund in data_list:
        code = fund['FCODE']
        update = fund['PDATE']
        row = [code,update]
        temp = dict(zip(columns, row))
        rows = temp.copy()
    return rows
    
    
def compare_update():
    data_file = '/root/testbot/testbot/plugins/config.json'
    with open(data_file,encoding='utf-8') as f:
        file_data = json.load(f)
    
    for userid in file_data:
        flag = 1
        data = {}
        data['flag'] = 0
        data_file2 = '/root/testbot/testbot/plugins/jjconfig/' + userid + '/update.json'
        test_file(data_file2)
        with open(data_file2,encoding='utf-8') as f:
            tempdata = json.load(f)
        if tempdata['flag'] == 1:
            continue
        try:
            if tempdata['remind'] == 1:
                data['remind'] = 1
            if tempdata['remind'] == 0:
                data['remind'] = 0
        except:
            data['remind'] = 0
        for code in file_data[userid]['codes']:
            rows = get_jjcx(code)
            pdate = rows['更新时间']
            today = get_time_now(fmt='%Y-%m-%d')
            if pdate != today:
                flag = 0
        if flag == 1:
            data['flag'] = 1
        with open(data_file2,'w',encoding='utf-8') as f:
            json.dump(data,f)
            
            
compare_update()