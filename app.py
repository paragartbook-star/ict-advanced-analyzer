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
# TradingView Dark Theme | Live Market Data | Technical + Fundamental Analysis
# ═══════════════════════════════════════════════════════════════════════════════

# Page Configuration
st.set_page_config(
    page_title="ICT Advanced Analyzer 2026",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - TradingView Dark Theme
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #0f0f23 100%);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #161629 0%, #1a1a2e 100%);
        border-right: 1px solid #2d3748;
    }
    
    /* Metric Cards */
    [data-testid="stMetric"] {
        background: rgba(26, 32, 44, 0.6);
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #2d3748;
        backdrop-filter: blur(10px);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #00d4ff !important;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
    }
    
    /* Tables */
    .dataframe {
        background: rgba(26, 32, 44, 0.8) !important;
        color: #e2e8f0 !important;
        border: 1px solid #2d3748;
        border-radius: 8px;
    }
    
    .dataframe thead tr th {
        background: #1a202c !important;
        color: #00d4ff !important;
        font-weight: bold;
        border-bottom: 2px solid #00d4ff;
    }
    
    .dataframe tbody tr:hover {
        background: rgba(0, 212, 255, 0.1) !important;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
    }
    
    /* Signal Badges */
    .signal-strong-buy {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 6px 12px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        box-shadow: 0 4px 10px rgba(16, 185, 129, 0.4);
    }
    
    .signal-buy {
        background: linear-gradient(135deg, #34d399 0%, #10b981 100%);
        color: white;
        padding: 6px 12px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    
    .signal-hold {
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        color: #1a202c;
        padding: 6px 12px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    
    .signal-sell {
        background: linear-gradient(135deg, #f87171 0%, #ef4444 100%);
        color: white;
        padding: 6px 12px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    
    /* Kill Zone Status */
    .killzone-active {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #34d399;
        margin: 10px 0;
    }
    
    .killzone-inactive {
        background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #9ca3af;
        margin: 10px 0;
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

# Initialize session state for advanced features
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []
if 'alerts' not in st.session_state:
    st.session_state.alerts = []
if 'trade_history' not in st.session_state:
    st.session_state.trade_history = []
if 'portfolio_value' not in st.session_state:
    st.session_state.portfolio_value = 100000  # Starting capital

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
            'color': '#10b981'
        }
    
    # London Session (12:30 PM - 3:30 PM IST)
    elif (ist_hour == 12 and ist_min >= 30) or (ist_hour >= 13 and ist_hour < 15) or (ist_hour == 15 and ist_min < 30):
        return {
            'name': '🇬🇧 London Kill Zone',
            'multiplier': 1.8,
            'priority': 5,
            'active': True,
            'color': '#3b82f6'
        }
    
    # NY Session (5:30 PM - 8:30 PM IST)
    elif (ist_hour == 17 and ist_min >= 30) or (ist_hour >= 18 and ist_hour < 20) or (ist_hour == 20 and ist_min < 30):
        return {
            'name': '🇺🇸 NY Kill Zone',
            'multiplier': 1.9,
            'priority': 5,
            'active': True,
            'color': '#8b5cf6'
        }
    
    # Asian Session (6:30 AM - 9:30 AM IST)
    elif (ist_hour == 6 and ist_min >= 30) or (ist_hour >= 7 and ist_hour < 9) or (ist_hour == 9 and ist_min < 30):
        return {
            'name': '🌏 Asian Session',
            'multiplier': 1.2,
            'priority': 3,
            'active': True,
            'color': '#f59e0b'
        }
    
    else:
        return {
            'name': '⏸️ Off Hours',
            'multiplier': 0.5,
            'priority': 1,
            'active': False,
            'color': '#6b7280'
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
                'atl': market_data.get('atl', {}).get('usd', 0)
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
            'sector': info.get('sector', 'Unknown')
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
            'low_52w': close_prices.min()
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
        market_cap_score = min(100, (asset_data.get('market_cap', 0) / 1e9) * 10)
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
        
        fundamental_score = (pe_score * 0.25 + roe_score * 0.30 + 
                            debt_score * 0.25 + div_score * 0.20)
    
    elif asset_type == 'Forex':
        # Forex fundamental (technical-based for simplicity)
        rsi = asset_data.get('rsi', 50)
        rsi_score = 100 - abs(rsi - 50) * 2
        
        volume_score = min(100, (asset_data.get('volume', 0) / 1e6) * 10)
        
        fundamental_score = (rsi_score * 0.6 + volume_score * 0.4)
    
    # Combined score (60% technical, 40% fundamental)
    combined_score = (technical_score * 0.6) + (fundamental_score * 0.4)
    
    # Trend detection
    price_change = asset_data.get('price_change_24h', 0)
    rsi = asset_data.get('rsi', 50)
    
    if combined_score > 75 and price_change > 0:
        trend = 'BULLISH'
    elif combined_score > 75 and price_change < 0:
        trend = 'BEARISH'
    elif combined_score > 50:
        trend = 'NEUTRAL'
    else:
        trend = 'WEAK'
    
    # Signal generation
    if combined_score >= 85 and kill_zone['priority'] >= 4 and trend == 'BULLISH':
        signal = '🟢 STRONG BUY'
    elif combined_score >= 75 and trend == 'BULLISH':
        signal = '🟢 BUY'
    elif combined_score >= 85 and kill_zone['priority'] >= 4 and trend == 'BEARISH':
        signal = '🔴 STRONG SELL'
    elif combined_score >= 75 and trend == 'BEARISH':
        signal = '🔴 SELL'
    elif combined_score >= 60:
        signal = '🟡 HOLD'
    else:
        signal = '⚪ WAIT'
    
    # Risk calculation
    volatility = abs(price_change)
    risk = min(10, max(1, int(volatility / 2) + (10 - kill_zone['priority'])))
    
    # Target price calculation
    current_price = asset_data.get('price', 0)
    if signal in ['🟢 STRONG BUY', '🟢 BUY']:
        target_price = current_price * (1 + (combined_score / 100) * 0.15)
        stop_loss = current_price * 0.95
    elif signal in ['🔴 STRONG SELL', '🔴 SELL']:
        target_price = current_price * (1 - (combined_score / 100) * 0.15)
        stop_loss = current_price * 1.05
    else:
        target_price = current_price
        stop_loss = current_price * 0.97
    
    return {
        **asset_data,
        'asset_type': asset_type,
        'technical_score': round(technical_score, 1),
        'fundamental_score': round(fundamental_score, 1),
        'combined_score': round(combined_score, 1),
        'trend': trend,
        'signal': signal,
        'risk': risk,
        'confidence': round((combined_score / 100) * 100, 1),
        'ict_scores': ict_scores,
        'target_price': round(target_price, 2),
        'stop_loss': round(stop_loss, 2),
        'potential_return': round(((target_price - current_price) / current_price) * 100, 2)
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
        
        # Create figure with secondary y-axis
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            subplot_titles=('Price', 'Volume'),
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
                name='Price',
                increasing_line_color='#10b981',
                decreasing_line_color='#ef4444'
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
                line=dict(color='#3b82f6', width=1)
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
                    line=dict(color='#f59e0b', width=1)
                ),
                row=1, col=1
            )
        
        # Volume
        colors = ['#10b981' if hist['Close'].iloc[i] >= hist['Open'].iloc[i] else '#ef4444' 
                  for i in range(len(hist))]
        
        fig.add_trace(
            go.Bar(
                x=hist.index,
                y=hist['Volume'],
                name='Volume',
                marker_color=colors,
                opacity=0.5
            ),
            row=2, col=1
        )
        
        # Update layout
        fig.update_layout(
            template='plotly_dark',
            height=600,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            xaxis_rangeslider_visible=False,
            paper_bgcolor='rgba(26, 32, 44, 0.8)',
            plot_bgcolor='rgba(26, 32, 44, 0.8)',
            font=dict(color='#e2e8f0')
        )
        
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(45, 55, 72, 0.5)')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(45, 55, 72, 0.5)')
        
        return fig
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")
        return None

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    # Header
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.title("📊 ICT Advanced Analyzer 2026")
        st.markdown("**TradingView Style** | Real-Time Multi-Asset Analysis")
    
    with col2:
        current_time = datetime.now().strftime("%d %b %Y, %I:%M %p")
        st.markdown(f"**⏰ IST:** {current_time}")
    
    with col3:
        auto_refresh = st.checkbox("🔄 Auto Refresh", value=False)
        if auto_refresh:
            st.rerun()
    
    # Kill Zone Status
    kill_zone = get_kill_zone()
    status_class = "killzone-active" if kill_zone['active'] else "killzone-inactive"
    
    st.markdown(f"""
    <div class="{status_class}">
        <h3 style="margin: 0; color: white !important;">{kill_zone['name']}</h3>
        <p style="margin: 5px 0 0 0; color: rgba(255,255,255,0.8);">
            Priority: {kill_zone['priority']}/5 | Multiplier: {kill_zone['multiplier']}x | 
            Status: {'🟢 ACTIVE' if kill_zone['active'] else '⚪ INACTIVE'}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sidebar - Filters
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/artificial-intelligence.png", width=80)
        st.title("⚙️ Control Panel")
        
        # Watchlist Management
        st.markdown("### ⭐ Watchlist")
        if st.session_state.watchlist:
            st.markdown(f"**{len(st.session_state.watchlist)} assets tracked**")
            for item in st.session_state.watchlist[:5]:
                st.text(f"• {item}")
            if len(st.session_state.watchlist) > 5:
                st.text(f"... and {len(st.session_state.watchlist) - 5} more")
        else:
            st.info("No assets in watchlist")
        
        st.markdown("### 📂 Asset Selection")
        asset_types = st.multiselect(
            "Select Asset Types",
            ['Indian Stocks', 'Cryptocurrencies', 'Forex'],
            default=['Indian Stocks', 'Cryptocurrencies']
        )
        
        st.markdown("### 🎯 Filters")
        min_score = st.slider("Minimum Combined Score", 0, 100, 60)
        
        signal_filter = st.multiselect(
            "Signal Type",
            ['🟢 STRONG BUY', '🟢 BUY', '🟡 HOLD', '🔴 SELL', '🔴 STRONG SELL', '⚪ WAIT'],
            default=['🟢 STRONG BUY', '🟢 BUY']
        )
        
        max_risk = st.slider("Maximum Risk Level", 1, 10, 7)
        
        # Advanced Filters
        with st.expander("🔍 Advanced Filters"):
            min_confidence = st.slider("Min Confidence %", 0, 100, 70)
            min_volume = st.number_input("Min Daily Volume (M)", min_value=0, value=0, step=1)
            trend_filter = st.multiselect(
                "Trend Filter",
                ['BULLISH', 'BEARISH', 'NEUTRAL', 'WEAK'],
                default=['BULLISH']
            )
        
        st.markdown("### 📊 Display Options")
        top_n = st.number_input("Top N Assets", min_value=10, max_value=100, value=21, step=1)
        show_charts = st.checkbox("Show Candlestick Charts", value=True)
        show_heatmap = st.checkbox("Show Performance Heatmap", value=True)
        
        # Alert Settings
        st.markdown("### 🔔 Alert Settings")
        alert_enabled = st.checkbox("Enable Price Alerts", value=True)
        if alert_enabled:
            alert_threshold = st.slider("Score Threshold for Alerts", 80, 100, 85)
        
        # Paper Trading
        st.markdown("### 💰 Paper Trading")
        st.metric("Portfolio Value", f"₹{st.session_state.portfolio_value:,.2f}")
        if len(st.session_state.trade_history) > 0:
            total_trades = len(st.session_state.trade_history)
            st.metric("Total Trades", total_trades)
        
        st.markdown("---")
        
        # PERFORMANCE HEATMAP
        if 'show_heatmap' in locals() and show_heatmap:
            st.markdown("## 🔥 Performance Heatmap")
            
            # Create heatmap data
            heatmap_data = df_filtered.pivot_table(
                values='combined_score',
                index='asset_type',
                columns='trend',
                aggfunc='mean'
            ).fillna(0)
            
            fig = go.Figure(data=go.Heatmap(
                z=heatmap_data.values,
                x=heatmap_data.columns,
                y=heatmap_data.index,
                colorscale='Viridis',
                text=heatmap_data.values.round(1),
                texttemplate='%{text}',
                textfont={"size": 14},
                colorbar=dict(title="Score")
            ))
            
            fig.update_layout(
                title="Average Score by Asset Type & Trend",
                template='plotly_dark',
                height=400,
                paper_bgcolor='rgba(26, 32, 44, 0.8)',
                plot_bgcolor='rgba(26, 32, 44, 0.8)',
                font=dict(color='#e2e8f0')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # CORRELATION MATRIX
        st.markdown("## 🔗 Score Correlation Analysis")
        
        # Select numeric columns for correlation
        corr_cols = ['technical_score', 'fundamental_score', 'combined_score', 
                     'confidence', 'risk', 'price_change_24h']
        corr_data = df_filtered[corr_cols].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_data.values,
            x=corr_cols,
            y=corr_cols,
            colorscale='RdBu',
            zmid=0,
            text=corr_data.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 12},
            colorbar=dict(title="Correlation")
        ))
        
        fig.update_layout(
            title="Feature Correlation Matrix",
            template='plotly_dark',
            height=500,
            paper_bgcolor='rgba(26, 32, 44, 0.8)',
            plot_bgcolor='rgba(26, 32, 44, 0.8)',
            font=dict(color='#e2e8f0')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # TRADE HISTORY
        if len(st.session_state.trade_history) > 0:
            st.markdown("## 📜 Recent Trade History")
            
            trade_df = pd.DataFrame(st.session_state.trade_history[-10:])
            trade_df['time'] = trade_df['time'].dt.strftime('%Y-%m-%d %H:%M')
            
            st.dataframe(
                trade_df[['symbol', 'type', 'price', 'signal', 'time']],
                use_container_width=True,
                height=300
            )
            
            if st.button("🗑️ Clear Trade History"):
                st.session_state.trade_history = []
                st.rerun()
        
        st.markdown("---")
        
        # ICT CONCEPT BREAKDOWN
        st.markdown("## 🧩 ICT Concept Analysis - Top 5 Assets")
        
        top_5_ict = df_filtered.head(5)
        
        for idx, asset in top_5_ict.iterrows():
            with st.expander(f"📊 {asset['symbol']} - ICT Breakdown"):
                ict_scores = asset['ict_scores']
                
                # Create radar chart
                categories = list(ict_scores.keys())
                values = list(ict_scores.values())
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill='toself',
                    name=asset['symbol'],
                    line_color='#3b82f6'
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100],
                            gridcolor='#2d3748'
                        ),
                        bgcolor='rgba(26, 32, 44, 0.8)'
                    ),
                    showlegend=False,
                    template='plotly_dark',
                    height=400,
                    paper_bgcolor='rgba(26, 32, 44, 0.8)',
                    font=dict(color='#e2e8f0')
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 🔄 Data Refresh")
        if st.button("🔄 Refresh Data Now", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        st.markdown("**💡 Pro Tip:** Focus on STRONG BUY signals during active kill zones!")
        st.markdown("**🎯 Tip:** Add assets to watchlist for tracking!")
    
    # Data Collection Progress
    with st.spinner("🔍 Scanning Markets..."):
        all_assets = []
        
        # Progress tracking
        total_assets = 0
        if 'Indian Stocks' in asset_types:
            total_assets += len(NIFTY_50)
        if 'Cryptocurrencies' in asset_types:
            total_assets += len(TOP_50_CRYPTO)
        if 'Forex' in asset_types:
            total_assets += len(FOREX_PAIRS[:20])
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        processed = 0
        
        # Fetch Indian Stocks
        if 'Indian Stocks' in asset_types:
            status_text.text("📈 Fetching Indian Stocks...")
            for ticker in NIFTY_50:
                data = fetch_stock_data(ticker)
                if data:
                    analyzed = analyze_asset(data, 'Stock', kill_zone)
                    all_assets.append(analyzed)
                processed += 1
                progress_bar.progress(processed / total_assets)
                time.sleep(0.1)  # Rate limiting
        
        # Fetch Cryptocurrencies
        if 'Cryptocurrencies' in asset_types:
            status_text.text("🪙 Fetching Cryptocurrencies...")
            for coin in TOP_50_CRYPTO:
                data = fetch_crypto_data(coin)
                if data:
                    analyzed = analyze_asset(data, 'Crypto', kill_zone)
                    all_assets.append(analyzed)
                processed += 1
                progress_bar.progress(processed / total_assets)
                time.sleep(0.1)
        
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
                time.sleep(0.1)
        
        progress_bar.empty()
        status_text.empty()
    
    if not all_assets:
        st.error("❌ No data available. Please check your internet connection.")
        return
    
    # Create DataFrame
    df = pd.DataFrame(all_assets)
    
    # Apply filters
    df_filtered = df[
        (df['combined_score'] >= min_score) &
        (df['signal'].isin(signal_filter)) &
        (df['risk'] <= max_risk)
    ].sort_values('combined_score', ascending=False).reset_index(drop=True)
    
    # Apply advanced filters
    if 'min_confidence' in locals():
        df_filtered = df_filtered[df_filtered['confidence'] >= min_confidence]
    if 'trend_filter' in locals():
        df_filtered = df_filtered[df_filtered['trend'].isin(trend_filter)]
    
    df_filtered['rank'] = range(1, len(df_filtered) + 1)
    
    # Generate alerts
    if 'alert_enabled' in locals() and alert_enabled:
        high_score_assets = df[df['combined_score'] >= alert_threshold]
        for _, asset in high_score_assets.iterrows():
            alert_msg = f"⚠️ {asset['symbol']}: Score {asset['combined_score']:.1f} - {asset['signal']}"
            if alert_msg not in st.session_state.alerts:
                st.session_state.alerts.append(alert_msg)
    
    # Show alerts
    if st.session_state.alerts:
        with st.expander(f"🔔 Active Alerts ({len(st.session_state.alerts)})", expanded=True):
            for alert in st.session_state.alerts[-10:]:  # Show last 10 alerts
                st.warning(alert)
    
    # Summary Metrics
    st.markdown("## 📊 Market Overview")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Assets Scanned", len(df))
    with col2:
        strong_buy_count = len(df[df['signal'] == '🟢 STRONG BUY'])
        st.metric("Strong Buy Signals", strong_buy_count)
    with col3:
        avg_score = df['combined_score'].mean()
        st.metric("Avg Combined Score", f"{avg_score:.1f}")
    with col4:
        bullish_count = len(df[df['trend'] == 'BULLISH'])
        st.metric("Bullish Assets", bullish_count)
    with col5:
        high_conf = len(df[df['confidence'] >= 80])
        st.metric("High Confidence (>80)", high_conf)
    
    st.markdown("---")
    
    # TOP 21 RECOMMENDATIONS
    st.markdown("## 🏆 TOP 21 RECOMMENDED ASSETS")
    st.markdown("**Premium picks based on ICT analysis + Fundamentals**")
    
    top_21 = df_filtered.head(top_n)
    
    if len(top_21) == 0:
        st.warning("⚠️ No assets match your filter criteria. Try adjusting the filters.")
    else:
        # Display cards for top 21
        for i in range(0, len(top_21), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(top_21):
                    asset = top_21.iloc[i + j]
                    with cols[j]:
                        signal_class = (
                            'signal-strong-buy' if 'STRONG BUY' in asset['signal']
                            else 'signal-buy' if 'BUY' in asset['signal']
                            else 'signal-hold' if 'HOLD' in asset['signal']
                            else 'signal-sell'
                        )
                        
                        # Watchlist button
                        watchlist_key = f"{asset['symbol']}_{i}_{j}"
                        is_in_watchlist = asset['symbol'] in st.session_state.watchlist
                        
                        st.markdown(f"""
                        <div style='background: rgba(26, 32, 44, 0.8); padding: 20px; border-radius: 10px; 
                                    border-left: 4px solid {kill_zone['color']}; margin-bottom: 15px;'>
                            <h3 style='margin: 0; color: #00d4ff !important;'>#{asset['rank']} {asset['symbol']}</h3>
                            <p style='margin: 5px 0; color: #94a3b8; font-size: 14px;'>{asset['name'][:30]}</p>
                            <div style='margin: 10px 0;'>
                                <span class='{signal_class}'>{asset['signal']}</span>
                            </div>
                            <div style='margin-top: 10px;'>
                                <p style='margin: 3px 0;'><strong>Score:</strong> {asset['combined_score']}/100</p>
                                <p style='margin: 3px 0;'><strong>Trend:</strong> {asset['trend']}</p>
                                <p style='margin: 3px 0;'><strong>Risk:</strong> {asset['risk']}/10</p>
                                <p style='margin: 3px 0;'><strong>Type:</strong> {asset['asset_type']}</p>
                                <p style='margin: 3px 0; color: #10b981;'><strong>Target:</strong> ₹{asset.get('target_price', 0):.2f}</p>
                                <p style='margin: 3px 0; color: #ef4444;'><strong>SL:</strong> ₹{asset.get('stop_loss', 0):.2f}</p>
                                <p style='margin: 3px 0;'><strong>Potential:</strong> {asset.get('potential_return', 0):+.2f}%</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col_btn1, col_btn2 = st.columns(2)
                        with col_btn1:
                            if st.button("⭐ Watch" if not is_in_watchlist else "❌ Unwatch", 
                                       key=watchlist_key, use_container_width=True):
                                if is_in_watchlist:
                                    st.session_state.watchlist.remove(asset['symbol'])
                                else:
                                    st.session_state.watchlist.append(asset['symbol'])
                                st.rerun()
                        with col_btn2:
                            if st.button("📊 Trade", key=f"trade_{watchlist_key}", use_container_width=True):
                                # Add to trade history
                                trade = {
                                    'symbol': asset['symbol'],
                                    'type': 'BUY' if 'BUY' in asset['signal'] else 'SELL',
                                    'price': asset.get('price', 0),
                                    'time': datetime.now(),
                                    'signal': asset['signal']
                                }
                                st.session_state.trade_history.append(trade)
                                st.success(f"Added {asset['symbol']} to trade history!")
        
        st.markdown("---")
        
        # DETAILED TABLE
        st.markdown("## 📋 Detailed Analysis Table")
        
        # Prepare display dataframe
        display_cols = [
            'rank', 'symbol', 'name', 'asset_type', 'signal', 'combined_score',
            'technical_score', 'fundamental_score', 'trend', 'risk', 'confidence',
            'price_change_24h'
        ]
        
        display_df = top_21[display_cols].copy()
        display_df.columns = [
            'Rank', 'Symbol', 'Name', 'Type', 'Signal', 'Combined Score',
            'Technical', 'Fundamental', 'Trend', 'Risk', 'Confidence %', '24h Change %'
        ]
        
        # Format numbers
        display_df['Combined Score'] = display_df['Combined Score'].apply(lambda x: f"{x:.1f}")
        display_df['Technical'] = display_df['Technical'].apply(lambda x: f"{x:.1f}")
        display_df['Fundamental'] = display_df['Fundamental'].apply(lambda x: f"{x:.1f}")
        display_df['Confidence %'] = display_df['Confidence %'].apply(lambda x: f"{x:.1f}%")
        display_df['24h Change %'] = display_df['24h Change %'].apply(lambda x: f"{x:+.2f}%")
        
        st.dataframe(
            display_df,
            use_container_width=True,
            height=600
        )
        
        # Download CSV
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            label="📥 Download Full Analysis (CSV)",
            data=csv,
            file_name=f"ICT_Analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
        st.markdown("---")
        
        # CANDLESTICK CHARTS
        if show_charts and 'Indian Stocks' in asset_types:
            st.markdown("## 📈 Interactive Charts - Top 5 Stocks")
            
            top_stocks = df_filtered[df_filtered['asset_type'] == 'Stock'].head(5)
            
            for idx, stock in top_stocks.iterrows():
                with st.expander(f"📊 {stock['symbol']} - {stock['name']}", expanded=(idx == top_stocks.index[0])):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        ticker = stock['symbol'] if '.NS' in stock['symbol'] else f"{stock['symbol']}.NS"
                        chart = create_candlestick_chart(ticker, period="3mo")
                        if chart:
                            st.plotly_chart(chart, use_container_width=True)
                    
                    with col2:
                        st.markdown("### 📊 Key Metrics")
                        st.metric("Combined Score", f"{stock['combined_score']:.1f}/100")
                        st.metric("Signal", stock['signal'])
                        st.metric("Risk Level", f"{stock['risk']}/10")
                        st.metric("Confidence", f"{stock['confidence']:.1f}%")
                        
                        st.markdown("### 🎯 ICT Analysis")
                        ict = stock['ict_scores']
                        for concept, score in list(ict.items())[:5]:
                            st.progress(score / 100, text=f"{concept}: {score:.1f}")
        
        st.markdown("---")
        
        # SECTOR ANALYSIS (for stocks)
        if 'Indian Stocks' in asset_types:
            st.markdown("## 🏭 Sector Performance")
            
            stock_df = df_filtered[df_filtered['asset_type'] == 'Stock']
            if len(stock_df) > 0:
                sector_avg = stock_df.groupby('sector').agg({
                    'combined_score': 'mean',
                    'symbol': 'count'
                }).round(1)
                sector_avg.columns = ['Avg Score', 'Count']
                sector_avg = sector_avg.sort_values('Avg Score', ascending=False)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.dataframe(sector_avg, use_container_width=True)
                
                with col2:
                    fig = go.Figure(data=[
                        go.Bar(
                            x=sector_avg.index,
                            y=sector_avg['Avg Score'],
                            marker_color='#3b82f6',
                            text=sector_avg['Avg Score'],
                            textposition='auto'
                        )
                    ])
                    fig.update_layout(
                        title="Average Score by Sector",
                        template='plotly_dark',
                        height=400,
                        paper_bgcolor='rgba(26, 32, 44, 0.8)',
                        plot_bgcolor='rgba(26, 32, 44, 0.8)',
                        font=dict(color='#e2e8f0')
                    )
                    st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # RISK DISTRIBUTION
        st.markdown("## ⚠️ Risk Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            risk_counts = df_filtered['risk'].value_counts().sort_index()
            fig = go.Figure(data=[
                go.Bar(
                    x=risk_counts.index,
                    y=risk_counts.values,
                    marker_color=['#10b981' if x <= 3 else '#f59e0b' if x <= 6 else '#ef4444' 
                                  for x in risk_counts.index],
                    text=risk_counts.values,
                    textposition='auto'
                )
            ])
            fig.update_layout(
                title="Assets by Risk Level",
                xaxis_title="Risk Level",
                yaxis_title="Count",
                template='plotly_dark',
                height=400,
                paper_bgcolor='rgba(26, 32, 44, 0.8)',
                plot_bgcolor='rgba(26, 32, 44, 0.8)',
                font=dict(color='#e2e8f0')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            signal_counts = df_filtered['signal'].value_counts()
            fig = go.Figure(data=[
                go.Pie(
                    labels=signal_counts.index,
                    values=signal_counts.values,
                    marker=dict(
                        colors=['#10b981', '#34d399', '#fbbf24', '#f87171', '#ef4444', '#9ca3af']
                    ),
                    hole=0.4
                )
            ])
            fig.update_layout(
                title="Signal Distribution",
                template='plotly_dark',
                height=400,
                paper_bgcolor='rgba(26, 32, 44, 0.8)',
                plot_bgcolor='rgba(26, 32, 44, 0.8)',
                font=dict(color='#e2e8f0')
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 20px; color: #94a3b8;'>
        <p><strong>ICT Advanced Analyzer 2026</strong></p>
        <p>Professional Trading Tool | Real-Time Analysis | Multi-Asset Support</p>
        <p style='font-size: 12px;'>⚠️ Disclaimer: This tool is for educational purposes only. Always do your own research before trading.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
