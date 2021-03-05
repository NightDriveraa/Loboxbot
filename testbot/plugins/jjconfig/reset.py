import json

data_file1 = "/root/testbot/testbot/plugins/config.json"
with open(data_file1,encoding='utf-8') as f:
    userid_data = json.load(f)
for userid in userid_data:
    data_file2 = "/root/testbot/testbot/plugins/jjconfig/" + userid + '/update.json'
    with open(data_file2,'r',encoding='utf-8') as f:
        data = json.load(f)
    data['flag'] = 0
    data['remind'] = 0
    with open(data_file2,'w',encoding='utf-8') as f:
        json.dump(data,f)
            