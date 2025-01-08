from typing import List, Any, Union

import requests
import pandas as pd
import re
import xlsxwriter
from datetime import datetime
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service

import time
import html2text

# chrome_options = webdriver.ChromeOptions()

user = ''
password = ''
url = 'https://www.olx.co.id'


# browser = webdriver.Chrome('chromedriver',options=chrome_options)

edge_options = Options()
edge_options.add_argument('--headless')
edge_options.add_argument('--disable-gpu')

# firefox_options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
edge_options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
driver_path = 'D:\web_scrapping\olx_scrapping\msedgedriver.exe'
service = Service(driver_path)
browser = webdriver.Edge(
    executable_path=driver_path,
    options=edge_options
)

now = datetime.now()
dt_string = now.strftime("%d%m%y")
id_location = [[2000007,"Jakarta D.K.I."],
               [2000031,"Sumatra Utara"],
               [2000009,"Jawa Barat"],
               [2000011,"Jawa Timur"],
               [2000004,"Banten"],
               [2000032,"Yogyakarta"],
               [2000010,"Jawa Tengah"],
               [2000002,"Bali"],
               [2000016,"Lampung"],
               [2000013,"Kalimantan Selatan"],
               [2000030,"Sumatra Selatan"],
               [2000025,"Sulawesi Selatan"],
               [2000001,"Aceh D.I."],
               [2000024,"Riau"],
               [2000015,"Kalimantan Timur"],
               [2000029,"Sumatra Barat"],
               [2000034,"Kepulauan Riau"],
               [2000019,"Nusa Tenggara Barat"],
               [2000008,"Jambi"],
               [2000012,"Kalimantan Barat"]]
sorting=['desc-relevance',
         'desc-creation',
         'asc-price',
         'desc-price']
file_level = 'level3.xlsx'
result = [['url', 'id', 'user_id', 'location_region', 'location_city', 'location_district', \
           'title', 'price', 'alamat', 'latitude', 'longitude', 'kamar_mandi', 'fasilitas', 'luas_bangunan', 'description', 'has_phone_param']]
output = 'olx_result_'+dt_string+'.xlsx'
# output_previous = 'olx_result_011122 - 1.xlsx'
output_user = 'olx_user_'+dt_string+'.xlsx'
# output = 'olx_result_311022.xlsx'

def getPage(location = 1000001, page = 0):
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'category': '4833',
        'facet_limit': '1000',
        'location': str(location),
        'location_facet_limit': '200',
        'page': str(page),
        'platform': 'web-desktop',
        'sorting':'desc-price',
        'user': '',
    }

    response = requests.get('https://www.olx.co.id/api/relevance/v2/search', params=params, headers=headers)

    return response

