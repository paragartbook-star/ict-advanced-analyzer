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
# ICT ADVANCED MULTI-ASSET ANALYZER - PROFESSIONAL UI REDESIGN
# Clean, Minimal, Professional Design with Premium Feel
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="ICT Pro Analyzer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Custom CSS - Clean & Minimal Design
st.markdown("""
<style>
    /* Base Theme - Professional Dark Theme */
    .stApp {
        background-color: #0F1116;
        color: #E0E0E0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    }
    
    /* Sidebar - Subtle Gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1A1D29 0%, #141721 100%);
        border-right: 1px solid #2A2D3A;
    }
    
    /* Metrics Cards - Clean Design */
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"], [data-testid="stMetricDelta"] {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Headers - Professional Typography */
    h1 {
        color: #FFFFFF !important;
        font-weight: 600;
        font-size: 32px;
        letter-spacing: -0.5px;
        margin-bottom: 8px;
    }
    
    h2 {
        color: #FFFFFF !important;
        font-weight: 600;
        font-size: 24px;
        letter-spacing: -0.3px;
        margin-top: 24px;
        margin-bottom: 16px;
    }
    
    h3 {
        color: #A0A0A0 !important;
        font-weight: 500;
        font-size: 18px;
        letter-spacing: -0.2px;
        margin-top: 20px;
        margin-bottom: 12px;
    }
    
    /* DataFrames - Clean Tables */
    .dataframe {
        background-color: #1A1D29 !important;
        color: #E0E0E0 !important;
        border: 1px solid #2A2D3A;
        border-radius: 8px;
        overflow: hidden;
    }
    
    .dataframe thead {
        background-color: #252836 !important;
    }
    
    .dataframe thead tr th {
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 12px 16px !important;
        border-bottom: 2px solid #3A3D4A;
    }
    
    .dataframe tbody tr td {
        color: #E0E0E0 !important;
        padding: 12px 16px !important;
        border-bottom: 1px solid #2A2D3A;
        font-size: 14px;
    }
    
    .dataframe tbody tr:hover {
        background-color: #252836 !important;
    }
    
    /* Buttons - Clean & Consistent */
    .stButton>button {
        background-color: #2563EB !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 10px 20px !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        letter-spacing: 0.3px;
        transition: all 0.2s ease !important;
        height: 40px !important;
        min-width: 100px !important;
    }
    
    .stButton>button:hover {
        background-color: #1D4ED8 !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    /* Primary Button */
    .primary-button {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
    }
    
    /* Secondary Button */
    .secondary-button {
        background-color: #3A3D4A !important;
        color: #E0E0E0 !important;
    }
    
    /* Success Button */
    .success-button {
        background-color: #059669 !important;
    }
    
    /* Danger Button */
    .danger-button {
        background-color: #DC2626 !important;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input, 
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>div {
        background-color: #1A1D29 !important;
        border: 1px solid #3A3D4A !important;
        color: #FFFFFF !important;
        border-radius: 6px !important;
        padding: 8px 12px !important;
        font-size: 14px !important;
    }
    
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1) !important;
    }
    
    /* Selectbox */
    .stSelectbox>div>div {
        background-color: #1A1D29 !important;
    }
    
    /* Checkbox & Radio */
    .stCheckbox, .stRadio {
        color: #E0E0E0 !important;
    }
    
    /* Slider */
    .stSlider>div>div>div {
        background-color: #2563EB !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #1A1D29 !important;
        color: #A0A0A0 !important;
        border-radius: 6px !important;
        padding: 8px 16px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        border: 1px solid #2A2D3A !important;
        transition: all 0.2s ease !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border-color: #2563EB !important;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background-color: #2A2D3A;
        margin: 24px 0;
    }
    
    /* Cards & Containers */
    .card {
        background-color: #1A1D29;
        border: 1px solid #2A2D3A;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
    }
    
    .metric-card {
        background-color: #1A1D29;
        border: 1px solid #2A2D3A;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    
    .metric-card .value {
        font-size: 32px;
        font-weight: 600;
        color: #FFFFFF;
        margin: 8px 0;
    }
    
    .metric-card .label {
        font-size: 14px;
        color: #A0A0A0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Status Indicators */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
        letter-spacing: 0.3px;
    }
    
    .status-active {
        background-color: rgba(5, 150, 105, 0.15);
        color: #10B981;
        border: 1px solid rgba(5, 150, 105, 0.3);
    }
    
    .status-inactive {
        background-color: rgba(107, 114, 128, 0.15);
        color: #9CA3AF;
        border: 1px solid rgba(107, 114, 128, 0.3);
    }
    
    .status-warning {
        background-color: rgba(245, 158, 11, 0.15);
        color: #F59E0B;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    
    /* Trading Colors */
    .positive {
        color: #10B981 !important;
    }
    
    .negative {
        color: #EF4444 !important;
    }
    
    .neutral {
        color: #9CA3AF !important;
    }
    
    /* Spacing Utilities */
    .mt-1 { margin-top: 4px; }
    .mt-2 { margin-top: 8px; }
    .mt-3 { margin-top: 12px; }
    .mt-4 { margin-top: 16px; }
    .mt-6 { margin-top: 24px; }
    
    .mb-1 { margin-bottom: 4px; }
    .mb-2 { margin-bottom: 8px; }
    .mb-3 { margin-bottom: 12px; }
    .mb-4 { margin-bottom: 16px; }
    .mb-6 { margin-bottom: 24px; }
    
    /* Loading Spinner */
    .stSpinner>div {
        border-color: #2563EB transparent transparent transparent !important;
    }
    
    /* Tooltips */
    [data-testid="stTooltip"] {
        background-color: #1A1D29 !important;
        border: 1px solid #2A2D3A !important;
        color: #E0E0E0 !important;
        border-radius: 6px !important;
        font-size: 13px !important;
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1A1D29;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #3A3D4A;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #4B4F5E;
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
# DATA CONFIGURATIONS (Unchanged from original)
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
    'USDCHF=X', 'NZUSD=X', 'EURJPY=X', 'GBPJPY=X', 'USDINR=X',
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
# KILL ZONE DETECTION (Unchanged)
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
            'color': '#10B981',
            'description': 'Indian market hours - High volume'
        }
    elif (ist_hour == 12 and ist_min >= 30) or (ist_hour >= 13 and ist_hour < 15) or (ist_hour == 15 and ist_min < 30):
        return {
            'name': 'London Kill Zone',
            'multiplier': 1.8,
            'priority': 5,
            'active': True,
            'color': '#3B82F6',
            'description': 'London session - High liquidity'
        }
    elif (ist_hour == 17 and ist_min >= 30) or (ist_hour >= 18 and ist_hour < 20) or (ist_hour == 20 and ist_min < 30):
        return {
            'name': 'NY Kill Zone',
            'multiplier': 1.9,
            'priority': 5,
            'active': True,
            'color': '#8B5CF6',
            'description': 'New York session - Major moves'
        }
    elif (ist_hour == 6 and ist_min >= 30) or (ist_hour >= 7 and ist_hour < 9) or (ist_hour == 9 and ist_min < 30):
        return {
            'name': 'Asian Session',
            'multiplier': 1.2,
            'priority': 3,
            'active': True,
            'color': '#F59E0B',
            'description': 'Asian hours - Range trading'
        }
    else:
        return {
            'name': 'Off Hours',
            'multiplier': 0.5,
            'priority': 1,
            'active': False,
            'color': '#6B7280',
            'description': 'Low activity period'
        }

# ═══════════════════════════════════════════════════════════════════════════════
# DATA FETCHING FUNCTIONS (Unchanged from original)
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
# TECHNICAL INDICATORS (Unchanged)
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
    order_blocks = []
    
    for i in range(2, len(hist_data) - 1):
        prev_close = hist_data['Close'].iloc[i-1]
        prev_open = hist_data['Open'].iloc[i-1]
        curr_close = hist_data['Close'].iloc[i]
        curr_open = hist_data['Open'].iloc[i]
        next_close = hist_data['Close'].iloc[i+1]
        
        if prev_close < prev_open and curr_close > curr_open and next_close > curr_close:
            order_blocks.append({
                'type': 'bullish',
                'index': i-1,
                'high': hist_data['High'].iloc[i-1],
                'low': hist_data['Low'].iloc[i-1],
                'date': hist_data.index[i-1]
            })
        
        elif prev_close > prev_open and curr_close < curr_open and next_close < curr_close:
            order_blocks.append({
                'type': 'bearish',
                'index': i-1,
                'high': hist_data['High'].iloc[i-1],
                'low': hist_data['Low'].iloc[i-1],
                'date': hist_data.index[i-1]
            })
    
    return order_blocks[-5:] if len(order_blocks) > 5 else order_blocks

def detect_fair_value_gaps(hist_data: pd.DataFrame) -> List[Dict]:
    fvgs = []
    
    for i in range(1, len(hist_data) - 1):
        prev_high = hist_data['High'].iloc[i-1]
        prev_low = hist_data['Low'].iloc[i-1]
        next_high = hist_data['High'].iloc[i+1]
        next_low = hist_data['Low'].iloc[i+1]
        
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
    highs = hist_data['High']
    lows = hist_data['Low']
    
    resistance_levels = []
    support_levels = []
    
    for i in range(2, len(highs) - 2):
        if highs.iloc[i] > highs.iloc[i-1] and highs.iloc[i] > highs.iloc[i-2] and \
           highs.iloc[i] > highs.iloc[i+1] and highs.iloc[i] > highs.iloc[i+2]:
            resistance_levels.append(highs.iloc[i])
    
    for i in range(2, len(lows) - 2):
        if lows.iloc[i] < lows.iloc[i-1] and lows.iloc[i] < lows.iloc[i-2] and \
           lows.iloc[i] < lows.iloc[i+1] and lows.iloc[i] < lows.iloc[i+2]:
            support_levels.append(lows.iloc[i])
    
    return {
        'resistance': sorted(set(resistance_levels), reverse=True)[:3],
        'support': sorted(set(support_levels))[:3]
    }

# ═══════════════════════════════════════════════════════════════════════════════
# ICT ANALYSIS ENGINE (Unchanged)
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
# ADVANCED CHARTING (Unchanged)
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
            vertical_spacing=0.03,
            subplot_titles=('Price Action with ICT Concepts', 'Volume', 'RSI'),
            row_heights=[0.6, 0.2, 0.2]
        )
        
        fig.add_trace(
            go.Candlestick(
                x=hist.index,
                open=hist['Open'],
                high=hist['High'],
                low=hist['Low'],
                close=hist['Close'],
                name='Price',
                increasing_line_color='#10B981',
                decreasing_line_color='#EF4444'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=hist.index, y=hist['EMA_50'], mode='lines',
                      name='EMA 50', line=dict(color='#3B82F6', width=1.5)),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=hist.index, y=hist['EMA_200'], mode='lines',
                      name='EMA 200', line=dict(color='#F59E0B', width=1.5)),
            row=1, col=1
        )
        
        if show_ict and len(hist) > 10:
            order_blocks = detect_order_blocks(hist)
            for ob in order_blocks:
                color = 'rgba(16, 185, 129, 0.3)' if ob['type'] == 'bullish' else 'rgba(239, 68, 68, 0.3)'
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
                color = 'rgba(59, 130, 246, 0.2)' if fvg['type'] == 'bullish' else 'rgba(245, 158, 11, 0.2)'
                fig.add_shape(
                    type="rect",
                    x0=fvg['date'], x1=hist.index[-1],
                    y0=fvg['bottom'], y1=fvg['top'],
                    fillcolor=color,
                    line=dict(color=color.replace('0.2', '0.8'), width=1, dash='dot'),
                    row=1, col=1
                )
            
            sr_levels = calculate_support_resistance(hist)
            for level in sr_levels['resistance']:
                fig.add_hline(y=level, line_dash="dash", line_color="#EF4444", 
                             line_width=1, opacity=0.5, row=1, col=1)
            for level in sr_levels['support']:
                fig.add_hline(y=level, line_dash="dash", line_color="#10B981", 
                             line_width=1, opacity=0.5, row=1, col=1)
        
        colors = ['#10B981' if hist['Close'].iloc[i] >= hist['Open'].iloc[i] else '#EF4444' 
                  for i in range(len(hist))]
        fig.add_trace(
            go.Bar(x=hist.index, y=hist['Volume'], name='Volume', marker_color=colors),
            row=2, col=1
        )
        
        rsi_values = [calculate_rsi(hist['Close'][:i+14]) for i in range(len(hist)-13)]
        rsi_dates = hist.index[13:]
        fig.add_trace(
            go.Scatter(x=rsi_dates, y=rsi_values, mode='lines',
                      name='RSI', line=dict(color='#8B5CF6', width=2)),
            row=3, col=1
        )
        fig.add_hline(y=70, line_dash="dash", line_color="#EF4444", line_width=1, row=3, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="#10B981", line_width=1, row=3, col=1)
        
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='#1A1D29',
            height=700,
            showlegend=True,
            xaxis_rangeslider_visible=False,
            hovermode='x unified',
            font=dict(color='#E0E0E0'),
            margin=dict(t=40, b=40, l=40, r=40)
        )
        
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#2A2D3A')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#2A2D3A')
        
        return fig
    except Exception as e:
        st.error(f"Chart error: {str(e)}")
        return None

# ═══════════════════════════════════════════════════════════════════════════════
# WATCHLIST MANAGEMENT (Updated UI)
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
    st.header("Watchlist")
    
    if not st.session_state.watchlist:
        st.info("Your watchlist is empty. Add assets from the Market Analysis page.")
        return
    
    with st.container():
        for item in st.session_state.watchlist:
            col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])
            
            with col1:
                st.markdown(f"**{item['name']}**")
                st.caption(f"{item['symbol']} • {item['asset_type']}")
            
            with col2:
                st.markdown("**Target**")
                st.markdown(f"${item['target_price']:,.2f}")
            
            with col3:
                st.markdown("**Stop Loss**")
                st.markdown(f"${item['stop_loss']:,.2f}")
            
            with col4:
                st.markdown("**Added**")
                st.caption(item['added_date'])
            
            with col5:
                if st.button("Remove", key=f"del_{item['symbol']}", type="secondary"):
                    remove_from_watchlist(item['symbol'])
                    st.rerun()
            
            st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# ALERT SYSTEM (Updated UI)
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
    st.header("Alert Management")
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.subheader("Create New Alert")
        
        with st.container():
            alert_symbol = st.text_input("Asset Symbol", placeholder="e.g., BTC, RELIANCE")
            
            col_a, col_b = st.columns(2)
            with col_a:
                alert_condition = st.selectbox("Condition", 
                    ['price_above', 'price_below', 'rsi_above', 'rsi_below'])
            with col_b:
                alert_value = st.number_input("Target Value", min_value=0.0, step=0.1)
            
            if st.button("Create Alert", type="primary", use_container_width=True):
                if alert_symbol:
                    create_alert(alert_symbol, alert_condition, alert_value)
                    st.success("Alert created successfully!")
                    st.rerun()
                else:
                    st.error("Please enter an asset symbol")
    
    with col2:
        st.subheader("Active Alerts")
        
        if st.session_state.alerts:
            for alert in st.session_state.alerts:
                status = "🔴 Triggered" if alert['triggered'] else "🟢 Active"
                col_x, col_y, col_z = st.columns([1, 2, 1])
                
                with col_x:
                    st.markdown(f"`{status[:3]}`")
                with col_y:
                    st.markdown(f"**{alert['symbol']}**")
                    st.caption(f"{alert['condition']} {alert['target_value']}")
                with col_z:
                    st.caption(alert['created_at'])
                
                st.divider()
        else:
            st.info("No alerts created yet")

# ═══════════════════════════════════════════════════════════════════════════════
# PORTFOLIO TRACKER (Updated UI)
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
    st.header("Portfolio Tracker")
    
    if not st.session_state.portfolio:
        st.info("Your portfolio is empty. Add positions to track performance.")
        
        with st.expander("Add New Position", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                pos_symbol = st.text_input("Symbol", placeholder="e.g., RELIANCE")
            with col2:
                pos_quantity = st.number_input("Quantity", min_value=0.01, step=0.01, value=1.0)
            with col3:
                pos_entry = st.number_input("Entry Price", min_value=0.01, step=0.01, value=100.0)
            
            if st.button("Add Position", type="primary", use_container_width=True):
                if pos_symbol:
                    add_to_portfolio(
                        {'symbol': pos_symbol, 'name': pos_symbol, 'asset_type': 'Manual', 'price': pos_entry},
                        pos_quantity, pos_entry
                    )
                    st.success("Position added successfully!")
                    st.rerun()
                else:
                    st.error("Please enter a symbol")
        return
    
    total_value, total_pnl = calculate_portfolio_value()
    pnl_pct = (total_pnl / (total_value - total_pnl)) * 100 if total_value > 0 else 0
    
    # Portfolio Summary
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Value", f"${total_value:,.2f}")
    with col2:
        st.metric("Total P&L", f"${total_pnl:,.2f}", f"{pnl_pct:+.2f}%")
    with col3:
        st.metric("Positions", len(st.session_state.portfolio))
    with col4:
        avg_return = pnl_pct / len(st.session_state.portfolio) if st.session_state.portfolio else 0
        st.metric("Avg. Return", f"{avg_return:+.2f}%")
    
    st.divider()
    
    # Positions Table
    st.subheader("Positions")
    
    positions_data = []
    for position in st.session_state.portfolio:
        current_value = position['quantity'] * position['current_price']
        cost_basis = position['quantity'] * position['entry_price']
        pnl = current_value - cost_basis
        pnl_pct = (pnl / cost_basis) * 100 if cost_basis > 0 else 0
        
        positions_data.append({
            'Symbol': position['symbol'],
            'Name': position['name'],
            'Quantity': position['quantity'],
            'Entry': f"${position['entry_price']:.2f}",
            'Current': f"${position['current_price']:.2f}",
            'P&L': f"${pnl:,.2f}",
            'P&L %': f"{pnl_pct:+.2f}%"
        })
    
    df = pd.DataFrame(positions_data)
    st.dataframe(df, use_container_width=True, height=300)
    
    # Close Position
    st.subheader("Close Position")
    position_ids = [p['id'] for p in st.session_state.portfolio]
    if position_ids:
        close_id = st.selectbox("Select Position to Close", position_ids, 
                               format_func=lambda x: f"{next(p['symbol'] for p in st.session_state.portfolio if p['id'] == x)} - ID: {x}")
        
        if st.button("Close Position", type="secondary"):
            st.session_state.portfolio = [p for p in st.session_state.portfolio if p['id'] != close_id]
            st.success("Position closed successfully!")
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# BACKTESTING ENGINE (Updated UI)
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
        
        hist['RSI'] = pd.Series([calculate_rsi(hist['Close'][:i+14]) for i in range(len(hist)-13)], 
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
        
        win_trades = sum(1 for i in range(1, len(trades), 2) if i < len(trades) and trades[i]['price'] > trades[i-1]['price'])
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
    st.header("Strategy Backtesting")
    
    with st.container():
        col1, col2, col3 = st.columns(3)
        
        with col1:
            backtest_ticker = st.text_input("Ticker Symbol", value="RELIANCE.NS", key="backtest_ticker")
        with col2:
            backtest_strategy = st.selectbox("Strategy", 
                ["RSI Oversold/Overbought", "EMA Crossover"], key="backtest_strategy")
        with col3:
            backtest_period = st.selectbox("Period", 
                ["6mo", "1y", "2y", "5y"], key="backtest_period")
    
    if st.button("Run Backtest", type="primary", use_container_width=True):
        with st.spinner("Running backtest..."):
            results = run_backtest(backtest_ticker, backtest_strategy, backtest_period)
            
            if results:
                st.success("Backtest Complete!")
                
                # Results Metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Initial Capital", f"${results['initial_capital']:,.2f}")
                with col2:
                    st.metric("Final Value", f"${results['final_value']:,.2f}")
                with col3:
                    st.metric("Total Return", f"{results['total_return']:.2f}%")
                with col4:
                    st.metric("Win Rate", f"{results['win_rate']:.1f}%")
                
                st.divider()
                
                # Trade History
                st.subheader("Trade History")
                if results['trades']:
                    trades_df = pd.DataFrame(results['trades'])
                    st.dataframe(trades_df, use_container_width=True, height=300)
                else:
                    st.info("No trades executed in this period")

# ═══════════════════════════════════════════════════════════════════════════════
# CORRELATION ANALYSIS (Updated UI)
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
        colorscale='RdBu',
        zmid=0,
        text=correlation.values.round(2),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Correlation")
    ))
    
    fig.update_layout(
        title="Asset Correlation Matrix",
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#1A1D29',
        height=500,
        font=dict(color='#E0E0E0')
    )
    
    return fig

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION WITH CLEAN UI
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    # Header with Logo and Title
    col_logo, col_title = st.columns([1, 10])
    with col_logo:
        st.markdown("<h1 style='text-align: center;'>📈</h1>", unsafe_allow_html=True)
    with col_title:
        st.title("ICT Advanced Multi-Asset Analyzer")
        st.caption("Professional Trading Suite • Real-time Analysis • Portfolio Management")
    
    kill_zone = get_kill_zone()
    
    # Kill Zone Status
    if kill_zone['active']:
        st.success(f"**{kill_zone['name']}** • {kill_zone['description']} • Multiplier: {kill_zone['multiplier']}x")
    else:
        st.info(f"**{kill_zone['name']}** • {kill_zone['description']}")
    
    st.divider()
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("### Navigation")
        page = st.radio(
            "",
            [
                "📊 Market Analysis",
                "👁️ Watchlist",
                "💼 Portfolio",
                "🔔 Alerts",
                "⏮️ Backtesting",
                "📈 Correlation",
                "⚙️ Settings"
            ],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        # Quick Stats
        st.markdown("### Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Watchlist", len(st.session_state.watchlist))
        with col2:
            st.metric("Portfolio", len(st.session_state.portfolio))
        
        st.divider()
        
        # System Info
        st.markdown("### System")
        st.caption(f"Last Updated: {datetime.now().strftime('%H:%M:%S')}")
        st.caption(f"Kill Zone: {kill_zone['name']}")
        
        with st.expander("ICT Concepts"):
            st.markdown("""
            - **Market Structure**: Swing highs and lows
            - **Order Blocks**: Last opposite candle before strong move
            - **Fair Value Gaps**: Price imbalances
            - **Liquidity Pools**: Stop loss zones
            """)
    
    # Page Routing
    if page == "📊 Market Analysis":
        display_market_analysis(kill_zone)
    elif page == "👁️ Watchlist":
        display_watchlist()
    elif page == "💼 Portfolio":
        display_portfolio()
    elif page == "🔔 Alerts":
        display_alerts()
    elif page == "⏮️ Backtesting":
        display_backtesting()
    elif page == "📈 Correlation":
        display_correlation_analysis()
    elif page == "⚙️ Settings":
        display_settings()

def display_market_analysis(kill_zone):
    st.header("Market Analysis")
    
    # Asset Class Selection
    asset_type = st.selectbox(
        "Asset Class",
        ["📈 Indian Stocks (Nifty 50)", "₿ Cryptocurrencies", "💱 Forex Pairs"],
        key="asset_class"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        analyze_count = st.slider("Assets to Analyze", 5, 30, 10, key="analyze_count")
    with col2:
        show_ict_overlays = st.checkbox("Show ICT Overlays", value=True, key="show_ict")
    
    if st.button("Start Analysis", type="primary", use_container_width=True):
        if "Stocks" in asset_type:
            analyze_stocks(kill_zone, analyze_count, show_ict_overlays)
        elif "Crypto" in asset_type:
            analyze_crypto(kill_zone, analyze_count, show_ict_overlays)
        elif "Forex" in asset_type:
            analyze_forex(kill_zone, analyze_count, show_ict_overlays)

def analyze_stocks(kill_zone, count, show_ict):
    st.subheader("Nifty 50 Stock Analysis")
    assets_to_analyze = NIFTY_50[:count]
    
    with st.spinner(f"Analyzing {count} stocks..."):
        results = []
        progress_bar = st.progress(0)
        
        for i, ticker in enumerate(assets_to_analyze):
            data = fetch_stock_data(ticker)
            if data:
                analysis = analyze_asset(data, 'Stock', kill_zone)
                results.append(analysis)
            progress_bar.progress((i + 1) / len(assets_to_analyze))
            time.sleep(0.1)
        
        progress_bar.empty()
        
        if results:
            results_sorted = sorted(results, key=lambda x: x['combined_score'], reverse=True)
            display_stock_results(results_sorted, show_ict)

def display_stock_results(results, show_ict):
    # Top Opportunities Table
    st.subheader("Top Opportunities")
    
    display_data = []
    for r in results[:10]:
        change_color = "positive" if r['price_change_24h'] >= 0 else "negative"
        display_data.append({
            'Rank': f"#{results.index(r)+1}",
            'Symbol': r['symbol'],
            'Name': r['name'][:20] + ('...' if len(r['name']) > 20 else ''),
            'Price': f"₹{r['price']:.2f}",
            'Change': f"<span class='{change_color}'>{r['price_change_24h']:+.2f}%</span>",
            'Score': f"{r['combined_score']:.1f}",
            'Signal': r['signal'],
            'Risk': f"{r['risk']}/10"
        })
    
    df = pd.DataFrame(display_data)
    st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)
    
    st.divider()
    
    # Top Pick Analysis
    if results:
        top_pick = results[0]
        st.subheader(f"Detailed Analysis: {top_pick['name']} ({top_pick['symbol']})")
        
        # Key Metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Score", f"{top_pick['combined_score']:.1f}/100")
        with col2:
            st.metric("Technical", f"{top_pick['technical_score']:.1f}")
        with col3:
            st.metric("Fundamental", f"{top_pick['fundamental_score']:.1f}")
        with col4:
            risk_color = "green" if top_pick['risk'] <= 3 else "orange" if top_pick['risk'] <= 6 else "red"
            st.metric("Risk", f"{top_pick['risk']}/10", delta_color="off")
        with col5:
            st.metric("RSI", f"{top_pick['rsi']:.1f}")
        
        # Action Buttons
        col_a, col_b, col_c, col_d = st.columns(4)
        with col_a:
            if st.button("Add to Watchlist", key="add_watchlist"):
                if add_to_watchlist(top_pick):
                    st.success("Added to watchlist!")
                else:
                    st.warning("Already in watchlist")
        with col_b:
            if st.button("View Chart", key="view_chart"):
                st.session_state.show_chart = True
        with col_c:
            if st.button("Create Alert", key="create_alert"):
                st.session_state.create_alert = True
        with col_d:
            csv = pd.DataFrame([top_pick]).to_csv(index=False)
            st.download_button("Export CSV", csv, "analysis.csv", "text/csv")
        
        # Chart Display
        if st.session_state.get('show_chart', False):
            st.divider()
            st.subheader("Advanced Chart")
            chart = create_advanced_chart(top_pick['symbol'] + '.NS', show_ict=show_ict)
            if chart:
                st.plotly_chart(chart, use_container_width=True)
        
        # ICT Scores Visualization
        st.divider()
        st.subheader("ICT Concept Scores")
        
        ict_df = pd.DataFrame(list(top_pick['ict_scores'].items()), 
                             columns=['Concept', 'Score'])
        
        fig = go.Figure(data=[
            go.Bar(x=ict_df['Concept'], y=ict_df['Score'],
                  marker_color='#2563EB',
                  text=ict_df['Score'],
                  textposition='auto')
        ])
        
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='#1A1D29',
            height=400,
            showlegend=False,
            font=dict(color='#E0E0E0'),
            margin=dict(t=20, b=20, l=20, r=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)

def analyze_crypto(kill_zone, count, show_ict):
    st.subheader("Cryptocurrency Analysis")
    assets_to_analyze = TOP_CRYPTO[:count]
    
    with st.spinner(f"Analyzing {count} cryptocurrencies..."):
        results = []
        progress_bar = st.progress(0)
        
        for i, coin in enumerate(assets_to_analyze):
            data = fetch_crypto_data(coin)
            if data:
                analysis = analyze_asset(data, 'Crypto', kill_zone)
                results.append(analysis)
            progress_bar.progress((i + 1) / len(assets_to_analyze))
            time.sleep(0.5)
        
        progress_bar.empty()
        
        if results:
            results_sorted = sorted(results, key=lambda x: x['combined_score'], reverse=True)
            display_crypto_results(results_sorted)

def display_crypto_results(results):
    st.subheader("Top Crypto Opportunities")
    
    display_data = []
    for r in results[:10]:
        change_color = "positive" if r['price_change_24h'] >= 0 else "negative"
        display_data.append({
            'Rank': f"#{results.index(r)+1}",
            'Symbol': r['symbol'],
            'Name': r['name'],
            'Price': f"${r['price']:.2f}",
            '24h Change': f"<span class='{change_color}'>{r['price_change_24h']:+.2f}%</span>",
            'Score': f"{r['combined_score']:.1f}",
            'Signal': r['signal'],
            'Market Cap': f"${r['market_cap']/1e9:.2f}B"
        })
    
    df = pd.DataFrame(display_data)
    st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)

def analyze_forex(kill_zone, count, show_ict):
    st.subheader("Forex Pair Analysis")
    assets_to_analyze = FOREX_PAIRS[:count]
    
    with st.spinner(f"Analyzing {count} forex pairs..."):
        results = []
        progress_bar = st.progress(0)
        
        for i, pair in enumerate(assets_to_analyze):
            data = fetch_forex_data(pair)
            if data:
                analysis = analyze_asset(data, 'Forex', kill_zone)
                results.append(analysis)
            progress_bar.progress((i + 1) / len(assets_to_analyze))
        
        progress_bar.empty()
        
        if results:
            results_sorted = sorted(results, key=lambda x: x['combined_score'], reverse=True)
            display_forex_results(results_sorted, show_ict)

def display_forex_results(results, show_ict):
    st.subheader("Top Forex Opportunities")
    
    display_data = []
    for r in results[:10]:
        change_color = "positive" if r['price_change_24h'] >= 0 else "negative"
        display_data.append({
            'Pair': r['symbol'],
            'Price': f"{r['price']:.4f}",
            '24h Change': f"<span class='{change_color}'>{r['price_change_24h']:+.2f}%</span>",
            'RSI': f"{r['rsi']:.1f}",
            'Score': f"{r['combined_score']:.1f}",
            'Signal': r['signal'],
            'Trend': r['trend']
        })
    
    df = pd.DataFrame(display_data)
    st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)
    
    if results:
        top_pick = results[0]
        chart = create_advanced_chart(top_pick['name'], show_ict=show_ict)
        if chart:
            st.plotly_chart(chart, use_container_width=True)

def display_correlation_analysis():
    st.header("Correlation Analysis")
    
    st.write("Select assets to compare correlation:")
    
    col1, col2 = st.columns(2)
    with col1:
        correlation_type = st.radio("Asset Type", ["Stocks", "Crypto", "Forex"], horizontal=True)
    with col2:
        num_assets = st.slider("Number of Assets", 3, 10, 5)
    
    if correlation_type == "Stocks":
        selected_assets = st.multiselect("Select Stocks", NIFTY_50, default=NIFTY_50[:num_assets])
    elif correlation_type == "Crypto":
        crypto_tickers = [f"{c.upper()}-USD" for c in TOP_CRYPTO[:10]]
        selected_assets = st.multiselect("Select Cryptos", crypto_tickers, default=crypto_tickers[:num_assets])
    else:
        selected_assets = st.multiselect("Select Forex Pairs", FOREX_PAIRS, default=FOREX_PAIRS[:num_assets])
    
    if st.button("Calculate Correlation", type="primary") and len(selected_assets) >= 2:
        with st.spinner("Calculating correlation..."):
            fig = calculate_correlation_matrix(selected_assets)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
                
                st.info("""
                **Interpretation:**
                - **+1.0**: Perfect positive correlation (assets move together)
                - **0.0**: No correlation (independent movement)
                - **-1.0**: Perfect negative correlation (assets move opposite)
                """)
            else:
                st.error("Unable to calculate correlation. Please check asset symbols.")

def display_settings():
    st.header("Settings")
    
    st.subheader("Trading Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        theme = st.selectbox("Theme", ["Dark (Professional)", "Light", "Auto"], 
                            index=0 if st.session_state.preferences['theme'] == 'dark' else 1)
        st.session_state.preferences['theme'] = 'dark' if theme == "Dark (Professional)" else 'light'
        
        default_tf = st.selectbox("Default Timeframe", list(TIMEFRAMES.keys()),
                                 index=5)
        st.session_state.preferences['default_timeframe'] = TIMEFRAMES[default_tf]
    
    with col2:
        risk_tolerance = st.select_slider("Risk Tolerance", 
                                         options=['Very Low', 'Low', 'Medium', 'High', 'Very High'],
                                         value=st.session_state.preferences['risk_tolerance'].title())
        st.session_state.preferences['risk_tolerance'] = risk_tolerance.lower()
        
        notification_email = st.text_input("Email for Alerts", 
                                          value=st.session_state.preferences['notification_email'],
                                          placeholder="your@email.com")
        st.session_state.preferences['notification_email'] = notification_email
    
    st.divider()
    
    st.subheader("Display Options")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        show_ict = st.checkbox("Show ICT Overlays", value=True)
    with col2:
        auto_refresh = st.checkbox("Auto-refresh Data", value=False)
    with col3:
        show_tooltips = st.checkbox("Show Tooltips", value=True)
    
    st.divider()
    
    st.subheader("Data Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Export All Data", type="secondary", use_container_width=True):
            export_data = {
                'watchlist': st.session_state.watchlist,
                'portfolio': st.session_state.portfolio,
                'alerts': st.session_state.alerts,
                'preferences': st.session_state.preferences
            }
            json_str = json.dumps(export_data, indent=2)
            st.download_button("Download JSON", json_str, "ict_data.json", "application/json")
    
    with col2:
        if st.button("Clear Watchlist", type="secondary", use_container_width=True):
            st.session_state.watchlist = []
            st.success("Watchlist cleared!")
            st.rerun()
    
    with col3:
        if st.button("Reset Settings", type="secondary", use_container_width=True):
            st.session_state.preferences = {
                'theme': 'dark',
                'default_timeframe': '1d',
                'risk_tolerance': 'medium',
                'notification_email': ''
            }
            st.success("Settings reset!")
            st.rerun()

if __name__ == "__main__":
    # Initialize session state for chart display
    if 'show_chart' not in st.session_state:
        st.session_state.show_chart = False
    if 'create_alert' not in st.session_state:
        st.session_state.create_alert = False
    
    main()
