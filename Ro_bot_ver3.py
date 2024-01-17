import pandas as pd
from binance.client import Client
import talib
import numpy as np
from talib import MA_Type
from talib import ADX, RSI, MACD, STOCH
import datetime
from datetime import datetime
import matplotlib.pyplot as plt
import time
import math
import telebot
from telebot import types
bot = telebot.TeleBot('6312689394:AAE0wejoCqGdUDprRpXjIc401zCmN21SVl4')
id = 1660691311

def startTelebot():
    bot.send_message(id, "We start a work, let's see what statistic will be", parse_mode='Markdown')
    

def sendStatistic(statistic, cycle):
    bot.send_message(id, f' Statistic is {str(statistic)}, num of tickets is {str(len(tickets))}, cycle num {cycle}', parse_mode='Markdown')
def sendLose(symbol):
    bot.send_message(id, f'We need to sell this coin {symbol}')
# def sendSignalToBuy(coin):
#     bot.send_message(id, f'We should buy {coin}')
def sendBought(symbol):
    bot.send_message(id, f'We bought {symbol}')
def sendSold(symbol):
    bot.send_message(id, f"We sold {symbol}")
def sendMessage():
    if len(balances) > 1:
        bot.send_message(id, f'balance now - {str(balances[-1])}')
def sendCantBuy(symbol):
    bot.send_message(id, f"We can't buy coin {symbol}")
def sendWhiteList(whiteList):
    bot.send_message(id, f"White list is {whiteList}")
def sendSellError(coin):
    bot.send_message(id, f"Error in sell in {coin}")
def sendSell(coin):
    bot.send_message(id, f'We in a sell stage {coin}')
def sendTicket(ticket):
    bot.send_message(id, f'Coin is {ticket.symbol} price{ticket.price} takeprofit is {ticket.takeprofit[0]} stoploss is {ticket.stoploss[0]}')

api_secret = 'l8yABl6afXbNUhKZRowpnnenT8Aef0P4VwdtLg3tJjPDF5ucuKXEQGunZdZhAodd'
api_key = 'y9VrYUhVwnnHrymwAvlPS3MbqpsNJBK1pLRYy71qudlJadJTruNnk5APTOnVp0zu'
orders = []

client = Client(api_key, api_secret)

tickers = client.get_all_tickers()
tickers = pd.DataFrame(tickers)

info = client.futures_exchange_info()

partOfBalance = 12

balances, tickets = [], []
balance = float(client.get_asset_balance(asset='USDT')['free'])
counterProfit = 1
counterLoss = 1

def takeprofitMove(ord, percent):
    ord.takeprofit = ord.takeprofit + percent * 0.7
def stoplossMove(ord, percent):
    ord.stoploss = ord.stoploss + percent * 0.5

class passcoin:
    def __init__(self, coin, dataframe):
        self.coin = coin
        self.dataframe = dataframe

class ticket:
    def __init__(self, symbol, price, qty, precision):
        now = datetime.now()
        self.symbol = symbol,
        self.price = price,
        self.takeprofit = price + price / 100,
        self.stoploss = price - price / 100,
        self.qty = qty,
        self.time = now,
        self.sold = False,
        self.precision = precision,

def get_history_data(coin):
    global result
    client = Client(api_key, api_secret)
    klines = client.get_historical_klines(coin, Client.KLINE_INTERVAL_1MINUTE, "5 hours ago UTC")
    result = pd.DataFrame(klines)
    result = result.rename(columns={0 : 'time', 1 : 'Open', 2 : 'High', 3 : 'Low', 4 : 'Close', 5 : 'Volume', 6 : 'Close time', 7 : 'Quote', 8 : 'Number of trades', 9 : 'Taker buy', 10 : 'Taker buy quote', 11 : 'Ignore'})
    # result['time'] = pd.to_datetime(result['time'], unit='ms')
    result['SMA_50'] = talib.SMA(result['Close'])
    result['SMA_100'] = talib.SMA(result['Close'], 100)
    result['SMA_hist'] = result['SMA_50'] - result['SMA_100']
    result['RSI'] = RSI(result['Close'], timeperiod=14)
    result['MACD'], result['Macdsignal'], result['Macdhist'] = MACD(result['Close'], 12, 26, 9)
    result['MACDDay'], result['MacdsignalDay'], result['MacdhistDay'] = MACD(result['Close'], 360, 720, 81)
    result['STOCH'], result['STOCH_k'] = STOCH(result['Close'], result['High'], result['Low'])
    result['ADX'] = ADX(result['High'], result['Low'], result['Close'], timeperiod = 12)
    make_obj_coin(coin, result)
    return result

