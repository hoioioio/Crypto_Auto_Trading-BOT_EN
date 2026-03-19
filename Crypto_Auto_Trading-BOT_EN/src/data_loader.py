import pandas as pd
from config import settings
from utils.logger import send_telegram_message

def fetch_ohlcv_live(symbol, timeframe, exchange, limit=1500):
    """
    Data Pipeline: Deep Warm-up (History Cache + Live API Supply)
    - Merges historical Pickle data with Live API supply to bridge indicator calculation lag (Zero-latency start-up)
    """
    try:
        # 1. High-speed loading of Historical Base from Local Cache
        hist_df = preload_history(symbol, timeframe) # Pseudo Function
        
        # 2. Fetch Fresh OHLCV payload from Exchange REST API
        data = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        if not data: 
            return hist_df if not hist_df.empty else pd.DataFrame() 

        fresh_df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        fresh_df['datetime'] = pd.to_datetime(fresh_df['timestamp'], unit='ms', utc=True)
        fresh_df.set_index('datetime', inplace=True)
        fresh_df = fresh_df[['open', 'high', 'low', 'close', 'volume']]
        
        # 3. Integrity Merge & Deduplication of Historical and Live Data
        if not hist_df.empty:
            combined_df = pd.concat([hist_df, fresh_df])
            combined_df = combined_df[~combined_df.index.duplicated(keep='last')]
            combined_df.sort_index(inplace=True)
            return combined_df
        else:
            return fresh_df

    except Exception as e:
        send_telegram_message(f"⚠️ {symbol} Live API Fetch Failed, using Cache fallback: {e}")
        return _HISTORY_CACHE.get((symbol, timeframe), pd.DataFrame())
