
import requests
import time
import time, base64, hmac, hashlib, requests, json
import telegram

# talib 불러오기
import talib
import numpy as np

apikey = ''                 #API KEY
secret = ''

my_token = ''               #TeleToken
chat_id = ''                #TeleChat

bot = telegram.Bot(token = my_token)
# is_buy = True
message = '트레이딩 봇 시작!'
tradingPair = "BTC-KRW"
tradingPair2 = "ETH-KRW"
buy_account = 0.005
sell_account = buy_account*0.998
buy_account2 = 1
sell_account2 = buy_account2 * 0.998
# bot.sendMessage(chat_id=chat_id, text=message)
rsi_status = ''
rsi_status2 = ''
buy_price1 = 0      #taradingPair 산가격
buy_price2 = 0      #taradingPair2 산가격
sell_price1 = 0     #taradingPair 판가격
sell_price2 = 0     #taradingPair2 판가격
total_price = 0
total_price2 = 0
priceCount = 0
priceCount2 = 0
tradecount = 0      #사고판횟수
tradecount2 = 0      #사고판횟수2
fee1 = 0
fee2 = 0


def buy(amount, price, pair, msg):
    nonce = str(time.time())
    method = 'POST'
    request_path = '/orders'
    request_body = {
        "amount": amount,
        "price": price,
        "side": "buy",
        "tradingPairName": pair,
        "type": "limit"
    };
    # 필수 정보를 연결하여 prehash 문자열을 생성함
    what = nonce + method + request_path + json.dumps(request_body, sort_keys=True)
    # base64로 secret을 디코딩함
    key = base64.b64decode(secret)
    # hmac으로 필수 메시지에 서명하고
    signature = hmac.new(key, str(what).encode('utf-8'), hashlib.sha512)
    # 그 결과물을 base64로 인코딩함
    signature_b64 = base64.b64encode(signature.digest())

    custom_headers = {
        'API-Key': apikey,
        'Signature': signature_b64,
        'Nonce': nonce
    }

    req = requests.post(url='https://api.gopax.co.kr' + request_path, headers=custom_headers, json=request_body)

    message = '종목매수 : ' + pair + ' \n 가격 : {} \n 수량 : {} \n 이유 : {}'.format(price, amount, msg)

    bot.sendMessage(chat_id=chat_id, text=message)

    print('매수')


def sell(amount, price, pair, msg):
    nonce = str(time.time())
    method = 'POST'
    request_path = '/orders'
    request_body = {
        "amount": amount,
        "price": price,
        "side": "sell",
        "tradingPairName": pair,
        "type": "limit"
    };

    # 필수 정보를 연결하여 prehash 문자열을 생성함
    what = nonce + method + request_path + json.dumps(request_body, sort_keys=True)
    # base64로 secret을 디코딩함
    key = base64.b64decode(secret)
    # hmac으로 필수 메시지에 서명하고
    signature = hmac.new(key, str(what).encode('utf-8'), hashlib.sha512)
    # 그 결과물을 base64로 인코딩함
    signature_b64 = base64.b64encode(signature.digest())

    custom_headers = {
        'API-Key': apikey,
        'Signature': signature_b64,
        'Nonce': nonce
    }

    req = requests.post(url='https://api.gopax.co.kr' + request_path, headers=custom_headers, json=request_body)

    message = '종목매도 : ' + pair + ' \n 가격 : {} \n 수량 : {} \n 이유 : {}'.format(price, amount, msg)

    bot.sendMessage(chat_id=chat_id, text=message)

    print('매도')


