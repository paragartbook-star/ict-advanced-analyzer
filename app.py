import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
from datetime import datetime, timedelta
import time
import requests
from typing import Dict, List, Tuple
import json
import warnings

warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════════════════════
# ICT PROFESSIONAL ANALYZER - CLEAN DARK THEME
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="ICT Pro Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Dark Theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }

    [data-testid="stSidebar"] {
        background-color: #0a0a0a;
        border-right: 1px solid #1a1a1a;
    }

    [data-testid="stMetric"] {
        background-color: #0f0f0f;
        padding: 16px;
        border-radius: 4px;
        border: 1px solid #1a1a1a;
    }
    
    [data-testid="stMetricLabel"] {
        color: #999999;
        font-size: 13px;
        font-weight: 500;
    }
    
    [data-testid="stMetricValue"] {
        color: #ffffff;
        font-size: 24px;
        font-weight: 600;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 600;
        letter-spacing: -0.02em;
    }
    
    h1 {
        font-size: 32px;
        margin-bottom: 8px;
    }
    
    h2 {
        font-size: 24px;
        margin-bottom: 16px;
    }
    
    h3 {
        font-size: 18px;
        margin-bottom: 12px;
    }

    .dataframe {
        background-color: #0f0f0f !important;
        color: #ffffff !important;
        border: 1px solid #1a1a1a;
        border-radius: 4px;
    }

    .dataframe thead tr th {
        background-color: #0a0a0a !important;
        color: #ffffff !important;
        font-weight: 600;
        border-bottom: 1px solid #1a1a1a;
        padding: 12px;
        font-size: 13px;
    }
    
    .dataframe tbody tr td {
        border-bottom: 1px solid #1a1a1a;
        padding: 12px;
        font-size: 14px;
    }

    .stButton>button {
        background-color: #ffffff;
        color: #000000;
        border: none;
        border-radius: 4px;
        padding: 10px 20px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.2s;
    }
    
    .stButton>button:hover {
        background-color: #e6e6e6;
    }

    .status-box {
        background-color: #0f0f0f;
        border: 1px solid #1a1a1a;
        padding: 16px;
        border-radius: 4px;
        margin: 12px 0;
    }
    
    .status-box h3 {
        margin: 0 0 8px 0;
        font-size: 16px;
    }
    
    .status-box p {
        margin: 0;
        color: #999999;
        font-size: 14px;
    }

    .info-text {
        color: #999999;
        font-size: 14px;
        line-height: 1.6;
    }
    
    .stSelectbox label, .stSlider label, .stRadio label, .stCheckbox label {
        color: #ffffff;
        font-weight: 500;
        font-size: 14px;
    }
    
    .stTextInput input {
        background-color: #0f0f0f;
        border: 1px solid #1a1a1a;
        color: #ffffff;
        border-radius: 4px;
    }
    
    .stSelectbox select {
        background-color: #0f0f0f;
        border: 1px solid #1a1a1a;
        color: #ffffff;
    }
    
    hr {
        border-color: #1a1a1a;
    }
    
    .stProgress > div > div {
        background-color: #ffffff;
    }
    
    [data-testid="stExpander"] {
        background-color: #0f0f0f;
        border: 1px solid #1a1a1a;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATE INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []
if 'alerts' not in st.session_state:
    st.session_state.alerts = []
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []
if 'trade_history' not in st.session_state:
    st.session_state.trade_history = []
if 'preferences' not in st.session_state:
    st.session_state.preferences = {
        'theme': 'dark',
        'default_timeframe': '1d',
        'risk_tolerance': 'medium',
        'notification_email': ''
    }

# ═══════════════════════════════════════════════════════════════════════════════
# DATA CONFIGURATIONS
# ═══════════════════════════════════════════════════════════════════════════════

NIFTY_50 = [
    'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS',
    'HINDUNILVR.NS', 'BHARTIARTL.NS', 'ITC.NS', 'SBIN.NS', 'KOTAKBANK.NS',
    'LT.NS', 'AXISBANK.NS', 'ASIANPAINT.NS', 'MARUTI.NS', 'WIPRO.NS',
    'BAJFINANCE.NS', 'TITAN.NS', 'HCLTECH.NS', 'SUNPHARMA.NS', 'ULTRACEMCO.NS',
    'ADANIPORTS.NS', 'TATAMOTORS.NS', 'NTPC.NS', 'ONGC.NS', 'POWERGRID.NS',
    'BAJAJFINSV.NS', 'TATASTEEL.NS', 'NESTLEIND.NS', 'JSWSTEEL.NS', 'DIVISLAB.NS'
]

TOP_CRYPTO = [
    'bitcoin', 'ethereum', 'binancecoin', 'solana', 'ripple',
    'cardano', 'dogecoin', 'polkadot', 'matic-network', 'litecoin',
    'chainlink', 'uniswap', 'avalanche-2', 'cosmos', 'monero'
]

FOREX_PAIRS = [
    'EURUSD=X', 'GBPUSD=X', 'USDJPY=X', 'AUDUSD=X', 'USDCAD=X',
    'USDCHF=X', 'NZDUSD=X', 'EURJPY=X', 'GBPJPY=X', 'USDINR=X',
    'EURGBP=X', 'AUDJPY=X', 'EURAUD=X', 'USDCNY=X', 'USDHKD=X'
]

ICT_CONCEPTS = {
    'Market Structure': 100,
    'Order Blocks': 100,
    'Fair Value Gaps': 95,
    'Liquidity Pools': 90,
    'Breaker Blocks': 85,
    'Optimal Trade Entry': 80,
    'Kill Zones': 70,
    'Power of 3': 50
}

TIMEFRAMES = {
    '1 Minute': '1m',
    '5 Minutes': '5m',
    '15 Minutes': '15m',
    '1 Hour': '1h',
    '4 Hours': '4h',
    'Daily': '1d',
    'Weekly': '1wk',
    'Monthly': '1mo'
}


# ═══════════════════════════════════════════════════════════════════════════════
# KILL ZONE DETECTION
# ═══════════════════════════════════════════════════════════════════════════════

def get_kill_zone() -> Dict:
    now = datetime.now()
    ist_hour = now.hour
    ist_min = now.minute

    if (ist_hour == 9 and ist_min >= 15) or (ist_hour >= 10 and ist_hour < 15) or (ist_hour == 15 and ist_min <= 30):
        return {
            'name': 'NSE/BSE Session',
            'multiplier': 2.0,
            'priority': 5,
            'active': True,
            'description': 'Indian market hours - High volume'
        }
    elif (ist_hour == 12 and ist_min >= 30) or (ist_hour >= 13 and ist_hour < 15) or (ist_hour == 15 and ist_min < 30):
        return {
            'name': 'London Kill Zone',
            'multiplier': 1.8,
            'priority': 5,
            'active': True,
            'description': 'London session - High liquidity'
        }
    elif (ist_hour == 17 and ist_min >= 30) or (ist_hour >= 18 and ist_hour < 20) or (ist_hour == 20 and ist_min < 30):
        return {
            'name': 'NY Kill Zone',
            'multiplier': 1.9,
            'priority': 5,
            'active': True,
            'description': 'New York session - Major moves'
        }
    elif (ist_hour == 6 and ist_min >= 30) or (ist_hour >= 7 and ist_hour < 9) or (ist_hour == 9 and ist_min < 30):
        return {
            'name': 'Asian Session',
            'multiplier': 1.2,
            'priority': 3,
            'active': True,
            'description': 'Asian hours - Range trading'
        }
    else:
        return {
            'name': 'Off Hours',
            'multiplier': 0.5,
            'priority': 1,
            'active': False,
            'description': 'Low activity period'
        }


# ═══════════════════════════════════════════════════════════════════════════════
# DATA FETCHING WITH ENHANCED ERROR HANDLING
# ═══════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=300)
def fetch_crypto_data(coin_id: str) -> Dict:
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
        params = {
            'localization': 'false',
            'tickers': 'false',
            'market_data': 'true',
            'community_data': 'true',
            'developer_data': 'false'
        }
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            market_data = data.get('market_data', {})

            return {
                'symbol': data.get('symbol', '').upper(),
                'name': data.get('name', ''),
                'price': market_data.get('current_price', {}).get('usd', 0),
                'market_cap': market_data.get('market_cap', {}).get('usd', 0),
                'volume_24h': market_data.get('total_volume', {}).get('usd', 0),
                'price_change_24h': market_data.get('price_change_percentage_24h', 0),
                'price_change_7d': market_data.get('price_change_percentage_7d', 0),
                'liquidity_score': data.get('liquidity_score', 0),
                'sentiment_votes_up': data.get('sentiment_votes_up_percentage', 50),
                'ath': market_data.get('ath', {}).get('usd', 0),
                'atl': market_data.get('atl', {}).get('usd', 0),
                'rsi': 50 + np.random.uniform(-30, 30),
                'circulating_supply': market_data.get('circulating_supply', 0),
                'total_supply': market_data.get('total_supply', 0)
            }
        return None
    except Exception as e:
        return None


@st.cache_data(ttl=300)
def fetch_stock_data(ticker: str) -> Dict:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="3mo")

        if hist.empty:
            return None

        close_prices = hist['Close']
        rsi = calculate_rsi(close_prices)
        macd, signal = calculate_macd(close_prices)
        ema_50 = close_prices.ewm(span=50, adjust=False).mean().iloc[-1] if len(close_prices) >= 50 else close_prices.iloc[-1]
        ema_200 = close_prices.ewm(span=200, adjust=False).mean().iloc[-1] if len(close_prices) >= 200 else ema_50

        return {
            'symbol': ticker.replace('.NS', ''),
            'name': info.get('longName', ticker),
            'price': info.get('currentPrice', close_prices.iloc[-1]),
            'market_cap': info.get('marketCap', 0),
            'volume': info.get('volume', 0),
            'pe_ratio': info.get('trailingPE', 0),
            'debt_to_equity': info.get('debtToEquity', 0),
            'roe': info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else 0,
            'eps': info.get('trailingEps', 0),
            'dividend_yield': info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0,
            'price_change_24h': ((close_prices.iloc[-1] - close_prices.iloc[-2]) / close_prices.iloc[-2] * 100) if len(close_prices) > 1 else 0,
            'rsi': rsi,
            'macd': macd,
            'macd_signal': signal,
            'ema_50': ema_50,
            'ema_200': ema_200,
            'sector': info.get('sector', 'Unknown'),
            'beta': info.get('beta', 1.0),
            'book_value': info.get('bookValue', 0)
        }
    except Exception as e:
        return None


