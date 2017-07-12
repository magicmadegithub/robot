import requests
from wxpy import *

robot_url = 'http://www.tuling123.com/openapi/api'
robot_key = '7c7a0eaee61447c5b664091387916365'

coin_url = 'https://yunbi.com/api/v2/tickers/'
coin_map = {'btc': 'btccny',
            'eth': 'ethcny',
            'etc': 'etccny',
            'sc': 'sccny',
            'bts': 'btscny',
            '1st': '1stcny',
            'qtum': 'qtumcny',
            'ans': 'anscny',
            'zmc': 'zmccny',
            'eos': 'eoscny'}

bot = Bot(cache_path=True, console_qr=True)
my_friend = bot.friends().search('小麻&amp;bits')[0]
my_group = ensure_one(bot.groups().search('python^_^java'))


# 查询云币币价
def query_coin_price(coin_name):
    url = coin_url + coin_name + ".json"
    r = requests.get(url)
    return "云币当前价格：" + r.json()['ticker']['buy']


# 图灵机器人
def get_robot_response(msg):
    data = {
        'key': robot_key,
        'info': msg,
        'userid': 'wechat-robot',
    }
    try:
        r = requests.post(robot_url, data=data).json()
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        if r.get('code') == 200000:
            text = r.get('text')
            url = r.get('url')
            print(text)
            print(url)
            return text + " " + url
        else:
            return r.get('text')
    except:
        return "我好像生病了"


# 打印来自其他好友、群聊和公众号的消息
@bot.register()
def print_others(msg):
    print(msg)


# 回复 my_friend 的消息 (优先匹配后注册的函数!)
@bot.register(my_friend)
def reply_my_friend(msg):
    return get_robot_response(msg.text)


# 回复指定群消息
@bot.register(my_group)
def forward_group_message(msg):
    if msg.is_at:
        text = msg.text.split()[1]
        return get_robot_response(text)
    elif msg.text.lower() in coin_map.keys():
        return query_coin_price(coin_map.get(msg.text.lower()))
    else:
        print(msg)


# 注册好友请求类消息
@bot.register(msg_types=FRIENDS)
# 自动接受验证信息中包含 'robot' 的好友请求
def auto_accept_friends(msg):
    # 判断好友请求中的验证文本
    if 'robot' in msg.text.lower():
        # 接受好友 (msg.card 为该请求的用户对象)
        new_friend = bot.accept_friend(msg.card)
        # 或 new_friend = msg.card.accept()
        # 向新的好友发送消息
        new_friend.send('你好，我是小图～')


if __name__ == '__main__':
    embed()
