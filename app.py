import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
from datetime import datetime, timedelta
import time
import requests
import warnings
import pytz
import json
import base64
from io import BytesIO
from typing import Dict, List, Tuple, Optional
import hashlib


warnings.filterwarnings('ignore')
IST = pytz.timezone('Asia/Kolkata')


# ═══════════════════════════════════════════════════════════════════════
# ECOPLUS ANALYZER 2026 PRO
# Professional Trading Analysis Platform
# ═══════════════════════════════════════════════════════════════════════


# Page Configuration
st.set_page_config(
   page_title="ECOPLUS Analyzer Pro",
   page_icon="📈",
   layout="wide",
   initial_sidebar_state="expanded"
)


# Custom CSS - Clean Professional Dark Theme
st.markdown("""
<style>
   /* Main Background */
   .stApp {
       background: #000000 !important;
       font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
   }


   /* Sidebar */
   [data-testid="stSidebar"] {
       background: #111111 !important;
       border-right: 1px solid #333333;
   }


   /* Headers - Professional Look */
   h1, h2, h3 {
       color: #FFFFFF !important;
       font-family: 'Inter', sans-serif !important;
       font-weight: 600 !important;
       letter-spacing: -0.5px;
       margin-bottom: 15px !important;
   }


   h1 {
       font-size: 28px !important;
       font-weight: 700 !important;
   }


   h2 {
       font-size: 22px !important;
       font-weight: 600 !important;
       border-bottom: 2px solid #444444;
       padding-bottom: 10px;
   }


   h3 {
       font-size: 18px !important;
       font-weight: 600 !important;
   }


   h4, h5, h6 {
       color: #CCCCCC !important;
       font-weight: 500 !important;
   }


   /* Text Colors */
   p, span, div {
       color: #DDDDDD !important;
   }


   /* Metric Cards - Clean Design */
   [data-testid="stMetric"] {
       background: #1A1A1A !important;
       padding: 20px !important;
       border-radius: 8px !important;
       border: 1px solid #333333 !important;
   }


   [data-testid="stMetricLabel"] {
       color: #999999 !important;
       font-size: 14px !important;
       font-weight: 500 !important;
   }


   [data-testid="stMetricValue"] {
       color: #FFFFFF !important;
       font-size: 24px !important;
       font-weight: 600 !important;
   }


   [data-testid="stMetricDelta"] {
       font-size: 14px !important;
       font-weight: 500 !important;
   }


   /* Tables */
   .dataframe {
       background: #1A1A1A !important;
       border: 1px solid #333333 !important;
       border-radius: 8px !important;
       overflow: hidden !important;
   }


   .dataframe thead {
       background: #222222 !important;
   }


   .dataframe thead th {
       color: #FFFFFF !important;
       font-weight: 600 !important;
       border-bottom: 2px solid #444444 !important;
       padding: 12px 15px !important;
       font-size: 14px !important;
   }


   .dataframe tbody tr {
       border-bottom: 1px solid #333333;
       transition: background-color 0.2s ease;
   }


   .dataframe tbody tr:hover {
       background: #222222 !important;
   }


   .dataframe tbody td {
       color: #DDDDDD !important;
       padding: 10px 15px !important;
       font-size: 13px !important;
   }


   /* Buttons - Clean Professional */
   .stButton > button {
       background: #2D2D2D !important;
       color: white !important;
       border: 1px solid #444444 !important;
       border-radius: 6px !important;
       padding: 10px 24px !important;
       font-weight: 500 !important;
       font-size: 14px !important;
       transition: all 0.2s ease !important;
   }


   .stButton > button:hover {
       background: #3A3A3A !important;
       border-color: #555555 !important;
       transform: none !important;
       box-shadow: none !important;
   }


   .stButton > button:focus {
       background: #3A3A3A !important;
       border-color: #666666 !important;
   }


   /* Primary Button */
   div[data-testid="stButton"]:has(> button[kind="primary"]) > button {
       background: #0066CC !important;
       border-color: #0066CC !important;
       color: white !important;
   }


   div[data-testid="stButton"]:has(> button[kind="primary"]) > button:hover {
       background: #0052A3 !important;
       border-color: #0052A3 !important;
   }


   /* Inputs and Selectboxes */
   .stTextInput > div > div > input,
   .stNumberInput > div > div > input,
   .stSelectbox > div > div > select,
   .stTextArea > div > div > textarea {
       background: #1A1A1A !important;
       border: 1px solid #444444 !important;
       color: #FFFFFF !important;
       border-radius: 6px !important;
       padding: 10px 12px !important;
       font-size: 14px !important;
   }


   .stTextInput > div > div > input:focus,
   .stNumberInput > div > div > input:focus,
   .stSelectbox > div > div > select:focus,
   .stTextArea > div > div > textarea:focus {
       border-color: #666666 !important;
       box-shadow: 0 0 0 1px #666666 !important;
   }


   /* Checkboxes and Radio */
   .stCheckbox > div > label,
   .stRadio > div > label {
       color: #DDDDDD !important;
       font-weight: 400 !important;
       font-size: 14px !important;
   }


   /* Progress Bars */
   .stProgress > div > div > div > div {
       background: #0066CC !important;
   }


   /* Expanders */
   .streamlit-expanderHeader {
       background: #1A1A1A !important;
       border-radius: 6px !important;
       border: 1px solid #333333 !important;
       color: #FFFFFF !important;
       font-weight: 500 !important;
       font-size: 14px !important;
   }


   .streamlit-expanderContent {
       background: #1A1A1A !important;
       border-radius: 0 0 6px 6px !important;
       border: 1px solid #333333 !important;
       border-top: none !important;
   }


   /* Signal Badges - Simplified */
   .signal-strong-buy {
       background: #0A6E0A !important;
       color: white !important;
       padding: 6px 12px !important;
       border-radius: 4px !important;
       font-weight: 500 !important;
       font-size: 12px !important;
   }


   .signal-buy {
       background: #1A8C1A !important;
       color: white !important;
       padding: 5px 10px !important;
       border-radius: 4px !important;
       font-weight: 500 !important;
       font-size: 12px !important;
   }


   .signal-hold {
       background: #B38B00 !important;
       color: #000000 !important;
       padding: 5px 10px !important;
       border-radius: 4px !important;
       font-weight: 500 !important;
       font-size: 12px !important;
   }


   .signal-sell {
       background: #CC3300 !important;
       color: white !important;
       padding: 5px 10px !important;
       border-radius: 4px !important;
       font-weight: 500 !important;
       font-size: 12px !important;
   }


   .signal-strong-sell {
       background: #990000 !important;
       color: white !important;
       padding: 6px 12px !important;
       border-radius: 4px !important;
       font-weight: 500 !important;
       font-size: 12px !important;
   }


   /* Alert Boxes */
   .stAlert {
       border-radius: 6px !important;
       border: 1px solid !important;
       background: #1A1A1A !important;
   }


   [data-baseweb="notification"] {
       background: #1A1A1A !important;
       border-color: #333333 !important;
   }


   /* Success Alert */
   div[data-baseweb="notification"][kind="success"] {
       background: #0A6E0A20 !important;
       border-color: #0A6E0A !important;
   }


   /* Info Alert */
   div[data-baseweb="notification"][kind="info"] {
       background: #0066CC20 !important;
       border-color: #0066CC !important;
   }


   /* Warning Alert */
   div[data-baseweb="notification"][kind="warning"] {
       background: #B38B0020 !important;
       border-color: #B38B00 !important;
   }


   /* Error Alert */
   div[data-baseweb="notification"][kind="error"] {
       background: #CC330020 !important;
       border-color: #CC3300 !important;
   }


   /* Custom Tabs */
   .stTabs [data-baseweb="tab-list"] {
       gap: 0px;
       background-color: #1A1A1A;
       border-radius: 6px;
       border: 1px solid #333333;
       padding: 4px;
   }


   .stTabs [data-baseweb="tab"] {
       background-color: transparent;
       border-radius: 4px;
       padding: 8px 16px;
       color: #999999;
       font-weight: 500;
       font-size: 14px;
       transition: all 0.2s ease;
   }


   .stTabs [data-baseweb="tab"]:hover {
       background-color: #222222;
       color: #CCCCCC;
   }


   .stTabs [aria-selected="true"] {
       background: #2D2D2D !important;
       color: #FFFFFF !important;
   }


   /* Tooltips */
   .tooltip {
       position: relative;
       display: inline-block;
       cursor: help;
   }


   .tooltip .tooltiptext {
       visibility: hidden;
       width: 250px;
       background-color: #1A1A1A;
       color: #DDDDDD;
       text-align: center;
       border-radius: 4px;
       padding: 10px;
       position: absolute;
       z-index: 1000;
       bottom: 125%;
       left: 50%;
       margin-left: -125px;
       opacity: 0;
       transition: opacity 0.3s;
       border: 1px solid #333333;
       font-size: 12px;
       font-weight: 400;
   }


   .tooltip:hover .tooltiptext {
       visibility: visible;
       opacity: 1;
   }


   /* Chart Container */
   .chart-container {
       background: #1A1A1A;
       border-radius: 8px;
       padding: 20px;
       margin: 20px 0;
       border: 1px solid #333333;
   }


   /* Footer */
   .footer {
       text-align: center;
       padding: 25px;
       color: #666666;
       font-size: 12px;
       border-top: 1px solid #333333;
       margin-top: 40px;
       background: #111111;
   }


   /* Custom Scrollbar */
   ::-webkit-scrollbar {
       width: 8px;
       height: 8px;
   }


   ::-webkit-scrollbar-track {
       background: #1A1A1A;
       border-radius: 4px;
   }


   ::-webkit-scrollbar-thumb {
       background: #444444;
       border-radius: 4px;
   }


   ::-webkit-scrollbar-thumb:hover {
       background: #555555;
   }


   /* Loading Animation */
   .loading {
       display: inline-block;
       width: 18px;
       height: 18px;
       border: 2px solid #444444;
       border-radius: 50%;
       border-top-color: #0066CC;
       animation: spin 1s ease-in-out infinite;
       margin-right: 8px;
   }


   @keyframes spin {
       to { transform: rotate(360deg); }
   }


   /* Section Headers */
   .section-header {
       display: flex;
       align-items: center;
       justify-content: space-between;
       margin-bottom: 20px;
       padding-bottom: 10px;
       border-bottom: 1px solid #333333;
   }


   .section-title {
       color: #FFFFFF;
       font-size: 18px;
       font-weight: 600;
   }


   /* Status Badges */
   .status-badge {
       display: inline-block;
       padding: 4px 10px;
       border-radius: 12px;
       font-size: 11px;
       font-weight: 500;
       text-transform: uppercase;
       letter-spacing: 0.5px;
   }


   .status-active {
       background: #0A6E0A;
       color: white;
   }


   .status-inactive {
       background: #666666;
       color: white;
   }


   .status-warning {
       background: #B38B00;
       color: white;
   }


   /* Card Design */
   .card {
       background: #1A1A1A;
       border: 1px solid #333333;
       border-radius: 8px;
       padding: 20px;
       margin-bottom: 16px;
       transition: border-color 0.2s ease;
   }


   .card:hover {
       border-color: #444444;
   }


   .card-title {
       color: #FFFFFF;
       font-size: 16px;
       font-weight: 600;
       margin-bottom: 12px;
   }


   .card-content {
       color: #CCCCCC;
       font-size: 14px;
       line-height: 1.5;
   }


   /* Divider */
   .divider {
       height: 1px;
       background: #333333;
       margin: 20px 0;
       border: none;
   }


   /* Small Text */
   .small-text {
       font-size: 12px;
       color: #999999;
   }


   /* Link Styling */
   a {
       color: #0066CC !important;
       text-decoration: none;
       transition: color 0.2s ease;
   }


   a:hover {
       color: #0088FF !important;
       text-decoration: underline;
   }
</style>
""", unsafe_allow_html=True)


