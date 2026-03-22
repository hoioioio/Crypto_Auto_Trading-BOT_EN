from config import settings

def check_pyramiding_triggers(symbol, pos_data, ticker_data):
    """
    3-Stage Pyramiding Logic (Conditional Scaling-in)
    """
    current_stage = pos_data.get('stage', 1)
    entry_price = float(pos_data['entry_price'])
    current_price = float(ticker_data['last'])
    is_long = pos_data['side'] in ['buy', 'long']
    
    # Calculate Unrealized PnL %
    if is_long:
        pnl_pct = (current_price - entry_price) / entry_price * 100 * float(pos_data['leverage'])
    else:
        pnl_pct = (entry_price - current_price) / entry_price * 100 * float(pos_data['leverage'])
        
    # Stage 1 -> Stage 2 Trigger (Secure Margin, Inject 30%)
    if current_stage == 1 and pnl_pct >= settings.PYRAMID_TRIGGER_1: 
        add_qty = pos_data['total_target_qty'] * 0.3 # Inject 30% aggregate size
        # execute_market_order(symbol, pos_data['side'], add_qty, reason="Pyramid_Stage_2")
        pos_data['stage'] = 2
        
    # Stage 2 -> Stage 3 Trigger (Trend Confirmed, Inject Remaining 40%)
    elif current_stage == 2 and pnl_pct >= settings.PYRAMID_TRIGGER_2: 
        add_qty = pos_data['total_target_qty'] * 0.4 # Inject remaining 40% aggregate size
        # execute_market_order(symbol, pos_data['side'], add_qty, reason="Pyramid_Stage_3")
        pos_data['stage'] = 3
        
    return pos_data

def check_dynamic_early_exit(row, position):
    """
    Reversal Hunter: Reversal & Exhaustion Detection Logic
    """
    current_mfi = row['mfi']
    rev_ma_val = row['rev_ma'] 
    close_price = row['close']
    
    exit_reason = None
    
    # [Long Position] Immediate exit if Overbought MFI coincides with price breaking below Short-term MA
    if position['side'] == 'buy':
        if current_mfi > settings.EARLY_EXIT_MFI_OVERBOUGHT and close_price < rev_ma_val:
            exit_reason = 'Reversal_Overbought_Drop'
            
    # [Short Position] Immediate exit if Oversold MFI coincides with price breaking above Short-term MA
    elif position['side'] == 'sell':
        if current_mfi < settings.EARLY_EXIT_MFI_OVERSOLD and close_price > rev_ma_val:
            exit_reason = 'Reversal_Oversold_Spike'
            
    return exit_reason