def get_data(coin):
    global result
    client = Client(api_key, api_secret)
    klines = client.get_historical_klines(coin, Client.KLINE_INTERVAL_1MINUTE, "1 minute ago UTC")
    result = pd.DataFrame(klines)
    result = result.rename(columns={0 : 'time', 1 : 'Open', 2 : 'High', 3 : 'Low', 4 : 'Close', 5 : 'Volume', 6 : 'Close time', 7 : 'Quote', 8 : 'Number of trades', 9 : 'Taker buy', 10 : 'Taker buy quote', 11 : 'Ignore'})
    # cresult['time'] = pd.to_datetime(result['time'], unit='ms')
    result['SMA_50'] = talib.SMA(result['Close'])
    result['SMA_100'] = talib.SMA(result['Close'], 100)
    result['SMA_hist'] = result['SMA_50'] - result['SMA_100']
    result['RSI'] = RSI(result['Close'], timeperiod=14)
    result['MACD'], result['Macdsignal'], result['Macdhist'] = MACD(result['Close'], 12, 26, 9)
    result['MACDDay'], result['MacdsignalDay'], result['MacdhistDay'] = MACD(result['Close'], 360, 720, 81)
    result['STOCH'], result['STOCH_k'] = STOCH(result['Close'], result['High'], result['Low'])
    result['ADX'] = ADX(result['High'], result['Low'], result['Close'], timeperiod = 12)
    append_last_minute(passcoin, result)
    return result

def update_dataframe(dataframe):
    dataframe['SMA_50'] = talib.SMA(dataframe['Close'])
    dataframe['SMA_100'] = talib.SMA(dataframe['Close'], 100)
    dataframe['SMA_hist'] = dataframe['SMA_50'] - dataframe['SMA_100']
    dataframe['RSI'] = RSI(dataframe['Close'], timeperiod=14)
    dataframe['MACD'], dataframe['Macdsignal'], dataframe['Macdhist'] = MACD(dataframe['Close'], 12, 26, 9)
    dataframe['MACDDay'], dataframe['MacdsignalDay'], dataframe['MacdhistDay'] = MACD(dataframe['Close'], 360, 720, 81)
    dataframe['STOCH'], dataframe['STOCH_k'] = STOCH(dataframe['Close'], dataframe['High'], dataframe['Low'])
    dataframe['ADX'] = ADX(dataframe['High'], dataframe['Low'], dataframe['Close'], timeperiod = 12)
    
def make_obj_coin(coin, dataframe):
    x = passcoin(coin, dataframe)
    passescoins.append(x)

def append_last_minute(obj, dataframe):
    obj.dataframe = pd.concat([obj.dataframe, dataframe], ignore_index=True)

def get_precision(symbol):
   for x in info['symbols']:
       if x['symbol'] == symbol:
         precision = x['quantityPrecision']
         if precision == 0 or precision == None:
             precision = 1
         else:
            precision = int(precision)
         return precision
        
def checkPrecision(price, precision):
    if precision == 0 or precision == None:
        precision = 1
    else:
        precision = int(precision)
    x = round(price, precision)
    return x

