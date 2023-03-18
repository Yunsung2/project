from django.shortcuts import render
import requests
# dict를 통해 딕셔너리 생성
def usd_to_krw(url):
    response = requests.get(url)
    response_json = response.json() # [ { } ] 
    usd_price = response_json[0]['basePrice']

    return usd_price

def get_upbit_ticker(url):
    response=requests.get(url)
    response_json=response.json()
    upbit_ticker_dict={}

    for coin in response_json:
        ticker=coin['market']
        name=coin['korean_name']

        if ticker.startswith("KRW"):
            upbit_ticker_dict.update({ticker : name})
    return upbit_ticker_dict

# 업비트 api를 이용한 실시간 시세 함수

def get_upbit_price(url):
    response=requests.get(url)
    response_json=response.json()

    upbit_price_list={}
    upbit_price_rate={}
    upbit_trade_volume={}

    for i in range(len(response_json)):
        trade_price=response_json[i]['trade_price'] #현재가
        prev_closing_price=response_json[i]['prev_closing_price'] #종가
        change_rate=((trade_price-prev_closing_price)/prev_closing_price*100) #변동률
        ticker=response_json[i]['market'] #마켓 전체 코인
        acc_trade_price_24h=response_json[i]['acc_trade_price_24h']#24시간 거래량

        upbit_price_list.update({ticker : format(trade_price,',')})
        upbit_price_rate.update({ticker: round(change_rate, 2)})
        upbit_trade_volume.update({ticker: format(round(acc_trade_price_24h/1000000),',')})

    return upbit_price_list, upbit_price_rate, upbit_trade_volume

def index(request):
    usd_price=usd_to_krw("https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWUSD")
    upbit_ticker_list=get_upbit_ticker("https://api.upbit.com/v1/market/all")
    upbit_ticker_str=",".join(upbit_ticker_list)

    upbit_price, upbit_change_rate, upbit_trade_volume=get_upbit_price(f"https://api.upbit.com/v1/ticker?markets={upbit_ticker_str}")
    # bithumb_price, bithumb_changed_rate, bithumb_trade_volume = get_bithumb_price("https://api.bithumb.com/public/ticker/ALL_KRW")
    # coinone_price, coinone_changed_rate, coinone_trade_volume = get_coinone_price("https://api.coinone.co.kr/ticker?currency=all")
    # korbit_price, korbit_changed_rate, korbit_trade_volume = get_korbit_price("https://api.korbit.co.kr/v1/ticker/detailed/all")
    context={'usd_price' : usd_price, 'upbit_ticker_list': upbit_ticker_list, 'upbit_price': upbit_price, 'upbit_change_rate': upbit_change_rate, 'upbit_trade_volume': upbit_trade_volume}
    print(context)
    return render(request, 'index.html', context)


def realtime(request):
    context={'abc': 'hello'}
    return render(request, "realtime.html", context)