# def getPhoneOri():
#     import requests
#
#     cookies = {
#         # '__exponea_etc__': '181bbbbd-2c69-41b0-bb7c-cb88449bace7',
#         # '_gcl_au': '1.1.30555702.1663668509',
#         # '_rtb_user_id': '1e886c08-539a-8c2f-c13e-fe670146ceef',
#         # '_ga': 'GA1.3.1256204247.1663668509',
#         # 'WZRK_G': 'c7691855eb13421086847570790a9d2e',
#         # '_fbp': 'fb.2.1663668509573.1816142443',
#         # '_tt_enable_cookie': '1',
#         # '_ttp': 'b85268a9-12c1-45ea-9b48-c099f8b9ebbf',
#         # '__gads': 'ID=17a38a90a2f5a8e1:T=1663668509:S=ALNI_Ma89YsbDvXUBZgmJx10I6sjeBP0qA',
#         # 'g_state': '{"i_p":1663675779940,"i_l":1}',
#         # 'G_ENABLED_IDPS': 'google',
#         # 'laquesisff': '',
#         # 'laquesissu': '',
#         # 'user': 'j%3A%7B%22id%22%3A%2260359769%22%2C%22name%22%3A%22OLX%20User%22%7D',
#         # 'lf': '1',
#         # 'bm_sz': 'B3BE7A64E4E60F2A6F681FB6300CC511~YAAQVSg0F5NUfPWDAQAABGMT+RE6W0nx79JCZjLXPTna/cFPwqovUF8b/Lv6lVIu1g8Kx44mvdfWe8UxOzpVLPOlmKKQZjJ6bNmxn+jygwWwscuvS/Z3oeTZDn+j/Mn0ZF3O4kTSFypqRyQWyRWMTO3dat5Qn1XMz5phjYw799QRUFVXn/+LQjUUdkP6G/GdMbW3oW+6jrsA3VFkjOOj2EEG+9bhDdmeaSw2+1HQ6pRvBNdMItmQumhyXKIUZoqBoEmyT3KrDQOCfN3byB6mSUqSqaKYinTqrWw7fvRmnnbQgg==~3616825~3487809',
#         # '_gid': 'GA1.3.1982268791.1666331154',
#         # '__gpi': 'UID=000009d1299e2a67:T=1663668509:RT=1666331154:S=ALNI_MYkK1mp7F7GmkgPoT1OxS44ayjcNw',
#         # '_cc_id': 'fa43097bdfd9f4edcc4af431dceabb7c',
#         # 'panoramaId_expiry': '1666935955745',
#         # 'panoramaId': '3e9583293a579e9d620ad61e4d8d16d539380bbd2b2f92f2d5b5d6d4e15c5223',
#         # 'reply_restriction': 'false',
#         # 'kyc_reply_count': '0',
#         # 'laquesis': 'pan-60601@b#pan-67471@b#road-10534@a',
#         # '__exponea_time2__': '-0.2243027687072754',
#         # 'locationPath': '%5B%7B%22id%22%3A2000007%2C%22name%22%3A%22Jakarta%20D.K.I.%22%2C%22type%22%3A%22STATE%22%2C%22longitude%22%3A106.84513%2C%22latitude%22%3A-6.21462%2C%22parentId%22%3A1000001%7D%5D',
#         # 'bm_mi': 'E41AD44D3B10F28C085AD8D0CF1FC9D2~YAAQhXpAF8DtktGDAQAANN2C+RFYQcdSemdPDEqmo6TOFxAilWikVDQWmVTuerPSXAIPyPLb6wumT1wCFIixwNViYh1NUK3WwCXbi7u/KY6kM7cRH6t9ZlPZ0YiluOQ2/OpENKqrKj0jCiK7mRxJEkfrFm69ck0HeW6UxP3VJEYB/2IEW5PwGi9QOL8MfTlF7xIRPzy3u1VsayZcls4DVPKUM348eMi9DIwBTysKHb+USIIy2YgyN+9c3j35f+Wgz0KIx2OLKzQzdo1tmRWdGKRrfiJDWYDS3+bzJrFUDRpAiGZW7JyQmnJ1T8C5hgCPknRZrqow9kH8ugN93xqg~1',
#         # 'ak_bmsc': '7C3F21F9E928BD40610D6FBAE58B6769~000000000000000000000000000000~YAAQhXpAF2vxktGDAQAAIR6D+RFKU/ROsD7ysoxAF5QKtBXS8I3zOQj0Egs9/TEcE93es1OA6eckYfMw6bjofcum4WLQKbIaEy0MMZlN3Xx+MguUqz2mRCYunCdT2Bvkx7Y/efjCbt9VY3vXBCwmzN2nknEtZpeZxIOhLpjQoWbj87cV93m/Is5fmF1LxYhy/t/R41pfa9N50pr+S9WxnZpdEi/TzQWzfqAnBSsKVAqhhRkp007SOFov/+tlBs2TDbRfjkIBAbUWNGJOsrRODPQE1UsjhjoyIDnzVuphWRuDm2ohxTI0kog9LCizPvEx7wKaveNnnSrdaDCPJd/5iekFBtmsOAFWikU3PLf/+7XungyXQqp9UOO0/SDwqze2/kAYvXCf+bX7QAR3EKggx64URqqWCopxFHoLSo0t/bjpkV3Yjdny0wIZvKrTU0aMFX0MJzQJFO2s5dVQYuFC566WDFP0dcp/UclkBRtnzroMmj7gaP93RJUE6lHl4prPSc0ImaJZYQae5cb2JIU=',
#         # 'AMP_TOKEN': '%24NOT_FOUND',
#         # 'lqstatus': '1666340009|183f943e121x25fe11a7|pan-60601||',
#         't': '',
#         # 't': 'eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCIsImtpZCI6ImViT21QTmlrIn0.eyJncmFudFR5cGUiOiJncGx1cyIsImNsaWVudFR5cGUiOiJ3ZWIiLCJ0b2tlblR5cGUiOiJhY2Nlc3NUb2tlbiIsImlzTmV3VXNlciI6ZmFsc2UsImlhdCI6MTY2NjMzOTMzMiwiZXhwIjoxNjY2MzQwMjMyLCJhdWQiOiJvbHhpZCIsImlzcyI6Im9seCIsInN1YiI6IjYwMzU5NzY5IiwianRpIjoiYmI4NjhhZGJkMDVkMWQ1MmY1Zjc1NmE3ZTUzYWM2ODVlODc3OGU1MyJ9.P9nTJWVJMIRDztsAbzKeo-t1zYGqtSa5gSVnUy0bOWsiyIcal5WBTqKNrT5tG1nkIT2atwU_BOQi34FqLF_di6vxXBQHnIvcnb5fNsu4xMsDXZJKb0v8eEEKlHaZvsVqJEykRwfREp9oMgv8wkh1UPtTF28iPa1wHEOgVt23E3FmtkJY_LtHzEK0OpFR7ddKIwwmPbm0qrM37QPheytQlQTayb-SolxVZUdXXd5tijatQciskowNNfZ5xccr2lLf3223X5rocG6Nx7YYC-zSsDnj4MwEtt7gWaiNhPJf4V0Yn7rGPakU83gM3Tctgi0w_46vs1f8azkgmzENBX2nng',
#         # 'rt': 'eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCIsImtpZCI6ImViT21QTmlrIn0.eyJncmFudFR5cGUiOiJncGx1cyIsImNsaWVudFR5cGUiOiJ3ZWIiLCJ0b2tlblR5cGUiOiJyZWZyZXNoVG9rZW4iLCJyZWFjdGl2YXRlZCI6ZmFsc2UsImlhdCI6MTY2NjMzOTMzMiwiZXhwIjoxNjc0Mzc0NTMyLCJhdWQiOiJvbHhpZCIsImlzcyI6Im9seCIsInN1YiI6IjYwMzU5NzY5IiwianRpIjoiYmI4NjhhZGJkMDVkMWQ1MmY1Zjc1NmE3ZTUzYWM2ODVlODc3OGU1MyJ9.DuvokG7x0pUtnqWhJcKU6aZ7gV8BpVlBoAdmooIVw09Azwp5-O1PNYdjMaDvwcAfDY2FoaVHXX17VoLjBII2FKlRebJEiY9lFv6e21L34WKExHGT6rHwwlSzXwVT1o9xu4J1hvZRjcNQV6hxttJ-CZ1khlCVlE1e1POH5a_v3UMD1yPg0MQlGIhp60c_n8ggWXlAtJZtS_F34xuHs7mYnicL0ImvFnldsVg5o07n1gh1lG5MOpUHFR2Il1p4NIh32UHjIBnSadqsZ5xHpb2eKmFkWTZBcw3ASuOzFI06-o4Tack1xPU70lW_PoHU85ntAMZS0DmGlgkfz1Pm4Gnmng',
#         # 'ct': 'eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCIsImtpZCI6ImViT21QTmlrIn0.eyJ0b2tlblR5cGUiOiJjaGF0VG9rZW4iLCJ2ZXJzaW9uIjoiMSIsImlhdCI6MTY2NjMzOTMzMiwiZXhwIjoxNjY2NDI1NzMyLCJhdWQiOiJvbHhpZCIsImlzcyI6Im9seCIsInN1YiI6IjYwMzU5NzY5IiwianRpIjoiYmI4NjhhZGJkMDVkMWQ1MmY1Zjc1NmE3ZTUzYWM2ODVlODc3OGU1MyJ9.k6NNzlSy7BoEUCdokDXWSEjWMeEeU-SZqxpN7-ege9Jbry3Oa4M96yipizD8euYEPGDkvKD7tr1o9aCkI3tnNZ8nXITlnFCFD9TaYSBh61dEgZPT69zpAMpFgkZRlYnzGO0bFUm-yrawbXvIF3ElCK3hd_oll2CCQEIiTYxNkQwrVYrM3DgskAOMc5q2NaZ20pgM8KjSwGhdMMl0VVxutPZ2QIE-rT3Aj2dSwFEtrUGP8-o8y1rh9dnCso_tL5kQWmxu_mhGcSj5Q0tVEuafQIytU2D0YcPE9Q2iCy3wZVOK6qFY8uI8B2Tnhnxo--q5731vgemca4GvnZb9ZN5VXQ',
#         # 'nt': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2NjYzMzkzMzIsImJyYW5kIjoib2x4IiwiY291bnRyeUNvZGUiOiJpZCIsInVzZXJJZCI6NjAzNTk3Njl9.fyiFk_wdMoB50m-kpG-VWo3l0DG4EEmUDznPPXW-T9Y',
#         # '_gat_clientNinja': '1',
#         # '_abck': 'D2DB6D16FA06AEA0A1FCCCD72E0AE17A~0~YAAQVSg0Fy6fjPWDAQAA3IyQ+QiZg5iZEH0tyq7htkqxXlrUfxqTS9nvrvXO1omXJLt7sKLNu9PRvtrd/8Vt7qSBV1J0zw3sstTOBh3MUcEpFnaAob/0NNUqniQf2L4I6VcPImbn1It4WJ5fZA2QQXGOi94BSEhPXPUz2meMSvCaQU7TKUdHgln+tfhM7yUv0R3E4vTJyY4Yi/pTt61qyj+ajrxJAoZOmkDrMnzKBQpe+eE5R1pwY4urhJntQ9XHyh4DnHJklHksfnJ8YlyilplFH/mMNmF296ukFoQMgmncrdMsxyvea0B8bDCUOhdD+HzSWAGo+K4rWocVPjnpmag+shZwCz/M/vkB0jgTDTVE320KkIKQ7K+l2WJnPWiIoPrrz4wagRYE5HWvWa96FnBMsXsPBhM=~-1~-1~-1',
#         # 'ldTd': 'true',
#         # 'MgidSensorNVis': '45',
#         # 'MgidSensorHref': 'https://www.olx.co.id/item/falukost-tomang-kos-exclusive-pria-wanita-kost-tomang-untar-trisakti-iid-806356711',
#         # '_gat_UA-116132414-3': '1',
#         # 'cto_bundle': 'puiFKF80U0hmV3V1eGxRQkE2dFlxRWdYWUd0d2hNZUMzamw1eU5vSFMzb1YxQURucjFyRFp0Z29lTHQ2Zmc4WUVVV1FvYUdrRjk2SjdWNXF4bHhzQ1FiWVRycGM1STA1R1hmMlN4bnBuZSUyQjQ3WWFuR0lzeW1CM1klMkZYQzdvMmlGWFczVUN0V2p6T0REUmM4NGpjaDd1SEwwaHVRJTNEJTNE',
#         # 'WZRK_S_W6K-746-995Z': '%7B%22p%22%3A43%2C%22s%22%3A1666337086%2C%22t%22%3A1666339358%7D',
#         # 'onap': '1835a5ec649x378f8b0b-3-183f943e121x25fe11a7-331-1666341161',
#         # 'bm_sv': 'EAD5B20681125C2D001B7EE1FE7A6537~YAAQVSg0F36rjPWDAQAA/9GQ+RFeGf7/5rABsvwsbezru4N+4wUy0gygdXoTsBsNFPosFgCu6vz1rsxIvyOmir/QYxNt+QicR7/fH4T9+vnEnwXs51cGvEaWgd9L1NOKKEUQtg7wO0uMnqPFUvi+XKqGvz3XglvQ3oUdyQ0DSL/RYdvgI+VN+s4QDJUDF1rXBUBnwv2TEkILqRtHnd0CVvrzT+CXNMSbI8KW5PiGvMMo1iUyla5F6dgHZ2OdHDA1aA==~1',
#     }
#
#     headers = {
#         'authority': 'www.olx.co.id',
#         'accept': '*/*',
#         'accept-language': 'en-US,en;q=0.9,id;q=0.8',
#         # Requests sorts cookies= alphabetically
#         # 'cookie': '__exponea_etc__=181bbbbd-2c69-41b0-bb7c-cb88449bace7; _gcl_au=1.1.30555702.1663668509; _rtb_user_id=1e886c08-539a-8c2f-c13e-fe670146ceef; _ga=GA1.3.1256204247.1663668509; WZRK_G=c7691855eb13421086847570790a9d2e; _fbp=fb.2.1663668509573.1816142443; _tt_enable_cookie=1; _ttp=b85268a9-12c1-45ea-9b48-c099f8b9ebbf; __gads=ID=17a38a90a2f5a8e1:T=1663668509:S=ALNI_Ma89YsbDvXUBZgmJx10I6sjeBP0qA; g_state={"i_p":1663675779940,"i_l":1}; G_ENABLED_IDPS=google; laquesisff=; laquesissu=; user=j%3A%7B%22id%22%3A%2260359769%22%2C%22name%22%3A%22OLX%20User%22%7D; lf=1; bm_sz=B3BE7A64E4E60F2A6F681FB6300CC511~YAAQVSg0F5NUfPWDAQAABGMT+RE6W0nx79JCZjLXPTna/cFPwqovUF8b/Lv6lVIu1g8Kx44mvdfWe8UxOzpVLPOlmKKQZjJ6bNmxn+jygwWwscuvS/Z3oeTZDn+j/Mn0ZF3O4kTSFypqRyQWyRWMTO3dat5Qn1XMz5phjYw799QRUFVXn/+LQjUUdkP6G/GdMbW3oW+6jrsA3VFkjOOj2EEG+9bhDdmeaSw2+1HQ6pRvBNdMItmQumhyXKIUZoqBoEmyT3KrDQOCfN3byB6mSUqSqaKYinTqrWw7fvRmnnbQgg==~3616825~3487809; _gid=GA1.3.1982268791.1666331154; __gpi=UID=000009d1299e2a67:T=1663668509:RT=1666331154:S=ALNI_MYkK1mp7F7GmkgPoT1OxS44ayjcNw; _cc_id=fa43097bdfd9f4edcc4af431dceabb7c; panoramaId_expiry=1666935955745; panoramaId=3e9583293a579e9d620ad61e4d8d16d539380bbd2b2f92f2d5b5d6d4e15c5223; reply_restriction=false; kyc_reply_count=0; laquesis=pan-60601@b#pan-67471@b#road-10534@a; __exponea_time2__=-0.2243027687072754; locationPath=%5B%7B%22id%22%3A2000007%2C%22name%22%3A%22Jakarta%20D.K.I.%22%2C%22type%22%3A%22STATE%22%2C%22longitude%22%3A106.84513%2C%22latitude%22%3A-6.21462%2C%22parentId%22%3A1000001%7D%5D; bm_mi=E41AD44D3B10F28C085AD8D0CF1FC9D2~YAAQhXpAF8DtktGDAQAANN2C+RFYQcdSemdPDEqmo6TOFxAilWikVDQWmVTuerPSXAIPyPLb6wumT1wCFIixwNViYh1NUK3WwCXbi7u/KY6kM7cRH6t9ZlPZ0YiluOQ2/OpENKqrKj0jCiK7mRxJEkfrFm69ck0HeW6UxP3VJEYB/2IEW5PwGi9QOL8MfTlF7xIRPzy3u1VsayZcls4DVPKUM348eMi9DIwBTysKHb+USIIy2YgyN+9c3j35f+Wgz0KIx2OLKzQzdo1tmRWdGKRrfiJDWYDS3+bzJrFUDRpAiGZW7JyQmnJ1T8C5hgCPknRZrqow9kH8ugN93xqg~1; ak_bmsc=7C3F21F9E928BD40610D6FBAE58B6769~000000000000000000000000000000~YAAQhXpAF2vxktGDAQAAIR6D+RFKU/ROsD7ysoxAF5QKtBXS8I3zOQj0Egs9/TEcE93es1OA6eckYfMw6bjofcum4WLQKbIaEy0MMZlN3Xx+MguUqz2mRCYunCdT2Bvkx7Y/efjCbt9VY3vXBCwmzN2nknEtZpeZxIOhLpjQoWbj87cV93m/Is5fmF1LxYhy/t/R41pfa9N50pr+S9WxnZpdEi/TzQWzfqAnBSsKVAqhhRkp007SOFov/+tlBs2TDbRfjkIBAbUWNGJOsrRODPQE1UsjhjoyIDnzVuphWRuDm2ohxTI0kog9LCizPvEx7wKaveNnnSrdaDCPJd/5iekFBtmsOAFWikU3PLf/+7XungyXQqp9UOO0/SDwqze2/kAYvXCf+bX7QAR3EKggx64URqqWCopxFHoLSo0t/bjpkV3Yjdny0wIZvKrTU0aMFX0MJzQJFO2s5dVQYuFC566WDFP0dcp/UclkBRtnzroMmj7gaP93RJUE6lHl4prPSc0ImaJZYQae5cb2JIU=; AMP_TOKEN=%24NOT_FOUND; lqstatus=1666340009|183f943e121x25fe11a7|pan-60601||; t=eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCIsImtpZCI6ImViT21QTmlrIn0.eyJncmFudFR5cGUiOiJncGx1cyIsImNsaWVudFR5cGUiOiJ3ZWIiLCJ0b2tlblR5cGUiOiJhY2Nlc3NUb2tlbiIsImlzTmV3VXNlciI6ZmFsc2UsImlhdCI6MTY2NjMzOTMzMiwiZXhwIjoxNjY2MzQwMjMyLCJhdWQiOiJvbHhpZCIsImlzcyI6Im9seCIsInN1YiI6IjYwMzU5NzY5IiwianRpIjoiYmI4NjhhZGJkMDVkMWQ1MmY1Zjc1NmE3ZTUzYWM2ODVlODc3OGU1MyJ9.P9nTJWVJMIRDztsAbzKeo-t1zYGqtSa5gSVnUy0bOWsiyIcal5WBTqKNrT5tG1nkIT2atwU_BOQi34FqLF_di6vxXBQHnIvcnb5fNsu4xMsDXZJKb0v8eEEKlHaZvsVqJEykRwfREp9oMgv8wkh1UPtTF28iPa1wHEOgVt23E3FmtkJY_LtHzEK0OpFR7ddKIwwmPbm0qrM37QPheytQlQTayb-SolxVZUdXXd5tijatQciskowNNfZ5xccr2lLf3223X5rocG6Nx7YYC-zSsDnj4MwEtt7gWaiNhPJf4V0Yn7rGPakU83gM3Tctgi0w_46vs1f8azkgmzENBX2nng; rt=eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCIsImtpZCI6ImViT21QTmlrIn0.eyJncmFudFR5cGUiOiJncGx1cyIsImNsaWVudFR5cGUiOiJ3ZWIiLCJ0b2tlblR5cGUiOiJyZWZyZXNoVG9rZW4iLCJyZWFjdGl2YXRlZCI6ZmFsc2UsImlhdCI6MTY2NjMzOTMzMiwiZXhwIjoxNjc0Mzc0NTMyLCJhdWQiOiJvbHhpZCIsImlzcyI6Im9seCIsInN1YiI6IjYwMzU5NzY5IiwianRpIjoiYmI4NjhhZGJkMDVkMWQ1MmY1Zjc1NmE3ZTUzYWM2ODVlODc3OGU1MyJ9.DuvokG7x0pUtnqWhJcKU6aZ7gV8BpVlBoAdmooIVw09Azwp5-O1PNYdjMaDvwcAfDY2FoaVHXX17VoLjBII2FKlRebJEiY9lFv6e21L34WKExHGT6rHwwlSzXwVT1o9xu4J1hvZRjcNQV6hxttJ-CZ1khlCVlE1e1POH5a_v3UMD1yPg0MQlGIhp60c_n8ggWXlAtJZtS_F34xuHs7mYnicL0ImvFnldsVg5o07n1gh1lG5MOpUHFR2Il1p4NIh32UHjIBnSadqsZ5xHpb2eKmFkWTZBcw3ASuOzFI06-o4Tack1xPU70lW_PoHU85ntAMZS0DmGlgkfz1Pm4Gnmng; ct=eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCIsImtpZCI6ImViT21QTmlrIn0.eyJ0b2tlblR5cGUiOiJjaGF0VG9rZW4iLCJ2ZXJzaW9uIjoiMSIsImlhdCI6MTY2NjMzOTMzMiwiZXhwIjoxNjY2NDI1NzMyLCJhdWQiOiJvbHhpZCIsImlzcyI6Im9seCIsInN1YiI6IjYwMzU5NzY5IiwianRpIjoiYmI4NjhhZGJkMDVkMWQ1MmY1Zjc1NmE3ZTUzYWM2ODVlODc3OGU1MyJ9.k6NNzlSy7BoEUCdokDXWSEjWMeEeU-SZqxpN7-ege9Jbry3Oa4M96yipizD8euYEPGDkvKD7tr1o9aCkI3tnNZ8nXITlnFCFD9TaYSBh61dEgZPT69zpAMpFgkZRlYnzGO0bFUm-yrawbXvIF3ElCK3hd_oll2CCQEIiTYxNkQwrVYrM3DgskAOMc5q2NaZ20pgM8KjSwGhdMMl0VVxutPZ2QIE-rT3Aj2dSwFEtrUGP8-o8y1rh9dnCso_tL5kQWmxu_mhGcSj5Q0tVEuafQIytU2D0YcPE9Q2iCy3wZVOK6qFY8uI8B2Tnhnxo--q5731vgemca4GvnZb9ZN5VXQ; nt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2NjYzMzkzMzIsImJyYW5kIjoib2x4IiwiY291bnRyeUNvZGUiOiJpZCIsInVzZXJJZCI6NjAzNTk3Njl9.fyiFk_wdMoB50m-kpG-VWo3l0DG4EEmUDznPPXW-T9Y; _gat_clientNinja=1; _abck=D2DB6D16FA06AEA0A1FCCCD72E0AE17A~0~YAAQVSg0Fy6fjPWDAQAA3IyQ+QiZg5iZEH0tyq7htkqxXlrUfxqTS9nvrvXO1omXJLt7sKLNu9PRvtrd/8Vt7qSBV1J0zw3sstTOBh3MUcEpFnaAob/0NNUqniQf2L4I6VcPImbn1It4WJ5fZA2QQXGOi94BSEhPXPUz2meMSvCaQU7TKUdHgln+tfhM7yUv0R3E4vTJyY4Yi/pTt61qyj+ajrxJAoZOmkDrMnzKBQpe+eE5R1pwY4urhJntQ9XHyh4DnHJklHksfnJ8YlyilplFH/mMNmF296ukFoQMgmncrdMsxyvea0B8bDCUOhdD+HzSWAGo+K4rWocVPjnpmag+shZwCz/M/vkB0jgTDTVE320KkIKQ7K+l2WJnPWiIoPrrz4wagRYE5HWvWa96FnBMsXsPBhM=~-1~-1~-1; ldTd=true; MgidSensorNVis=45; MgidSensorHref=https://www.olx.co.id/item/falukost-tomang-kos-exclusive-pria-wanita-kost-tomang-untar-trisakti-iid-806356711; _gat_UA-116132414-3=1; cto_bundle=puiFKF80U0hmV3V1eGxRQkE2dFlxRWdYWUd0d2hNZUMzamw1eU5vSFMzb1YxQURucjFyRFp0Z29lTHQ2Zmc4WUVVV1FvYUdrRjk2SjdWNXF4bHhzQ1FiWVRycGM1STA1R1hmMlN4bnBuZSUyQjQ3WWFuR0lzeW1CM1klMkZYQzdvMmlGWFczVUN0V2p6T0REUmM4NGpjaDd1SEwwaHVRJTNEJTNE; WZRK_S_W6K-746-995Z=%7B%22p%22%3A43%2C%22s%22%3A1666337086%2C%22t%22%3A1666339358%7D; onap=1835a5ec649x378f8b0b-3-183f943e121x25fe11a7-331-1666341161; bm_sv=EAD5B20681125C2D001B7EE1FE7A6537~YAAQVSg0F36rjPWDAQAA/9GQ+RFeGf7/5rABsvwsbezru4N+4wUy0gygdXoTsBsNFPosFgCu6vz1rsxIvyOmir/QYxNt+QicR7/fH4T9+vnEnwXs51cGvEaWgd9L1NOKKEUQtg7wO0uMnqPFUvi+XKqGvz3XglvQ3oUdyQ0DSL/RYdvgI+VN+s4QDJUDF1rXBUBnwv2TEkILqRtHnd0CVvrzT+CXNMSbI8KW5PiGvMMo1iUyla5F6dgHZ2OdHDA1aA==~1',
#         'if-none-match': 'W/"08a75ea0840ea539dfa7c070f2840aaf7"',
#         'referer': 'https://www.olx.co.id/item/falukost-tomang-kos-exclusive-pria-wanita-kost-tomang-untar-trisakti-iid-806356711',
#         'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
#         'sec-ch-ua-mobile': '?0',
#         'sec-ch-ua-platform': '"Windows"',
#         'sec-fetch-dest': 'empty',
#         'sec-fetch-mode': 'cors',
#         'sec-fetch-site': 'same-origin',
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
#         'x-newrelic-id': 'VQMGU1ZVDxABU1lbBgMDUlI=',
#         'x-panamera-fingerprint': '0460e7a312689a47c1b5137766b8e5e3#1651121435103',
#     }
#
#     response = requests.get('https://www.olx.co.id/api/users/108286559', cookies=cookies, headers=headers)
#
#     return response