def buy(symbol, price):
    try:
        balance = float(client.get_asset_balance(asset='USDT')['free'])
        if float(balance) > partOfBalance:
            precision = get_precision(symbol)
            x = checkPrecision(price, precision)
            if x > 0:
                qty = partOfBalance / x
                qty = round(qty, precision)
                order = client.create_order(
                    symbol=symbol,
                    side=Client.SIDE_BUY,
                    type=Client.ORDER_TYPE_MARKET,
                    quantity=qty
                )
                print(f'Bought {symbol}')
                sendBought(symbol)
                
                x = ticket(symbol, price, qty, precision)
                sendTicket(x)
                tickets.append(x)
    except Exception as E:
        print(E)    
        sendCantBuy(symbol)
        print(symbol)

def sell(ticket):
    try:
        balance_coin = float(client.get_asset_balance(asset=f"{ticket.symbol.replace('USDT', '')}")['free'])
        balance_usdt = balance_coin * ticket.price
        if balance_usdt > 10:
            order = client.order_market_sell(
                symbol=ticket.symbol,
                quantity=ticket.qty
                )
            print('Sold ', ticket.symbol)
            sendSold(ticket.symbol)
            ticket.sold = True 
            balance = float(client.get_asset_balance(asset='USDT')['free'])
            balances.append(balance)
        else:
            sendLose(ticket.symbol)
            ticket.sold = True
    except Exception as E:
        sendSellError(ticket.symbol)
        balance_coin = float(client.get_asset_balance(asset=f"{ticket.symbol.replace('USDT', '')}")['free'])
        balance_usdt = balance_coin * ticket.price
        if balance_usdt > 10:
            # quantity = math.floor(balance_coin * (10 ** ticket.precision) * 0.999) / (10 ** ticket.precision)
            quantity = round(ticket.qty, ticket.precision)
            errorSell(ticket, quantity)
            balance = float(client.get_asset_balance(asset='USDT')['free'])
            balances.append(balance)

def errorSell(ticket, quantity):
    try:
        order = client.order_market_sell(
            symbol=ticket.symbol,
            quantity=quantity
            )
        print('Sold before error', ticket.symbol)
        ticket.sold = True
        balance = float(client.get_asset_balance(asset='USDT')['free'])
        balances.append(balance)
    except Exception as E:
        print(ticket.symbol)
        print("Okey it doesn't work")
        counter = 0
        while True:
            try:
                quantity = math.floor(quantity * (10 ** ticket.precision) * 0.99) / (10 ** ticket.precision)
                quantity = round(ticket.qty, ticket.precision)
                order = client.order_market_sell(
                    symbol=ticket.symbol,
                    quantity=quantity
                )
                print('sold before error error')
                break
            except:
                counter += 1
                if counter == 5:
                    print('We lose all')
                    sendLose(ticket.symbol)
                    ticket.sold = True
                    break

def Strategy(passcoin):
    global balances
    coin = passcoin.coin
    price = float(passcoin.dataframe['Close'].iloc[[-1]].iloc[0])
    percent = price / 100
    rsi = float(passcoin.dataframe['RSI'].iloc[[-1]].iloc[0])
    macdhist = float(passcoin.dataframe['Macdhist'].iloc[[-1]].iloc[0])
    adx = float(passcoin.dataframe['ADX'].iloc[[-1]].iloc[0])
    smaK = float(passcoin.dataframe['SMA_50'].iloc[[-1]].iloc[0])
    sma = float(passcoin.dataframe['SMA_100'].iloc[[-1]].iloc[0])
    percentMacd = float(passcoin.dataframe['Macdhist'].max()) / 100 * 10
    adxmo = float(passcoin.dataframe['ADX'].iloc[[-2]].iloc[0])
    # oldmacd = float(result['Macdhist'].iloc[[-5]].iloc[0])
    if smaK - price >= 0 and macdhist >= -percentMacd and macdhist <= percentMacd and rsi >= 10 and rsi <= 35 and adx > adxmo:
        buy(passcoin.coin, price)
        balance = float(client.get_asset_balance(asset='USDT')['free'])
        balances.append(balance)
    for ticket in tickets:
        if ticket.symbol == coin and sma - smaK >= 0 and ticket.takeprofit < price and ticket.sold == False:
            takeprofitMove(ticket, percent)
            stoplossMove(ticket, percent)
    for ticket in tickets:
        if ticket.symbol == coin and ticket.takeprofit[0] < price and ticket.sold == False:
            ticket.profit = True
            sell(ticket)
            balance = float(client.get_asset_balance(asset='USDT')['free'])
            balances.append(balance)
        elif ticket.symbol == coin and ticket.stoploss[0] > price and ticket.sold == False:
            ticket.profit = False
            sell(ticket)
            balance = float(client.get_asset_balance(asset='USDT')['free'])
            balances.append(balance)

