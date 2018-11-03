import json

str_web_data = '{"name":"aspiring", "age": 17, "hobby": ["money","power", "read"],"parames":{"a":1,"b":2}}'
json_res = json.loads(str_web_data, encoding='utf-8')    # 输入str，返回json数据,BUGS FIND HERE,20181103 1600
encoded_json = json.dumps(json_res, sort_keys=True)     # 输入json，返回str，目的是排序


result = json.loads(encoded_json, encoding='utf-8')     # 输入str，返回json，务必要以utf-8加载json数据
print(result)
