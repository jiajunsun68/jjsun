from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']
start_date2 = os.environ['START_DATE2']
city2 = os.environ['CITY2']
birthday2 = os.environ['BIRTHDAY2']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]
user_id2 = os.environ["USER_ID2"]
template_id2 = os.environ["TEMPLATE_ID2"]

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['city'],weather['date'],weather['weather'], math.floor(weather['temp'])

def get_weather2():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city2
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['city'],weather['date'],weather['weather'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("http://open.iciba.com/dsapi/")
  if words.status_code != 200:
    return get_words()
  return words.json()['content']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
city,dat,wea, temperature = get_weather()
focus = "热爱学习，热爱当下！"
data = {"focus":{"value":focus,"color":get_random_color()},"date":{"value":dat},"city":{"value":city},"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday(),"color":get_random_color()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
city2,dat,wea, temperature = get_weather2()
data2 = {"focus":{"value":focus,"color":get_random_color()},"date":{"value":dat},"city":{"value":city2},"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday(),"color":get_random_color()},"words":{"value":get_words(), "color":get_random_color()}}
res2 = wm.send_template(user_id2, template_id2, data2)
print(res2)
