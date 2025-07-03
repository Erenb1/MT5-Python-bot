
import MetaTrader5 as mt5
import talib as ta
import pandas as pd

def open_position_checker(symbol):
    positions = mt5.positions_get(symbol=symbol)
    if positions is None or len(positions) == 0:
        return None
    position = positions[0]
    return "Short" if position.type == 1 else "Long"

def calculate_atr(symbol, timeframe, period=14):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, period + 11)
    df = pd.DataFrame(rates)
    df['ATR'] = ta.ATR(df['high'], df['low'], df['close'], timeperiod=period)
    return df.iloc[-1]["ATR"]

def place_order_long(symbol, lot_size=0.1):
    atr_value = calculate_atr(symbol, mt5.TIMEFRAME_M5)
    price = mt5.symbol_info_tick(symbol).ask
    sl = price - atr_value
    tp = price + 1.4 * atr_value
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot_size,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": 20,
        "magic": 234000,
        "comment": "Crossover Strategy",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    mt5.order_send(request)

def place_order_short(symbol, lot_size=0.1):
    atr_value = calculate_atr(symbol, mt5.TIMEFRAME_M5)
    price = mt5.symbol_info_tick(symbol).bid
    sl = price + atr_value
    tp = price - 1.4 * atr_value
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot_size,
        "type": mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": 20,
        "magic": 234000,
        "comment": "Crossover Strategy",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    mt5.order_send(request)

def position_close_short(symbol, position):
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": position.volume,
        "type": mt5.ORDER_TYPE_BUY,
        "position": position.ticket,
        "price": mt5.symbol_info_tick(symbol).ask,
        "deviation": 20,
        "magic": 234000,
        "comment": "Close Short",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    mt5.order_send(request)

def position_close_long(symbol, position):
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": position.volume,
        "type": mt5.ORDER_TYPE_SELL,
        "position": position.ticket,
        "price": mt5.symbol_info_tick(symbol).bid,
        "deviation": 20,
        "magic": 234000,
        "comment": "Close Long",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    mt5.order_send(request)
