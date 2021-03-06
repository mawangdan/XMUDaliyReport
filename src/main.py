# coding=utf-8
import requests
import re
import execjs
import json
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

sendAddress = ''
emailPsw = ''
receiveAddress = ''
username = ''
psw = ''


def loadConfig():
    with open('config.json', 'r', encoding='utf-8') as f:
        config = f.read()
    configJson = json.loads(config)
    print(configJson)
    global sendAddress, emailPsw, receiveAddress, username, psw
    sendAddress = configJson['sendAddress']
    emailPsw = configJson['emailPsw']
    receiveAddress = configJson['receiveAddress']
    username = configJson['username']
    psw = configJson['psw']


def sendEmail(msgJson):
    try:
        stuName = msgJson['data']['owner']['name']
        info = stuName + '\n您已打卡成功'
    except:
        info = '打卡失败\n详细信息:' + str(msgJson)
    msg = MIMEText(info, 'plain', 'utf-8')  # 填写邮件内容
    msg['From'] = formataddr(["厦门大学健康打卡", sendAddress])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
    msg['To'] = formataddr([receiveAddress, receiveAddress])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
    msg['Subject'] = "厦门大学健康打卡"  # 邮件的主题，也可以说是标题

    server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器
    server.login(sendAddress, emailPsw)  # 括号中对应的是发件人邮箱账号、邮箱授权码
    server.sendmail(sendAddress, [receiveAddress, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
    server.quit()  # 关闭连接


def encrypt(pwd, key):
    """
    调用js加密函数
    :param pwd:
    :param key:
    :return:
    """
    with open('encrypt.js', 'r', encoding='utf-8') as f:
        j = f.read()
    js = execjs.compile(j)
    return js.call('encryptAES', pwd, key)


def getDataFrame(session, headers, businessId):
    """
    获得打卡的post json框架
    :param session:
    :param headers:
    :param businessId:
    :return: 框架
    """
    authorityMap = {'readonly': {'hide': 'true', "readonly": 'false'}, 'hide': {"hide": 'true', "readonly": 'false'},
                    'required': {'hide': 'true', "readonly": 'false'},
                    'optional': {'hide': 'true', "readonly": 'false'}}

    list = []
    dataFrameJson = session.get(
        'https://xmuxg.xmu.edu.cn/api/formEngine/business/' + str(businessId) + '/formRenderData?playerId=owner',
        headers=headers).json()['data']['components']
    for data in dataFrameJson:
        tempDict = {}
        tempDict.update({"name": data['name']})
        tempDict.update({"title": data['title']})
        tempDict.update({'value': {}})
        tempDict.update(authorityMap[data['properties']['authority']])
        list.append(tempDict)
    return {"formData": list, "playerId": "owner"}


def injectPersonalData(formDataJson, personalDataList):
    """
    将个人信息注入到formData内
    并修改为已打卡
    :param formDataJson:
    :param personalDataList:
    :return: 注入值的框架
    """

    dataMap = {}  # 建立title与value映射表
    for personalData in personalDataList:
        valueData = {}
        # 地址字段
        if (personalData['value']['dataType'] == "ADDRESS_VALUE"):
            valueData.update({'addressValue': personalData['value']['addressValue']})
        # 普通字段
        elif (personalData['value']['dataType'] == "STRING"):
            valueData.update({'stringValue': personalData['value']['stringValue']})
        # 时间字段
        elif (personalData['value']['dataType'] == "DATE"):
            valueData.update({'dateValue': personalData['value']['dateValue']})

        dataMap.update({personalData['title']: valueData})
    # 修改为已打卡
    title1 = 'Can you hereby declare that all the information provided is all true and accurate and there is no concealment, false information or omission. 本人是否承诺所填报的全部内容均属实、准确，不存在任何隐瞒和不实的情况，更无遗漏之处。'
    dataMap[title1]['stringValue'] = "是 Yes"
    title2 = '学生本人是否填写'
    dataMap[title2]['stringValue'] = '是'
    # 将value注射进list
    list = formDataJson['formData']
    for i in range(0, list.__len__()):
        # 如果有此字段的value则注入
        if (dataMap.__contains__(list[i]['title'])):
            list[i]['value'] = dataMap[list[i]['title']]

    return {"formData": list, "playerId": "owner"}


if __name__ == '__main__':
    # 加载配置
    loadConfig()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    }
    s = requests.session()
    response = s.get('https://ids.xmu.edu.cn/authserver/login?service=https://xmuxg.xmu.edu.cn/login/cas/xmu')
    HTML = BeautifulSoup(response.text, 'html.parser')
    pwdDefaultEncryptSalt = HTML.find_all('input', attrs={'id': 'pwdDefaultEncryptSalt'})[0].attrs['value']
    lt = HTML.find_all('input', attrs={'name': 'lt'})[0].attrs['value']
    dllt = HTML.find_all('input', attrs={'name': 'dllt'})[0].attrs['value']
    execution = HTML.find_all('input', attrs={'name': 'execution'})[0].attrs['value']
    _eventId = HTML.find_all('input', attrs={'name': '_eventId'})[0].attrs['value']
    rmShown = HTML.find_all('input', attrs={'name': 'rmShown'})[0].attrs['value']

    encryptPsw = encrypt(psw, pwdDefaultEncryptSalt)
    body = {'username': username,
            'password': encryptPsw,
            'lt': lt,
            'dllt': dllt,
            'execution': execution,
            '_eventId': _eventId,
            'rmShown': rmShown}
    s.post('https://ids.xmu.edu.cn/authserver/login?service=https://xmuxg.xmu.edu.cn/login/cas/xmu', data=body,
           headers=headers)
    r1 = s.get('https://xmuxg.xmu.edu.cn/api/app/214/business/now?getFirst=true', headers=headers)
    print(r1.text)
    businessId = r1.json()['data'][0]['business']['id']
    businessId = businessId
    # 获得框架
    formDataJson = getDataFrame(s, headers, businessId)

    # 获得个人信息
    r2Json = s.get(
        'https://xmuxg.xmu.edu.cn/api/formEngine/business/' + str(businessId) + '/myFormInstance').json()

    # 注入个人信息
    formData = injectPersonalData(formDataJson, r2Json['data']['formData'])

    # 打卡post的url
    instanceId = r2Json['data']['id']
    form_url = f'https://xmuxg.xmu.edu.cn/api/formEngine/formInstance/' + instanceId
    # 打卡
    resp = s.post(form_url, json=formData, headers=headers)
    sendEmail(resp.json())