# ==================== CONFIGURATIONS ====================
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


TOP_CRYPTO = [
   'BTC-USD', 'ETH-USD', 'BNB-USD', 'SOL-USD', 'XRP-USD',
   'ADA-USD', 'DOGE-USD', 'DOT-USD', 'MATIC-USD', 'SHIB-USD'
]


FOREX_PAIRS = [
   'EURUSD=X', 'USDJPY=X', 'GBPUSD=X', 'AUDUSD=X', 'USDCAD=X',
   'USDCHF=X', 'NZDUSD=X', 'EURJPY=X', 'GBPJPY=X', 'EURGBP=X'
]


ICT_CONCEPTS = {
   'Market Structure': {'weight': 100, 'color': '#0066CC'},
   'Order Blocks': {'weight': 100, 'color': '#CC3300'},
   'Fair Value Gaps': {'weight': 95, 'color': '#0A6E0A'},
   'Liquidity': {'weight': 90, 'color': '#B38B00'},
   'Optimal Trade Entry': {'weight': 80, 'color': '#663399'},
   'Kill Zones': {'weight': 70, 'color': '#990099'}
}




# ==================== SIMPLIFIED ICT DETECTION ====================
def detect_simple_patterns(df):
   """Simple pattern detection"""
   patterns = []


   # Bullish pattern
   if len(df) > 3:
       if df['Close'].iloc[-1] > df['Close'].iloc[-2] > df['Close'].iloc[-3]:
           patterns.append('Bullish Trend')


       # Bearish pattern
       if df['Close'].iloc[-1] < df['Close'].iloc[-2] < df['Close'].iloc[-3]:
           patterns.append('Bearish Trend')


   return patterns




