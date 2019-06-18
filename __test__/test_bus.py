import sys
import urllib
from datetime import datetime
from itertools import count
from pprint import pprint
from urllib.request import Request, urlopen
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import xml.etree.ElementTree

'''
<ServiceResult>
<comMsgHeader/>
<msgHeader>
<headerCd>0</headerCd>
<headerMsg>정상적으로 처리되었습니다.</headerMsg>
<itemCount>0</itemCount>
</msgHeader>
<msgBody>
<itemList>
<arsId>0</arsId>
<posX>207497.59097137256</posX>
<posY>423412.5139605715</posY>
<stId>228000872</stId>
<stNm>만현10단지아이파크.현대성우5차</stNm>
<tmX>127.0845868208</tmX>
<tmY>37.30985611</tmY>
</itemList>
</msgBody>
</ServiceResult>
'''

def find_bus():
    route_list = {
        '234000026':'720-2',
        '241420004':'82',
        '241420009':'99',
        '234000316':'60',
        '200000040':'7-2',
        '241420006':'82-1',
        '234000027':'6900',
        '234000046':'660',
        '234000047':'720',
        '234000136':'1550',
        '234000148':'5500-2'
    }

    for routeId, busNo in route_list.items():
        serviceKey = '1lBTg3Wf3TL8YVmhzsITTekQ9sLbCsYdgN900X7wl5kwx70UMdmKHTl60QPh%2B%2FiSVHn7fJjI99CinyOkZy6gRg%3D%3D'
        stationId='228000872'
        routeId=str(routeId)
        url = "http://openapi.gbis.go.kr/ws/rest/busarrivalservice?serviceKey={}&stationId={}&routeId={}".format(serviceKey, stationId,routeId)

        request = Request(url)

        response = urlopen(request)

        receive = response.read()
        html = receive.decode('utf-8', errors='replace')
        bs = BeautifulSoup(html, 'html.parser')

        if bs.resultmessage.text == '정상적으로 처리되었습니다.':
            print(busNo, ' : ', bs.predicttime1.text)
            print(busNo, ' : ', bs.predicttime2.text)



if __name__ == '__main__':
    find_bus()

