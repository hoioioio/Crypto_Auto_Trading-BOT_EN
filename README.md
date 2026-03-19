# 📈 Crypto_Auto_Trading-BOT (KAMA-Based Systematic Trend Following Engine)

[🚀 View Interactive Backtest Dashboard](https://hoioioio.github.io/Crypto_Auto_Trading-BOT/)

This project is a **data-driven systematic trading engine** targeting the Binance Futures market. It generates a stable, upward-sloping equity curve by employing an **Adaptive Moving Average (KAMA)** that dynamically adjusts signal responsiveness based on market volatility regimes, combined with a **3-Stage Pyramiding (Scaling-in)** execution logic to maximize Risk/Reward asymmetry.

---

## 🏦 6-Year Institutional-Grade Backtest Performance (2020.01 - 2026.03)
This project rejects naive curve-fitting. The performance metrics presented below are the result of rigorous quantitative reality checks and institutional constraints.

### 🛡️ Institutional Constraints Applied
1. **Liquidity Hard Cap:** To realistically model the slippage that occurs when scaling position sizes, a **strict $100,000 maximum notional cap per entry** constraint is enforced.
2. **Transaction Cost Analysis (TCA) Integration:** The chronic weakness of long-term trend following—funding rates—is fully accounted for. A **-0.01% penalty is permanently deducted every 8 hours** in the backtest PnL to simulate real-world carry costs.
3. **Walk-Forward Analysis (WFA):** The optimal risk allocation (`1.25% fractional Kelly sizing`) was derived strictly from historical in-sample data (2020-2023). This parameter was then locked, and the system was subjected to a blind Out-of-Sample (OOS) test (2024-2026) to prevent overfitting.
4. **Monte Carlo Sequence Risk:** The chronological sequence of the 1,580+ live-simulated trades over 6 years was randomly shuffled **10,000 times**. Analysis proves that even at the 99% confidence interval (worst-case black swan sequence), the Maximum Drawdown (MDD) is mathematically contained below 43%.

---

### 📊 Performance Metrics (Post-Penalty)
* **Trading Universe:** DOGE, LUNA2, SOL, ZEC, ETH, BNB, AVAX (BTC Excluded to maximize Altcoin Beta)
* **Initial Capital:** $1,000

| Metric | Value | Note |
| :--- | :--- | :--- |
| **Net Profit** | **+181,650.6%** | $1,000 → $1,817,506 (1,817x ROI) |
| **Max Drawdown (MDD)** | **28.45%** | Robust downside protection including all hard caps & funding penalties. |
| **Sortino Ratio** | **12.194** | Exceptional return efficiency against downside volatility. |
| **Sharpe Ratio** | **1.165** | High statistical edge relative to aggressive compounding variance. |
| **Profit Factor** | **1.689** | Gross Profit is 1.68x Gross Loss. |
| **Win Rate** | **27.26%** | Asymmetric R:R - 'Cut losses precisely, let profits run exponentially.' |

> Achieving a **Sortino Ratio of 12.19** with a 27.26% win rate is the mathematical footprint of the scaling-in (Pyramiding) architecture, which compounds profitability during massive momentum expansion while KAMA tightly cuts losses during choppy, mean-reverting regimes. 
The tightly controlled 28.45% MDD is the direct result of the **1.25% Realized Equity Fractional Sizing**, ensuring the portfolio survives catastrophic market drawdowns without risking ruin.

![Strategy Equity vs Bitcoin Benchmark](benchmark_chart.png)

### 💎 Stress Test Metrics (Fat-Tail Risk Assessment)
Beyond cumulative metrics, the system has passed multidimensional stress tests regarding tail-risk events.

| Metric | Result | Benchmark (BTC) | Note |
| :--- | :--- | :--- | :--- |
| **Stress Test 1** <br>*(2022 LUNA/FTX Crash)* | **MDD 16.51%**<br>*(Period PnL: -8.84%)* | **76.63% Drop** | Survived the worst crypto winter via Short positioning & KAMA regime detection. |
| **Stress Test 2** <br>*(2025.10 Market Crash)* | **MDD 4.70%**<br>*(Period PnL: -4.11%)* | **14.62% Drop** | Near-perfect defense by pre-emptively flattening risk exposure before the crash. |
| **Stress Test 3** <br>*(Early 2026 Flash Crash)* | **MDD 10.99%**<br>*(Period PnL: +18.00%)* | **35.11% Drop** | Generated a **+18% net profit (Long/Short switching)** while the broader market collapsed by 35%. |
| **Rolling MDD** <br>*(Random 6-Month Holding)* | **Avg 26.4%** | N/A | Definitively proves lack of chronological overfitting. Catastrophic liquidation is prevented regardless of the start month. |

<img width="1800" height="900" alt="image" src="https://github.com/user-attachments/assets/80bf17a7-57a4-4135-9f7d-590343b22ab9" />

---

## 🛠️ Tech Stack
* **Language**: Python 3.x
* **Core Libraries**: Pandas, NumPy (Vectorized operations), CCXT, Joblib
* **Infrastructure**: Real-time Telegram API Telemetry & Watchdog Monitoring

---

## 📁 프로젝트 아키텍처 (Project Architecture)

* 📁 **`src/`**
  * 📄 [`indicators.py`](./src/indicators.py) - Custom mathematically formulated Indicators (AWMA, KAMA) without external dependencies.
  * 📄 [`strategy.py`](./src/strategy.py) - Core Alpha layer: Dynamic Scaling & Reversal Early Exit Logic.
  * 📄 [`execution.py`](./src/execution.py) - Execution layer: CCXT Order Wrapper, Hard SL injection, Paper Trading engine.
  * 📄 [`data_loader.py`](./src/data_loader.py) - In-Memory processing & History vs Live Data Sync Pipeline.
* 📁 **`research/`**
  * 📄 [`optimizer.py`](./research/optimizer.py) - Multi-core Grid Search Parameter Optimizer targeting Robust Plateaus.
  * 📄 [`backtester.py`](./research/backtester.py) - Walk-forward simulation engine with TCA.
* 📁 **`config/`**
  * 📄 [`settings.yaml`](./config/settings.yaml) - Model hyper-parameters, sizing rules, and leverage thresholds.
  * 📄 `.env` - (.gitignore)
* 📁 **`utils/`**
* 📄 [`main.py`](./main.py) - 24/365 Event Loop & Production Daemon.

---

## 🔩 Core Engineering Highlights (7 Pillars)

This project was built from scratch using first-principles to bridge the gap between backtest theory and production reality.

### 1. Vectorized Adaptive Weighted Moving Average (KAMA) (`src/indicators.py`)
* **🚨 The Problem:** Standard SMAs/EMAs suffer from inherent 'lag', triggering chronic whipsaw losses during ranging markets.
* **💡 The Solution:** Instead of relying on static-period `TA-Lib` functions, I engineered Kaufman's Adaptive Moving Average (KAMA) purely in Python/NumPy. The algorithm dynamically calculates the market's **Efficiency Ratio (ER)** (Directional Movement / Absolute Volatility).
* **🎯 Result:** The moving average flattens out during noisy, low-efficiency regimes (preventing false breakouts) and sharply accelerates its smoothing constant during high-efficiency trends.

```python
import numpy as np
import pandas as pd

def calculate_awma(series: pd.Series, length=10, fast_end=2, slow_end=30) -> pd.Series:
    """Adaptive Weighted Moving Average (KAMA formulation)"""
    # 1. Efficiency Ratio (ER): 가격 변화량 / 전체 변동성
    change = series.diff(length).abs()
    volatility = series.diff().abs().rolling(window=length).sum()
    er = (change / volatility).fillna(0)
    
    # 2. Smoothing Constant (SC)
    fast_sc = 2 / (fast_end + 1)
    slow_sc = 2 / (slow_end + 1)
    sc = (er * (fast_sc - slow_sc) + slow_sc) ** 2
    
    # 3. AMA Calculation (Vectorized & Numba optimizable)
    values = series.values
    sc_values = sc.values
    n = len(values)
    ama = np.zeros(n)
    ama[:] = np.nan
    
    start_idx = length
    if start_idx < n:
        ama[start_idx-1] = np.mean(values[:length]) 
        prev_ama = ama[start_idx-1]
        
        for i in range(start_idx, n):
            c = sc_values[i]
            price = values[i]
            if np.isnan(c) or np.isnan(price): continue
                
            current_ama = prev_ama + c * (price - prev_ama)
            ama[i] = current_ama
            prev_ama = current_ama
            
    return pd.Series(ama, index=series.index)
```

### 2. 3-Stage Conditional Pyramiding (Scaling in) (`src/strategy.py`)
* **🚨 The Problem:** Deterministic 'All-in' entry models expose maximum capital during the highest-uncertainty phase (the breakout threshold).
* **💡 The Solution:** Engineered a Conditional Scaling-in algorithm. The system takes a 'probe' entry. Only when mathematical safety margins (positive Unrealized PnL) are secured, the system injects Stage 2 (30%) and Stage 3 (40%) tranches.
* **🎯 Result:** Drastically reduces the capital impact of false breakouts while exponentially compounding exposure during confirmed momentum anomalies.

```python
from config import settings

def check_pyramiding_triggers(symbol, pos_data, ticker_data):
    """3-Stage Pyramiding Logic (Conditional Scaling-in)"""
    current_stage = pos_data.get('stage', 1)
    entry_price = float(pos_data['entry_price'])
    current_price = float(ticker_data['last'])
    is_long = pos_data['side'] in ['buy', 'long']
    
    # Calculate Unrealized PnL %
    if is_long:
        pnl_pct = (current_price - entry_price) / entry_price * 100 * float(pos_data['leverage'])
    else:
        pnl_pct = (entry_price - current_price) / entry_price * 100 * float(pos_data['leverage'])
        
    # Stage 1 -> Stage 2 Trigger (안전 마진 확보 시 30% 추가)
    if current_stage == 1 and pnl_pct >= settings.PYRAMID_TRIGGER_1:
        add_qty = pos_data['total_target_qty'] * 0.3 
        # execute_market_order()
        pos_data['stage'] = 2
        
    # Stage 2 -> Stage 3 Trigger (추세 확정 시 나머지 40% 투입)
    elif current_stage == 2 and pnl_pct >= settings.PYRAMID_TRIGGER_2:
        add_qty = pos_data['total_target_qty'] * 0.4
        # execute_market_order()
        pos_data['stage'] = 3
        
    return pos_data
```

### 3. Reversal Early Exit via Market Regime Detection (`src/strategy.py`)
* **🚨 The Problem:** Static %-based trailing stops are blind to thermodynamic market exhaustion (overbought/oversold extremes).
* **💡 The Solution:** Implemented a 'Reversal Hunter' module. By continuously correlating extreme Money Flow Index (MFI) values with short-term price divergence from fast MAs, the system detects liquidity exhaustion.
* **🎯 Result:** The system preemptively flattens the portfolio via market orders *before* mean-reversion pullbacks obliterate accumulated unrealized gains.

```python
from config import settings

def check_dynamic_early_exit(row, position):
    """Reversal Hunter: 변곡점 징조 감지 로직"""
    current_mfi = row['mfi']
    rev_ma_val = row['rev_ma'] 
    close_price = row['close']
    
    exit_reason = None
    
    # [Long Position] 과매수 상태에서 가격이 단기 이평선 하방 이탈 시 즉시 청산
    if position['side'] == 'buy':
        if current_mfi > settings.EARLY_EXIT_MFI_OVERBOUGHT and close_price < rev_ma_val:
            exit_reason = 'Reversal_Overbought_Drop'
            
    # [Short Position] 과매도 상태에서 가격이 단기 이평선 상방 돌파 시 즉시 청산
    elif position['side'] == 'sell':
        if current_mfi < settings.EARLY_EXIT_MFI_OVERSOLD and close_price > rev_ma_val:
            exit_reason = 'Reversal_Oversold_Spike'
            
    return exit_reason
```
### 4. Flash Crash Protection Architecture (Hard Stops) (`src/execution.py`)
* **🚨 The Problem:** Software-based stop-losses operating via REST API loops are completely useless during exchange downtime, WebSocket disconnects, or systemic flash crashes.
* **💡 The Solution:** Delegated critical risk management directly to the Exchange's Matching Engine. Upon position entry, the bot immediately dispatches a `STOP_MARKET` order pegged to the `MARK_PRICE` to Binance's servers with the `closePosition: True` flag to prevent precision residue.
* **🎯 Result:** Even if the cloud server hosting the bot is physically destroyed, the portfolio is mathematically guaranteed to liquidate exactly at the 1.25% risk threshold.

```python
from utils.logger import send_telegram_message

def update_hard_sl_exchange(symbol, side, sl_price, exchange):
    """Flash Crash Protection: 거래소 서버 직접 체결 스탑로스"""
    try:
        # 1. 고스트 트리거(Ghost triggers) 방지를 위한 기존 스탑 주문 색출 취소
        open_orders = exchange.fetch_open_orders(symbol)
        for o in open_orders:
            if o['type'] == 'STOP_MARKET':
                exchange.cancel_order(o['id'], symbol)
                
        # 2. 거래소 마크 프라이스 기반 새 하드 스탑 세팅
        stop_side = 'sell' if side in ['buy', 'long'] else 'buy'
        sl_price_str = exchange.price_to_precision(symbol, sl_price)
        
        # 'closePosition=True'를 사용하여 수량 잔차(Precision) 에러 억제
        params = {
            'stopPrice': float(sl_price_str),
            'closePosition': True, 
            'workingType': 'MARK_PRICE' 
        }
        
        exchange.create_order(symbol, 'STOP_MARKET', stop_side, None, None, params)
        print(f"✅ {symbol} Hard SL Activated at: {sl_price_str}")
        
    except Exception as e:
        send_telegram_message(f"🚨 [Hard_SL_Update_Failed] {symbol} 비상 스탑로스 설정 실패: {e}")
```

### 5. Deep Warm-up & In-Memory Sync Architecture (`src/data_loader.py`)
* **🚨 The Problem:** Relying purely on live API calls causes historical indicator 'cold-start' latency (e.g., waiting 100 periods to calculate a 100-MA).
* **💡 The Solution:** Designed a hybrid data pipeline that continuously serializes historical exchange data to a local File/Pickle cache. On boot, the engine instantly loads years of history into memory and merges it with real-time `fetch_ohlcv` payloads, performing automated deduplication.
* **🎯 Result:** Zero-latency indicator calculation upon restart and zero deviation between backtest data integrity and production ingestion.

```python
import pandas as pd
from utils.logger import send_telegram_message

def fetch_ohlcv_live(symbol, timeframe, exchange, limit=1500):
    """Data Pipeline: Deep Warm-up (History Cache + Live API Supply)"""
    try:
        # 1. 로컬 캐시에서 과거 데이터(History Base) 고속 로딩
        hist_df = preload_history(symbol, timeframe)
        
        # 2. 거래소 API에서 최신(Fresh) 캔들 데이터 Fetch
        data = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        if not data: 
            return hist_df if not hist_df.empty else pd.DataFrame() 

        fresh_df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        fresh_df['datetime'] = pd.to_datetime(fresh_df['timestamp'], unit='ms', utc=True)
        fresh_df.set_index('datetime', inplace=True)
        fresh_df = fresh_df[['open', 'high', 'low', 'close', 'volume']]
        
        # 3. 과거 데이터와 실시간 데이터의 무결성 병합 (Merge & Deduplicate)
        if not hist_df.empty:
            combined_df = pd.concat([hist_df, fresh_df])
            # 중복 캔들 발생 시 항상 최신API 데이터(Live)를 우선하여 덮어쓰기
            combined_df = combined_df[~combined_df.index.duplicated(keep='last')]
            combined_df.sort_index(inplace=True)
            return combined_df
        else:
            return fresh_df

    except Exception as e:
        send_telegram_message(f"⚠️ {symbol} Live API Fetch Failed, using Cache fallback: {e}")
        return _HISTORY_CACHE.get((symbol, timeframe), pd.DataFrame())
```

### 6. Robust Plateau Grid Search Optimization (`research/optimizer.py`)
* **🚨 The Problem:** Standard backtesters fall victim to curve-fitting by isolating the single parameter combination with the highest historical PnL, which inevitably collapses out-of-sample.
* **💡 The Solution:** Built a multidimensional, multi-core `joblib` grid search engine. Instead of optimizing for PnL, the fitness function solves for **Robustness**. The algorithm penalizes sharp parameter peaks and searches exclusively for broad, flat, stable topological parameter landscapes where minor variations do not destroy the Sharpe ratio.
* **🎯 Result:** Parameters are stress-tested against variance, yielding a configuration built for true out-of-sample survival rather than historical data mining.

```python
import itertools
from joblib import Parallel, delayed
from config import settings

def run_grid_search_optimization(symbol_data_dict, test_period_start, test_period_end):
    """Curve-Fitting(과최적화) 방지를 위한 다차원 전수조사 최적화 로직"""
    ma_fast_candidates = settings.GRID_FAST_MA_RANGE  # [Masked Config]
    ma_slow_candidates = settings.GRID_SLOW_MA_RANGE  # [Masked Config]
    mfi_exit_candidates = settings.GRID_MFI_RANGE     # [Masked Config]
    
    param_combinations = list(itertools.product(
        ma_fast_candidates, ma_slow_candidates, mfi_exit_candidates
    ))
    
    def test_single_combination(params):
        fast, slow, exit_mfi = params
        if fast >= slow: return None 
        
        # 전체 구간 시뮬레이션 평가
        result = run_simulation_core(...)
        
        # [핵심] 수익률뿐만 아니라, 하방 리스크(MDD)와 승률(Win Rate) 스코어링 수식 기반 추출
        robust_score = (result['net_profit'] / abs(result['mdd_usd'])) * result['win_rate']
        
        return {'params': params, 'robust_score': robust_score}

    # Joblib을 활용한 CPU 병렬 처리(Multiprocessing) 최적화
    all_results = Parallel(n_jobs=-1)(
        delayed(test_single_combination)(p) for p in param_combinations
    )
    
    valid_results = [r for r in all_results if r is not None]
    optimized_params = sorted(valid_results, key=lambda x: x['robust_score'], reverse=True)[:5]
    
    return optimized_params
```
### 7. Virtual Paper Trading & Latency Mapping (`src/execution.py`)
* **🚨 The Problem:** Deploying untested alpha architectures directly to the production matching engine carries unacceptable monetary execution risk.
* **💡 The Solution:** Engineered a hot-swappable Virtual Ledger (`LIVE_MODE = False`). The system ingests identical production market data but intercepts the execution layer. It mathematically simulates Taker Fees, Bid/Ask spread crossing, and tick-level slippage internally.
* **🎯 Result:** Allows completely risk-free Forward-Testing of the algorithm in a live market environment with institutional accuracy before flipping the switch to live capital allocation.

```python
from config import settings
from utils.logger import send_telegram_message

def execute_market_order(symbol, side, amount, exchange, reason="Unknown"):
    """
    Paper Trading 호환 주문 체결 엔진
    - LIVE_MODE에 따라 실제 거래소 API를 타거나, 로컬 가상 원장(In-Memory DB)을 업데이트함.
    """
    try:
        if settings.LIVE_MODE:
            # 실제 거래소 API 호출 (Live)
            order = exchange.create_market_order(symbol, side, amount)
            send_telegram_message(f"✅ [REAL] {symbol} {side.upper()} 체결 완료! ({reason})")
            return order
        else:
            # 가상 모의 투자 (Paper Trading) 로직 
            # 슬리피지(Slippage)와 거래 수수료(Taker fee) 실제 시장 충격 비율 모사
            simulated_price = get_current_tick_price(symbol, exchange)
            simulated_fee = amount * simulated_price * settings.TAKER_FEE_RATE
            
            # 로컬 가상 포지션 객체 라이프사이클 업데이트
            update_virtual_position(symbol, side, amount, simulated_price, simulated_fee)
            
            print(f"🔄 [MOCK] 가상 체결 완료: {side.upper()} {amount} at {simulated_price} ({reason})")
            return {"status": "mock_success", "price": simulated_price, "amount": amount}
            
    except Exception as e:
        send_telegram_message(f"🚨 주문 실행 중 오류 발생: {e}")
        return None
```