def get_support_resistance(df):
   """Calculate support and resistance levels"""
   if len(df) < 20:
       return {'support': 0, 'resistance': 0}


   recent = df.tail(20)
   support = recent['Low'].min()
   resistance = recent['High'].max()


   return {'support': support, 'resistance': resistance}




# ==================== TECHNICAL INDICATORS ====================
def calculate_simple_rsi(prices, period=14):
   """Simple RSI calculation"""
   if len(prices) < period:
       return 50


   delta = prices.diff()
   gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
   loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()


   rs = gain / loss
   rsi = 100 - (100 / (1 + rs))
   return rsi.iloc[-1] if not rsi.empty else 50




def calculate_moving_averages(df):
   """Calculate moving averages"""
   if len(df) >= 50:
       ma_20 = df['Close'].rolling(20).mean().iloc[-1]
       ma_50 = df['Close'].rolling(50).mean().iloc[-1]
   else:
       ma_20 = df['Close'].mean()
       ma_50 = df['Close'].mean()


   return {'MA20': ma_20, 'MA50': ma_50}




# ==================== DATA FETCHING ====================
@st.cache_data(ttl=300)
def fetch_stock_data(ticker):
   """Fetch stock data"""
   try:
       stock = yf.Ticker(ticker)
       hist = stock.history(period="1mo")


       if hist.empty:
           return None


       info = stock.info


       # Calculate indicators
       close = hist['Close']
       rsi = calculate_simple_rsi(close)
       ma = calculate_moving_averages(hist)
       patterns = detect_simple_patterns(hist)
       sr = get_support_resistance(hist)


       return {
           'symbol': ticker.replace('.NS', ''),
           'name': info.get('longName', ticker),
           'price': info.get('currentPrice', close.iloc[-1]),
           'change': ((close.iloc[-1] - close.iloc[-2]) / close.iloc[-2] * 100) if len(close) > 1 else 0,
           'volume': info.get('volume', 0),
           'rsi': rsi,
           'ma20': ma['MA20'],
           'ma50': ma['MA50'],
           'patterns': patterns,
           'support': sr['support'],
           'resistance': sr['resistance'],
           'market_cap': info.get('marketCap', 0),
           'pe_ratio': info.get('trailingPE', 0),
           'sector': info.get('sector', 'Unknown')
       }
   except:
       return None




