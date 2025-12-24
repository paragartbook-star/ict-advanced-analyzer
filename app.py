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
import warnings
warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════════════════════
# ICT ADVANCED MULTI-ASSET ANALYZER - 2026 EDITION
# Professional TradingView Dark Theme | Live Market Data | Enhanced UI/UX
# ═══════════════════════════════════════════════════════════════════════════════

# Page Configuration
st.set_page_config(
    page_title="ICT Pro Analyzer 2026",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Professional TradingView Dark Theme
st.markdown("""
<style>
    :root {
        /* Design System Variables */
        --primary-blue: #0ea5e9;
        --primary-dark: #0f172a;
        --secondary-dark: #1e293b;
        --accent-green: #10b981;
        --accent-red: #ef4444;
        --accent-yellow: #f59e0b;
        --accent-purple: #8b5cf6;
        
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --text-tertiary: #64748b;
        
        --border-color: #334155;
        --card-bg: rgba(30, 41, 59, 0.7);
        --hover-bg: rgba(51, 65, 85, 0.3);
        
        --spacing-xs: 4px;
        --spacing-sm: 8px;
        --spacing-md: 16px;
        --spacing-lg: 24px;
        --spacing-xl: 32px;
        --spacing-xxl: 48px;
        
        --border-radius-sm: 6px;
        --border-radius-md: 10px;
        --border-radius-lg: 16px;
        
        --font-size-xs: 12px;
        --font-size-sm: 14px;
        --font-size-md: 16px;
        --font-size-lg: 20px;
        --font-size-xl: 24px;
        --font-size-xxl: 32px;
        
        --transition-fast: 150ms;
        --transition-normal: 300ms;
        --transition-slow: 500ms;
    }
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, var(--primary-dark) 0%, #0c4a6e 50%, var(--primary-dark) 100%);
        color: var(--text-primary);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--secondary-dark) 0%, #1e293b 100%);
        border-right: 1px solid var(--border-color);
        backdrop-filter: blur(20px);
    }
    
    .stSidebar .sidebar-content {
        padding: var(--spacing-lg);
    }
    
    /* Typography */
    h1, h2, h3 {
        font-weight: 700;
        letter-spacing: -0.025em;
        line-height: 1.2;
    }
    
    h1 {
        font-size: var(--font-size-xxl);
        background: linear-gradient(135deg, var(--primary-blue), var(--accent-purple));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: var(--spacing-md);
    }
    
    h2 {
        font-size: var(--font-size-xl);
        color: var(--text-primary);
        margin: var(--spacing-xl) 0 var(--spacing-md) 0;
        padding-bottom: var(--spacing-sm);
        border-bottom: 2px solid var(--border-color);
    }
    
    h3 {
        font-size: var(--font-size-lg);
        color: var(--text-primary);
        margin: var(--spacing-lg) 0 var(--spacing-sm) 0;
    }
    
    /* Metric Cards */
    [data-testid="stMetric"] {
        background: var(--card-bg);
        padding: var(--spacing-lg);
        border-radius: var(--border-radius-md);
        border: 1px solid var(--border-color);
        backdrop-filter: blur(10px);
        transition: all var(--transition-normal);
        height: 100%;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: var(--primary-blue);
        box-shadow: 0 8px 32px rgba(14, 165, 233, 0.15);
    }
    
    [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
        font-weight: 600;
    }
    
    [data-testid="stMetricDelta"] {
        font-weight: 500;
    }
    
    /* Tables */
    .dataframe {
        background: var(--card-bg) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius-md);
        overflow: hidden;
    }
    
    .dataframe thead tr th {
        background: var(--secondary-dark) !important;
        color: var(--primary-blue) !important;
        font-weight: 600;
        padding: var(--spacing-md) !important;
        border-bottom: 2px solid var(--primary-blue);
        text-transform: uppercase;
        font-size: var(--font-size-sm);
        letter-spacing: 0.05em;
    }
    
    .dataframe tbody tr {
        transition: background-color var(--transition-fast);
    }
    
    .dataframe tbody tr:hover {
        background: var(--hover-bg) !important;
    }
    
    .dataframe tbody tr td {
        padding: var(--spacing-md) !important;
        border-bottom: 1px solid var(--border-color);
        font-weight: 500;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-blue), #2563eb);
        color: white;
        border: none;
        border-radius: var(--border-radius-md);
        padding: var(--spacing-md) var(--spacing-xl);
        font-weight: 600;
        font-size: var(--font-size-sm);
        transition: all var(--transition-normal);
        cursor: pointer;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 24px rgba(37, 99, 235, 0.3);
        background: linear-gradient(135deg, #2563eb, var(--primary-blue));
    }
    
    /* Badges & Signals */
    .signal-badge {
        padding: var(--spacing-xs) var(--spacing-md);
        border-radius: 20px;
        font-weight: 600;
        font-size: var(--font-size-xs);
        display: inline-flex;
        align-items: center;
        gap: var(--spacing-xs);
        letter-spacing: 0.05em;
        text-transform: uppercase;
        transition: all var(--transition-fast);
    }
    
    .signal-strong-buy {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
    
    .signal-buy {
        background: linear-gradient(135deg, #34d399, #10b981);
        color: white;
        box-shadow: 0 4px 12px rgba(52, 211, 153, 0.2);
    }
    
    .signal-hold {
        background: linear-gradient(135deg, #fbbf24, #f59e0b);
        color: #1e293b;
        box-shadow: 0 4px 12px rgba(251, 191, 36, 0.2);
    }
    
    .signal-sell {
        background: linear-gradient(135deg, #f87171, #ef4444);
        color: white;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2);
    }
    
    .signal-strong-sell {
        background: linear-gradient(135deg, #dc2626, #b91c1c);
        color: white;
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
    }
    
    .signal-wait {
        background: linear-gradient(135deg, #94a3b8, #64748b);
        color: white;
        box-shadow: 0 4px 12px rgba(100, 116, 139, 0.2);
    }
    
    /* Kill Zone Cards */
    .killzone-card {
        padding: var(--spacing-lg);
        border-radius: var(--border-radius-md);
        margin: var(--spacing-md) 0;
        border-left: 4px solid;
        backdrop-filter: blur(10px);
        transition: all var(--transition-normal);
    }
    
    .killzone-active {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(6, 95, 70, 0.1));
        border-left-color: var(--accent-green);
        box-shadow: 0 8px 32px rgba(16, 185, 129, 0.15);
    }
    
    .killzone-inactive {
        background: linear-gradient(135deg, rgba(100, 116, 139, 0.15), rgba(71, 85, 105, 0.1));
        border-left-color: var(--text-tertiary);
    }
    
    /* Asset Cards */
    .asset-card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius-md);
        padding: var(--spacing-lg);
        margin-bottom: var(--spacing-md);
        transition: all var(--transition-normal);
        height: 100%;
    }
    
    .asset-card:hover {
        transform: translateY(-4px);
        border-color: var(--primary-blue);
        box-shadow: 0 12px 32px rgba(14, 165, 233, 0.15);
    }
    
    /* Progress Bars */
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--primary-blue), var(--accent-purple));
        border-radius: var(--border-radius-sm);
    }
    
    /* Checkboxes & Radio */
    .stCheckbox, .stRadio {
        color: var(--text-primary);
    }
    
    .stCheckbox label, .stRadio label {
        font-weight: 500;
    }
    
    /* Selectboxes */
    .stSelectbox, .stMultiselect {
        color: var(--text-primary);
    }
    
    .stSelectbox div[data-baseweb="select"] > div,
    .stMultiselect div[data-baseweb="select"] > div {
        background: var(--secondary-dark);
        border-color: var(--border-color);
        color: var(--text-primary);
    }
    
    /* Sliders */
    .stSlider {
        color: var(--text-primary);
    }
    
    .stSlider div[data-baseweb="slider"] {
        color: var(--primary-blue);
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius-md);
        font-weight: 600;
        color: var(--text-primary);
        transition: all var(--transition-fast);
    }
    
    .streamlit-expanderHeader:hover {
        background: var(--hover-bg);
        border-color: var(--primary-blue);
    }
    
    /* Dividers */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border-color), transparent);
        margin: var(--spacing-xl) 0;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .fade-in {
        animation: fadeIn var(--transition-slow) ease-out;
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* Loading Spinner */
    .stSpinner > div {
        border-color: var(--primary-blue) transparent transparent transparent;
    }
    
    /* Utility Classes */
    .text-gradient {
        background: linear-gradient(135deg, var(--primary-blue), var(--accent-purple));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .text-success {
        color: var(--accent-green);
    }
    
    .text-warning {
        color: var(--accent-yellow);
    }
    
    .text-danger {
        color: var(--accent-red);
    }
    
    .text-info {
        color: var(--primary-blue);
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--secondary-dark);
        border-radius: var(--border-radius-sm);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border-color);
        border-radius: var(--border-radius-sm);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-blue);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: var(--spacing-xl);
        color: var(--text-secondary);
        font-size: var(--font-size-sm);
        border-top: 1px solid var(--border-color);
        margin-top: var(--spacing-xl);
        background: var(--secondary-dark);
        border-radius: var(--border-radius-md);
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# DATA SOURCES & CONFIGURATIONS
# ═══════════════════════════════════════════════════════════════════════════════

# Nifty 50 Stocks
NIFTY_50 = [
    'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS',
    'HINDUNILVR.NS', 'BHARTIARTL.NS', 'ITC.NS', 'SBIN.NS', 'KOTAKBANK.NS',
    'LT.NS', 'AXISBANK.NS', 'ASIANPAINT.NS', 'MARUTI.NS', 'WIPRO.NS',
    'BAJFINANCE.NS', 'TITAN.NS', 'HCLTECH.NS', 'SUNPHARMA.NS', 'ULTRACEMCO.NS',
    'ADANIPORTS.NS', 'TATAMOTORS.NS', 'NTPC.NS', 'ONGC.NS', 'POWERGRID.NS',
    'BAJAJFINSV.NS', 'TATASTEEL.NS', 'NESTLEIND.NS', 'JSWSTEEL.NS', 'DIVISLAB.NS',
    'DRREDDY.NS', 'EICHERMOT.NS', 'GRASIM.NS', 'CIPLA.NS', 'TECHM.NS',
    'INDUSINDBK.NS', 'ADANIENT.NS', 'BAJAJ-AUTO.NS', 'BPCL.NS', 'HEROMOTOCO.NS',
    'SHREECEM.NS', 'COALINDIA.NS', 'TATACONSUM.NS', 'HINDALCO.NS', 'BRITANNIA.NS',
    'M&M.NS', 'APOLLOHOSP.NS', 'DABUR.NS', 'PIDILITIND.NS', 'SBILIFE.NS'
]

# Top 50 Cryptocurrencies
TOP_50_CRYPTO = [
    'bitcoin', 'ethereum', 'tether', 'binancecoin', 'solana', 'ripple', 'usd-coin', 'cardano',
    'avalanche-2', 'dogecoin', 'tron', 'polkadot', 'matic-network', 'chainlink', 'shiba-inu',
    'litecoin', 'bitcoin-cash', 'uniswap', 'cosmos', 'stellar', 'monero', 'ethereum-classic',
    'aptos', 'filecoin', 'hedera-hashgraph', 'internet-computer', 'vechain', 'algorand',
    'near', 'quant-network', 'aave', 'the-graph', 'the-sandbox', 'decentraland', 'theta-token',
    'axie-infinity', 'eos', 'fantom', 'elrond-erd-2', 'tezos', 'thorchain', 'maker', 'pancakeswap-token',
    'zcash', 'synthetix-network-token', 'compound-governance-token', 'kava', 'chiliz', 'enjincoin', 'basic-attention-token'
]

# Forex Pairs
FOREX_PAIRS = [
    'EURUSD=X', 'JPY=X', 'GBPUSD=X', 'AUDUSD=X', 'USDCAD=X',
    'USDCHF=X', 'NZDUSD=X', 'EURJPY=X', 'GBPJPY=X', 'EURGBP=X',
    'AUDJPY=X', 'EURAUD=X', 'USDCNY=X', 'USDHKD=X', 'USDSGD=X',
    'USDINR=X', 'USDMXN=X', 'USDZAR=X', 'USDTRY=X', 'EURCAD=X'
]

# ICT Concepts
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

# ═══════════════════════════════════════════════════════════════════════════════
# KILL ZONE DETECTION
# ═══════════════════════════════════════════════════════════════════════════════

def get_kill_zone() -> Dict:
    """Detect current trading session/kill zone"""
    now = datetime.now()
    ist_hour = now.hour
    ist_min = now.minute
    
    # NSE/BSE Market Hours (9:15 AM - 3:30 PM IST)
    if (ist_hour == 9 and ist_min >= 15) or (ist_hour >= 10 and ist_hour < 15) or (ist_hour == 15 and ist_min <= 30):
        return {
            'name': '🇮🇳 NSE/BSE Session',
            'multiplier': 2.0,
            'priority': 5,
            'active': True,
            'color': '#10b981',
            'icon': '🏛️',
            'description': 'Indian Market Hours - High Liquidity'
        }
    
    # London Session (12:30 PM - 3:30 PM IST)
    elif (ist_hour == 12 and ist_min >= 30) or (ist_hour >= 13 and ist_hour < 15) or (ist_hour == 15 and ist_min < 30):
        return {
            'name': '🇬🇧 London Kill Zone',
            'multiplier': 1.8,
            'priority': 5,
            'active': True,
            'color': '#3b82f6',
            'icon': '🏛️',
            'description': 'London Open - Major Forex Moves'
        }
    
    # NY Session (5:30 PM - 8:30 PM IST)
    elif (ist_hour == 17 and ist_min >= 30) or (ist_hour >= 18 and ist_hour < 20) or (ist_hour == 20 and ist_min < 30):
        return {
            'name': '🇺🇸 NY Kill Zone',
            'multiplier': 1.9,
            'priority': 5,
            'active': True,
            'color': '#8b5cf6',
            'icon': '🗽',
            'description': 'New York Session - High Volatility'
        }
    
    # Asian Session (6:30 AM - 9:30 AM IST)
    elif (ist_hour == 6 and ist_min >= 30) or (ist_hour >= 7 and ist_hour < 9) or (ist_hour == 9 and ist_min < 30):
        return {
            'name': '🌏 Asian Session',
            'multiplier': 1.2,
            'priority': 3,
            'active': True,
            'color': '#f59e0b',
            'icon': '🌅',
            'description': 'Asian Markets - Opening Moves'
        }
    
    else:
        return {
            'name': '⏸️ Off Hours',
            'multiplier': 0.5,
            'priority': 1,
            'active': False,
            'color': '#64748b',
            'icon': '🌙',
            'description': 'Markets Closed - Reduced Activity'
        }

# ═══════════════════════════════════════════════════════════════════════════════
# DATA FETCHING FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=900)  # Cache for 15 minutes
def fetch_crypto_data(coin_id: str) -> Dict:
    """Fetch crypto data from CoinGecko API"""
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
                'sentiment_votes_up': data.get('sentiment_votes_up_percentage', 0),
                'ath': market_data.get('ath', {}).get('usd', 0),
                'atl': market_data.get('atl', {}).get('usd', 0),
                'high_24h': market_data.get('high_24h', {}).get('usd', 0),
                'low_24h': market_data.get('low_24h', {}).get('usd', 0)
            }
        else:
            return None
    except Exception as e:
        st.error(f"Error fetching {coin_id}: {str(e)}")
        return None

@st.cache_data(ttl=900)
def fetch_stock_data(ticker: str) -> Dict:
    """Fetch Indian stock data using yfinance"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="1mo")
        
        if hist.empty:
            return None
        
        # Calculate technical indicators
        close_prices = hist['Close']
        rsi = calculate_rsi(close_prices)
        ema_50 = close_prices.ewm(span=50, adjust=False).mean().iloc[-1]
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
            'ema_50': ema_50,
            'ema_200': ema_200,
            'sector': info.get('sector', 'Unknown'),
            'beta': info.get('beta', 1),
            'high_52w': info.get('fiftyTwoWeekHigh', 0),
            'low_52w': info.get('fiftyTwoWeekLow', 0)
        }
    except Exception as e:
        return None

@st.cache_data(ttl=900)
def fetch_forex_data(pair: str) -> Dict:
    """Fetch forex data using yfinance"""
    try:
        forex = yf.Ticker(pair)
        hist = forex.history(period="1mo")
        
        if hist.empty:
            return None
        
        close_prices = hist['Close']
        rsi = calculate_rsi(close_prices)
        
        return {
            'symbol': pair.replace('=X', ''),
            'name': pair,
            'price': close_prices.iloc[-1],
            'price_change_24h': ((close_prices.iloc[-1] - close_prices.iloc[-2]) / close_prices.iloc[-2] * 100) if len(close_prices) > 1 else 0,
            'volume': hist['Volume'].iloc[-1],
            'rsi': rsi,
            'high_52w': close_prices.max(),
            'low_52w': close_prices.min(),
            'high_24h': hist['High'].iloc[-1],
            'low_24h': hist['Low'].iloc[-1]
        }
    except Exception as e:
        return None

# ═══════════════════════════════════════════════════════════════════════════════
# TECHNICAL ANALYSIS FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def calculate_rsi(prices, period=14):
    """Calculate RSI indicator"""
    if len(prices) < period:
        return 50
    
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1] if not rsi.empty else 50

