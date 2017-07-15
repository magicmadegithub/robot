import requests

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


def query_all_coins():
    r = requests.get(coin_url)
    dict_coins = r.json()
    all_coins_price = '云币主流币价格:' + '\n'
    for k, value in dict_coins.items():
        name = k[:-3]
        price = value['ticker']['buy']
        if name in coin_map:
            all_coins_price = all_coins_price + name + ":" + price + '\n'
    print(all_coins_price)


def forward_group_message(msg):
    if msg == 'coins':
        return query_all_coins()
    else:
        print(msg)


if __name__ == '__main__':
    forward_group_message('coins')