@st.cache_data(ttl=300)
def fetch_crypto_data(ticker):
   """Fetch crypto data"""
   try:
       crypto = yf.Ticker(ticker)
       hist = crypto.history(period="1mo")


       if hist.empty:
           return None


       close = hist['Close']
       rsi = calculate_simple_rsi(close)
       ma = calculate_moving_averages(hist)
       patterns = detect_simple_patterns(hist)


       return {
           'symbol': ticker.replace('-USD', ''),
           'name': ticker,
           'price': close.iloc[-1],
           'change': ((close.iloc[-1] - close.iloc[-2]) / close.iloc[-2] * 100) if len(close) > 1 else 0,
           'volume': hist['Volume'].iloc[-1] if 'Volume' in hist.columns else 0,
           'rsi': rsi,
           'ma20': ma['MA20'],
           'ma50': ma['MA50'],
           'patterns': patterns,
           'type': 'Crypto'
       }
   except:
       return None




# ==================== ANALYSIS FUNCTIONS ====================
def analyze_asset(asset_data, asset_type):
   """Analyze asset and generate signal"""
   if not asset_data:
       return None


   score = 50  # Base score


   # RSI based scoring
   rsi = asset_data.get('rsi', 50)
   if 30 <= rsi <= 70:
       score += 10
   elif 40 <= rsi <= 60:
       score += 15


   # Price change based scoring
   change = asset_data.get('change', 0)
   if abs(change) < 5:  # Moderate volatility
       score += 10


   # Pattern based scoring
   patterns = asset_data.get('patterns', [])
   if 'Bullish Trend' in patterns:
       score += 15
   elif 'Bearish Trend' in patterns:
       score -= 10


   # Volume check
   volume = asset_data.get('volume', 0)
   if volume > 1000000:  # Good liquidity
       score += 5


   # Generate signal
   if score >= 80:
       signal = '🟢 STRONG BUY'
       color = 'signal-strong-buy'
   elif score >= 70:
       signal = '🟢 BUY'
       color = 'signal-buy'
   elif score >= 60:
       signal = '🟡 HOLD'
       color = 'signal-hold'
   elif score >= 50:
       signal = '🔴 SELL'
       color = 'signal-sell'
   else:
       signal = '🔴 STRONG SELL'
       color = 'signal-strong-sell'


   # Determine trend
   if change > 0:
       trend = 'BULLISH'
   elif change < 0:
       trend = 'BEARISH'
   else:
       trend = 'NEUTRAL'


   return {
       **asset_data,
       'score': score,
       'signal': signal,
       'signal_color': color,
       'trend': trend,
       'asset_type': asset_type
   }