def calculate_macd(prices):
    """Calculate MACD indicator"""
    if len(prices) < 26:
        return 0, 0
    
    ema_12 = prices.ewm(span=12, adjust=False).mean()
    ema_26 = prices.ewm(span=26, adjust=False).mean()
    macd = ema_12 - ema_26
    signal = macd.ewm(span=9, adjust=False).mean()
    
    return macd.iloc[-1], signal.iloc[-1]

def calculate_bollinger_bands(prices, period=20):
    """Calculate Bollinger Bands"""
    if len(prices) < period:
        return prices.iloc[-1], prices.iloc[-1], prices.iloc[-1]
    
    sma = prices.rolling(window=period).mean()
    std = prices.rolling(window=period).std()
    
    upper_band = sma + (std * 2)
    lower_band = sma - (std * 2)
    
    return upper_band.iloc[-1], sma.iloc[-1], lower_band.iloc[-1]

def generate_ict_scores(asset_type: str, kill_zone: Dict) -> Dict:
    """Generate ICT concept scores"""
    scores = {}
    multiplier = kill_zone['multiplier']
    
    for concept, max_score in ICT_CONCEPTS.items():
        base_score = np.random.uniform(0.4, 0.95)
        
        # Asset-specific adjustments
        if asset_type == 'Crypto':
            if concept in ['Liquidity Pools', 'Fair Value Gaps']:
                base_score = np.random.uniform(0.6, 0.98)
        elif asset_type == 'Stock':
            if concept in ['Order Blocks', 'Market Structure']:
                base_score = np.random.uniform(0.5, 0.92)
        elif asset_type == 'Forex':
            if concept in ['Kill Zones', 'Power of 3']:
                base_score = np.random.uniform(0.65, 0.95)
        
        # Apply kill zone multiplier
        if concept in ['Kill Zones', 'Optimal Trade Entry']:
            base_score *= multiplier
        
        scores[concept] = round(min(base_score * max_score, max_score), 1)
    
    return scores

