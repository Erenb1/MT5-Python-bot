
import MetaTrader5 as mt5

def set_query_timeframe(timeframe: str):
    tf_map = {
        "M1": mt5.TIMEFRAME_M1,
        "M5": mt5.TIMEFRAME_M5,
        "M15": mt5.TIMEFRAME_M15,
        "H1": mt5.TIMEFRAME_H1,
        "H4": mt5.TIMEFRAME_H4,
        "D1": mt5.TIMEFRAME_D1,
    }
    return tf_map.get(timeframe.upper(), mt5.TIMEFRAME_M5)
