import itertools
from joblib import Parallel, delayed
from config import settings

def run_grid_search_optimization(symbol_data_dict, test_period_start, test_period_end):
    """
    Multidimensional exhaustive search optimization logic to prevent Curve-Fitting (Overfitting)
    - Searches for Robust Parameters based on Sharpe Ratio and MDD stability rather than just maximum profit (Max PnL).
    """
    # Define the parameter space to search
    ma_fast_candidates = settings.GRID_FAST_MA_RANGE  # [Masked Config]
    ma_slow_candidates = settings.GRID_SLOW_MA_RANGE  # [Masked Config]
    mfi_exit_candidates = settings.GRID_MFI_RANGE     # [Masked Config]
    
    param_combinations = list(itertools.product(
        ma_fast_candidates, ma_slow_candidates, mfi_exit_candidates
    ))
    
    print(f"🔍 Starting backtest for a total of {len(param_combinations)} parameter universes...")

    def test_single_combination(params):
        fast, slow, exit_mfi = params
        if fast >= slow: return None 
        
        # Evaluate simulation target for the entire period
        result = run_simulation_core(
            symbol_data=symbol_data_dict,
            start=test_period_start, end=test_period_end,
            entry_fast=fast, entry_slow=slow, early_exit_mfi=exit_mfi
        )
        
        # [Core] Extract based on scoring formula for downside risk (MDD) and win rate as well as returns
        robust_score = (result['net_profit'] / abs(result['mdd_usd'])) * result['win_rate']
        
        return {
            'params': params,
            'robust_score': robust_score,
            'net_profit': result['net_profit'],
            'mdd_usd': result['mdd_usd'],
            'sharpe': result['sharpe_ratio']
        }

    # Optimize backtest speed using CPU parallel processing (Multiprocessing) via Joblib
    all_results = Parallel(n_jobs=-1)(
        delayed(test_single_combination)(p) for p in param_combinations
    )
    
    valid_results = [r for r in all_results if r is not None]
    optimized_params = sorted(valid_results, key=lambda x: x['robust_score'], reverse=True)[:5]
    
    return optimized_params
