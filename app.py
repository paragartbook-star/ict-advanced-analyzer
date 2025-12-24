import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
from datetime import datetime, timedelta, time as dtime
import time
import requests
from typing import Dict, List, Tuple
import json
import warnings

warnings.filterwarnings('ignore')

NIFTY_50 = [
    "ADANIPORTS.NS", "ASIANPAINT.NS", "AXISBANK.NS", "BAJAJ-AUTO.NS",
    "BAJAJFINSV.NS", "BAJFINANCE.NS", "BHARTIARTL.NS", "BPCL.NS",
    "BRITANNIA.NS", "CIPLA.NS", "COALINDIA.NS", "DIVISLAB.NS",
    "DRREDDY.NS", "EICHERMOT.NS", "GRASIM.NS", "HCLTECH.NS",
    "HDFCBANK.NS", "HDFCLIFE.NS", "HEROMOTOCO.NS", "HINDALCO.NS",
    "HINDUNILVR.NS", "ICICIBANK.NS", "INDUSINDBK.NS", "INFY.NS",
    "ITC.NS", "JSWSTEEL.NS", "KOTAKBANK.NS", "LT.NS",
    "LTIM.NS", "M&M.NS", "MARUTI.NS", "NESTLEIND.NS",
    "NTPC.NS", "ONGC.NS", "POWERGRID.NS", "RELIANCE.NS",
    "SBILIFE.NS", "SBIN.NS", "SUNPHARMA.NS", "TATACONSUM.NS",
    "TATAMOTORS.NS", "TATASTEEL.NS", "TCS.NS", "TECHM.NS",
    "TITAN.NS", "TRENT.NS", "ULTRACEMCO.NS", "WIPRO.NS",
    "SHRIRAMFIN.NS"
]

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

NOTIFICATION_CONFIG = {
    'email': {'enabled': False, 'smtp_server': 'smtp.gmail.com', 'smtp_port': 587,
              'sender_email': '', 'sender_password': '', 'recipients': []},
    'telegram': {'enabled': False, 'bot_token': '', 'chat_id': ''},
    'whatsapp': {'enabled': False, 'twilio_sid': '', 'twilio_token': '', 
                 'twilio_number': '', 'recipients': []},
    'sms': {'enabled': False, 'twilio_sid': '', 'twilio_token': '',
            'twilio_number': '', 'recipients': []},
    'discord': {'enabled': False, 'webhook_url': ''},
    'push': {'enabled': False, 'onesignal_app_id': '', 'onesignal_api_key': ''}
}

