import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def vwap_breakout(data):
    breakout_indices = data[data['Close'] > data['VWAP']].index
    return breakout_indices

def vwap_reversal(data, deviation_threshold=2):
    deviations = (data['Close'] - data['VWAP']) / data['VWAP'] * 100
    reversal_indices = deviations[abs(deviations) > deviation_threshold].index
    return reversal_indices

def vwap_pullback(data, pullback_threshold=0.02):
    pullback_indices = data[(data['Close'] < data['VWAP']) & (data['Low'] > data['VWAP'] * (1 - pullback_threshold))].index
    return pullback_indices

def vwap_bands(data, num_std=2):
    upper_band = data['VWAP'] + num_std * data['Volume'].rolling(window=20).std() / data['Volume'].rolling(window=20).mean()
    lower_band = data['VWAP'] - num_std * data['Volume'].rolling(window=20).std() / data['Volume'].rolling(window=20).mean()
    return upper_band, lower_band

def vwap_divergence(data, window=14):
    price_momentum = (data['Close'] / data['Close'].shift(window) - 1) * 100
    vwap_momentum = (data['VWAP'] / data['VWAP'].shift(window) - 1) * 100
    divergence_indices = price_momentum[price_momentum != vwap_momentum].index
    return divergence_indices

def vwap_slope(data, window=10):
    vwap_slope = data['VWAP'].diff(window) > 0
    return vwap_slope

def vwap_support_resistance(data):
    support_indices = data[(data['Close'] < data['VWAP']) & (data['Low'] > data['VWAP'])].index
    resistance_indices = data[(data['Close'] > data['VWAP']) & (data['High'] < data['VWAP'])].index
    return support_indices, resistance_indices

def vwap_volume_confirmation(data, volume_threshold=1.5):
    volume_confirmation_indices = data[data['Volume'] > volume_threshold * data['Volume'].rolling(window=20).mean()].index
    return volume_confirmation_indices

def vwap_trailing_stop(data, stop_factor=0.98):
    trailing_stop = data['VWAP'] * stop_factor
    return trailing_stop

def vwap_crosses(data):
    cross_indices = data[(data['Close'] > data['VWAP']) & (data['Close'].shift() < data['VWAP'].shift())].index
    return cross_indices

# Main code execution
while True:
    ticker = input("Enter a ticker symbol (e.g., AAPL): ")
    if ticker.lower() == 'quit':
        break

    # Fetch historical data using yfinance
    stock = yf.Ticker(ticker)
    history = stock.history(period="1y")

    if history.empty:
        print("No data available for the provided ticker symbol.")
        continue

    # Calculate VWAP
    history['VWAP'] = (history['Volume'] * (history['High'] + history['Low'] + history['Close']) / 3).cumsum() / history['Volume'].cumsum()

    # VWAP Breakout
    breakout_indices = vwap_breakout(history)

    # VWAP Reversal
    reversal_indices = vwap_reversal(history)

    # VWAP Pullback
    pullback_indices = vwap_pullback(history)

    # VWAP Bands
    upper_band, lower_band = vwap_bands(history)

    # VWAP Divergence
    divergence_indices = vwap_divergence(history)

    # VWAP Slope
    vwap_slope_values = vwap_slope(history)

    # VWAP Support/Resistance
    support_indices, resistance_indices = vwap_support_resistance(history)

    # VWAP Volume Confirmation
    volume_confirmation_indices = vwap_volume_confirmation(history)

    # VWAP Trailing Stop
    trailing_stop = vwap_trailing_stop(history)

    # VWAP Crosses
    cross_indices = vwap_crosses(history)

    # Print analysis results
    print(f"\nAnalysis Results for Ticker: {ticker}\n")
    print("VWAP Breakout Indices:")
    print(breakout_indices)

    print("\nVWAP Reversal Indices:")
    print(reversal_indices)

    print("\nVWAP Pullback Indices:")
    print(pullback_indices)

    # Prompt forOops! It seems I got cut off while providing the code. My apologies for the inconvenience. Here's the remainder of the code:

    print("\nVWAP Bands:")
    plt.figure(figsize=(12, 6))
    plt.plot(history.index, history['Close'], label='Close')
    plt.plot(history.index, history['VWAP'], label='VWAP')
    plt.fill_between(history.index, lower_band, upper_band, alpha=0.2, color='gray')
    plt.title(f"VWAP Bands - {ticker}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.show()

    print("\nVWAP Divergence Indices:")
    print(divergence_indices)

    print("\nVWAP Slope:")
    print(vwap_slope_values)

    print("\nVWAP Support Indices:")
    print(support_indices)

    print("\nVWAP Resistance Indices:")
    print(resistance_indices)

    print("\nVWAP Volume Confirmation Indices:")
    print(volume_confirmation_indices)

    print("\nVWAP Trailing Stop:")
    print(trailing_stop)

    print("\nVWAP Crosses:")
    print(cross_indices)

    # Prompt for another ticker symbol
    next_ticker = input("\nEnter another ticker symbol or 'quit' to exit: ")
    if next_ticker.lower() == 'quit':
        break