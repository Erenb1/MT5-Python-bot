
import time
from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd
from strategies import generate_signals
from trade import open_position_checker, place_order_long, place_order_short, position_close_short, position_close_long
from config import USERNAME, PASSWORD, SERVER, SYMBOLS

def login_to_mt5():
    if not mt5.initialize(login=USERNAME, password=PASSWORD, server=SERVER):
        print(f"Failed to initialize MetaTrader 5. Error: {mt5.last_error()}")
        return False
    print("Logged in successfully.")
    return True

def get_seconds_until_next_candle(timeframe):
    tf_int = int(timeframe[1:])
    tf_seconds = tf_int * 60 if timeframe.startswith('M') else tf_int * 3600
    now = datetime.now()
    seconds_since_midnight = now.hour * 3600 + now.minute * 60 + now.second
    return tf_seconds - (seconds_since_midnight % tf_seconds)

def main():
    timeframe = input("Enter timeframe (M1, M5, H1): ").strip().upper()
    if not login_to_mt5():
        return

    candle_count = 50

    print("\n>>> Trading bot started...\n")
    while True:
        try:
            for symbol in SYMBOLS:
                df = generate_signals(symbol, timeframe, candle_count)
                signal = df.iloc[-1]
                direction = open_position_checker(symbol)

                if signal["Crossover"] == 1 and signal["Slope"] == 1:
                    if direction == "Short":
                        position_close_short(symbol, mt5.positions_get(symbol=symbol)[0])
                        place_order_long(symbol)
                    elif direction != "Long":
                        place_order_long(symbol)

                elif signal["Crossover"] == -1 and signal["Slope"] == -1:
                    if direction == "Long":
                        position_close_long(symbol, mt5.positions_get(symbol=symbol)[0])
                        place_order_short(symbol)
                    elif direction != "Short":
                        place_order_short(symbol)

                print(df.tail())

            sleep_time = get_seconds_until_next_candle(timeframe)
            print(f"Waiting {sleep_time} seconds for next candle...\n")
            time.sleep(10)

        except Exception as e:
            print(f"[ERROR] Main loop exception: {e}")
            break

if __name__ == "__main__":
    main()