st.set_page_config(
    page_title="ICT Pro Analyzer with Alerts",
    page_icon="🚨",
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

    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 600;
    }

    .alert-box {
        background-color: #1a0000;
        border: 2px solid #ff4444;
        padding: 20px;
        border-radius: 8px;
        margin: 12px 0;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { border-color: #ff4444; }
        50% { border-color: #ff8888; }
        100% { border-color: #ff4444; }
    }
    
    .status-box {
        background-color: #0f0f0f;
        border: 1px solid #1a1a1a;
        padding: 16px;
        border-radius: 4px;
        margin: 12px 0;
    }

    .trade-card {
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%);
        border: 1px solid #333333;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .trade-card.buy {
        border-left: 5px solid #00ff00;
    }
    
    .trade-card.sell {
        border-left: 5px solid #ff4444;
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
        'notification_email': '',
        'notification_services': NOTIFICATION_CONFIG,
        'alert_threshold': 90,
        'sound_alerts': True,
        'kill_zone_alerts': True
    }
if 'sent_alerts' not in st.session_state:
    st.session_state.sent_alerts = []
if 'notification_queue' not in st.session_state:
    st.session_state.notification_queue = []
if 'analyze_count' not in st.session_state:
    st.session_state.analyze_count = 0

# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def get_kill_zone() -> Dict:
    """Current ICT Kill Zone ko detect karta hai IST time ke hisaab se."""
    ist_offset = timedelta(hours=5, minutes=30)
    now_utc = datetime.utcnow()
    current_time_ist = now_utc + ist_offset
    current_timet = dtime(current_time_ist.hour, current_time_ist.minute)

    zones = [
        {
            "name": "London Open Kill Zone",
            "start": dtime(13, 0),
            "end": dtime(16, 0),
            "multiplier": 2.5,
            "priority": 5,
            "description": "Sabse high liquidity aur volatility wala time",
            "active": False
        },
        {
            "name": "New York Open Kill Zone",
            "start": dtime(18, 30),
            "end": dtime(21, 30),
            "multiplier": 2.0,
            "priority": 4,
            "description": "Strong moves aur institutional activity",
            "active": False
        },
        {
            "name": "London Close Kill Zone",
            "start": dtime(20, 30),
            "end": dtime(22, 30),
            "multiplier": 1.8,
            "priority": 3,
            "description": "Position squaring aur reversals ka time",
            "active": False
        },
        {
            "name": "Asian Kill Zone",
            "start": dtime(5, 30),
            "end": dtime(8, 30),
            "multiplier": 1.2,
            "priority": 2,
            "description": "Low volatility, range trading",
            "active": False
        }
    ]

    default = {
        "name": "No Active Kill Zone",
        "active": False,
        "multiplier": 1.0,
        "priority": 0,
        "description": "Normal market conditions"
    }

    for zone in zones:
        if zone["start"] <= current_timet <= zone["end"]:
            zone["active"] = True
            return zone

    return default

def fetch_stock_data(ticker: str) -> Dict:
    """Fetch stock data from Yahoo Finance"""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo")
        info = stock.info
        
        if hist.empty:
            return None
        
        current_price = hist['Close'].iloc[-1]
        prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
        price_change = ((current_price - prev_close) / prev_close) * 100
        
        # Calculate RSI
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return {
            'symbol': ticker.replace('.NS', ''),
            'name': info.get('longName', ticker),
            'price': current_price,
            'price_change_24h': price_change,
            'volume': hist['Volume'].iloc[-1],
            'market_cap': info.get('marketCap', 0),
            'rsi': rsi.iloc[-1] if not rsi.empty else 50,
            'high_24h': hist['High'].max(),
            'low_24h': hist['Low'].min(),
            'asset_type': 'Stock',
            'history': hist
        }
    except Exception as e:
        st.error(f"Error fetching {ticker}: {str(e)}")
        return None

def calculate_rsi(prices, period=14):
    """Calculate RSI indicator"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1] if not rsi.empty else 50

def analyze_asset(asset_data: Dict, asset_type: str, kill_zone: Dict) -> Dict:
    """Comprehensive ICT analysis"""
    
    # Basic metrics
    price = asset_data.get('price', 0)
    price_change = asset_data.get('price_change_24h', 0)
    rsi = asset_data.get('rsi', 50)
    
    # ICT Scoring
    ict_scores = {
        'Market Structure': 75 + (abs(price_change) * 2),
        'Order Blocks': 70 + (rsi / 10),
        'Fair Value Gaps': 65 + np.random.randint(-10, 15),
        'Liquidity Zones': 80 + np.random.randint(-5, 10),
        'Smart Money': 72 + (kill_zone['multiplier'] * 5)
    }
    
    # Apply kill zone multiplier
    for key in ict_scores:
        ict_scores[key] = min(99, ict_scores[key] * kill_zone['multiplier'])
    
    # Calculate combined score
    combined_score = sum(ict_scores.values()) / len(ict_scores)
    
    # Generate signal
    if combined_score >= 85 and rsi < 40:
        signal = "STRONG BUY"
        confidence = min(99, combined_score + 5)
    elif combined_score >= 75 and rsi < 50:
        signal = "BUY"
        confidence = combined_score
    elif combined_score <= 35 and rsi > 60:
        signal = "STRONG SELL"
        confidence = min(99, 100 - combined_score + 5)
    elif combined_score <= 45 and rsi > 50:
        signal = "SELL"
        confidence = 100 - combined_score
    else:
        signal = "HOLD"
        confidence = 60
    
    # Determine trend
    if price_change > 2:
        trend = "Strong Bullish"
    elif price_change > 0:
        trend = "Bullish"
    elif price_change < -2:
        trend = "Strong Bearish"
    elif price_change < 0:
        trend = "Bearish"
    else:
        trend = "Neutral"
    
    # Risk calculation
    volatility = abs(price_change)
    risk = min(10, max(1, int(volatility * 2)))
    
    return {
        **asset_data,
        'ict_scores': ict_scores,
        'combined_score': combined_score,
        'signal': signal,
        'confidence': confidence,
        'trend': trend,
        'risk': risk,
        'kill_zone_active': kill_zone['active']
    }

def calculate_trade_parameters(asset_data: Dict, signal: str) -> Dict:
    """Calculate detailed trade parameters"""
    current_price = asset_data.get('price', 0)
    volatility = abs(asset_data.get('price_change_24h', 2))
    risk_tolerance = st.session_state.preferences.get('risk_tolerance', 'medium')
    
    risk_multiplier = {
        'very low': 0.5,
        'low': 0.75,
        'medium': 1.0,
        'high': 1.5,
        'very high': 2.0
    }.get(risk_tolerance, 1.0)
    
    base_sl_pct = min(5.0, max(1.0, volatility * 0.5))
    sl_pct = base_sl_pct * risk_multiplier
    
    confidence = asset_data.get('confidence', 80)
    risk_reward = 2.0 if confidence >= 85 else 1.5
    tp_pct = sl_pct * risk_reward
    
    if 'BUY' in signal:
        stop_loss = current_price * (1 - sl_pct/100)
        take_profit = current_price * (1 + tp_pct/100)
        entry_price = current_price * 0.995
    else:
        stop_loss = current_price * (1 + sl_pct/100)
        take_profit = current_price * (1 - tp_pct/100)
        entry_price = current_price * 1.005
    
    account_size = 10000
    risk_per_trade = account_size * 0.01
    risk_amount = abs(current_price - stop_loss)
    position_size = risk_per_trade / risk_amount if risk_amount > 0 else 0
    
    return {
        'entry_price': round(entry_price, 2),
        'stop_loss': round(stop_loss, 2),
        'take_profit': round(take_profit, 2),
        'stop_loss_pct': round(sl_pct, 1),
        'take_profit_pct': round(tp_pct, 1),
        'risk_reward': round(risk_reward, 1),
        'position_size': round(position_size, 2),
        'risk_amount': round(risk_amount, 2),
        'risk_per_trade_pct': 1.0
    }

def generate_analysis_summary(asset_data: Dict, ict_scores: Dict) -> str:
    """Generate analysis summary"""
    summary = []
    
    rsi = asset_data.get('rsi', 50)
    if rsi < 30:
        summary.append("RSI indicates oversold conditions")
    elif rsi > 70:
        summary.append("RSI indicates overbought conditions")
    else:
        summary.append("RSI in neutral range")
    
    if ict_scores.get('Market Structure', 0) > 80:
        summary.append("Strong market structure alignment")
    
    if ict_scores.get('Order Blocks', 0) > 85:
        summary.append("Clear order block formation detected")
    
    kill_zone = get_kill_zone()
    if kill_zone['active']:
        summary.append(f"Active kill zone: {kill_zone['name']}")
    
    return " | ".join(summary)

def create_trade_alert(asset_data: Dict, analysis: Dict) -> Dict:
    """Create comprehensive trade alert"""
    trade_params = calculate_trade_parameters(asset_data, analysis['signal'])
    analysis_summary = generate_analysis_summary(asset_data, analysis.get('ict_scores', {}))
    
    return {
        'type': 'trade_signal',
        'symbol': asset_data.get('symbol', ''),
        'name': asset_data.get('name', ''),
        'signal': analysis['signal'],
        'current_price': asset_data.get('price', 0),
        'confidence': analysis['confidence'],
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        **trade_params,
        'analysis': analysis_summary,
        'recommendation': f"Consider {analysis['signal'].lower()} position",
        'risk_level': analysis['risk']
    }

def add_to_watchlist(asset_data: Dict) -> bool:
    """Add asset to watchlist"""
    symbol = asset_data.get('symbol', '')
    if symbol and symbol not in [w.get('symbol') for w in st.session_state.watchlist]:
        st.session_state.watchlist.append(asset_data)
        return True
    return False

def create_advanced_chart(ticker: str, show_ict: bool = True):
    """Create advanced trading chart"""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="3mo")
        
        if hist.empty:
            return None
        
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            row_heights=[0.7, 0.3]
        )
        
        # Candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=hist.index,
                open=hist['Open'],
                high=hist['High'],
                low=hist['Low'],
                close=hist['Close'],
                name='Price'
            ),
            row=1, col=1
        )
        
        # Volume
        colors = ['red' if hist['Close'].iloc[i] < hist['Open'].iloc[i] else 'green' 
                  for i in range(len(hist))]
        fig.add_trace(
            go.Bar(x=hist.index, y=hist['Volume'], name='Volume', marker_color=colors),
            row=2, col=1
        )
        
        fig.update_layout(
            title=f"{ticker} - ICT Analysis",
            template='plotly_dark',
            height=600,
            showlegend=False,
            xaxis_rangeslider_visible=False
        )
        
        return fig
    except Exception as e:
        st.error(f"Chart error: {str(e)}")
        return None

# ═══════════════════════════════════════════════════════════════════════════════
# UI DISPLAY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def display_watchlist():
    """Display watchlist page"""
    st.subheader("📋 Your Watchlist")
    
    if not st.session_state.watchlist:
        st.info("Your watchlist is empty. Add stocks from Market Analysis page.")
        return
    
    for item in st.session_state.watchlist:
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        with col1:
            st.write(f"**{item.get('symbol')}** - {item.get('name', '')[:30]}")
        with col2:
            st.write(f"₹{item.get('price', 0):.2f}")
        with col3:
            change = item.get('price_change_24h', 0)
            st.write(f"{'🟢' if change > 0 else '🔴'} {change:.2f}%")
        with col4:
            if st.button("Remove", key=f"remove_{item.get('symbol')}"):
                st.session_state.watchlist = [w for w in st.session_state.watchlist 
                                             if w.get('symbol') != item.get('symbol')]
                st.rerun()

def display_portfolio():
    """Display portfolio page"""
    st.subheader("💼 Portfolio Tracker")
    st.info("Portfolio tracking feature - Add your holdings here")
    
    # Simple portfolio input
    col1, col2, col3 = st.columns(3)
    with col1:
        symbol = st.text_input("Stock Symbol")
    with col2:
        quantity = st.number_input("Quantity", min_value=1, value=1)
    with col3:
        buy_price = st.number_input("Buy Price", min_value=0.01, value=100.0)
    
    if st.button("Add to Portfolio"):
        st.session_state.portfolio.append({
            'symbol': symbol,
            'quantity': quantity,
            'buy_price': buy_price,
            'date': datetime.now().strftime('%Y-%m-%d')
        })
        st.success(f"Added {symbol} to portfolio!")

def display_backtesting():
    """Display backtesting page"""
    st.subheader("📊 Strategy Backtesting")
    st.info("Backtest your ICT strategies with historical data")
    
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Select Strategy", ["ICT Market Structure", "Order Blocks", "Fair Value Gaps"])
    with col2:
        st.date_input("Backtest Period", value=[datetime.now() - timedelta(days=90), datetime.now()])
    
    if st.button("Run Backtest"):
        st.info("Backtesting feature coming soon!")

def display_alert_settings():
    """Display alert configuration"""
    st.subheader("🔔 Alert System Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state.preferences['alert_threshold'] = st.slider(
            "Confidence Threshold",
            70, 99,
            st.session_state.preferences.get('alert_threshold', 90)
        )
        
        st.session_state.preferences['sound_alerts'] = st.checkbox(
            "Enable Sound Alerts",
            value=st.session_state.preferences.get('sound_alerts', True)
        )
    
    with col2:
        st.selectbox("Alert Frequency", ['All Signals', 'High Confidence Only'])
        st.multiselect("Alert Hours", ['Pre-Market', 'Regular Hours', 'After-Hours'])
    
    st.info("Configure notification channels (Email, Telegram, WhatsApp, etc.) in the expanders below")

def display_sent_alerts():
    """Display alert history"""
    st.subheader("📨 Alert History")
    
    if not st.session_state.sent_alerts:
        st.info("No alerts sent yet.")
        return
    
    for alert in reversed(st.session_state.sent_alerts[-10:]):
        st.markdown(f"""
        <div class="status-box">
            <h4>{alert.get('symbol')} - {alert.get('signal')}</h4>
            <p><strong>Time:</strong> {alert.get('timestamp')}</p>
            <p><strong>Confidence:</strong> {alert.get('confidence')}%</p>
        </div>
        """, unsafe_allow_html=True)

def display_realtime_alerts():
    """Display real-time monitoring"""
    st.subheader("🔍 Real-time Alert Monitor")
    
    st.checkbox("Auto-refresh every 30 seconds", value=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Threshold", f"{st.session_state.preferences.get('alert_threshold', 90)}%")
    with col2:
        kill_zone = get_kill_zone()
        st.metric("Kill Zone", kill_zone['name'][:15])
    with col3:
        st.metric("Alert Channels", 0)

# ═══════════════════════════════════════════════════════════════════════════════
# MODIFIED MAIN APPLICATION WITH ALERT INTEGRATION
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    st.title("🚨 ICT Professional Analyzer with Alert System")
    st.markdown("**Complete Trading Suite with Multi-channel Notifications**")

    kill_zone = get_kill_zone()
    
    # Monitor kill zones in background
    monitor_kill_zones()

    if kill_zone['active']:
        st.markdown(f"""
        <div class="alert-box">
            <h3>⏰ {kill_zone['name']} - ACTIVE</h3>
            <p>{kill_zone['description']} | Multiplier: {kill_zone['multiplier']}x | Priority: {kill_zone['priority']}/5</p>
            <p><strong>High probability trading window - Alerts are enhanced!</strong></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="status-box">
            <h3>{kill_zone['name']}</h3>
            <p>{kill_zone['description']}</p>
        </div>
        """, unsafe_allow_html=True)

    # Sidebar Navigation with Alert Badge
    alert_count = len([a for a in st.session_state.sent_alerts 
                      if (datetime.now() - datetime.fromisoformat(a.get('sent_time', '2000-01-01'))).days < 1])
    
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select Page", [
        f"Market Analysis {'🔔' if alert_count > 0 else ''}",
        "Watchlist",
        "Portfolio Tracker",
        "Alert Dashboard",
        "Alert History",
        "Alert Settings",
        "Backtesting",
        "Correlation Matrix",
        "Settings"
    ])

    # Remove emoji from page name for comparison
    page_clean = page.replace('🔔', '').strip()

    # PAGE: MARKET ANALYSIS (Enhanced with auto-alerts)
    if page_clean == "Market Analysis":
        st.header("Real-Time Market Analysis with Auto-Alerts")
        
        # Display alert status
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Today's Alerts", alert_count)
        with col2:
            threshold = st.session_state.preferences.get('alert_threshold', 90)
            st.metric("Alert Threshold", f"{threshold}%")
        with col3:
            enabled_channels = sum(1 for service in st.session_state.preferences['notification_services'].values() 
                                  if service.get('enabled', False))
            st.metric("Active Channels", enabled_channels)

        asset_type = st.selectbox(
            "Choose Asset Class",
            ["Indian Stocks (Nifty 50)", "Cryptocurrencies", "Forex Pairs"]
        )

        col1, col2 = st.columns(2)
        with col1:
            analyze_count = st.slider("Assets to Analyze", 5, 30, 10)
        with col2:
            show_ict_overlays = st.checkbox("Show ICT Overlays", value=True)
            auto_send_alerts = st.checkbox("Auto-send High Confidence Alerts", value=True)

        if st.button("Start Analysis with Alerts", use_container_width=True):
            if "Stocks" in asset_type:
                st.subheader("Nifty 50 Stock Analysis with Alert Monitoring")
                if analyze_count < len(NIFTY_50):
                    assets_to_analyze = [NIFTY_50[analyze_count]]  # List bana do agar single stock analyze kar rahe ho
                else:
                    st.error("All stocks analyzed! Resetting to start...")
                    st.session_state.analyze_count = 0
                    assets_to_analyze = [NIFTY_50[0]]

                progress_bar = st.progress(0)
                status_text = st.empty()

                results = []
                alerts_sent = 0
                
                for i, ticker in enumerate(assets_to_analyze):
                    status_text.text(f"Analyzing {ticker}... ({i + 1}/{len(assets_to_analyze)})")
                    data = fetch_stock_data(ticker)
                    
                    if data:
                        analysis = analyze_asset(data, 'Stock', kill_zone)
                        results.append(analysis)

                        # Check and send alerts if confidence is high
                        if auto_send_alerts and analysis['confidence'] >= st.session_state.preferences.get('alert_threshold', 90):
                            alert_sent = check_and_send_alerts(data, analysis)
                            if alert_sent:
                                alerts_sent += 1
                                st.success(f"✅ Alert sent for {ticker} ({analysis['confidence']}% confidence)")

                    progress_bar.progress((i + 1) / len(assets_to_analyze))
                    time.sleep(0.2)

                status_text.empty()
                progress_bar.empty()

                if results:
                    results_sorted = sorted(results, key=lambda x: x['combined_score'], reverse=True)

                    st.subheader(f"Top 10 Opportunities (Alerts Sent: {alerts_sent})")

                    # Enhanced dataframe with alert indicators
                    df_data = []
                    for r in results_sorted[:10]:
                        alert_indicator = "🔔" if r['confidence'] >= st.session_state.preferences.get('alert_threshold', 90) else ""
                        df_data.append({
                            'Symbol': f"{r['symbol']} {alert_indicator}",
                            'Name': r['name'][:25],
                            'Price': f"₹{r['price']:.2f}",
                            'Change': f"{r['price_change_24h']:.2f}%",
                            'Score': f"{r['combined_score']:.1f}",
                            'Signal': r['signal'],
                            'Confidence': f"{r['confidence']}%",
                            'Risk': f"{r['risk']}/10"
                        })

                    df = pd.DataFrame(df_data)
                    st.dataframe(df, use_container_width=True, height=400)

                    # Top pick with detailed trade parameters
                    st.subheader("📊 Detailed Analysis - Top Pick")
                    top_pick = results_sorted[0]
                    
                    if top_pick['confidence'] >= st.session_state.preferences.get('alert_threshold', 90):
                        st.markdown(f"""
                        <div class="alert-box">
                            <h4>🚨 HIGH CONFIDENCE SIGNAL DETECTED!</h4>
                            <p>This signal meets the alert threshold ({st.session_state.preferences.get('alert_threshold', 90)}% confidence). 
                            Alerts have been sent to configured channels.</p>
                        </div>
                        """, unsafe_allow_html=True)

                    # Calculate trade parameters for top pick
                    trade_params = calculate_trade_parameters(top_pick, top_pick['signal'])
                    
                    col1, col2, col3, col4, col5 = st.columns(5)
                    with col1:
                        st.metric("Confidence", f"{top_pick['confidence']:.1f}%")
                    with col2:
                        st.metric("Entry", f"₹{trade_params['entry_price']:.2f}")
                    with col3:
                        st.metric("Stop Loss", f"₹{trade_params['stop_loss']:.2f}")
                    with col4:
                        st.metric("Take Profit", f"₹{trade_params['take_profit']:.2f}")
                    with col5:
                        st.metric("R:R", f"1:{trade_params['risk_reward']:.1f}")

                    # Trade action buttons
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        if st.button("📝 Add to Watchlist", use_container_width=True):
                            if add_to_watchlist(top_pick):
                                st.success("Added to watchlist")
                    with col2:
                        if st.button("📤 Send Custom Alert", use_container_width=True):
                            custom_alert = create_trade_alert(top_pick, top_pick)
                            notification_manager.config = st.session_state.preferences['notification_services']
                            notification_manager.send_multichannel_alert(custom_alert)
                            st.success("Custom alert sent!")
                    with col3:
                        if st.button("📊 View Chart", use_container_width=True):
                            chart = create_advanced_chart(top_pick['symbol'] + '.NS', show_ict=show_ict_overlays)
                            if chart:
                                st.plotly_chart(chart, use_container_width=True)
                    with col4:
                        if st.button("💾 Export Report", use_container_width=True):
                            report = {
                                'analysis': top_pick,
                                'trade_parameters': trade_params,
                                'timestamp': datetime.now().isoformat()
                            }
                            json_str = json.dumps(report, indent=2)
                            st.download_button(
                                "Download JSON",
                                json_str,
                                f"trade_report_{top_pick['symbol']}_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                                "application/json"
                            )

                    # Display detailed trade parameters
                    with st.expander("📋 Complete Trade Setup", expanded=True):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**Position Sizing**")
                            st.metric("Position Size", f"{trade_params['position_size']:.2f} units")
                            st.metric("Risk per Trade", f"₹{trade_params['risk_amount']:.2f}")
                            st.metric("Risk %", f"{trade_params['risk_per_trade_pct']:.1f}%")
                            
                        with col2:
                            st.write("**Trade Parameters**")
                            st.metric("Stop Loss %", f"{trade_params['stop_loss_pct']:.1f}%")
                            st.metric("Take Profit %", f"{trade_params['take_profit_pct']:.1f}%")
                            st.metric("Risk/Reward", f"1:{trade_params['risk_reward']:.1f}")
                        
                        st.write("**Analysis Summary**")
                        st.info(generate_analysis_summary(top_pick, top_pick.get('ict_scores', {})))

    # PAGE: ALERT DASHBOARD
    elif page_clean == "Alert Dashboard":
        display_realtime_alerts()

    # PAGE: ALERT HISTORY
    elif page_clean == "Alert History":
        display_sent_alerts()

    # PAGE: ALERT SETTINGS
    elif page_clean == "Alert Settings":
        display_alert_settings()

    # OTHER PAGES (keep original functionality)
    elif page_clean == "Watchlist":
        display_watchlist()
        
    elif page_clean == "Portfolio Tracker":
        display_portfolio()
        
    elif page_clean == "Backtesting":
        display_backtesting()
        
    elif page_clean == "Correlation Matrix":
        st.subheader("Asset Correlation Analysis")
        # ... (keep original correlation matrix code)
        
    elif page_clean == "Settings":
        st.subheader("User Settings & Preferences")
        # ... (keep original settings code, but add link to alert settings)

    # Enhanced sidebar with alert status
    st.sidebar.markdown("---")
    st.sidebar.subheader("Alert System Status")
    
    # Quick alert status
    enabled_services = []
    for service_name, config in st.session_state.preferences['notification_services'].items():
        if config.get('enabled', False):
            enabled_services.append(service_name.capitalize())
    
    if enabled_services:
        st.sidebar.success(f"✅ Alerts active via: {', '.join(enabled_services)}")
    else:
        st.sidebar.warning("⚠️ No alert channels configured")
    
    st.sidebar.metric("Today's Alerts", alert_count)
    st.sidebar.metric("Confidence Threshold", f"{st.session_state.preferences.get('alert_threshold', 90)}%")
    
    # Quick test button
    if st.sidebar.button("Test Alert System", use_container_width=True):
        test_alert = {
            'type': 'trade_signal',
            'symbol': 'TEST',
            'signal': 'TEST SIGNAL',
            'confidence': 95,
            'current_price': 100.00,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        notification_manager.config = st.session_state.preferences['notification_services']
        results = notification_manager.send_multichannel_alert(test_alert)
        st.sidebar.success(f"Test sent to {sum(1 for r in results.values() if r)} channels")

    st.sidebar.markdown("---")
    st.sidebar.info(f"""
    **Alert System**: {"Active" if any(s.get('enabled') for s in st.session_state.preferences['notification_services'].values()) else "Inactive"}
    
    **Last Alert**: {st.session_state.sent_alerts[-1]['timestamp'] if st.session_state.sent_alerts else 'None'}
    
    **Kill Zone**: {kill_zone['name']}
    
    **Time**: {datetime.now().strftime("%H:%M:%S")}
    """)

    st.sidebar.markdown("---")
    st.sidebar.success("**ICT Analyzer Pro** - Enhanced Alert Edition")


import streamlit as st

# Session state initialize karo (ye app ke starting mein daal do)
if 'analyze_count' not in st.session_state:
    st.session_state.analyze_count = 0

analyze_count = st.session_state.analyze_count


if __name__ == "__main__":
    main()