# def getPhone(user_id = 0):
#     import requests
#     cookies = {'t':'eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCIsImtpZCI6ImViT21QTmlrIn0.eyJncmFudFR5cGUiOiJncGx1cyIsImNsaWVudFR5cGUiOiJ3ZWIiLCJ0b2tlblR5cGUiOiJhY2Nlc3NUb2tlbiIsImlzTmV3VXNlciI6ZmFsc2UsImlhdCI6MTY2NjMzOTMzMiwiZXhwIjoxNjY2MzQwMjMyLCJhdWQiOiJvbHhpZCIsImlzcyI6Im9seCIsInN1YiI6IjYwMzU5NzY5IiwianRpIjoiYmI4NjhhZGJkMDVkMWQ1MmY1Zjc1NmE3ZTUzYWM2ODVlODc3OGU1MyJ9.P9nTJWVJMIRDztsAbzKeo-t1zYGqtSa5gSVnUy0bOWsiyIcal5WBTqKNrT5tG1nkIT2atwU_BOQi34FqLF_di6vxXBQHnIvcnb5fNsu4xMsDXZJKb0v8eEEKlHaZvsVqJEykRwfREp9oMgv8wkh1UPtTF28iPa1wHEOgVt23E3FmtkJY_LtHzEK0OpFR7ddKIwwmPbm0qrM37QPheytQlQTayb-SolxVZUdXXd5tijatQciskowNNfZ5xccr2lLf3223X5rocG6Nx7YYC-zSsDnj4MwEtt7gWaiNhPJf4V0Yn7rGPakU83gM3Tctgi0w_46vs1f8azkgmzENBX2nng'}
#     headers = {
#         'Upgrade-Insecure-Requests': '1',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
#         'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
#         'sec-ch-ua-mobile': '?0',
#         'sec-ch-ua-platform': '"Windows"',
#     }
#
#     response = requests.get('https://www.olx.co.id/api/users/'+str(user_id), headers=headers, cookies = cookies)
#
#     return response