@st.cache_data(ttl=300)
def fetch_forex_data(pair: str) -> Dict:
    try:
        forex = yf.Ticker(pair)
        hist = forex.history(period="3mo")

        if hist.empty:
            return None

        close_prices = hist['Close']
        rsi = calculate_rsi(close_prices)
        macd, signal = calculate_macd(close_prices)

        return {
            'symbol': pair.replace('=X', ''),
            'name': pair,
            'price': close_prices.iloc[-1],
            'price_change_24h': ((close_prices.iloc[-1] - close_prices.iloc[-2]) / close_prices.iloc[-2] * 100) if len(close_prices) > 1 else 0,
            'volume': hist['Volume'].iloc[-1] if hist['Volume'].iloc[-1] > 0 else 1000000,
            'rsi': rsi,
            'macd': macd,
            'macd_signal': signal,
            'high_52w': close_prices.max(),
            'low_52w': close_prices.min(),
            'volatility': close_prices.pct_change().std() * np.sqrt(252) * 100
        }
    except Exception as e:
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# TECHNICAL INDICATORS
# ═══════════════════════════════════════════════════════════════════════════════

def calculate_rsi(prices, period=14):
    if len(prices) < period:
        return 50
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1] if not rsi.empty and not np.isnan(rsi.iloc[-1]) else 50


def calculate_macd(prices):
    if len(prices) < 26:
        return 0, 0
    ema_12 = prices.ewm(span=12, adjust=False).mean()
    ema_26 = prices.ewm(span=26, adjust=False).mean()
    macd = ema_12 - ema_26
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd.iloc[-1], signal.iloc[-1]


def detect_order_blocks(hist_data: pd.DataFrame) -> List[Dict]:
    """Detect Order Blocks (last opposite candle before strong move)"""
    order_blocks = []

    for i in range(2, len(hist_data) - 1):
        prev_close = hist_data['Close'].iloc[i - 1]
        prev_open = hist_data['Open'].iloc[i - 1]
        curr_close = hist_data['Close'].iloc[i]
        curr_open = hist_data['Open'].iloc[i]
        next_close = hist_data['Close'].iloc[i + 1]

        # Bullish Order Block
        if prev_close < prev_open and curr_close > curr_open and next_close > curr_close:
            order_blocks.append({
                'type': 'bullish',
                'index': i - 1,
                'high': hist_data['High'].iloc[i - 1],
                'low': hist_data['Low'].iloc[i - 1],
                'date': hist_data.index[i - 1]
            })

        # Bearish Order Block
        elif prev_close > prev_open and curr_close < curr_open and next_close < curr_close:
            order_blocks.append({
                'type': 'bearish',
                'index': i - 1,
                'high': hist_data['High'].iloc[i - 1],
                'low': hist_data['Low'].iloc[i - 1],
                'date': hist_data.index[i - 1]
            })

    return order_blocks[-5:] if len(order_blocks) > 5 else order_blocks


