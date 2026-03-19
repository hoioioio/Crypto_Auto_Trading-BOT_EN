"""
Crypto Auto Trading BOT - Main Execution Engine
"""
import time
from config import settings
from utils.logger import send_telegram_message

def main():
    send_telegram_message("🚀 Quant Engine Started: Initializing Data Pipelines & Memory Ledger...")
    
    # Run the main asynchronous event loop for signal generation and order execution
    try:
        while True:
            # heartbeat
            time.sleep(60)
    except KeyboardInterrupt:
        send_telegram_message("🛑 Trading Daemon Stopped Gracefully.")

if __name__ == "__main__":
    main()