def getListingInformation(jsonLoads):
    try:
        id = jsonLoads["id"]
        has_phone_param = jsonLoads["has_phone_param"]
        description = jsonLoads["description"]
        title = jsonLoads["title"]
        price = str(jsonLoads["price"]["value"]["display"]).replace('Rp','').replace('.','').replace(' ','')
        location_region = jsonLoads["locations_resolved"]["ADMIN_LEVEL_1_name"]
        location_city = jsonLoads["locations_resolved"]["ADMIN_LEVEL_3_name"]
        location_district = jsonLoads["locations_resolved"]["SUBLOCALITY_LEVEL_1_name"]
        user_id = jsonLoads["user_id"]
        parameters = jsonLoads["parameters"]
        luas_bangunan = 0
        kamar_mandi = 0
        fasilitas = []
        alamat = ""
        for param in parameters:
            if param["key"] == "p_sqr_building":
                luas_bangunan = param["value"]
            if param["key"] == "p_bathroom":
                kamar_mandi = param["value"]
            if param["key"] == "p_facility":
                if "values" in param:
                    [fasilitas.append(f["value"]) for f in param["values"]]
            if param["key"] == "p_alamat":
                alamat = param["value"]
        fasilitas = ','.join(fasilitas)
        latitude = jsonLoads["locations"][0]["lat"]
        longitude = jsonLoads["locations"][0]["lon"]

        return ['https://www.olx.co.id/item/'+str(id), str(id), user_id, location_region, location_city, location_district, title, price, \
                alamat, latitude, longitude, kamar_mandi, fasilitas, luas_bangunan, description, has_phone_param]
    except Exception:
        print('Error','https://www.olx.co.id/item/'+str(id))
        return ['https://www.olx.co.id/item/'+str(id), str(id), '', '', '', '', '', 0, \
                '', 0, 0, 0, '', 0, '', False]

