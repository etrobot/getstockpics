# -*- coding: utf-8 -*-
# author:tonghouqi 2018-10-29
#获取港股通的每日交易数据
import json
import requests
from PIL import Image
import imgkit
import sys
import time
from locale import *
import pandas as pd

setlocale(LC_NUMERIC, 'English_US')

curDay = time.strftime("%Y%m%d")
curDay = "20181109"
temp = "https://sc.hkex.com.hk/TuniS/www.hkex.com.hk/chi/csm/DailyStat/data_tab_daily_20181115c.js"
ret_data = requests.get(temp)
json_data = ret_data.text.encode('utf-8').split("=")[1]
json_dict = json.loads(json_data)

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

for market in range(4):
    html = """
<html>
    <head>
    <meta charset="utf-8">
    <style>
        table,table tr th, table tr td { border:1px solid #000000; }
        table {text-align: center; border-collapse: collapse; padding:2px; font-weight: bold;}
        * {
            font-family: SimSun;
        }
    </style>
    </head>
	<body>
		<table bgcolor="#FFA500"width="1200" heigth="900" align="center">
"""

    sortArray = []
    tmp = json_dict[market]["content"]
    schema = tmp[0]["table"]["schema"][0]
    if market == 0 or market == 2:
        if market == 0:
            html = html + """
			<tr><td colspan=7 align="center">沪股通</td></tr>"""
        else:
            html = html + """
			<tr><td colspan=7 align="center">深股通</td></tr>"""
        html = html + """<tr>
				<td colspan=4>买入及卖出成交额 (RMB mil)</td>
				<td></td>
				<td colspan=2>""" + tmp[0]["table"]["tr"][0]["td"][0][0]+ """</td>
			</tr>
			<tr>
				<td colspan=4>买入成交额 (RMB mil)</td>
				<td></td>
				<td colspan=2>"""+  tmp[0]["table"]["tr"][1]["td"][0][0] + """</td>
			</tr>
			<tr>
				<td colspan=4>卖出成交额 (RMB mil)</td>
				<td></td>
				<td colspan=2>"""+  tmp[0]["table"]["tr"][2]["td"][0][0] + """</td>
			</tr>
			<tr>
				<td colspan=4>买入及卖出成交数目</td>
				<td></td>
				<td colspan=2>"""+  tmp[0]["table"]["tr"][3]["td"][0][0] + """</td>
			</tr>
			<tr>
				<td colspan=4>买入成交数目</td>
				<td></td>
				<td colspan=2>"""+  tmp[0]["table"]["tr"][4]["td"][0][0] + """</td>
			</tr>
			<tr>
				<td colspan=4>卖出成交数目</td>
				<td></td>
				<td colspan=2>"""+  tmp[0]["table"]["tr"][5]["td"][0][0] + """</td>
			</tr>
			<tr>
				<td colspan=4>每日额度余额(RMB mil)</td>
				<td></td>
				<td colspan=2>"""+  tmp[0]["table"]["tr"][6]["td"][0][0] + """</td>
			</tr>
			<tr>
				<td colspan=4>每日额度余额(%)</td>
				<td></td>
				<td colspan=2>"""+ tmp[0]["table"]["tr"][7]["td"][0][0] + """</td>
			</tr>
"""
    elif market == 1 or market ==3:
        if market == 1:
            html = html + """
			<tr><td colspan=7 align="center">港股通（沪）</td></tr>"""
        else:
            html = html + """
			<tr><td colspan=7 align="center">深股通（深）</td></tr>"""
        html = html + """<tr>
				<td colspan=4>买入及卖出成交额 (HKD mil)</td>
				<td></td>
				<td colspan=2>""" + tmp[0]["table"]["tr"][0]["td"][0][0]+ """</td>
			</tr>
			<tr>
				<td colspan=4>买入成交额 (HKD mil)</td>
				<td></td>
				<td colspan=2>"""+  tmp[0]["table"]["tr"][1]["td"][0][0] +"""</td>
			</tr>
			<tr>
				<td colspan=4>卖出成交额 (HKD mil)</td>
				<td></td>
				<td colspan=2>"""+  tmp[0]["table"]["tr"][2]["td"][0][0] +"""</td>
			</tr>
			<tr>
				<td colspan=4>买入及卖出成交数目</td>
				<td></td>
				<td colspan=2>"""+  tmp[0]["table"]["tr"][3]["td"][0][0] +"""</td>
			</tr>
			<tr>
				<td colspan=4>买入成交数目</td>
				<td></td>
				<td colspan=2>"""+  tmp[0]["table"]["tr"][4]["td"][0][0] +"""</td>
			</tr>
			<tr>
				<td colspan=4>卖出成交数目</td>
				<td></td>
				<td colspan=2>"""+  tmp[0]["table"]["tr"][5]["td"][0][0] +"""</td>
			</tr>
"""
    for tr in range(10):
        tmpList = []
        for td in range(1,6):
            tmpList.append(tmp[1]["table"]["tr"][tr]["td"][0][td])
        buy = (tmp[1]["table"]["tr"][tr]["td"][0][3].encode('utf-8'))
        sale = (tmp[1]["table"]["tr"][tr]["td"][0][4].encode('utf-8'))
        tmpList.append(long(atof(buy)-atof(sale)))
        sortArray.append(tmpList)

    data = pd.DataFrame(sortArray,columns=['a','b','c','d','e','f'])
    data = data.sort_values(by='f',ascending=False)

    #十大成交活跃股
    html = html + """
    <tr><td colspan=7 align="center">十大成交活跃股</td></tr>
			<tr>
				<td>排名</td>
				<td>股票代码</td>
				<td>股票名称</td>
				<td>买入金额(RMB)</td>
				<td>卖出金额(RMB)</td>
				<td>买入及卖出金额(RMB)</td>
				<td>净买入</td>
			</tr>
    """
    #循环获取十个股票的详情
    indexno = 0
    stockrow = ""
    for indexs in data.index:
        indexno = indexno + 1
        stockrow = stockrow + "<tr><td>" + str(indexno) + "</td>"
        for i in range(6):
            if i==5:
                stockrow = stockrow + "<td>" + str(data.loc[indexs].values[i].astype(long)) + "</td>"
            else:
                stockrow = stockrow + "<td>" + data.loc[indexs].values[i].encode('utf-8') + "</td>"
    stockrow = stockrow + "</td>"

    htmlend = """
		</table>
	</body>
</html>
"""

    html = html + stockrow + htmlend

#reload(sys)
#sys.setdefaultencoding('utf-8')
    options = {
        'width': 1200,
        'height': 800,
        'encoding': 'UTF-8',
     }
    imgkit.from_string(html.decode('utf-8'), 'out'+str(market)+'.jpg', options=options)