# ==================== CHART FUNCTIONS ====================
def create_simple_chart(ticker, period="1mo"):
   """Create simple candlestick chart"""
   try:
       df = yf.download(ticker, period=period, progress=False)


       if df.empty:
           return None


       # Create figure
       fig = go.Figure(data=[
           go.Candlestick(
               x=df.index,
               open=df['Open'],
               high=df['High'],
               low=df['Low'],
               close=df['Close'],
               name='Price',
               increasing_line_color='#0A6E0A',
               decreasing_line_color='#CC3300'
           )
       ])


       # Add moving averages
       df['MA20'] = df['Close'].rolling(20).mean()
       df['MA50'] = df['Close'].rolling(50).mean()


       fig.add_trace(go.Scatter(
           x=df.index, y=df['MA20'],
           mode='lines',
           name='MA 20',
           line=dict(color='#0066CC', width=1)
       ))


       if len(df) >= 50:
           fig.add_trace(go.Scatter(
               x=df.index, y=df['MA50'],
               mode='lines',
               name='MA 50',
               line=dict(color='#B38B00', width=1)
           ))


       # Update layout
       fig.update_layout(
           title=f"{ticker} - Price Chart",
           template='plotly_dark',
           height=500,
           xaxis_rangeslider_visible=False,
           paper_bgcolor='#1A1A1A',
           plot_bgcolor='#1A1A1A',
           font=dict(color='#DDDDDD'),
           showlegend=True,
           legend=dict(
               orientation="h",
               yanchor="bottom",
               y=1.02,
               xanchor="right",
               x=1
           )
       )


       fig.update_xaxes(
           showgrid=True,
           gridwidth=1,
           gridcolor='#333333'
       )


       fig.update_yaxes(
           showgrid=True,
           gridwidth=1,
           gridcolor='#333333'
       )


       return fig
   except:
       return None




# ==================== MAIN APPLICATION ====================
def main():
   # Initialize session state
   if 'watchlist' not in st.session_state:
       st.session_state.watchlist = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS']


   # Header
   st.markdown("""
   <div class="section-header">
       <h1>📈 ECOPLUS ANALYZER PRO</h1>
       <div class="small-text">Professional Trading Analysis Platform</div>
   </div>
   """, unsafe_allow_html=True)


   # Current time
   current_time = datetime.now(IST).strftime("%d %b %Y, %I:%M %p")
   st.markdown(f"<div class='small-text' style='text-align: right;'>🕒 {current_time} IST</div>",
               unsafe_allow_html=True)


   st.markdown("---")


   # Main tabs
   tabs = st.tabs(["Dashboard", "Market Analysis", "Portfolio", "Settings"])


   with tabs[0]:  # Dashboard
       render_dashboard()


   with tabs[1]:  # Market Analysis
       render_market_analysis()


   with tabs[2]:  # Portfolio
       render_portfolio()


   with tabs[3]:  # Settings
       render_settings()


   # Footer
   st.markdown("---")
   st.markdown("""
   <div class="footer">
       <div>ECOPLUS Analyzer Pro 2026 | Professional Trading Tool</div>
       <div class="small-text" style="margin-top: 10px;">
           For educational purposes only. Past performance is not indicative of future results.
       </div>
   </div>
   """, unsafe_allow_html=True)