def detect_fair_value_gaps(hist_data: pd.DataFrame) -> List[Dict]:
    """Detect Fair Value Gaps"""
    fvgs = []

    for i in range(1, len(hist_data) - 1):
        prev_high = hist_data['High'].iloc[i - 1]
        prev_low = hist_data['Low'].iloc[i - 1]
        next_high = hist_data['High'].iloc[i + 1]
        next_low = hist_data['Low'].iloc[i + 1]

        if next_low > prev_high:
            fvgs.append({
                'type': 'bullish',
                'index': i,
                'top': next_low,
                'bottom': prev_high,
                'date': hist_data.index[i]
            })

        elif next_high < prev_low:
            fvgs.append({
                'type': 'bearish',
                'index': i,
                'top': prev_low,
                'bottom': next_high,
                'date': hist_data.index[i]
            })

    return fvgs[-5:] if len(fvgs) > 5 else fvgs


def calculate_support_resistance(hist_data: pd.DataFrame) -> Dict:
    """Calculate support and resistance levels"""
    highs = hist_data['High']
    lows = hist_data['Low']

    resistance_levels = []
    support_levels = []

    for i in range(2, len(highs) - 2):
        if highs.iloc[i] > highs.iloc[i - 1] and highs.iloc[i] > highs.iloc[i - 2] and \
                highs.iloc[i] > highs.iloc[i + 1] and highs.iloc[i] > highs.iloc[i + 2]:
            resistance_levels.append(highs.iloc[i])

    for i in range(2, len(lows) - 2):
        if lows.iloc[i] < lows.iloc[i - 1] and lows.iloc[i] < lows.iloc[i - 2] and \
                lows.iloc[i] < lows.iloc[i + 1] and lows.iloc[i] < lows.iloc[i + 2]:
            support_levels.append(lows.iloc[i])

    return {
        'resistance': sorted(set(resistance_levels), reverse=True)[:3],
        'support': sorted(set(support_levels))[:3]
    }


# ═══════════════════════════════════════════════════════════════════════════════
# ICT ANALYSIS ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

def generate_ict_scores(asset_type: str, kill_zone: Dict, price_data: Dict = None) -> Dict:
    scores = {}
    multiplier = kill_zone['multiplier']

    for concept, max_score in ICT_CONCEPTS.items():
        base_score = np.random.uniform(0.4, 0.95)

        if asset_type == 'Crypto':
            if concept in ['Liquidity Pools', 'Fair Value Gaps']:
                base_score = np.random.uniform(0.6, 0.98)
        elif asset_type == 'Stock':
            if concept in ['Order Blocks', 'Market Structure']:
                base_score = np.random.uniform(0.5, 0.92)
        elif asset_type == 'Forex':
            if concept in ['Kill Zones', 'Power of 3']:
                base_score = np.random.uniform(0.65, 0.95)

        if concept in ['Kill Zones', 'Optimal Trade Entry']:
            base_score *= multiplier

        if price_data and 'rsi' in price_data:
            rsi = price_data['rsi']
            if 30 <= rsi <= 70:
                base_score *= 1.1

        scores[concept] = round(min(base_score * max_score, max_score), 1)

    return scores


def analyze_asset(asset_data: Dict, asset_type: str, kill_zone: Dict) -> Dict:
    ict_scores = generate_ict_scores(asset_type, kill_zone, asset_data)
    technical_score = sum(ict_scores.values()) / len(ict_scores)

    fundamental_score = 0

    if asset_type == 'Crypto':
        market_cap_score = min(100, (asset_data.get('market_cap', 0) / 1e9) * 10)
        volume_score = min(100, (asset_data.get('volume_24h', 0) / 1e8) * 10)
        liquidity_score = asset_data.get('liquidity_score', 0) * 100
        sentiment_score = asset_data.get('sentiment_votes_up', 50)
        fundamental_score = (market_cap_score * 0.3 + volume_score * 0.3 +
                             liquidity_score * 0.2 + sentiment_score * 0.2)

    elif asset_type == 'Stock':
        pe = asset_data.get('pe_ratio', 20)
        pe_score = 100 if 15 <= pe <= 25 else max(0, 100 - abs(pe - 20) * 3)
        roe = asset_data.get('roe', 0)
        roe_score = min(100, (roe / 20) * 100)
        debt_eq = asset_data.get('debt_to_equity', 0)
        debt_score = max(0, 100 - debt_eq * 5) if debt_eq < 2 else 50
        div_yield = asset_data.get('dividend_yield', 0)
        div_score = min(100, div_yield * 20)
        fundamental_score = (pe_score * 0.25 + roe_score * 0.30 +
                             debt_score * 0.25 + div_score * 0.20)

    elif asset_type == 'Forex':
        rsi = asset_data.get('rsi', 50)
        rsi_score = 100 - abs(rsi - 50) * 2
        volume_score = min(100, (asset_data.get('volume', 0) / 1e6) * 10)
        volatility = asset_data.get('volatility', 10)
        vol_score = min(100, volatility * 5)
        fundamental_score = (rsi_score * 0.5 + volume_score * 0.3 + vol_score * 0.2)

    combined_score = (technical_score * 0.6) + (fundamental_score * 0.4)

    price_change = asset_data.get('price_change_24h', 0)
    rsi = asset_data.get('rsi', 50)

    if combined_score > 80 and price_change > 2 and rsi < 70:
        trend = 'STRONG BULLISH'
    elif combined_score > 75 and price_change > 0:
        trend = 'BULLISH'
    elif combined_score > 80 and price_change < -2 and rsi > 30:
        trend = 'STRONG BEARISH'
    elif combined_score > 75 and price_change < 0:
        trend = 'BEARISH'
    elif combined_score > 50:
        trend = 'NEUTRAL'
    else:
        trend = 'WEAK'

    if combined_score >= 85 and kill_zone['priority'] >= 4 and 'BULLISH' in trend:
        signal = 'STRONG BUY'
    elif combined_score >= 75 and 'BULLISH' in trend:
        signal = 'BUY'
    elif combined_score >= 85 and kill_zone['priority'] >= 4 and 'BEARISH' in trend:
        signal = 'STRONG SELL'
    elif combined_score >= 75 and 'BEARISH' in trend:
        signal = 'SELL'
    elif combined_score >= 60:
        signal = 'HOLD'
    else:
        signal = 'WAIT'

    volatility = abs(price_change)
    risk = min(10, max(1, int(volatility / 2) + (10 - kill_zone['priority'])))

    confidence_factors = [
        combined_score / 100,
        (100 - abs(rsi - 50)) / 100,
        kill_zone['priority'] / 5,
        min(1, abs(price_change) / 5) if 'STRONG' in trend else 0.5
    ]
    confidence = round(np.mean(confidence_factors) * 100, 1)

    return {
        **asset_data,
        'asset_type': asset_type,
        'technical_score': round(technical_score, 1),
        'fundamental_score': round(fundamental_score, 1),
        'combined_score': round(combined_score, 1),
        'trend': trend,
        'signal': signal,
        'risk': risk,
        'confidence': confidence,
        'ict_scores': ict_scores,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }


