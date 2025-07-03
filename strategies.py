
import pandas as pd
import MetaTrader5 as mt5
import talib as ta
from utils import set_query_timeframe

def generate_signals(symbol, timeframe, candle_count=30):
    mt_timeframe = set_query_timeframe(timeframe)
    rates = mt5.copy_rates_from_pos(symbol, mt_timeframe, 0, candle_count)
    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df.set_index("time", inplace=True)

    df["EMA_high_period"] = ta.EMA(ta.EMA(df["close"], 20), 2)
    df["EMA_slope"] = df["EMA_high_period"].diff()
    df["Fastema"] = ta.EMA(df["close"], 3)
    df["Slope"] = df["EMA_slope"].apply(lambda x: -1 if x <= 0 else 1)
    df["Crossover"] = 0

    for i in range(1, len(df)):
        if df["Fastema"].iloc[i] > df["EMA_high_period"].iloc[i] and df["Fastema"].iloc[i-1] <= df["EMA_high_period"].iloc[i-1]:
            df.loc[df.index[i], "Crossover"] = 1
        elif df["Fastema"].iloc[i] < df["EMA_high_period"].iloc[i] and df["Fastema"].iloc[i-1] >= df["EMA_high_period"].iloc[i-1]:
            df.loc[df.index[i], "Crossover"] = -1

    return df