def render_dashboard():
   """Render dashboard"""
   col1, col2, col3, col4 = st.columns(4)


   with col1:
       st.metric("NIFTY 50", "21,850", "+0.8%")


   with col2:
       st.metric("SENSEX", "72,450", "+0.7%")


   with col3:
       st.metric("BTC/USD", "$42,150", "+2.1%")


   with col4:
       st.metric("Market Sentiment", "Neutral", "52% Bullish")


   st.markdown("---")


   # Quick Analysis
   st.markdown("### Quick Analysis")


   col1, col2 = st.columns([2, 1])


   with col1:
       symbol = st.text_input("Enter Symbol:", "RELIANCE.NS")
       if st.button("Analyze", type="primary"):
           with st.spinner("Analyzing..."):
               data = fetch_stock_data(symbol)
               if data:
                   analysis = analyze_asset(data, 'Stock')
                   if analysis:
                       display_analysis_results(analysis)
               else:
                   st.error("Unable to fetch data for this symbol")


   with col2:
       st.markdown("""
       <div class="card">
           <div class="card-title">Market Hours</div>
           <div class="card-content">
               <div>🇮🇳 NSE: 9:15 AM - 3:30 PM</div>
               <div>🇺🇸 NYSE: 9:30 PM - 4:00 AM</div>
               <div>🇬🇧 LSE: 1:30 PM - 10:00 PM</div>
           </div>
       </div>
       """, unsafe_allow_html=True)


   st.markdown("---")


   # Top Picks
   st.markdown("### Today's Top Picks")


   # Sample top picks
   top_picks = [
       {"symbol": "RELIANCE.NS", "name": "Reliance Industries", "price": "₹2,415", "change": "+1.2%", "signal": "BUY"},
       {"symbol": "TCS.NS", "name": "Tata Consultancy", "price": "₹3,845", "change": "+0.8%", "signal": "BUY"},
       {"symbol": "INFY.NS", "name": "Infosys", "price": "₹1,520", "change": "-0.5%", "signal": "HOLD"},
       {"symbol": "HDFCBANK.NS", "name": "HDFC Bank", "price": "₹1,650", "change": "+0.9%", "signal": "BUY"},
       {"symbol": "BITCOIN", "name": "Bitcoin", "price": "$42,150", "change": "+2.1%", "signal": "STRONG BUY"},
   ]


   for pick in top_picks:
       col1, col2, col3, col4 = st.columns([1, 2, 1, 1])
       with col1:
           st.write(f"**{pick['symbol']}**")
       with col2:
           st.write(pick['name'])
       with col3:
           st.write(f"{pick['price']} ({pick['change']})")
       with col4:
           if 'STRONG' in pick['signal']:
               st.markdown(f"<span class='signal-strong-buy'>{pick['signal']}</span>", unsafe_allow_html=True)
           elif 'BUY' in pick['signal']:
               st.markdown(f"<span class='signal-buy'>{pick['signal']}</span>", unsafe_allow_html=True)
           else:
               st.markdown(f"<span class='signal-hold'>{pick['signal']}</span>", unsafe_allow_html=True)
       st.markdown("---")




def render_market_analysis():
   """Render market analysis"""
   st.markdown("### Market Analysis")


   # Analysis type
   analysis_type = st.selectbox(
       "Select Analysis Type:",
       ["Stock Analysis", "Crypto Analysis", "Technical Analysis", "Pattern Detection"]
   )


   if analysis_type == "Stock Analysis":
       render_stock_analysis()
   elif analysis_type == "Crypto Analysis":
       render_crypto_analysis()
   elif analysis_type == "Technical Analysis":
       render_technical_analysis()
   elif analysis_type == "Pattern Detection":
       render_pattern_analysis()