def to_excel(list,output):
    with xlsxwriter.Workbook(output) as workbook:
        worksheet = workbook.add_worksheet()
        for row_num, data in enumerate(list):
            worksheet.write_row(row_num, 0, data)

def scrapListing(continue_previous = False,continue_location = '',continue_page = 0):
    id_clean = []
    for location in id_location:
        page = -1
        if continue_previous == True:
            if location[1] == continue_location:
                continue_previous = False
                page = continue_page
                id_clean = readPrevListingId()
        while not continue_previous:
            page+=1
            while True:
                print(location[0],location[1],page, datetime.now())
                scrape = getPage(location[0],page).text
                try:
                    jsontext = json.loads(scrape)
                    break
                except Exception:
                    # print(scrape)
                    print("getPage error. Re-scrape")
                    continue
            if "data" not in jsontext:
                break
            if len(jsontext["data"]) == 0:
                break
            total_duplicate = 0
            for listing in jsontext["data"]:
                kost = getListingInformation(listing)
                id = int(kost[1])
                if id not in id_clean:
                    id_clean.append(id)
                    result.append(kost)
                    to_excel(result,output)
                else:
                    total_duplicate+=1
            if total_duplicate>1:
                print('total_duplicate',total_duplicate)

def readLocation():
    data = pd.read_excel(file_level)
    list_location = data[["id","name"]]
    return  list_location.values.tolist()