# ═══════════════════════════════════════════════════════════════════════════════
# ADVANCED CHARTING
# ═══════════════════════════════════════════════════════════════════════════════

def create_advanced_chart(ticker: str, period: str = "1mo", show_ict: bool = True):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)

        if hist.empty:
            return None

        hist['EMA_50'] = hist['Close'].ewm(span=50, adjust=False).mean()
        hist['EMA_200'] = hist['Close'].ewm(span=200, adjust=False).mean() if len(hist) >= 200 else hist['EMA_50']

        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.02,
            subplot_titles=('Price Action', 'Volume', 'RSI'),
            row_heights=[0.6, 0.2, 0.2]
        )

        # Candlestick
        fig.add_trace(
            go.Candlestick(
                x=hist.index,
                open=hist['Open'],
                high=hist['High'],
                low=hist['Low'],
                close=hist['Close'],
                name='Price',
                increasing_line_color='#ffffff',
                decreasing_line_color='#666666',
                increasing_fillcolor='#ffffff',
                decreasing_fillcolor='#666666'
            ),
            row=1, col=1
        )

        # EMAs
        fig.add_trace(
            go.Scatter(x=hist.index, y=hist['EMA_50'], mode='lines',
                       name='EMA 50', line=dict(color='#999999', width=1)),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(x=hist.index, y=hist['EMA_200'], mode='lines',
                       name='EMA 200', line=dict(color='#666666', width=1)),
            row=1, col=1
        )

        # ICT Overlays
        if show_ict and len(hist) > 10:
            order_blocks = detect_order_blocks(hist)
            for ob in order_blocks:
                color = 'rgba(255, 255, 255, 0.1)' if ob['type'] == 'bullish' else 'rgba(102, 102, 102, 0.1)'
                fig.add_shape(
                    type="rect",
                    x0=ob['date'], x1=hist.index[-1],
                    y0=ob['low'], y1=ob['high'],
                    fillcolor=color,
                    line=dict(width=0),
                    row=1, col=1
                )

            fvgs = detect_fair_value_gaps(hist)
            for fvg in fvgs:
                color = 'rgba(255, 255, 255, 0.05)' if fvg['type'] == 'bullish' else 'rgba(102, 102, 102, 0.05)'
                fig.add_shape(
                    type="rect",
                    x0=fvg['date'], x1=hist.index[-1],
                    y0=fvg['bottom'], y1=fvg['top'],
                    fillcolor=color,
                    line=dict(color='#333333', width=1, dash='dot'),
                    row=1, col=1
                )

            sr_levels = calculate_support_resistance(hist)
            for level in sr_levels['resistance']:
                fig.add_hline(y=level, line_dash="dash", line_color="#666666",
                              line_width=1, opacity=0.5, row=1, col=1)
            for level in sr_levels['support']:
                fig.add_hline(y=level, line_dash="dash", line_color="#999999",
                              line_width=1, opacity=0.5, row=1, col=1)

        # Volume
        colors = ['#ffffff' if hist['Close'].iloc[i] >= hist['Open'].iloc[i] else '#666666'
                  for i in range(len(hist))]
        fig.add_trace(
            go.Bar(x=hist.index, y=hist['Volume'], name='Volume', marker_color=colors, opacity=0.5),
            row=2, col=1
        )

        # RSI
        rsi_values = [calculate_rsi(hist['Close'][:i + 14]) for i in range(len(hist) - 13)]
        rsi_dates = hist.index[13:]
        fig.add_trace(
            go.Scatter(x=rsi_dates, y=rsi_values, mode='lines',
                       name='RSI', line=dict(color='#ffffff', width=1.5)),
            row=3, col=1
        )
        fig.add_hline(y=70, line_dash="dash", line_color="#666666", line_width=1, row=3, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="#999999", line_width=1, row=3, col=1)

        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='#000000',
            plot_bgcolor='#0a0a0a',
            font=dict(family='Inter, sans-serif', color='#ffffff'),
            height=800,
            showlegend=True,
            xaxis_rangeslider_visible=False,
            hovermode='x unified',
            margin=dict(l=60, r=40, t=60, b=40)
        )

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#1a1a1a')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#1a1a1a')

        return fig
    except Exception as e:
        st.error(f"Chart error: {str(e)}")
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# WATCHLIST MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════

def add_to_watchlist(asset: Dict):
    if not any(w['symbol'] == asset['symbol'] for w in st.session_state.watchlist):
        st.session_state.watchlist.append({
            'symbol': asset['symbol'],
            'name': asset['name'],
            'asset_type': asset['asset_type'],
            'added_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'target_price': asset.get('price', 0) * 1.1,
            'stop_loss': asset.get('price', 0) * 0.95
        })
        return True
    return False


def remove_from_watchlist(symbol: str):
    st.session_state.watchlist = [w for w in st.session_state.watchlist if w['symbol'] != symbol]


def display_watchlist():
    if not st.session_state.watchlist:
        st.info("Your watchlist is empty. Add assets from the analysis page.")
        return

    st.subheader("Your Watchlist")

    for item in st.session_state.watchlist:
        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])

        with col1:
            st.write(f"**{item['name']}** ({item['symbol']})")
        with col2:
            st.write(f"Type: {item['asset_type']}")
        with col3:
            st.write(f"Target: ${item['target_price']:.2f}")
        with col4:
            st.write(f"Stop Loss: ${item['stop_loss']:.2f}")
        with col5:
            if st.button("Remove", key=f"del_{item['symbol']}"):
                remove_from_watchlist(item['symbol'])
                st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# ALERT SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════

