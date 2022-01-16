import json

#验证了post的数据框架是由 GET https://xmuxg.xmu.edu.cn/api/formEngine/business/xxx/formRenderData?playerId=owner获得
#验证了若authority的几种情况分布对应为"hide":,"readonly":的值
#readonly  [False, True]
#hide  [True, False]
#required  [False, False]
#optional  [False, False]
if __name__ == '__main__':
    with open('tempdata.json', 'r', encoding='utf-8') as f:
        j = f.read()
    with open('postData.json', 'r', encoding='utf-8') as f:
        postadta = f.read()
    jsD=json.loads(postadta)['formData']
    l=[]
    l2=[]
    jsonData=json.loads(j)['data']['components']

    for i in jsonData:
        l.append({i['title']:i['properties']['authority']})

    #l2为post请求
    for i in range(0,jsD.__len__()):
        j=jsD[i]
        l2.append({j['title']:[j['hide'],j['readonly']]})
        print(str(l[i])+str(l2[i]))
    print(l2)
    print(l)