def readUserId():
    data = pd.read_excel(output)
    list_user_id = data["user_id"]
    list_user_id.drop_duplicates(inplace=True)
    return  list_user_id.values.tolist()

def readPrevListingId():
    data = pd.read_excel(output_previous)
    list_id = data["id"]
    list_id.drop_duplicates(inplace=True)
    return list_id.values.tolist()

url_location_0 = 'https://www.olx.co.id/indekos_c4833'
def getLocation(_url):
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    response = requests.get(_url, headers=headers)
    return response

# def getHref():
#     data = '<ul class="_21vyG" data-aut-id="ulLevel_3"><li><a class="_1HnJ6 _2OYDZ _2L7t8" rel="" data-aut-id="location_Padalarang" href="/padalarang_g5000765/indekos_c4833">Padalarang<span> (8)</span></a></li><li><a class="_1HnJ6 _2OYDZ _2L7t8" rel="" data-aut-id="location_Batujajar" href="/batujajar_g5000754/indekos_c4833">Batujajar<span> (4)</span></a></li><li><a class="_1HnJ6 _2OYDZ _2L7t8" rel="" data-aut-id="location_Ngamprah" href="/ngamprah_g5000764/indekos_c4833">Ngamprah<span> (4)</span></a></li><li><a class="_1HnJ6 _2OYDZ _2L7t8" rel="" data-aut-id="location_Lembang" href="/lembang_g5000763/indekos_c4833">Lembang<span> (3)</span></a></li><li><a class="_1HnJ6 _2OYDZ _2L7t8" rel="" data-aut-id="location_Parongpong" href="/parongpong_g5000766/indekos_c4833">Parongpong<span> (2)</span></a></li><div class=""><li><a class="_1HnJ6 _2OYDZ _2L7t8" rel="" data-aut-id="location_Cililin" href="/cililin_g5000757/indekos_c4833">Cililin<span> (1)</span></a></li><li><a class="_1HnJ6 _2OYDZ _2L7t8" rel="" data-aut-id="location_Cisarua" href="/cisarua_g5000761/indekos_c4833">Cisarua<span> (1)</span></a></li></div></ul>'
#     for location in re.findall(r'href="/(.*?)/indekos_c4833">',data):
#         id = location.split('_')[-1].replace('g','')
#         name = location.split('_')[0].replace('-',' ')
#         print('['+id+',"'+name+'"],')
# def check_exists_then_click(xpath):
#     try:
#         browser.find_element(By.XPATH,xpath)
#         browser.find_element(By.XPATH,xpath).click()
#     except NoSuchElementException:
#         return False
#     return True