def makeStatistic(i):
    global counterProfit
    for ticket in tickets:
        if hasattr(ord, 'profit'):
            if ticket.profit == True:
                counterProfit += 1
            
    Statistic = len(tickets) / counterProfit
    sendStatistic(Statistic, i)

def makeWhiteList(coins):
    global whiteList
    whiteList = []
    for coin in coins:
        try:
            result = get_history_data(coin)
            openPrice = float(result['Close'].iloc[[0]].iloc[0])
            closePrice = float(result['Close'].iloc[[-1]].iloc[0])
            if closePrice > openPrice:
                whiteList.append(coin)
        except Exception as E:
            continue
    


passescoins = []
coins = ['BTCUSDT', 'LTCUSDT', 'ETHUSDT', 'NEOUSDT', 'BNBUSDT', 'QTUMUSDT', 'EOSUSDT', 'SNTUSDT', 'BNTUSDT', 'GASUSDT', 'OAXUSDT', 'ZRXUSDT', 'OMGUSDT', 'LRCUSDT', 'TRXUSDT', 'FUNUSDT', 'KNCUSDT', 'XVGUSDT', 'IOTAUSDT', 'LINKUSDT', 'CVCUSDT', 'MTLUSDT', 'NULSUSDT', 'STXUSDT', 'ADXUSDT', 'ETCUSDT', 'ZECUSDT', 'ASTUSDT', 'BATUSDT', 'DASHUSDT', 'POWRUSDT', 'REQUSDT', 'XMRUSDT', 'VIBUSDT', 'ENJUSDT', 'ARKUSDT', 'XRPUSDT', 'STORJUSDT', 'KMDUSDT', 'DATAUSDT', 'MANAUSDT', 'AMBUSDT', 'LSKUSDT', 'ADAUSDT', 'XLMUSDT', 'WAVESUSDT', 'ICXUSDT', 'ELFUSDT', 'RLCUSDT', 'PIVXUSDT', 'IOSTUSDT', 'STEEMUSDT', 'BLZUSDT', 'SYSUSDT', 'ONTUSDT', 'ZILUSDT', 'XEMUSDT', 'WANUSDT', 'LOOMUSDT', 'TUSDUSDT', 'ZENUSDT', 'THETAUSDT', 'IOTXUSDT', 'QKCUSDT', 'SCUSDT', 'KEYUSDT', 'DENTUSDT', 'IQUSDT', 'ARDRUSDT', 'HOTUSDT', 'VETUSDT', 'DOCKUSDT', 'VTHOUSDT', 'ONGUSDT', 'RVNUSDT', 'DCRUSDT', 'USDCUSDT', 'RENUSDT', 'FETUSDT', 'TFUELUSDT', 'CELRUSDT', 'MATICUSDT', 'ATOMUSDT', 'PHBUSDT', 'ONEUSDT', 'FTMUSDT', 'CHZUSDT', 'COSUSDT', 'ALGOUSDT', 'DOGEUSDT', 'DUSKUSDT', 'ANKRUSDT', 'WINUSDT', 'BANDUSDT', 'HBARUSDT', 'XTZUSDT', 'DGBUSDT', 'NKNUSDT', 'EURUSDT', 'KAVAUSDT', 'ARPAUSDT', 'CTXCUSDT', 'AERGOUSDT', 'BCHUSDT', 'TROYUSDT', 'VITEUSDT', 'FTTUSDT', 'OGNUSDT', 'DREPUSDT', 'WRXUSDT', 'LTOUSDT', 'MBLUSDT', 'COTIUSDT', 'HIVEUSDT', 'STPTUSDT', 'SOLUSDT', 'CTSIUSDT', 'CHRUSDT', 'BTCUPUSDT', 'BTCDOWNUSDT', 'JSTUSDT', 'FIOUSDT', 'STMXUSDT', 'MDTUSDT', 'PNTUSDT', 'COMPUSDT', 'IRISUSDT', 'MKRUSDT', 'SXPUSDT', 'SNXUSDT', 'ETHUPUSDT', 'ETHDOWNUSDT', 'DOTUSDT', 'BNBUPUSDT', 'BNBDOWNUSDT', 'AVAUSDT', 'BALUSDT', 'YFIUSDT', 'ANTUSDT', 'CRVUSDT', 'SANDUSDT', 'OCEANUSDT', 'NMRUSDT', 'LUNAUSDT', 'IDEXUSDT', 'RSRUSDT', 'PAXGUSDT', 'WNXMUSDT', 'TRBUSDT', 'WBTCUSDT', 'KSMUSDT', 'SUSHIUSDT', 'DIAUSDT', 'BELUSDT', 'UMAUSDT', 'WINGUSDT', 'CREAMUSDT', 'UNIUSDT', 'OXTUSDT', 'SUNUSDT', 'AVAXUSDT', 'BURGERUSDT', 'BAKEUSDT', 'FLMUSDT', 'SCRTUSDT', 'XVSUSDT', 'CAKEUSDT', 'ALPHAUSDT', 'ORNUSDT', 'UTKUSDT', 'NEARUSDT', 'VIDTUSDT', 'AAVEUSDT', 'FILUSDT', 'INJUSDT', 'CTKUSDT', 'AUDIOUSDT', 'AXSUSDT', 'AKROUSDT', 'HARDUSDT', 'KP3RUSDT', 'SLPUSDT', 'STRAXUSDT', 'UNFIUSDT', 'CVPUSDT', 'FORUSDT', 'FRONTUSDT', 'ROSEUSDT', 'PROMUSDT', 'SKLUSDT', 'GLMUSDT', 'GHSTUSDT', 'DFUSDT', 'JUVUSDT', 'PSGUSDT', 'GRTUSDT', 'CELOUSDT', 'TWTUSDT', 'REEFUSDT', 'OGUSDT', 'ATMUSDT', 'ASRUSDT', '1INCHUSDT', 'RIFUSDT', 'TRUUSDT', 'DEXEUSDT', 'CKBUSDT', 'FIROUSDT', 'LITUSDT', 'PROSUSDT', 'SFPUSDT', 'FXSUSDT', 'DODOUSDT', 'UFTUSDT', 'ACMUSDT', 'PHAUSDT', 'BADGERUSDT', 'FISUSDT', 'OMUSDT', 'PONDUSDT', 'ALICEUSDT', 'DEGOUSDT', 'BIFIUSDT', 'LINAUSDT']
makeWhiteList(coins)
for coin in whiteList:
    get_history_data(coin)
    
for passcoin in passescoins:
    try:
        get_data(passcoin.coin)
    except Exception as E:
        print(f'Error with coin {passcoin.coin}')        
startTelebot()
sendWhiteList(whiteList)
OnPosition = False
for i in range(600):
    for passcoin in passescoins:
        try:
            get_data(passcoin.coin)
            update_dataframe(passcoin.dataframe)
            Strategy(passcoin)
        except Exception as E:
            print(E)
            continue
    if i % 30 == 0:
        sendMessage()
        makeStatistic(i)
    print('Cycle ', i)
    time.sleep(60)