is_buy = False
is_buy2 = False
while True:
    print("is_buy : " + str(is_buy))
    print("is_buy2 : " + str(is_buy2))
    now = time.localtime()
    now_time = round(time.time() * 1000)
    # 1000 이 1초
    # 60*1000 이 1분
    # 60*60*1000 이 1시간
    start = int(now_time)-60*60*1000*1000
    end = int(now_time)
    # print(start)
    # print(end)
    r = requests.get('https://api.gopax.co.kr/trading-pairs/' + tradingPair + '/candles?start='+str(start)+'&end='+str(end)+'&interval=5')
    r2 = requests.get('https://api.gopax.co.kr/trading-pairs/' + tradingPair2 + '/candles?start='+str(start)+'&end='+str(end)+'&interval=5')
    now_price1 = requests.get('https://api.gopax.co.kr/trading-pairs/' + tradingPair + '/ticker')
    now_price2 = requests.get('https://api.gopax.co.kr/trading-pairs/' + tradingPair2 + '/ticker')
    arpri1 = now_price1.json()
    arpri2 = now_price2.json()
    print("산가격1 : " + str(buy_price1))
    print("현재가1 : " + str(arpri1["price"]))
    print("산가격2 : " + str(buy_price2))
    print("현재가2 : " + str(arpri2["price"]))
    print("현재시간 : %04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))

    arr = r.json()
    arr2 = r2.json()
    # print(r2.json())
    close_price_list = []
    close_price_list2 = []
    for ar in arr:
        close_price_list.append(float(ar[4]))
    for ar2 in arr2:
        close_price_list2.append(float(ar2[4]))
        # print(ar2[4])
    close_price_list_nparr = np.array(close_price_list, dtype='f8')
    close_price_list2_nparr = np.array(close_price_list2, dtype='f8')
    output = talib.SMA(close_price_list_nparr)
    output2 = talib.SMA(close_price_list2_nparr)

    # rsi 계산
    rsi = talib.RSI(close_price_list_nparr, timeperiod = 14)
    rsi2 = talib.RSI(close_price_list2_nparr, timeperiod = 14)
    print("RSI : " + str(rsi[-1]))
    # print(rsi[-1])
    print("RSI2 : " + str(rsi2[-1]))
    # print(rsi[-1])
    # print(rsi[-2])
    # print(rsi[-3])
    print("rsi_status : " + rsi_status)
    print("rsi_status2 : " + rsi_status2)

    avg_min_15 = sum(close_price_list[-15:]) / 15
    avg_min_50 = sum(close_price_list[-50:]) / 50
    avg_min_15_2 = sum(close_price_list2[-15:]) / 15
    avg_min_50_2 = sum(close_price_list2[-50:]) / 50
    percent1 = (buy_price1 - arpri1["price"]) / arpri1["price"] * 100
    percent2 = (buy_price2 - arpri2["price"]) / arpri2["price"] * 100

    print(percent1)
    print(percent2)

    # if rsi[-1] < 30:
    #     rsi_status = 'low'
    # elif 30 <= rsi[-1] < 70:
    #     if rsi_status == 'low' and is_buy is False:
    #         # buy(0.001, close_price_list[-1])
    #         print('rsi 상향 돌파 매수!')
    #     if rsi_status == 'high' and is_buy is True:
    #         if avg_min_15 > avg_min_50 * 1.004:
    #             message = '종목매도 : ' + tradingPair + ' \n 매도 매수점 같아서 안하게함'
    #             bot.sendMessage(chat_id=chat_id, text=message)
    #         else:
    #             is_buy = False
    #             # sell(sell_account, close_price_list[-1], tradingPair, "RSI1 sell")
    #             sell_price1 = close_price_list[-1]
    #             total_price += sell_price1
    #             buy_price1 = 0
    #             tradecount += 1
    #             print('rsi 하향 돌파 매도!')
    #     rsi_status = 'middle'
    # else:
    #     rsi_status = 'high'
    #
    # if rsi2[-1] < 30:
    #     rsi_status2 = 'low'
    # elif 30 <= rsi2[-1] < 70:
    #     if rsi_status2 == 'low' and is_buy2 is False:
    #         # buy(0.001, close_price_list[-1])
    #         print('rsi2 상향 돌파 매수!')
    #     if rsi_status2 == 'high' and is_buy2 is True:
    #         if avg_min_15_2 > avg_min_50_2 * 1.004:
    #             message = '종목매도 : ' + tradingPair2 + ' \n 매도 매수점 같아서 안하게함'
    #             bot.sendMessage(chat_id=chat_id, text=message)
    #         else:
    #             is_buy2 = False
    #             # sell(sell_account2, close_price_list2[-1], tradingPair2, "RSI2 sell")
    #             sell_price2 = close_price_list2[-1]
    #             total_price2 += sell_price2
    #             buy_price2 = 0
    #             tradecount2 += 1
    #             print('rsi2 하향 돌파 매도!')
    #     rsi_status2 = 'middle'
    # else:
    #     rsi_status2 = 'high'

    # if rsi[-1] < 30:
    #     rsi_status = 'low'
    # elif 30 <= rsi[-1] < 70:
    #     if rsi_status == 'low' and is_buy is False:
    #         # buy(0.001, close_price_list[-1])
    #         print('rsi 상향 돌파 매수!')
    #     if rsi_status == 'high' and is_buy is True:
    #         is_buy = False
    #         # sell(sell_account, close_price_list[-1], tradingPair, "RSI1 sell")
    #         sell_price1 = close_price_list[-1]
    #         fee1 += sell_price1 * 0.002
    #         total_price += sell_price1
    #         buy_price1 = 0
    #         tradecount += 1
    #         print('rsi 하향 돌파 매도!')
    #     rsi_status = 'middle'
    # else:
    #     rsi_status = 'high'
    #
    # if rsi2[-1] < 30:
    #     rsi_status2 = 'low'
    # elif 30 <= rsi2[-1] < 70:
    #     if rsi_status2 == 'low' and is_buy2 is False:
    #         # buy(0.001, close_price_list[-1])
    #         print('rsi2 상향 돌파 매수!')
    #     if rsi_status2 == 'high' and is_buy2 is True:
    #         is_buy2 = False
    #         # sell(sell_account2, close_price_list2[-1], tradingPair2, "RSI2 sell")
    #         sell_price2 = close_price_list2[-1]
    #         fee2 += sell_price2 * 0.002
    #         total_price2 += sell_price2
    #         buy_price2 = 0
    #         tradecount2 += 1
    #         print('rsi2 하향 돌파 매도!')
    #     rsi_status2 = 'middle'
    # else:
    #     rsi_status2 = 'high'

    if avg_min_15 > avg_min_50 and is_buy is False:
        print("매수 전 is_buy 확인 : " + str(is_buy))
        is_buy = True
        # buy(buy_account, close_price_list[-1], tradingPair, "buy1")
        priceCount = 1
        buy_price1 = close_price_list[-1]
        fee1 += buy_price1 * 0.002
        total_price -= buy_price1
        tradecount += 1
        print("매수 후 is_buy 확인 : " + str(is_buy))
    # print(output)

    if avg_min_15_2 > avg_min_50_2 and is_buy2 is False:
        print("매수2 전 is_buy 확인 : " + str(is_buy2))
        is_buy2 = True
        # buy(buy_account2, close_price_list2[-1], tradingPair2, "buy2")
        priceCount2 = 1
        buy_price2 = close_price_list2[-1]
        fee2 += buy_price2 * 0.002
        total_price2 -= buy_price2
        tradecount2 += 1
        print("매수2 후 is_buy 확인 : " + str(is_buy2))

    if avg_min_50 > avg_min_15 and is_buy is True:
        print("매도 전 is_buy 확인 : " + str(is_buy))
        is_buy = False
        # sell(sell_account, close_price_list[-1], tradingPair, "Ave_sell1")
        buy_price1 = 0
        sell_price1 = close_price_list[-1]
        fee1 += sell_price1 * 0.002
        total_price += sell_price1
        tradecount += 1
        print("매도 후 is_buy 확인 : " + str(is_buy))

    if avg_min_50_2 > avg_min_15_2 and is_buy2 is True:
        print("매도2 전 is_buy 확인 : " + str(is_buy2))
        is_buy2 = False
        # sell(sell_account2, close_price_list2[-1], tradingPair2, "Ave_sell2")
        buy_price2 = 0
        sell_price2 = close_price_list2[-1]
        fee2 += sell_price2 * 0.002
        total_price2 += sell_price2
        tradecount2 += 1
        print("매도2 후 is_buy 확인 : " + str(is_buy2))

    # if percent1 > 5 and is_buy is True:
    #     print("percent 매도 전 is_buy 확인 : " + str(is_buy))
    #     is_buy = False
    #     # sell(sell_account, close_price_list[-1], tradingPair, "per_sell1")
    #     buy_price1 = 0
    #     sell_price1 = close_price_list[-1]
    #     fee1 += sell_price1 * 0.002
    #     total_price += sell_price1
    #     tradecount += 1
    #     print("percent 매도 후 is_buy 확인 : " + str(is_buy))
    #
    # if percent2 > 5 and is_buy2 is True:
    #     print("percent 매도 전 is_buy 확인 : " + str(is_buy2))
    #     is_buy2 = False
    #     # sell(sell_account2, close_price_list2[-1], tradingPair2, "per_sell2")
    #     buy_price2 = 0
    #     sell_price2 = close_price_list2[-1]
    #     fee2 += sell_price2 * 0.002
    #     total_price2 += sell_price2
    #     tradecount2 += 1
    #     print("percent 매도 후 is_buy 확인 : " + str(is_buy2))

    # print(close_price_lsit)
    # [
    #   [
    #     <Time>,
    #     <Low>,
    #     <High>,
    #     <Open>,
    #     <Close>,
    #     <Volume>
    #   ],
    #   [
    #     1521004080000,
    #     10081000,
    #     10081000,
    #     10081000,
    #     10081000,
    #     0.01
    #   ]
    # ]


    #
    print("avg_min_15 : " + str(avg_min_15))
    print("avg_min_50 : " + str(avg_min_50))
    print("avg_min_15_2 : " + str(avg_min_15_2))
    print("avg_min_50_2 : " + str(avg_min_50_2))

    print("total Price : " + str(total_price) + " // 수수료 : " + str(fee1))
    print("tradeCount : " + str(tradecount))
    print("total Price2 : " + str(total_price2) + " // 수수료 : " + str(fee2))
    print("tradeCount2 : " + str(tradecount2))

    # if is_buy is True and priceCount == 1:
    #     priceCount = 0
    #     total_price += buy_price1
    #     print("total Price : " + str(total_price) + " // 수수료 : " + str(fee1))
    #     print("tradeCount : " + str(tradecount))
    # else:
    #     print("total Price : " + str(total_price) + " // 수수료 : " + str(fee1))
    #     print("tradeCount : " + str(tradecount))
    #
    # if is_buy2 is True and priceCount2 == 1:
    #     priceCount2 = 0
    #     total_price2 += buy_price2
    #     print("total Price2 : " + str(total_price2) + " // 수수료 : " + str(fee2))
    #     print("tradeCount2 : " + str(tradecount2))
    # else:
    #     print("total Price2 : " + str(total_price2) + " // 수수료 : " + str(fee2))
    #     print("tradeCount2 : " + str(tradecount2))

        # if avg_min_15 > avg_min_50 * 1.004 and is_buy == False:
    #     buy(0.001,close_price_list[-1])
    #
    # if avg_min_50 > avg_min_15 and is_buy == True:
    #     sell(0.001,close_price_list[-1])

    time.sleep(8)