def check_exists_then_print(xpath):
    try:
        txt = browser.find_element(By.XPATH,xpath).text
    except NoSuchElementException:
        return False
    return txt

def check_exists_attribute(xpath,attribute):
    try:
        txt = browser.find_element(By.XPATH,xpath).get_attribute(attribute)
    except NoSuchElementException:
        return False
    return txt

def check_exists_then_click(xpath):
    try:
        browser.find_element(By.XPATH,xpath)
        browser.find_element(By.XPATH,xpath).click()
    except NoSuchElementException:
        return False
    return True

def getLocation(url,level):
    i = 0
    while True:
        if i == 5:
            return False
        browser.get(url)
        time.sleep(3)
        profil = check_exists_attribute('//*[@data-aut-id="ulLevel_'+str(level)+'"]','outerHTML')
        if profil == False:
            i+=1
            continue
        list_location = []
        try:
            for location in re.findall('href="/(.*?)/',profil):
                name = location.split('_')[0].replace('-',' ')
                id = location.split('_')[-1].replace('g','')
                link = 'https://www.olx.co.id/'+location+'/indekos_c4833'
                list_location.append(["ulLevel_"+str(level),name, id, link])
            return list_location
        except TypeError:
            i+=1
            continue
            # print("Loading took too much time!")

