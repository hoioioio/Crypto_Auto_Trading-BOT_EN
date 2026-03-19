from config import settings
from utils.logger import send_telegram_message

def update_hard_sl_exchange(symbol, side, sl_price, exchange):
    """
    Flash Crash Protection: Exchange Server-side Hard Stop Loss Routing
    """
    try:
        # 1. Cancel Existing Stops to avoid ghost triggers
        open_orders = exchange.fetch_open_orders(symbol)
        for o in open_orders:
            if o['type'] == 'STOP_MARKET':
                exchange.cancel_order(o['id'], symbol)
                
        # 2. Place New Stop Order
        stop_side = 'sell' if side in ['buy', 'long'] else 'buy'
        sl_price_str = exchange.price_to_precision(symbol, sl_price)
        
        # Use 'closePosition=True' to prevent decimal precision residue / dust errors
        params = {
            'stopPrice': float(sl_price_str),
            'closePosition': True, 
            'workingType': 'MARK_PRICE' 
        }
        
        exchange.create_order(symbol, 'STOP_MARKET', stop_side, None, None, params)
        print(f"✅ {symbol} Hard SL Activated at: {sl_price_str}")
        
    except Exception as e:
        send_telegram_message(f"🚨 [Hard_SL_Update_Failed] {symbol} Emergency Stop Loss setup failed: {e}")

def execute_market_order(symbol, side, amount, exchange, reason="Unknown"):
    """
    Paper Trading Compatible Execution Engine
    - Routes to Live Exchange API or updates robust In-Memory Ledger (Paper Trading) based on LIVE_MODE parameter.
    """
    try:
        if settings.LIVE_MODE:
            # Route: Live Exchange API
            order = exchange.create_market_order(symbol, side, amount)
            send_telegram_message(f"✅ [REAL] {symbol} {side.upper()} Execution Confirmed! ({reason})")
            return order
        else:
            # Route: Paper Trading Simulation Logic
            # Mathematically simulates execution Slippage and Taker Fees to reflect true market impact in virtual ledger
            simulated_price = get_current_tick_price(symbol, exchange) # Pseudo-function mapping
            simulated_fee = amount * simulated_price * settings.TAKER_FEE_RATE
            
            # Update lifecycle of In-Memory Virtual Position object
            update_virtual_position(symbol, side, amount, simulated_price, simulated_fee) # Pseudo-function
            
            print(f"🔄 [MOCK] Virtual Execution Confirmed: {side.upper()} {amount} at {simulated_price} ({reason})")
            return {"status": "mock_success", "price": simulated_price, "amount": amount}
            
    except Exception as e:
        send_telegram_message(f"🚨 Critical Failure during Order Execution: {e}")
        return None
