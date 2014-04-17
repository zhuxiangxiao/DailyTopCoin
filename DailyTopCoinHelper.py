# -*- coding: UTF-8 -*-
import requests
import json
import sys
import time
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')


def getCoin(username,password):
	loginHeaders={"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Connection":"keep-alive","Accept-Language":"zh-cn","Accept-Encoding":"gzip, deflate","Content-Type":"application/x-www-form-urlencoded","Origin":"http://login.m.taobao.com","Content-Length":"347","Connection":"keep-alive","User-Agent":'''Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_6 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B651 Safari/9537.53'''}
	banHeaders={"Host":"server.ban.taobao.com","Accept-Encoding":"gzip","User-Agent":"淘伴 3.0.3 (iPhone; iPhone OS 7.0.6; zh_CN)","Connection":"keep-alive"}
	dailyCoinUrl="http://server.ban.taobao.com/v1/coin/getDailyCoin.do"
	randomCoinUrl="http://server.ban.taobao.com/v1/coin/getRandomCoin.do"
	loginUrl="http://login.m.taobao.com/login.htm"
	loginPostUrl=""
	loginParamsPage=requests.get(loginUrl).text
	loginParamsSoup=BeautifulSoup(loginParamsPage)
	loginPostUrl=loginParamsSoup.select("form")[0]["action"]
	tbToken=loginParamsSoup.select("input[name=_tb_token_]")[0]["value"]
	sid=loginParamsSoup.select("input[name=sid]")[0]["value"]
	umidToken=loginParamsSoup.select("input[name=_umid_token]")[0]["value"]
	loginParams={"_tb_token_":tbToken,"action":"LoginAction","sid":sid,"_umid_token":umidToken,"event_submit_do_login":"1","TPL_username":username,"TPL_password":password}
	loginResult=requests.post(loginPostUrl,data=loginParams,headers=loginHeaders,verify=False,allow_redirects=True)
	loginResultSoup=BeautifulSoup(loginResult.text)
	print username
	if len(loginResultSoup.select("#J_Link"))>0:
		sid=loginResultSoup.select("#J_Link")[0]["value"]



		datas={"checkCode":"","sid":sid[-32:],"clientType":"1","versionStr":"3.0.3","token":"e240e0a53fffe3846684cfc39edb520b899a9421edbc2dc6871d721646566e24"}
		request=requests.get(dailyCoinUrl, params=datas,headers=banHeaders,verify=False)
		result=json.loads(request.text)
		if result['data']['grantStatus']==1:
			print "已领取"+str(result['data']['coinToday'])+"个"
			pass
		else:
			print "每日金币已领取过"


		request=requests.get(randomCoinUrl, params=datas,headers=banHeaders,verify=False)
		result=json.loads(request.text)
		if result['data']['getCount']==0:
			print "摇一摇金币已领取过"
			pass
		else:
			print "摇一摇金币"+str(result['data']['getCount'])+"个"
		print "淘金币总数"+str(result['data']['coinSum'])+"个\n"


		
	else:
		print "登录失败\n"


config = open('config.json', 'w')
accounts = open('accounts.txt', 'r')
users=json.loads(accounts.read())
for username,password in users.items():
	getCoin(username,password)