def render_stock_analysis():
   """Render stock analysis"""
   selected_stocks = st.multiselect(
       "Select Stocks:",
       NIFTY_50[:10],
       default=['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS']
   )


   if st.button("Analyze Selected Stocks", type="primary"):
       with st.spinner("Fetching data..."):
           results = []
           for stock in selected_stocks:
               data = fetch_stock_data(stock)
               if data:
                   analysis = analyze_asset(data, 'Stock')
                   if analysis:
                       results.append(analysis)


           if results:
               display_stock_results(results)




def render_crypto_analysis():
   """Render crypto analysis"""
   selected_crypto = st.multiselect(
       "Select Cryptocurrencies:",
       TOP_CRYPTO,
       default=['BTC-USD', 'ETH-USD', 'BNB-USD']
   )


   if st.button("Analyze Selected Crypto", type="primary"):
       with st.spinner("Fetching data..."):
           results = []
           for crypto in selected_crypto:
               data = fetch_crypto_data(crypto)
               if data:
                   analysis = analyze_asset(data, 'Crypto')
                   if analysis:
                       results.append(analysis)


           if results:
               display_crypto_results(results)




def render_technical_analysis():
   """Render technical analysis"""
   symbol = st.text_input("Enter Symbol for Technical Analysis:", "RELIANCE.NS")


   if st.button("Generate Technical Analysis", type="primary"):
       with st.spinner("Generating analysis..."):
           chart = create_simple_chart(symbol)
           if chart:
               st.plotly_chart(chart, use_container_width=True)


               # Fetch data for indicators
               data = fetch_stock_data(symbol)
               if data:
                   display_technical_indicators(data)




def render_pattern_analysis():
   """Render pattern analysis"""
   symbol = st.text_input("Enter Symbol for Pattern Analysis:", "RELIANCE.NS")


   if st.button("Detect Patterns", type="primary"):
       with st.spinner("Detecting patterns..."):
           data = fetch_stock_data(symbol)
           if data:
               patterns = data.get('patterns', [])


               if patterns:
                   st.success("Patterns Detected:")
                   for pattern in patterns:
                       st.write(f"• {pattern}")
               else:
                   st.info("No clear patterns detected")


               # Display support/resistance
               st.markdown("### Support & Resistance")
               col1, col2 = st.columns(2)
               with col1:
                   st.metric("Support", f"₹{data.get('support', 0):.2f}")
               with col2:
                   st.metric("Resistance", f"₹{data.get('resistance', 0):.2f}")




def render_portfolio():
   """Render portfolio"""
   st.markdown("### Portfolio Management")


   # Add position
   with st.expander("Add New Position", expanded=False):
       col1, col2, col3 = st.columns(3)


       with col1:
           symbol = st.text_input("Symbol", "RELIANCE.NS")
           qty = st.number_input("Quantity", min_value=1, value=100)


       with col2:
           buy_price = st.number_input("Buy Price", min_value=0.0, value=2400.0)
           current_price = st.number_input("Current Price", min_value=0.0, value=2415.0)


       with col3:
           asset_type = st.selectbox("Asset Type", ["Stock", "Crypto", "ETF"])
           if st.button("Add to Portfolio", type="primary"):
               st.success(f"Added {qty} shares of {symbol} to portfolio")


   st.markdown("---")


   # Portfolio summary
   st.markdown("### Portfolio Summary")


   col1, col2, col3, col4 = st.columns(4)


   with col1:
       st.metric("Total Value", "₹1,24,560")


   with col2:
       st.metric("Total P&L", "₹12,450", "+11.1%")


   with col3:
       st.metric("Today's P&L", "₹1,250", "+1.0%")


   with col4:
       st.metric("Positions", "8")


   st.markdown("---")


   # Sample portfolio table
   st.markdown("### Current Positions")


   portfolio_data = {
       'Symbol': ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'BTC-USD'],
       'Quantity': [100, 50, 200, 150, 0.5],
       'Avg Cost': [2400, 3800, 1600, 1500, 38000],
       'Current Price': [2415, 3845, 1650, 1520, 42150],
       'P&L': [1500, 2250, 10000, 3000, 2075],
       'P&L %': [0.6, 1.2, 3.1, 1.3, 5.5]
   }


   portfolio_df = pd.DataFrame(portfolio_data)
   st.dataframe(portfolio_df, use_container_width=True)