def to_excel(list,output):
    with xlsxwriter.Workbook(output) as workbook:
        worksheet = workbook.add_worksheet()
        for row_num, data in enumerate(list):
            worksheet.write_row(row_num, 0, data)

def mainGetLocation(url = 'https://www.olx.co.id/indekos_c4833'):
    level_1 = getLocation(url,1)
    to_excel([['level','name','id','url']]+level_1,'level1.xlsx')
    level_2 = []
    level_3 = []
    for lv_1 in level_1:
        print(1,lv_1[1],lv_1[3])
        lv_2 = getLocation(lv_1[3],2)
        if lv_2 == False:
            lv_2 = [lv_1]
        level_2+=lv_2
        to_excel([['level','name','id','url']]+level_2,'level2.xlsx')
        for l_2 in lv_2:
            print(2,l_2[1],l_2[3])
            lv_3 = getLocation(l_2[3],3)
            if lv_3 == False:
                lv_3 = [l_2]
            level_3+=lv_3
            to_excel([['level','name','id','url']]+level_3,'level3.xlsx')

def loginOlx(url='https://www.olx.co.id'):
    try:
        browser.get(url)
        time.sleep(3)
        ## login
        browser.find_element(By.XPATH,'//*[@id="container"]/header/div/div/div[3]/button').click()
        time.sleep(3)
        browser.find_element(By.XPATH,'/html/body/div[2]/div/div/div/button[3]').click()
        time.sleep(3)
        WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="email_input_field"]'))).send_keys(user)
        time.sleep(3)
        browser.find_element(By.XPATH,'/html/body/div[2]/div/div/form/div/button').click()
        time.sleep(3)
        WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]'))).send_keys(password)
        time.sleep(3)
        browser.find_element(By.XPATH,'/html/body/div[2]/div/div/form/div/button').click()
        time.sleep(3)
        check_exists_then_click('//*[@id="wzrk-cancel"]')
        time.sleep(1)
    except TimeoutException:
        print("Loading took too much time!")

def getUserInfo(profil_id):
    browser.get('https://www.olx.co.id/api/users/'+profil_id)
    time.sleep(1)
    # print(browser.page_source)
    profil = check_exists_attribute('/html/body/pre','outerHTML')
    # print(html2text.html2text(profil))
    profil = json.loads(html2text.html2text(profil))
    # print(profil['data']['phone'])
    name = ''
    if 'name' in profil['data']:
        name = profil['data']['name']
    phone = ''
    if 'phone' in profil['data']:
        phone = profil['data']['phone']
    return [profil_id,name,phone]

def scrapUser():
    loginOlx()
    userId = readUserId()
    id_clean = []
    result = []
    for profil_id in userId:
        if profil_id not in id_clean:
            result.append(getUserInfo(profil_id))
            to_excel([['user_id','name','phone']]+result,output_user)

def main():
    global id_location
    mainGetLocation()
    # id_location = readLocation()
    ### new scrap
    # scrapListing()
    ### continue previous scrap
    # scrapListing(True, 'palmerah', 15)
    # scrapListing(True, 'benda', 13)
    # scrapUser()

if __name__ == '__main__':
    main()
    # mainGetLocation()
    # id_location = readLocation()
    # scrapListing()
    # scrapUser()
#calling main() function
main()