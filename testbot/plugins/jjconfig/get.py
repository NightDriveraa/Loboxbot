import requests
import json
import os
data_file = "/root/testbot/testbot/plugins/config.json"

def read_config():
    with open(data_file, encoding="utf-8") as f:
        config: dict = json.load(f)
    receivers = config
    return receivers


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

    columns = ['代码', '名称', '估算涨跌幅', '估算时间','单位净值']
    for fund in data_list:
        code = fund['FCODE']
        name = fund['SHORTNAME']
        try:
            rate = float(fund['GSZZL'])
        except:
            rate = 0
        gztime = fund['GZTIME']
        price = fund['NAV']
        row = [code, name, rate, gztime,price]
        temp = dict(zip(columns, row))
        rows = temp.copy()
    return rows

#盈亏估算
def count_income(receivers,userid,code,price,rate): #用户ID，基金代码，前日净值，预估涨跌幅
    price = float(price)
    code_info = receivers[userid]["codes"][code]
    count = float(code_info[0])  #份额
    old_price = float(code_info[1])
    estimate = (1+rate/100.0) * price #估计今日单份净值
    cost = count*old_price #购入总花费=购入份额*购入单价
    actual = price * count #现持有金额=前日净值*份额
    income = (estimate-price)*count #预估今日营收 = 预估今日净值*持有份额
    countincome = (estimate*count) - cost #预估总盈亏
    rows = {}
    rows["预估总盈亏"] = countincome
    rows["预估今日盈亏"] = income
    rows["现持有金额"] = actual
    return rows


def jjcx_get(userid):
    receivers = read_config()
    codes = receivers[userid]["codes"]
    strs=""
    sum2 = 0
    datafile = "/root/testbot/testbot/plugins/jjconfig/" + userid + '/'
    for code in codes:
        result1 = get_jjcx(code)
        code = result1['代码']
        name = result1['名称']
        rate = result1['估算涨跌幅']
        time = result1['估算时间']
        price = result1['单位净值']
        result2 = count_income(receivers,userid,code,price,rate) #盈亏计算
        income = round(result2['预估今日盈亏'],3)
        sum = round(result2['现持有金额'],3)
        countincome = round(result2['预估总盈亏'],3)
        sum2 += countincome
        sum2 = round(sum2,3)
        strs += "@" + str(name) + "\n" + "持有金额：" + str(sum) + '\n' + "预估涨跌幅：" + str(rate) + "\n" + "预估今日盈亏：" + str(income) + '\n' + "基金总盈亏" +str(countincome) + '\n' + "更新时间：" + str(time) + '\n' + "--------------------\n"
    strs += "总计盈亏：" + str(sum2)
    mkdir(datafile)
    datafile = datafile + 'data.json'
    with open(datafile,'w',encoding="utf-8") as f:
        json.dump(strs,f)
    return 0

def mkdir(path): 
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        return 0
    else:
        return 0



with open(data_file,'r',encoding="utf-8") as f:
    userdata = json.load(f)
for userid in userdata:
    jjcx_get(userid)