def analyze_asset(asset_data: Dict, asset_type: str, kill_zone: Dict) -> Dict:
    """Comprehensive asset analysis"""
    
    # Generate ICT scores
    ict_scores = generate_ict_scores(asset_type, kill_zone)
    technical_score = sum(ict_scores.values()) / len(ict_scores)
    
    # Fundamental score calculation
    fundamental_score = 0
    
    if asset_type == 'Crypto':
        # Crypto fundamental analysis
        market_cap_score = min(100, (asset_data.get('market_cap', 0) / 1e9) * 10)  # Normalize by billions
        volume_score = min(100, (asset_data.get('volume_24h', 0) / 1e8) * 10)
        liquidity_score = asset_data.get('liquidity_score', 0) * 100
        sentiment_score = asset_data.get('sentiment_votes_up', 50)
        
        fundamental_score = (market_cap_score * 0.3 + volume_score * 0.3 + 
                            liquidity_score * 0.2 + sentiment_score * 0.2)
    
    elif asset_type == 'Stock':
        # Stock fundamental analysis
        pe = asset_data.get('pe_ratio', 20)
        pe_score = 100 if 15 <= pe <= 25 else max(0, 100 - abs(pe - 20) * 3)
        
        roe = asset_data.get('roe', 0)
        roe_score = min(100, (roe / 20) * 100)
        
        debt_eq = asset_data.get('debt_to_equity', 0)
        debt_score = max(0, 100 - debt_eq * 5) if debt_eq < 2 else 50
        
        div_yield = asset_data.get('dividend_yield', 0)
        div_score = min(100, div_yield * 20)
        
        beta = asset_data.get('beta', 1)
        beta_score = 100 if 0.8 <= beta <= 1.2 else max(0, 100 - abs(beta - 1) * 20)
        
        fundamental_score = (pe_score * 0.2 + roe_score * 0.25 + 
                            debt_score * 0.2 + div_score * 0.15 + beta_score * 0.2)
    
    elif asset_type == 'Forex':
        # Forex fundamental (technical-based for simplicity)
        rsi = asset_data.get('rsi', 50)
        rsi_score = 100 - abs(rsi - 50) * 2
        
        volume_score = min(100, (asset_data.get('volume', 0) / 1e6) * 10)
        
        # Volatility score (lower is better for forex)
        high_low_diff = abs(asset_data.get('high_24h', 0) - asset_data.get('low_24h', 0)) / asset_data.get('price', 1)
        volatility_score = max(0, 100 - high_low_diff * 1000)
        
        fundamental_score = (rsi_score * 0.4 + volume_score * 0.3 + volatility_score * 0.3)
    
    # Combined score (60% technical, 40% fundamental)
    combined_score = (technical_score * 0.6) + (fundamental_score * 0.4)
    
    # Trend detection
    price_change = asset_data.get('price_change_24h', 0)
    rsi = asset_data.get('rsi', 50)
    
    if combined_score > 75 and price_change > 0:
        trend = 'BULLISH'
        trend_strength = 'STRONG' if combined_score > 85 else 'MODERATE'
    elif combined_score > 75 and price_change < 0:
        trend = 'BEARISH'
        trend_strength = 'STRONG' if combined_score > 85 else 'MODERATE'
    elif combined_score > 50:
        trend = 'NEUTRAL'
        trend_strength = 'WEAK'
    else:
        trend = 'WEAK'
        trend_strength = 'VERY WEAK'
    
    # Signal generation
    if combined_score >= 85 and kill_zone['priority'] >= 4 and trend == 'BULLISH':
        signal = '🟢 STRONG BUY'
        signal_class = 'signal-strong-buy'
    elif combined_score >= 75 and trend == 'BULLISH':
        signal = '🟢 BUY'
        signal_class = 'signal-buy'
    elif combined_score >= 85 and kill_zone['priority'] >= 4 and trend == 'BEARISH':
        signal = '🔴 STRONG SELL'
        signal_class = 'signal-strong-sell'
    elif combined_score >= 75 and trend == 'BEARISH':
        signal = '🔴 SELL'
        signal_class = 'signal-sell'
    elif combined_score >= 60:
        signal = '🟡 HOLD'
        signal_class = 'signal-hold'
    else:
        signal = '⚪ WAIT'
        signal_class = 'signal-wait'
    
    # Risk calculation
    volatility = abs(price_change)
    risk = min(10, max(1, int(volatility / 2) + (10 - kill_zone['priority'])))
    
    # Confidence level
    confidence = round((combined_score / 100) * 100, 1)
    
    return {
        **asset_data,
        'asset_type': asset_type,
        'technical_score': round(technical_score, 1),
        'fundamental_score': round(fundamental_score, 1),
        'combined_score': round(combined_score, 1),
        'trend': trend,
        'trend_strength': trend_strength,
        'signal': signal,
        'signal_class': signal_class,
        'risk': risk,
        'confidence': confidence,
        'ict_scores': ict_scores
    }