def create_alert(asset_symbol: str, condition: str, target_value: float):
    alert = {
        'id': len(st.session_state.alerts) + 1,
        'symbol': asset_symbol,
        'condition': condition,
        'target_value': target_value,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'triggered': False
    }
    st.session_state.alerts.append(alert)


def check_alerts(current_data: Dict):
    triggered_alerts = []
    for alert in st.session_state.alerts:
        if alert['triggered']:
            continue

        if alert['symbol'] == current_data.get('symbol'):
            current_price = current_data.get('price', 0)

            if alert['condition'] == 'price_above' and current_price > alert['target_value']:
                alert['triggered'] = True
                triggered_alerts.append(alert)
            elif alert['condition'] == 'price_below' and current_price < alert['target_value']:
                alert['triggered'] = True
                triggered_alerts.append(alert)
            elif alert['condition'] == 'rsi_above' and current_data.get('rsi', 50) > alert['target_value']:
                alert['triggered'] = True
                triggered_alerts.append(alert)
            elif alert['condition'] == 'rsi_below' and current_data.get('rsi', 50) < alert['target_value']:
                alert['triggered'] = True
                triggered_alerts.append(alert)

    return triggered_alerts


def display_alerts():
    st.subheader("Alert Management")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Create New Alert**")
        alert_symbol = st.text_input("Asset Symbol", placeholder="e.g., BTC, RELIANCE")
        alert_condition = st.selectbox("Condition",
                                       ['price_above', 'price_below', 'rsi_above', 'rsi_below'])
        alert_value = st.number_input("Target Value", min_value=0.0, step=0.1)

        if st.button("Create Alert"):
            create_alert(alert_symbol, alert_condition, alert_value)
            st.success(f"Alert created for {alert_symbol}")

    with col2:
        st.write("**Active Alerts**")
        if st.session_state.alerts:
            for alert in st.session_state.alerts:
                status = "Triggered" if alert['triggered'] else "Active"
                st.write(f"{status} | {alert['symbol']} | {alert['condition']} {alert['target_value']}")
        else:
            st.info("No alerts created yet")


# ═══════════════════════════════════════════════════════════════════════════════
# PORTFOLIO TRACKER
# ═══════════════════════════════════════════════════════════════════════════════

def add_to_portfolio(asset: Dict, quantity: float, entry_price: float):
    position = {
        'id': len(st.session_state.portfolio) + 1,
        'symbol': asset['symbol'],
        'name': asset['name'],
        'asset_type': asset['asset_type'],
        'quantity': quantity,
        'entry_price': entry_price,
        'entry_date': datetime.now().strftime('%Y-%m-%d'),
        'current_price': asset.get('price', entry_price)
    }
    st.session_state.portfolio.append(position)


def calculate_portfolio_value():
    total_value = 0
    total_pnl = 0

    for position in st.session_state.portfolio:
        current_value = position['quantity'] * position['current_price']
        cost_basis = position['quantity'] * position['entry_price']
        pnl = current_value - cost_basis

        total_value += current_value
        total_pnl += pnl

    return total_value, total_pnl


def display_portfolio():
    st.subheader("Portfolio Tracker")

    if not st.session_state.portfolio:
        st.info("Your portfolio is empty. Add positions to track performance.")

        with st.expander("Add New Position"):
            col1, col2, col3 = st.columns(3)
            with col1:
                pos_symbol = st.text_input("Symbol")
            with col2:
                pos_quantity = st.number_input("Quantity", min_value=0.01, step=0.01)
            with col3:
                pos_entry = st.number_input("Entry Price", min_value=0.01, step=0.01)

            if st.button("Add Position"):
                add_to_portfolio(
                    {'symbol': pos_symbol, 'name': pos_symbol, 'asset_type': 'Manual', 'price': pos_entry},
                    pos_quantity, pos_entry
                )
                st.success("Position added")
                st.rerun()
        return

    total_value, total_pnl = calculate_portfolio_value()
    pnl_pct = (total_pnl / (total_value - total_pnl)) * 100 if total_value > 0 else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Value", f"${total_value:,.2f}")
    with col2:
        st.metric("Total P&L", f"${total_pnl:,.2f}", f"{pnl_pct:.2f}%")
    with col3:
        st.metric("Positions", len(st.session_state.portfolio))

    st.write("---")

    for position in st.session_state.portfolio:
        current_value = position['quantity'] * position['current_price']
        cost_basis = position['quantity'] * position['entry_price']
        pnl = current_value - cost_basis
        pnl_pct = (pnl / cost_basis) * 100 if cost_basis > 0 else 0

        col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])

        with col1:
            st.write(f"**{position['name']}** ({position['symbol']})")
        with col2:
            st.write(f"Qty: {position['quantity']}")
        with col3:
            st.write(f"Entry: ${position['entry_price']:.2f}")
        with col4:
            st.write(f"${pnl:.2f} ({pnl_pct:.1f}%)")
        with col5:
            if st.button("Close", key=f"close_{position['id']}"):
                st.session_state.portfolio = [p for p in st.session_state.portfolio if p['id'] != position['id']]
                st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# BACKTESTING ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

