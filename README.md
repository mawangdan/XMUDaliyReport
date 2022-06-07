# 声明    
## 该项目仅用于学习和交流技术，请同学们按照自己实际情况打卡，造成的一切后果本人概不负责  
# XMUDailyReport厦门大学健康打卡
xmu健康打卡（厦门大学健康打卡）（基于python爬虫与docker自动部署）

version 1: js逆向,爬虫代码已完成  
version 2: 增加dockerfile  
version 3: 基于 Github Actions 自动打卡  

# 此情况为添加secret  CONFIG 时格式出错
![image](https://user-images.githubusercontent.com/68174279/151790352-94bf281a-8a57-454a-af5a-dc037d97ea4d.png)


# 使用说明  
## 0. 设置邮箱  
### 可参考https://service.mail.qq.com/cgi-bin/help?subtype=1&&no=1001256&&id=28  
### 0.1 依次点击  (并下拉)  
![image](https://user-images.githubusercontent.com/68174279/149703183-a94db2e0-0ce9-43f4-a738-b60c5995698d.png)  
### 0.2 设置  (需要发送短信取得的授权码即为下面的邮箱密码emailPsw)
![image](https://user-images.githubusercontent.com/68174279/149703272-ebd284b6-a377-4c7f-9859-90f4819f2a76.png)  

## 1. fork仓库  
![image](https://user-images.githubusercontent.com/68174279/149883079-3944ff23-4cbe-42e6-988e-f0fddc136b42.png)  
## 2. 添加secret  CONFIG  
### 2.1 找到secret  
![27c7598989acee9465a4cc2ac565a9d](https://user-images.githubusercontent.com/68174279/149702401-d6e58fab-7abb-483a-8136-60ef7bc82455.png)  
### 2.2 添加(添加时一定要准确复制下面的代码段并进行修改)  
![1643630732(1)](https://user-images.githubusercontent.com/68174279/151791020-bfc3600c-51b2-4242-9e17-c9181c2ad9c4.png)  

### 2.3 上方为以下代码片段
`  
{  
  "sendAddress": "",  
  "emailPsw": "",  
  "receiveAddress": "",  
  "username": "",  
  "psw": "",  
  "vpnPsw": ""  
}  
`
## 3. 开启action  
### 3.1 点击actions  
![image](https://user-images.githubusercontent.com/68174279/149702479-75bf2b14-36e1-4bbd-a611-f43a262c233d.png)  

### 3.2 enable actions  
![image](https://user-images.githubusercontent.com/68174279/149702683-3621181f-d007-47c1-9bfe-7e9090376c8f.png)

## 4. 测试运行  
![image](https://user-images.githubusercontent.com/68174279/149702965-48cae795-2d47-4db0-8060-fb46b6fe660f.png)
test4