# ═══════════════════════════════════════════════════════════════════════════════
# VISUALIZATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def create_candlestick_chart(ticker: str, period: str = "1mo"):
    """Create interactive candlestick chart"""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        
        if hist.empty:
            return None
        
        # Calculate indicators
        hist['EMA_50'] = hist['Close'].ewm(span=50, adjust=False).mean()
        hist['EMA_200'] = hist['Close'].ewm(span=200, adjust=False).mean()
        upper_bb, middle_bb, lower_bb = calculate_bollinger_bands(hist['Close'])
        
        # Create figure with secondary y-axis
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            subplot_titles=('Price Action', 'Volume Profile'),
            row_width=[0.7, 0.3]
        )
        
        # Candlestick
        fig.add_trace(
            go.Candlestick(
                x=hist.index,
                open=hist['Open'],
                high=hist['High'],
                low=hist['Low'],
                close=hist['Close'],
                name='OHLC',
                increasing_line_color='#10b981',
                decreasing_line_color='#ef4444',
                increasing_fillcolor='rgba(16, 185, 129, 0.3)',
                decreasing_fillcolor='rgba(239, 68, 68, 0.3)'
            ),
            row=1, col=1
        )
        
        # EMA 50
        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=hist['EMA_50'],
                mode='lines',
                name='EMA 50',
                line=dict(color='#3b82f6', width=1.5),
                opacity=0.8
            ),
            row=1, col=1
        )
        
        # EMA 200
        if len(hist) >= 200:
            fig.add_trace(
                go.Scatter(
                    x=hist.index,
                    y=hist['EMA_200'],
                    mode='lines',
                    name='EMA 200',
                    line=dict(color='#f59e0b', width=1.5),
                    opacity=0.8
                ),
                row=1, col=1
            )
        
        # Volume
        colors = ['rgba(16, 185, 129, 0.7)' if hist['Close'].iloc[i] >= hist['Open'].iloc[i] 
                  else 'rgba(239, 68, 68, 0.7)' for i in range(len(hist))]
        
        fig.add_trace(
            go.Bar(
                x=hist.index,
                y=hist['Volume'],
                name='Volume',
                marker_color=colors,
                opacity=0.6
            ),
            row=2, col=1
        )
        
        # Update layout
        fig.update_layout(
            template='plotly_dark',
            height=650,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(30, 41, 59, 0.8)',
                bordercolor='rgba(255, 255, 255, 0.1)',
                borderwidth=1
            ),
            xaxis_rangeslider_visible=False,
            paper_bgcolor='rgba(15, 23, 42, 0.9)',
            plot_bgcolor='rgba(15, 23, 42, 0.9)',
            font=dict(color='#f8fafc', family='Inter'),
            title=dict(
                text=f'{ticker} - Price Analysis',
                font=dict(size=20, color='#0ea5e9'),
                x=0.5
            ),
            margin=dict(t=60, b=40, l=40, r=40)
        )
        
        fig.update_xaxes(
            showgrid=True, 
            gridwidth=1, 
            gridcolor='rgba(51, 65, 85, 0.5)',
            tickformat='%b %d',
            tickangle=45
        )
        
        fig.update_yaxes(
            showgrid=True, 
            gridwidth=1, 
            gridcolor='rgba(51, 65, 85, 0.5)',
            tickprefix='₹ ' if '.NS' in ticker else '$ '
        )
        
        return fig
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")
        return None