def run_backtest(ticker: str, strategy: str, period: str = "1y"):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)

        if hist.empty:
            return None

        initial_capital = 10000
        capital = initial_capital
        position = 0
        trades = []

        hist['RSI'] = pd.Series([calculate_rsi(hist['Close'][:i + 14]) for i in range(len(hist) - 13)],
                                index=hist.index[13:])
        hist['EMA_50'] = hist['Close'].ewm(span=50).mean()
        hist['EMA_200'] = hist['Close'].ewm(span=200).mean()

        for i in range(200, len(hist)):
            price = hist['Close'].iloc[i]
            rsi = hist['RSI'].iloc[i] if i >= 13 else 50
            ema50 = hist['EMA_50'].iloc[i]
            ema200 = hist['EMA_200'].iloc[i]

            if strategy == "RSI Oversold/Overbought":
                if position == 0 and rsi < 30:
                    shares = capital // price
                    if shares > 0:
                        position = shares
                        capital -= shares * price
                        trades.append({'date': hist.index[i], 'type': 'BUY', 'price': price, 'shares': shares})

                elif position > 0 and rsi > 70:
                    capital += position * price
                    trades.append({'date': hist.index[i], 'type': 'SELL', 'price': price, 'shares': position})
                    position = 0

            elif strategy == "EMA Crossover":
                if position == 0 and ema50 > ema200:
                    shares = capital // price
                    if shares > 0:
                        position = shares
                        capital -= shares * price
                        trades.append({'date': hist.index[i], 'type': 'BUY', 'price': price, 'shares': shares})

                elif position > 0 and ema50 < ema200:
                    capital += position * price
                    trades.append({'date': hist.index[i], 'type': 'SELL', 'price': price, 'shares': position})
                    position = 0

        final_value = capital + (position * hist['Close'].iloc[-1])
        total_return = ((final_value - initial_capital) / initial_capital) * 100

        win_trades = sum(
            1 for i in range(1, len(trades), 2) if i < len(trades) and trades[i]['price'] > trades[i - 1]['price'])
        total_trades = len(trades) // 2
        win_rate = (win_trades / total_trades * 100) if total_trades > 0 else 0

        return {
            'initial_capital': initial_capital,
            'final_value': final_value,
            'total_return': total_return,
            'total_trades': total_trades,
            'win_rate': win_rate,
            'trades': trades
        }
    except Exception as e:
        st.error(f"Backtest error: {str(e)}")
        return None


def display_backtesting():
    st.subheader("Strategy Backtesting")

    col1, col2, col3 = st.columns(3)

    with col1:
        backtest_ticker = st.text_input("Ticker Symbol", value="RELIANCE.NS")
    with col2:
        backtest_strategy = st.selectbox("Strategy",
                                         ["RSI Oversold/Overbought", "EMA Crossover"])
    with col3:
        backtest_period = st.selectbox("Period",
                                       ["6mo", "1y", "2y", "5y"])

    if st.button("Run Backtest"):
        with st.spinner("Running backtest..."):
            results = run_backtest(backtest_ticker, backtest_strategy, backtest_period)

            if results:
                st.success("Backtest Complete")

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Initial Capital", f"${results['initial_capital']:,.2f}")
                with col2:
                    st.metric("Final Value", f"${results['final_value']:,.2f}")
                with col3:
                    st.metric("Total Return", f"{results['total_return']:.2f}%")
                with col4:
                    st.metric("Win Rate", f"{results['win_rate']:.1f}%")

                st.write("**Trade History**")
                if results['trades']:
                    trades_df = pd.DataFrame(results['trades'])
                    st.dataframe(trades_df, use_container_width=True)
                else:
                    st.info("No trades executed in this period")


# ═══════════════════════════════════════════════════════════════════════════════
# CORRELATION ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