def render_settings():
   """Render settings"""
   st.markdown("### Settings & Configuration")


   # Theme settings
   with st.expander("Display Settings", expanded=True):
       theme = st.selectbox("Theme", ["Dark", "Light", "System Default"])
       refresh_rate = st.selectbox("Data Refresh Rate", ["5 minutes", "15 minutes", "30 minutes", "1 hour"])


   # Notification settings
   with st.expander("Notification Settings", expanded=False):
       email_alerts = st.checkbox("Email Alerts", value=False)
       price_alerts = st.checkbox("Price Alerts", value=True)
       rsi_alerts = st.checkbox("RSI Alerts", value=True)


   # Data settings
   with st.expander("Data Settings", expanded=False):
       cache_duration = st.slider("Cache Duration (minutes)", 5, 60, 15)
       historical_data = st.selectbox("Historical Data Period", ["1 month", "3 months", "6 months", "1 year"])


   if st.button("Save Settings", type="primary"):
       st.success("Settings saved successfully!")




def display_analysis_results(analysis):
   """Display analysis results"""
   st.markdown("### Analysis Results")


   col1, col2, col3 = st.columns(3)


   with col1:
       st.metric("Current Price", f"₹{analysis['price']:.2f}")
       st.metric("24h Change", f"{analysis['change']:.2f}%")


   with col2:
       st.metric("RSI", f"{analysis['rsi']:.1f}")
       st.metric("MA20", f"₹{analysis['ma20']:.2f}")


   with col3:
       st.metric("Analysis Score", f"{analysis['score']}/100")
       st.markdown(f"<span class='{analysis['signal_color']}' style='font-size: 16px;'>{analysis['signal']}</span>",
                   unsafe_allow_html=True)


   st.markdown("---")


   # Additional info
   col1, col2 = st.columns(2)


   with col1:
       st.markdown("**Market Cap:**")
       st.write(f"₹{analysis.get('market_cap', 0):,.0f}")


       st.markdown("**P/E Ratio:**")
       st.write(f"{analysis.get('pe_ratio', 0):.2f}")


   with col2:
       st.markdown("**Sector:**")
       st.write(analysis.get('sector', 'Unknown'))


       st.markdown("**Trend:**")
       st.write(analysis['trend'])




def display_stock_results(results):
   """Display stock analysis results"""
   for result in results:
       st.markdown(f"### {result['symbol']} - {result['name']}")


       col1, col2, col3, col4 = st.columns(4)


       with col1:
           st.metric("Price", f"₹{result['price']:.2f}")


       with col2:
           st.metric("Change", f"{result['change']:.2f}%")


       with col3:
           st.metric("RSI", f"{result['rsi']:.1f}")


       with col4:
           st.markdown(f"<span class='{result['signal_color']}'>{result['signal']}</span>", unsafe_allow_html=True)


       st.markdown("---")




def display_crypto_results(results):
   """Display crypto analysis results"""
   for result in results:
       st.markdown(f"### {result['symbol']} - {result['name']}")


       col1, col2, col3, col4 = st.columns(4)


       with col1:
           st.metric("Price", f"${result['price']:.2f}")


       with col2:
           st.metric("Change", f"{result['change']:.2f}%")


       with col3:
           st.metric("RSI", f"{result['rsi']:.1f}")


       with col4:
           st.markdown(f"<span class='{result['signal_color']}'>{result['signal']}</span>", unsafe_allow_html=True)


       st.markdown("---")




def display_technical_indicators(data):
   """Display technical indicators"""
   st.markdown("### Technical Indicators")


   col1, col2, col3, col4 = st.columns(4)


   with col1:
       st.metric("RSI", f"{data['rsi']:.1f}")
       if data['rsi'] > 70:
           st.write("Overbought")
       elif data['rsi'] < 30:
           st.write("Oversold")
       else:
           st.write("Neutral")


   with col2:
       st.metric("MA20", f"₹{data['ma20']:.2f}")
       st.metric("MA50", f"₹{data['ma50']:.2f}")


   with col3:
       price_vs_ma20 = ((data['price'] - data['ma20']) / data['ma20'] * 100)
       st.metric("Price vs MA20", f"{price_vs_ma20:.2f}%")


   with col4:
       if data['patterns']:
           st.write("Patterns Detected:")
           for pattern in data['patterns']:
               st.write(f"• {pattern}")
       else:
           st.write("No clear patterns")




# ==================== APPLICATION INITIALIZATION ====================
if __name__ == "__main__":
   main()