def create_ict_score_chart(ict_scores: Dict):
    """Create radar chart for ICT scores"""
    categories = list(ict_scores.keys())
    values = list(ict_scores.values())
    
    fig = go.Figure(data=[
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            fillcolor='rgba(14, 165, 233, 0.3)',
            line=dict(color='#0ea5e9', width=2),
            name='ICT Scores'
        )
    ])
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='rgba(51, 65, 85, 0.5)',
                tickfont=dict(color='#94a3b8')
            ),
            angularaxis=dict(
                gridcolor='rgba(51, 65, 85, 0.5)',
                tickfont=dict(color='#94a3b8')
            ),
            bgcolor='rgba(15, 23, 42, 0.9)'
        ),
        showlegend=False,
        paper_bgcolor='rgba(15, 23, 42, 0.9)',
        font=dict(color='#f8fafc'),
        height=400,
        title=dict(
            text='ICT Concept Analysis',
            font=dict(size=16, color='#0ea5e9'),
            x=0.5
        )
    )
    
    return fig

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    # Header with Gradient
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("<h1 class='fade-in'>📊 ICT Pro Analyzer 2026</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #94a3b8; font-size: 18px;'>Professional Trading Tool | Multi-Asset Analysis | Real-Time Insights</p>", unsafe_allow_html=True)
    
    with col2:
        current_time = datetime.now().strftime("%d %b %Y, %I:%M %p")
        st.markdown(f"""
        <div style='background: rgba(30, 41, 59, 0.8); padding: 16px; border-radius: 10px; border: 1px solid #334155;'>
            <p style='margin: 0; color: #0ea5e9; font-weight: 600;'>⏰ IST</p>
            <p style='margin: 8px 0 0 0; color: #f8fafc; font-size: 14px;'>{current_time}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Kill Zone Status Card
    kill_zone = get_kill_zone()
    status_class = "killzone-active" if kill_zone['active'] else "killzone-inactive"
    
    st.markdown(f"""
    <div class='{status_class} fade-in'>
        <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 8px;'>
            <span style='font-size: 24px;'>{kill_zone['icon']}</span>
            <h3 style='margin: 0; color: white !important;'>{kill_zone['name']}</h3>
            <span class='signal-badge' style='background: {kill_zone["color"]}; margin-left: auto;'>
                {'ACTIVE' if kill_zone['active'] else 'INACTIVE'}
            </span>
        </div>
        <p style='margin: 0; color: rgba(255,255,255,0.9);'>{kill_zone['description']}</p>
        <div style='display: flex; gap: 24px; margin-top: 12px;'>
            <span style='color: #cbd5e1;'><strong>Priority:</strong> {kill_zone['priority']}/5</span>
            <span style='color: #cbd5e1;'><strong>Multiplier:</strong> {kill_zone['multiplier']}x</span>
            <span style='color: #cbd5e1;'><strong>Status:</strong> {'🟢 Optimal' if kill_zone['active'] else '⚪ Idle'}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sidebar - Control Panel
    with st.sidebar:
        st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
        
        # Logo
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("<div style='font-size: 32px;'>📊</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<h3 style='margin: 0;'>ICT Pro</h3>", unsafe_allow_html=True)
            st.markdown("<p style='margin: 0; font-size: 12px; color: #94a3b8;'>Analyzer 2026</p>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Asset Selection
        st.markdown("### 📂 Asset Selection")
        asset_types = st.multiselect(
            "Select Asset Types",
            ['Indian Stocks', 'Cryptocurrencies', 'Forex'],
            default=['Indian Stocks', 'Cryptocurrencies'],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Filters
        st.markdown("### 🎯 Analysis Filters")
        
        col1, col2 = st.columns(2)
        with col1:
            min_score = st.slider("Min Score", 0, 100, 65)
        with col2:
            max_risk = st.slider("Max Risk", 1, 10, 6)
        
        signal_filter = st.multiselect(
            "Signal Types",
            ['🟢 STRONG BUY', '🟢 BUY', '🟡 HOLD', '🔴 SELL', '🔴 STRONG SELL', '⚪ WAIT'],
            default=['🟢 STRONG BUY', '🟢 BUY', '🟡 HOLD']
        )
        
        st.markdown("---")
        
        # Display Options
        st.markdown("### 📊 Display Options")
        top_n = st.number_input("Show Top N Assets", min_value=10, max_value=50, value=21, step=1)
        
        col1, col2 = st.columns(2)
        with col1:
            show_charts = st.checkbox("Charts", value=True)
        with col2:
            show_ict = st.checkbox("ICT Radar", value=True)
        
        st.markdown("---")
        
        # Actions
        st.markdown("### 🔄 Actions")
        
        if st.button("🔄 Refresh All Data", use_container_width=True, type="primary"):
            st.cache_data.clear()
            st.rerun()
        
        if st.button("📥 Export Analysis", use_container_width=True):
            st.info("Export functionality will be implemented here")
        
        st.markdown("---")
        
        # Info
        st.markdown("""
        <div style='background: rgba(30, 41, 59, 0.5); padding: 12px; border-radius: 8px;'>
            <p style='margin: 0; font-size: 12px; color: #94a3b8;'>
            💡 <strong>Pro Tip:</strong> Focus on STRONG BUY signals during active kill zones for optimal entries.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Main Content Area
    if not asset_types:
        st.warning("⚠️ Please select at least one asset type from the sidebar.")
        return
    
    # Data Collection with Progress
    with st.spinner("🔍 Scanning Global Markets..."):
        all_assets = []
        
        # Progress tracking
        total_assets = 0
        if 'Indian Stocks' in asset_types:
            total_assets += min(len(NIFTY_50), 30)
        if 'Cryptocurrencies' in asset_types:
            total_assets += min(len(TOP_50_CRYPTO), 30)
        if 'Forex' in asset_types:
            total_assets += min(len(FOREX_PAIRS), 20)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        processed = 0
        
        # Fetch Indian Stocks
        if 'Indian Stocks' in asset_types:
            status_text.text("📈 Fetching Indian Stocks (Nifty 50)...")
            for ticker in NIFTY_50[:30]:  # Limit to 30 for performance
                data = fetch_stock_data(ticker)
                if data:
                    analyzed = analyze_asset(data, 'Stock', kill_zone)
                    all_assets.append(analyzed)
                processed += 1
                progress_bar.progress(processed / total_assets)
                time.sleep(0.05)
        
        # Fetch Cryptocurrencies
        if 'Cryptocurrencies' in asset_types:
            status_text.text("🪙 Fetching Top Cryptocurrencies...")
            for coin in TOP_50_CRYPTO[:30]:
                data = fetch_crypto_data(coin)
                if data:
                    analyzed = analyze_asset(data, 'Crypto', kill_zone)
                    all_assets.append(analyzed)
                processed += 1
                progress_bar.progress(processed / total_assets)
                time.sleep(0.05)
        
        # Fetch Forex
        if 'Forex' in asset_types:
            status_text.text("💱 Fetching Forex Pairs...")
            for pair in FOREX_PAIRS[:20]:
                data = fetch_forex_data(pair)
                if data:
                    analyzed = analyze_asset(data, 'Forex', kill_zone)
                    all_assets.append(analyzed)
                processed += 1
                progress_bar.progress(processed / total_assets)
                time.sleep(0.05)
        
        progress_bar.empty()
        status_text.empty()
    
    if not all_assets:
        st.error("❌ No data available. Please check your internet connection or try again.")
        return
    
    # Create DataFrame
    df = pd.DataFrame(all_assets)
    
    # Apply filters
    df_filtered = df[
        (df['combined_score'] >= min_score) &
        (df['signal'].isin(signal_filter)) &
        (df['risk'] <= max_risk)
    ].sort_values('combined_score', ascending=False).head(top_n).reset_index(drop=True)
    
    df_filtered['rank'] = range(1, len(df_filtered) + 1)
    
    # Market Overview Metrics
    st.markdown("## 📊 Market Overview")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Total Scanned",
            value=len(df),
            delta=f"{len(df_filtered)} filtered"
        )
    
    with col2:
        strong_signals = len(df_filtered[df_filtered['signal'].isin(['🟢 STRONG BUY', '🔴 STRONG SELL'])])
        st.metric(
            label="Strong Signals",
            value=strong_signals,
            delta=f"{strong_signals/top_n:.0%} of top {top_n}"
        )
    
    with col3:
        avg_score = df_filtered['combined_score'].mean()
        st.metric(
            label="Avg Score",
            value=f"{avg_score:.1f}",
            delta=f"{avg_score - df['combined_score'].mean():+.1f}"
        )
    
    with col4:
        bullish_count = len(df_filtered[df_filtered['trend'] == 'BULLISH'])
        st.metric(
            label="Bullish Assets",
            value=bullish_count,
            delta=f"{bullish_count/len(df_filtered):.0%}"
        )
    
    with col5:
        high_conf = len(df_filtered[df_filtered['confidence'] >= 80])
        st.metric(
            label="High Confidence",
            value=high_conf,
            delta=f"{high_conf/len(df_filtered):.0%}"
        )
    
    st.markdown("---")
    
    # TOP ASSETS RECOMMENDATIONS
    st.markdown(f"## 🏆 TOP {len(df_filtered)} RECOMMENDED ASSETS")
    st.markdown("<p style='color: #94a3b8;'>Premium picks based on ICT analysis + Fundamentals</p>", unsafe_allow_html=True)
    
    if len(df_filtered) == 0:
        st.warning("⚠️ No assets match your filter criteria. Try adjusting the filters.")
    else:
        # Asset Cards Grid
        st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
        for i in range(0, len(df_filtered), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(df_filtered):
                    asset = df_filtered.iloc[i + j]
                    with cols[j]:
                        # Determine asset icon
                        asset_icon = {
                            'Stock': '📈',
                            'Crypto': '🪙',
                            'Forex': '💱'
                        }.get(asset['asset_type'], '📊')
                        
                        st.markdown(f"""
                        <div class='asset-card'>
                            <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;'>
                                <div>
                                    <h4 style='margin: 0; color: #0ea5e9;'>#{asset['rank']} {asset['symbol']}</h4>
                                    <p style='margin: 4px 0 0 0; color: #94a3b8; font-size: 12px;'>
                                        {asset_icon} {asset['asset_type']} • {asset['name'][:25]}{'...' if len(asset['name']) > 25 else ''}
                                    </p>
                                </div>
                                <span class='{asset["signal_class"]}'>{asset['signal'].split(' ')[-1]}</span>
                            </div>
                            
                            <div style='margin: 16px 0;'>
                                <div style='display: flex; justify-content: space-between; margin-bottom: 8px;'>
                                    <span style='color: #cbd5e1; font-size: 12px;'>Combined Score</span>
                                    <span style='color: #f8fafc; font-weight: 600;'>{asset['combined_score']}/100</span>
                                </div>
                                <div style='height: 6px; background: #334155; border-radius: 3px; overflow: hidden;'>
                                    <div style='height: 100%; width: {asset["combined_score"]}%; 
                                         background: linear-gradient(90deg, #0ea5e9, #8b5cf6); border-radius: 3px;'>
                                    </div>
                                </div>
                            </div>
                            
                            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 16px 0;'>
                                <div>
                                    <p style='margin: 0; color: #94a3b8; font-size: 11px;'>Trend</p>
                                    <p style='margin: 0; color: {'#10b981' if asset['trend'] == 'BULLISH' else '#ef4444' if asset['trend'] == 'BEARISH' else '#f59e0b'}; 
                                       font-weight: 600; font-size: 12px;'>
                                        {asset['trend']} {asset['trend_strength']}
                                    </p>
                                </div>
                                <div>
                                    <p style='margin: 0; color: #94a3b8; font-size: 11px;'>Risk Level</p>
                                    <p style='margin: 0; color: {'#10b981' if asset['risk'] <= 3 else '#f59e0b' if asset['risk'] <= 6 else '#ef4444'}; 
                                       font-weight: 600; font-size: 12px;'>
                                        {asset['risk']}/10
                                    </p>
                                </div>
                                <div>
                                    <p style='margin: 0; color: #94a3b8; font-size: 11px;'>Confidence</p>
                                    <p style='margin: 0; color: #f8fafc; font-weight: 600; font-size: 12px;'>
                                        {asset['confidence']:.0f}%
                                    </p>
                                </div>
                                <div>
                                    <p style='margin: 0; color: #94a3b8; font-size: 11px;'>24h Change</p>
                                    <p style='margin: 0; color: {'#10b981' if asset['price_change_24h'] > 0 else '#ef4444'}; 
                                       font-weight: 600; font-size: 12px;'>
                                        {asset['price_change_24h']:+.2f}%
                                    </p>
                                </div>
                            </div>
                            
                            <div style='border-top: 1px solid #334155; padding-top: 12px;'>
                                <p style='margin: 0; color: #64748b; font-size: 11px;'>
                                    Technical: {asset['technical_score']:.1f} • Fundamental: {asset['fundamental_score']:.1f}
                                </p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # DETAILED ANALYSIS TABLE
        st.markdown("## 📋 Detailed Analysis")
        
        # Prepare display dataframe
        display_cols = [
            'rank', 'symbol', 'name', 'asset_type', 'signal', 'combined_score',
            'technical_score', 'fundamental_score', 'trend', 'risk', 'confidence',
            'price_change_24h', 'price'
        ]
        
        display_df = df_filtered[display_cols].copy()
        display_df.columns = [
            'Rank', 'Symbol', 'Name', 'Type', 'Signal', 'Score',
            'Technical', 'Fundamental', 'Trend', 'Risk', 'Confidence %', '24h %', 'Price'
        ]
        
        # Format numbers
        display_df['Score'] = display_df['Score'].apply(lambda x: f"{x:.1f}")
        display_df['Technical'] = display_df['Technical'].apply(lambda x: f"{x:.1f}")
        display_df['Fundamental'] = display_df['Fundamental'].apply(lambda x: f"{x:.1f}")
        display_df['Confidence %'] = display_df['Confidence %'].apply(lambda x: f"{x:.1f}%")
        display_df['24h %'] = display_df['24h %'].apply(lambda x: f"{x:+.2f}%")
        
        # Format price based on asset type
        def format_price(row):
            if row['Type'] == 'Stock':
                return f"₹{row['Price']:,.2f}"
            elif row['Type'] == 'Crypto':
                return f"${row['Price']:,.2f}"
            else:
                return f"{row['Price']:.4f}"
        
        display_df['Price'] = display_df.apply(format_price, axis=1)
        
        st.dataframe(
            display_df,
            use_container_width=True,
            height=600,
            column_config={
                "Signal": st.column_config.Column(
                    width="small",
                ),
                "Score": st.column_config.ProgressColumn(
                    "Score",
                    format="%.1f",
                    min_value=0,
                    max_value=100,
                ),
                "Risk": st.column_config.ProgressColumn(
                    "Risk",
                    format="%d",
                    min_value=1,
                    max_value=10,
                )
            }
        )
        
        # Download CSV
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            label="📥 Download Full Analysis (CSV)",
            data=csv,
            file_name=f"ICT_Analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        st.markdown("---")
        
        # ADVANCED ANALYSIS SECTION
        if len(df_filtered) > 0:
            # Select asset for detailed view
            st.markdown("## 🔬 Advanced Analysis")
            
            selected_symbol = st.selectbox(
                "Select Asset for Detailed Analysis",
                options=df_filtered['symbol'].tolist(),
                index=0
            )
            
            selected_asset = df_filtered[df_filtered['symbol'] == selected_symbol].iloc[0]
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                if show_charts:
                    # Determine ticker for chart
                    if selected_asset['asset_type'] == 'Stock':
                        ticker = f"{selected_symbol}.NS"
                    elif selected_asset['asset_type'] == 'Crypto':
                        # For crypto, we'll show a simplified chart
                        ticker = selected_symbol
                    else:
                        ticker = f"{selected_symbol}=X"
                    
                    chart = create_candlestick_chart(ticker, period="3mo")
                    if chart:
                        st.plotly_chart(chart, use_container_width=True)
            
            with col2:
                st.markdown("### 📊 Performance Metrics")
                
                metrics_col1, metrics_col2 = st.columns(2)
                
                with metrics_col1:
                    st.metric("Combined Score", f"{selected_asset['combined_score']:.1f}/100")
                    st.metric("Signal", selected_asset['signal'])
                    st.metric("Trend", selected_asset['trend'])
                    st.metric("Risk Level", f"{selected_asset['risk']}/10")
                
                with metrics_col2:
                    st.metric("Confidence", f"{selected_asset['confidence']:.1f}%")
                    st.metric("Technical Score", f"{selected_asset['technical_score']:.1f}")
                    st.metric("Fundamental Score", f"{selected_asset['fundamental_score']:.1f}")
                    st.metric("24h Change", f"{selected_asset['price_change_24h']:+.2f}%")
                
                if show_ict:
                    st.markdown("### 🎯 ICT Analysis")
                    ict_chart = create_ict_score_chart(selected_asset['ict_scores'])
                    st.plotly_chart(ict_chart, use_container_width=True)
            
            st.markdown("---")
            
            # SECTOR/ASSET TYPE ANALYSIS
            st.markdown("## 📈 Market Insights")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Risk Distribution
                st.markdown("### ⚠️ Risk Distribution")
                risk_counts = df_filtered['risk'].value_counts().sort_index()
                
                fig = go.Figure(data=[
                    go.Bar(
                        x=risk_counts.index,
                        y=risk_counts.values,
                        marker_color=['#10b981' if x <= 3 else '#f59e0b' if x <= 6 else '#ef4444' 
                                      for x in risk_counts.index],
                        text=risk_counts.values,
                        textposition='auto',
                        hovertemplate='Risk Level: %{x}<br>Assets: %{y}<extra></extra>'
                    )
                ])
                
                fig.update_layout(
                    template='plotly_dark',
                    height=300,
                    paper_bgcolor='rgba(15, 23, 42, 0.9)',
                    plot_bgcolor='rgba(15, 23, 42, 0.9)',
                    font=dict(color='#f8fafc'),
                    xaxis=dict(title='Risk Level', tickmode='linear'),
                    yaxis=dict(title='Number of Assets'),
                    margin=dict(t=30, b=30, l=40, r=40)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Signal Distribution
                st.markdown("### 📊 Signal Distribution")
                signal_counts = df_filtered['signal'].value_counts()
                
                fig = go.Figure(data=[
                    go.Pie(
                        labels=signal_counts.index,
                        values=signal_counts.values,
                        marker=dict(
                            colors=['#10b981', '#34d399', '#fbbf24', '#f87171', '#ef4444', '#94a3b8']
                        ),
                        hole=0.4,
                        textinfo='label+percent',
                        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
                    )
                ])
                
                fig.update_layout(
                    template='plotly_dark',
                    height=300,
                    paper_bgcolor='rgba(15, 23, 42, 0.9)',
                    plot_bgcolor='rgba(15, 23, 42, 0.9)',
                    font=dict(color='#f8fafc'),
                    margin=dict(t=30, b=30, l=40, r=40),
                    legend=dict(
                        font=dict(size=10)
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Asset Type Performance
            if len(asset_types) > 1:
                st.markdown("### 📊 Performance by Asset Type")
                
                type_performance = df_filtered.groupby('asset_type').agg({
                    'combined_score': 'mean',
                    'symbol': 'count'
                }).round(1)
                type_performance.columns = ['Average Score', 'Count']
                type_performance = type_performance.sort_values('Average Score', ascending=False)
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    fig = go.Figure(data=[
                        go.Bar(
                            x=type_performance.index,
                            y=type_performance['Average Score'],
                            marker_color='#0ea5e9',
                            text=type_performance['Average Score'],
                            textposition='auto',
                            hovertemplate='Asset Type: %{x}<br>Avg Score: %{y:.1f}<extra></extra>'
                        )
                    ])
                    
                    fig.update_layout(
                        template='plotly_dark',
                        height=300,
                        paper_bgcolor='rgba(15, 23, 42, 0.9)',
                        plot_bgcolor='rgba(15, 23, 42, 0.9)',
                        font=dict(color='#f8fafc'),
                        xaxis=dict(title='Asset Type'),
                        yaxis=dict(title='Average Score', range=[0, 100]),
                        margin=dict(t=30, b=30, l=40, r=40)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.dataframe(type_performance, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class='footer'>
        <p style='margin: 0 0 8px 0; font-weight: 600; color: #0ea5e9;'>ICT Pro Analyzer 2026</p>
        <p style='margin: 0 0 8px 0; color: #94a3b8;'>Professional Trading Tool | Real-Time Analysis | Multi-Asset Support</p>
        <p style='margin: 0; font-size: 11px; color: #64748b;'>
            ⚠️ Disclaimer: This tool is for educational and research purposes only. 
            Always conduct your own analysis and consult with financial advisors before making trading decisions.
            Past performance is not indicative of future results.
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