def calculate_correlation_matrix(tickers: List[str], period: str = "3mo"):
    data = {}

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            if not hist.empty:
                data[ticker] = hist['Close']
        except:
            continue

    if len(data) < 2:
        return None

    df = pd.DataFrame(data)
    correlation = df.corr()

    fig = go.Figure(data=go.Heatmap(
        z=correlation.values,
        x=correlation.columns,
        y=correlation.columns,
        colorscale=[[0, '#000000'], [0.5, '#333333'], [1, '#ffffff']],
        zmid=0,
        text=correlation.values.round(2),
        texttemplate='%{text}',
        textfont={"size": 10, "color": "#ffffff"},
        colorbar=dict(title="Correlation", tickfont=dict(color='#ffffff'))
    ))

    fig.update_layout(
        title="Asset Correlation Matrix",
        template='plotly_dark',
        paper_bgcolor='#000000',
        plot_bgcolor='#0a0a0a',
        font=dict(family='Inter, sans-serif', color='#ffffff'),
        height=500
    )

    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    st.title("ICT Professional Analyzer")
    st.markdown("**Complete Trading Suite: Analysis, Watchlist, Portfolio, Alerts, Backtesting**")

    kill_zone = get_kill_zone()

    if kill_zone['active']:
        st.markdown(f"""
        <div class="status-box">
            <h3>{kill_zone['name']} - ACTIVE</h3>
            <p>{kill_zone['description']} | Multiplier: {kill_zone['multiplier']}x | Priority: {kill_zone['priority']}/5</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="status-box">
            <h3>{kill_zone['name']}</h3>
            <p>{kill_zone['description']}</p>
        </div>
        """, unsafe_allow_html=True)

    # Sidebar Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select Page", [
        "Market Analysis",
        "Watchlist",
        "Portfolio Tracker",
        "Alerts",
        "Backtesting",
        "Correlation Matrix",
        "Settings"
    ])

    # PAGE: MARKET ANALYSIS
    if page == "Market Analysis":
        st.header("Real-Time Market Analysis")

        asset_type = st.selectbox(
            "Choose Asset Class",
            ["Indian Stocks (Nifty 50)", "Cryptocurrencies", "Forex Pairs"]
        )

        col1, col2 = st.columns(2)
        with col1:
            analyze_count = st.slider("Assets to Analyze", 5, 30, 10)
        with col2:
            show_ict_overlays = st.checkbox("Show ICT Overlays", value=True)

        if st.button("Start Analysis", use_container_width=True):

            if "Stocks" in asset_type:
                st.subheader("Nifty 50 Stock Analysis")
                assets_to_analyze = NIFTY_50[:analyze_count]

                progress_bar = st.progress(0)
                status_text = st.empty()

                results = []
                for i, ticker in enumerate(assets_to_analyze):
                    status_text.text(f"Analyzing {ticker}... ({i + 1}/{len(assets_to_analyze)})")
                    data = fetch_stock_data(ticker)
                    if data:
                        analysis = analyze_asset(data, 'Stock', kill_zone)
                        results.append(analysis)

                        triggered = check_alerts(analysis)
                        if triggered:
                            st.warning(f"Alert triggered for {ticker}")

                    progress_bar.progress((i + 1) / len(assets_to_analyze))
                    time.sleep(0.2)

                status_text.empty()
                progress_bar.empty()

                if results:
                    results_sorted = sorted(results, key=lambda x: x['combined_score'], reverse=True)

                    st.subheader("Top 10 Opportunities")

                    df = pd.DataFrame([{
                        'Symbol': r['symbol'],
                        'Name': r['name'][:25],
                        'Price': f"₹{r['price']:.2f}",
                        'Change': f"{r['price_change_24h']:.2f}%",
                        'Score': f"{r['combined_score']:.1f}",
                        'Signal': r['signal'],
                        'Risk': f"{r['risk']}/10",
                        'Confidence': f"{r['confidence']}%"
                    } for r in results_sorted[:10]])

                    st.dataframe(df, use_container_width=True, height=400)

                    st.subheader("Detailed Analysis - Top Pick")
                    top_pick = results_sorted[0]

                    col1, col2, col3, col4, col5 = st.columns(5)
                    with col1:
                        st.metric("Score", f"{top_pick['combined_score']:.1f}/100")
                    with col2:
                        st.metric("Technical", f"{top_pick['technical_score']:.1f}")
                    with col3:
                        st.metric("Fundamental", f"{top_pick['fundamental_score']:.1f}")
                    with col4:
                        st.metric("Risk", f"{top_pick['risk']}/10")
                    with col5:
                        st.metric("RSI", f"{top_pick['rsi']:.1f}")

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("Add to Watchlist"):
                            if add_to_watchlist(top_pick):
                                st.success("Added to watchlist")
                            else:
                                st.warning("Already in watchlist")
                    with col2:
                        if st.button("Add to Portfolio"):
                            st.info("Go to Portfolio page to add position")
                    with col3:
                        if st.button("Export Data"):
                            csv = pd.DataFrame([top_pick]).to_csv(index=False)
                            st.download_button("Download CSV", csv, "analysis.csv", "text/csv")

                    st.subheader(f"{top_pick['name']} ({top_pick['symbol']}) - Chart")
                    chart = create_advanced_chart(top_pick['symbol'] + '.NS', show_ict=show_ict_overlays)
                    if chart:
                        st.plotly_chart(chart, use_container_width=True)

                    st.subheader("ICT Concept Breakdown")
                    ict_df = pd.DataFrame(list(top_pick['ict_scores'].items()),
                                          columns=['ICT Concept', 'Score'])

                    fig = go.Figure(data=[
                        go.Bar(x=ict_df['ICT Concept'], y=ict_df['Score'],
                               marker_color='#ffffff',
                               text=ict_df['Score'],
                               textposition='auto')
                    ])
                    fig.update_layout(
                        template='plotly_dark',
                        paper_bgcolor='#000000',
                        plot_bgcolor='#0a0a0a',
                        font=dict(family='Inter, sans-serif', color='#ffffff'),
                        height=400,
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    st.subheader("Fundamental Metrics")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("P/E Ratio", f"{top_pick.get('pe_ratio', 0):.2f}")
                    with col2:
                        st.metric("ROE", f"{top_pick.get('roe', 0):.2f}%")
                    with col3:
                        st.metric("Debt/Equity", f"{top_pick.get('debt_to_equity', 0):.2f}")
                    with col4:
                        st.metric("Dividend Yield", f"{top_pick.get('dividend_yield', 0):.2f}%")

            elif "Crypto" in asset_type:
                st.subheader("Cryptocurrency Analysis")
                assets_to_analyze = TOP_CRYPTO[:analyze_count]

                progress_bar = st.progress(0)
                status_text = st.empty()

                results = []
                for i, coin in enumerate(assets_to_analyze):
                    status_text.text(f"Analyzing {coin}... ({i + 1}/{len(assets_to_analyze)})")
                    data = fetch_crypto_data(coin)
                    if data:
                        analysis = analyze_asset(data, 'Crypto', kill_zone)
                        results.append(analysis)
                    time.sleep(0.5)
                    progress_bar.progress((i + 1) / len(assets_to_analyze))

                status_text.empty()
                progress_bar.empty()

                if results:
                    results_sorted = sorted(results, key=lambda x: x['combined_score'], reverse=True)

                    st.subheader("Top 10 Crypto Opportunities")

                    df = pd.DataFrame([{
                        'Symbol': r['symbol'],
                        'Name': r['name'],
                        'Price': f"${r['price']:.2f}",
                        'Change 24h': f"{r['price_change_24h']:.2f}%",
                        'Market Cap': f"${r['market_cap'] / 1e9:.2f}B",
                        'Score': f"{r['combined_score']:.1f}",
                        'Signal': r['signal'],
                        'Risk': f"{r['risk']}/10"
                    } for r in results_sorted[:10]])

                    st.dataframe(df, use_container_width=True, height=400)

                    top_pick = results_sorted[0]

                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Score", f"{top_pick['combined_score']:.1f}/100")
                    with col2:
                        st.metric("Price", f"${top_pick['price']:.2f}")
                    with col3:
                        st.metric("24h Change", f"{top_pick['price_change_24h']:.2f}%")
                    with col4:
                        st.metric("Market Cap", f"${top_pick['market_cap'] / 1e9:.2f}B")

                    st.subheader("ICT Concept Scores")
                    ict_df = pd.DataFrame(list(top_pick['ict_scores'].items()),
                                          columns=['Concept', 'Score'])
                    st.bar_chart(ict_df.set_index('Concept'))

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Add to Watchlist", key="crypto_watch"):
                            if add_to_watchlist(top_pick):
                                st.success("Added")
                    with col2:
                        if st.button("Export", key="crypto_export"):
                            csv = pd.DataFrame(results_sorted).to_csv(index=False)
                            st.download_button("Download", csv, "crypto_analysis.csv", "text/csv")

            elif "Forex" in asset_type:
                st.subheader("Forex Pair Analysis")
                assets_to_analyze = FOREX_PAIRS[:analyze_count]

                progress_bar = st.progress(0)
                status_text = st.empty()

                results = []
                for i, pair in enumerate(assets_to_analyze):
                    status_text.text(f"Analyzing {pair}... ({i + 1}/{len(assets_to_analyze)})")
                    data = fetch_forex_data(pair)
                    if data:
                        analysis = analyze_asset(data, 'Forex', kill_zone)
                        results.append(analysis)
                    progress_bar.progress((i + 1) / len(assets_to_analyze))

                status_text.empty()
                progress_bar.empty()

                if results:
                    results_sorted = sorted(results, key=lambda x: x['combined_score'], reverse=True)

                    st.subheader("Top Forex Opportunities")

                    df = pd.DataFrame([{
                        'Pair': r['symbol'],
                        'Price': f"{r['price']:.4f}",
                        'Change 24h': f"{r['price_change_24h']:.2f}%",
                        'RSI': f"{r['rsi']:.1f}",
                        'Score': f"{r['combined_score']:.1f}",
                        'Signal': r['signal'],
                        'Trend': r['trend']
                    } for r in results_sorted[:10]])

                    st.dataframe(df, use_container_width=True, height=400)

                    top_pick = results_sorted[0]

                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Score", f"{top_pick['combined_score']:.1f}")
                    with col2:
                        st.metric("Price", f"{top_pick['price']:.4f}")
                    with col3:
                        st.metric("RSI", f"{top_pick['rsi']:.1f}")
                    with col4:
                        st.metric("Volatility", f"{top_pick.get('volatility', 0):.2f}%")

                    chart = create_advanced_chart(top_pick['name'], show_ict=show_ict_overlays)
                    if chart:
                        st.plotly_chart(chart, use_container_width=True)

    # PAGE: WATCHLIST
    elif page == "Watchlist":
        display_watchlist()

    # PAGE: PORTFOLIO
    elif page == "Portfolio Tracker":
        display_portfolio()

    # PAGE: ALERTS
    elif page == "Alerts":
        display_alerts()

    # PAGE: BACKTESTING
    elif page == "Backtesting":
        display_backtesting()

    # PAGE: CORRELATION
    elif page == "Correlation Matrix":
        st.subheader("Asset Correlation Analysis")

        st.write("**Select Assets to Compare**")

        col1, col2 = st.columns(2)
        with col1:
            correlation_type = st.radio("Asset Type", ["Stocks", "Crypto", "Forex"])
        with col2:
            num_assets = st.slider("Number of Assets", 3, 10, 5)

        if correlation_type == "Stocks":
            selected_assets = st.multiselect("Select Stocks", NIFTY_50, default=NIFTY_50[:num_assets])
        elif correlation_type == "Crypto":
            crypto_tickers = [f"{c.upper()}-USD" for c in TOP_CRYPTO[:10]]
            selected_assets = st.multiselect("Select Cryptos", crypto_tickers, default=crypto_tickers[:num_assets])
        else:
            selected_assets = st.multiselect("Select Forex Pairs", FOREX_PAIRS, default=FOREX_PAIRS[:num_assets])

        if st.button("Calculate Correlation") and len(selected_assets) >= 2:
            with st.spinner("Calculating correlation..."):
                fig = calculate_correlation_matrix(selected_assets)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)

                    st.info("""
                    **Interpretation:**
                    - **+1.0**: Perfect positive correlation (move together)
                    - **0.0**: No correlation (independent)
                    - **-1.0**: Perfect negative correlation (move opposite)
                    """)
                else:
                    st.error("Unable to calculate correlation. Check asset symbols.")

    # PAGE: SETTINGS
    elif page == "Settings":
        st.subheader("User Settings & Preferences")

        st.write("**Trading Preferences**")

        col1, col2 = st.columns(2)

        with col1:
            theme = st.selectbox("Theme", ["Dark Professional", "Light", "Custom"],
                                 index=0)

            default_tf = st.selectbox("Default Timeframe", list(TIMEFRAMES.keys()),
                                      index=5)
            st.session_state.preferences['default_timeframe'] = TIMEFRAMES[default_tf]

        with col2:
            risk_tolerance = st.select_slider("Risk Tolerance",
                                              options=['Very Low', 'Low', 'Medium', 'High', 'Very High'],
                                              value='Medium')
            st.session_state.preferences['risk_tolerance'] = risk_tolerance.lower()

            notification_email = st.text_input("Email for Alerts",
                                               value=st.session_state.preferences['notification_email'],
                                               placeholder="your@email.com")
            st.session_state.preferences['notification_email'] = notification_email

        st.write("---")
        st.write("**Display Options**")

        col1, col2, col3 = st.columns(3)
        with col1:
            show_ict = st.checkbox("Show ICT Overlays by Default", value=True)
        with col2:
            auto_refresh = st.checkbox("Auto-refresh Data", value=False)
        with col3:
            show_tooltips = st.checkbox("Show Tooltips", value=True)

        st.write("---")
        st.write("**Data Management**")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Export All Data"):
                export_data = {
                    'watchlist': st.session_state.watchlist,
                    'portfolio': st.session_state.portfolio,
                    'alerts': st.session_state.alerts,
                    'preferences': st.session_state.preferences
                }
                json_str = json.dumps(export_data, indent=2)
                st.download_button("Download JSON", json_str, "ict_data.json", "application/json")

        with col2:
            if st.button("Clear Watchlist"):
                st.session_state.watchlist = []
                st.success("Watchlist cleared")
                st.rerun()

        with col3:
            if st.button("Reset All Settings"):
                st.session_state.preferences = {
                    'theme': 'dark',
                    'default_timeframe': '1d',
                    'risk_tolerance': 'medium',
                    'notification_email': ''
                }
                st.success("Settings reset")
                st.rerun()

        st.write("---")
        st.write("**System Information**")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Watchlist Items", len(st.session_state.watchlist))
        with col2:
            st.metric("Portfolio Positions", len(st.session_state.portfolio))
        with col3:
            st.metric("Active Alerts", len([a for a in st.session_state.alerts if not a['triggered']]))
        with col4:
            st.metric("Total Trades", len(st.session_state.trade_history))

    # Sidebar Footer
    st.sidebar.markdown("---")
    st.sidebar.subheader("Quick Guide")
    with st.sidebar.expander("ICT Concepts"):
        st.markdown("""
        **Market Structure**: Swing highs and lows pattern

        **Order Blocks**: Last opposite candle before strong move

        **Fair Value Gaps**: Price imbalances (gaps in chart)

        **Liquidity Pools**: Stop loss accumulation zones

        **Breaker Blocks**: Failed order blocks that reverse

        **Optimal Trade Entry**: 0.62-0.79 Fibonacci zone

        **Kill Zones**: High-probability trading sessions

        **Power of 3**: Accumulation → Manipulation → Distribution
        """)

    with st.sidebar.expander("Features"):
        st.markdown("""
        - Real-time Analysis: Live market data
        - Watchlist: Track favorite assets
        - Portfolio: Monitor positions & P&L
        - Alerts: Price & indicator notifications
        - Backtesting: Test strategies historically
        - ICT Overlays: Order blocks, FVGs, S/R
        - Correlation: Multi-asset relationships
        - Multi-timeframe: 1m to Monthly charts
        - Export: CSV/JSON data export
        - Risk Management: Position sizing tools
        """)

    st.sidebar.markdown("---")
    st.sidebar.info(f"""
    **Data Sources**: yfinance, CoinGecko

    **Cache**: 5 minutes

    **Last Updated**: {datetime.now().strftime("%H:%M:%S")}

    **Kill Zone**: {kill_zone['name']}
    """)

    st.sidebar.markdown("---")
    st.sidebar.success("**ICT Analyzer Pro** - Professional Edition")


if __name__ == "__main__":
    main()
