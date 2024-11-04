from ib_insync import IB, Stock, Future, Index, util
import pandas as pd
import time

# Global list of stock symbols and their corresponding contract types
STOCKS = [
    ('VIX', 'INDEX'),
    ('SPX', 'INDEX'),
    ('SPY', 'STOCK'),
    ('QQQ', 'STOCK'),
    ('AMD', 'STOCK'),
    ('NVDA', 'STOCK'),
   # ('ES', 'FUTURE')  # ES (E-mini S&P 500 Futures)
]

# Function to connect to TWS
def connect_ib():
    ib = IB()
    ib.connect('127.0.0.1', 7496, clientId=1)  # Adjust port if necessary (7497 for TWS, 4001 for IB Gateway)
    return ib

# Function to calculate RSI
def calculate_rsi(data, period=9):
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Function to calculate VWAP
def calculate_vwap(data):
    vwap = (data['close'] * data['volume']).cumsum() / data['volume'].cumsum()
    return vwap

# Function to calculate VWAP bands (upper and lower bounds)
def calculate_vwap_bands(data, num_std=2):
    vwap = calculate_vwap(data)
    rolling_std = data['close'].rolling(window=20).std()  # Rolling standard deviation
    upper_band = vwap + (num_std * rolling_std)
    lower_band = vwap - (num_std * rolling_std)
    return upper_band.iloc[-1], lower_band.iloc[-1]

# Function to calculate percentage distance from current price to VWAP
def calculate_percentage_distance(current_price, vwap):
    if vwap == 0:  # Avoid division by zero
        return None
    return ((current_price - vwap) / vwap) * 100

# Function to get current data for a given stock symbol
def get_current_data(ib, symbol, contract_type):
    try:
        # Create contract based on type
        if contract_type == 'STOCK':
            contract = Stock(symbol, 'SMART', 'USD')
        elif contract_type == 'INDEX':
            contract = Index(symbol, 'CBOE')  # SPX and VIX are both traded on CBOE
        elif contract_type == 'FUTURE':
            contract = Future(conId=495512557, symbol='ES', lastTradeDateOrContractMonth='20241220', multiplier='50', exchange='CME', currency='USD', localSymbol='ESZ4', tradingClass='ES')

        # Request historical data (3-minute bars for the last day)
        historical_data = ib.reqHistoricalData(
            contract,
            endDateTime='',
            durationStr='1 D',  # 1 Day worth of historical data
            barSizeSetting='5 mins',  # 3-minute bars
            whatToShow='TRADES',
            useRTH=False,  # Use all trading hours (including extended)
            formatDate=1
        )

        if not historical_data:
            print(f"Error: No historical data returned for {symbol}.")
            return None, None, None, None, None, None

        df = util.df(historical_data)
        if df.empty:
            print(f"Error: DataFrame is empty for {symbol}.")
            return None, None, None, None, None, None

        current_price = df['close'].iloc[-1]
        vwap = calculate_vwap(df).iloc[-1]
        df['RSI'] = calculate_rsi(df)
        latest_rsi = df['RSI'].iloc[-1]
        upper_band, lower_band = calculate_vwap_bands(df)
        percentage_distance = calculate_percentage_distance(current_price, vwap)

        return current_price, vwap, latest_rsi, upper_band, lower_band, percentage_distance

    except Exception as e:
        print(f"An error occurred while fetching data for {symbol}: {e}")
        return None, None, None, None, None, None

# Main function to run the analysis for multiple stocks
def main():
    ib = connect_ib()

    while True:
        # Clear previous output
        print("\033c", end='')  # ANSI escape sequence to clear the console
        
        # Get the current time for formatting
        formatted_time = pd.Timestamp.now().strftime('%H:%M:%S')
        
        # Get current data for each stock
        current_price_spx, vwap_spx, latest_rsi_spx, upper_band_spx, lower_band_spx, percentage_distance_spx = get_current_data(ib, 'SPX', 'INDEX')
        current_price_spy, vwap_spy, latest_rsi_spy, upper_band_spy, lower_band_spy, percentage_distance_spy = get_current_data(ib, 'SPY', 'STOCK')
        current_price_qqq, vwap_qqq, latest_rsi_qqq, upper_band_qqq, lower_band_qqq, percentage_distance_qqq = get_current_data(ib, 'QQQ', 'STOCK')
        current_price_es, vwap_es, latest_rsi_es, upper_band_es, lower_band_es, percentage_distance_es = get_current_data(ib, 'ES', 'FUTURE')
        current_price_vix, vwap_vix, latest_rsi_vix, upper_band_vix, lower_band_vix, percentage_distance_vix = get_current_data(ib, 'VIX', 'INDEX')

        # Print data for each stock
        print(f"\rSymbol: SPX Time: {formatted_time} | Price: {current_price_spx:.2f} | VWAP: {vwap_spx:.2f} | "
              f"RSI (9): {latest_rsi_spx:.2f} | Upper Band: {upper_band_spx:.2f} | Lower Band: {lower_band_spx:.2f} | "
              f"Percentage Distance: {percentage_distance_spx:.2f}%")
        
        print(f"\rSymbol: SPY Time: {formatted_time} | Price: {current_price_spy:.2f} | VWAP: {vwap_spy:.2f} | "
              f"RSI (9): {latest_rsi_spy:.2f} | Upper Band: {upper_band_spy:.2f} | Lower Band: {lower_band_spy:.2f} | "
              f"Percentage Distance: {percentage_distance_spy:.2f}%")
        
        print(f"\rSymbol: QQQ Time: {formatted_time} | Price: {current_price_qqq:.2f} | VWAP: {vwap_qqq:.2f} | "
              f"RSI (9): {latest_rsi_qqq:.2f} | Upper Band: {upper_band_qqq:.2f} | Lower Band: {lower_band_qqq:.2f} | "
              f"Percentage Distance: {percentage_distance_qqq:.2f}%")

        print(f"\rSymbol: VIX Time: {formatted_time} | Price: {current_price_vix:.2f} | VWAP: {vwap_vix:.2f} | "
              f"RSI (9): {latest_rsi_vix:.2f} | Upper Band: {upper_band_vix:.2f} | Lower Band: {lower_band_vix:.2f} | "
              f"Percentage Distance: {percentage_distance_vix:.2f}%", end='')

        print(f"\rSymbol: ES Time: {formatted_time} | Price: {current_price_es:.2f} | VWAP: {vwap_es:.2f} | "
              f"RSI (9): {latest_rsi_es:.2f} | Upper Band: {upper_band_es:.2f} | Lower Band: {lower_band_es:.2f} | "
              f"Percentage Distance: {percentage_distance_es:.2f}%")

        # Move to the next line after printing all data
        print()  # This ensures the next output starts on a new line

        # Optional: Adjust the delay if needed
        #time.sleep(5)

    ib.disconnect()

if __name__ == "__main__":
    main()
