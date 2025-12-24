import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
from datetime import datetime, timedelta
import time
import requests
from typing import Dict, List, Tuple, Optional
import json
import warnings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════════════════════
# ICT PROFESSIONAL ANALYZER - PREMIUM EDITION
# Enhanced Features without Authentication
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="ICT Pro Analyzer - Premium",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════════
# PREMIUM CSS - PROFESSIONAL DARK THEME
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #111111 100%);
        color: #ffffff;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111111 0%, #0a0a0a 100%);
        border-right: 1px solid #222222;
    }

    /* Enhanced Metrics */
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 30, 30, 0.8) 0%, rgba(20, 20, 20, 0.9) 100%);
        border: 1px solid #333333;
        border-radius: 12px;
        padding: 20px;
        margin: 10px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.4);
        border-color: #444444;
    }
    
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #ffffff;
        margin: 8px 0;
        letter-spacing: -0.5px;
    }
    
    .metric-label {
        font-size: 14px;
        color: #aaaaaa;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    .metric-change {
        font-size: 14px;
        font-weight: 600;
        margin-top: 4px;
    }
    
    .positive-change {
        color: #10b981;
    }
    
    .negative-change {
        color: #ef4444;
    }
    
    /* Headers */
    h1 {
        background: linear-gradient(90deg, #ffffff 0%, #aaaaaa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 42px;
        margin-bottom: 10px;
        letter-spacing: -1px;
    }
    
    h2 {
        color: #ffffff;
        font-weight: 700;
        font-size: 28px;
        margin-bottom: 20px;
        letter-spacing: -0.5px;
    }
    
    h3 {
        color: #ffffff;
        font-weight: 600;
        font-size: 20px;
        margin-bottom: 16px;
    }
    
    /* Enhanced Tables */
    .dataframe {
        background: rgba(20, 20, 20, 0.8) !important;
        border: 1px solid #333333 !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        backdrop-filter: blur(10px);
    }
    
    .dataframe thead {
        background: linear-gradient(90deg, #222222 0%, #333333 100%) !important;
    }
    
    .dataframe thead tr th {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 13px;
        padding: 16px !important;
        border-bottom: 2px solid #444444 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .dataframe tbody tr {
        border-bottom: 1px solid #333333;
        transition: background-color 0.2s;
    }
    
    .dataframe tbody tr:hover {
        background-color: rgba(50, 50, 50, 0.5) !important;
    }
    
    .dataframe tbody tr td {
        color: #dddddd !important;
        padding: 14px 16px !important;
        font-size: 14px;
        font-weight: 500;
    }
    
    /* Enhanced Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        letter-spacing: 0.3px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
    }
    
    .secondary-button {
        background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%) !important;
        box-shadow: 0 4px 15px rgba(107, 114, 128, 0.3) !important;
    }
    
    .secondary-button:hover {
        background: linear-gradient(135deg, #4b5563 0%, #374151 100%) !important;
        box-shadow: 0 6px 20px rgba(107, 114, 128, 0.4) !important;
    }
    
    .success-button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3) !important;
    }
    
    .danger-button {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3) !important;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div {
        background: rgba(30, 30, 30, 0.8) !important;
        border: 2px solid #444444 !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        background: rgba(40, 40, 40, 0.9) !important;
    }
    
    /* Cards */
    .feature-card {
        background: linear-gradient(135deg, rgba(30, 30, 30, 0.8) 0%, rgba(20, 20, 20, 0.9) 100%);
        border: 1px solid #333333;
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        border-color: #444444;
    }
    
    /* Status Indicators */
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    .status-active {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(16, 185, 129, 0.1) 100%);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .status-inactive {
        background: linear-gradient(135deg, rgba(107, 114, 128, 0.2) 0%, rgba(107, 114, 128, 0.1) 100%);
        color: #9ca3af;
        border: 1px solid rgba(107, 114, 128, 0.3);
    }
    
    .status-warning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(245, 158, 11, 0.1) 100%);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    
    /* Trading Colors */
    .bullish {
        color: #10b981 !important;
        font-weight: 600;
    }
    
    .bearish {
        color: #ef4444 !important;
        font-weight: 600;
    }
    
    .neutral {
        color: #9ca3af !important;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #333333, transparent);
        margin: 30px 0;
    }
    
    /* Loading Animation */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #111111;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
    }
    
    /* Notification Badge */
    .notification-badge {
        position: relative;
        display: inline-flex;
    }
    
    .notification-badge::after {
        content: '';
        position: absolute;
        top: -5px;
        right: -5px;
        width: 8px;
        height: 8px;
        background: #ef4444;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SIMPLIFIED SESSION STATE MANAGEMENT
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
        'notification_channels': {
            'email': False,
            'telegram': False,
            'whatsapp': False,
            'sms': False,
            'browser': True,
            'discord': False,
            'sound': True,
            'kill_zone': True
        }
    }
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Market Analysis'
if 'show_chart' not in st.session_state:
    st.session_state.show_chart = False
if 'create_alert' not in st.session_state:
    st.session_state.create_alert = False
if 'user_settings' not in st.session_state:
    st.session_state.user_settings = {}

# ═══════════════════════════════════════════════════════════════════════════════
# SIMPLIFIED NOTIFICATION SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════

class NotificationSystem:
    def __init__(self):
        self.notification_history = []
    
    def send_email(self, to_email: str, subject: str, html_content: str) -> bool:
        """Send email notification (simplified for demo)"""
        try:
            # Store notification locally
            self.notification_history.append({
                'type': 'email',
                'to': to_email,
                'subject': subject,
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'content': html_content[:200] + '...'
            })
            
            st.toast(f"📧 Email notification prepared for {to_email}")
            return True
        except Exception as e:
            st.error(f"Email simulation error: {str(e)}")
            return False
    
    def send_trade_alert(self, trade_data: Dict, email_address: str = ""):
        """Send comprehensive trade alert"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Format message for display
        alert_message = f"""
        🚀 ICT PRO TRADE ALERT - {timestamp}
        
        Symbol: {trade_data['symbol']}
        Name: {trade_data['name']}
        Signal: {trade_data['signal']}
        
        Trade Setup:
        - Entry Price: ₹{trade_data.get('entry_price', trade_data['price']):.2f}
        - Stop Loss: ₹{trade_data.get('stop_loss', trade_data['price'] * 0.95):.2f}
        - Take Profit: ₹{trade_data.get('take_profit', trade_data['price'] * 1.1):.2f}
        - Position Size: {trade_data.get('position_size', 100)} units
        
        Analysis:
        - Confidence: {trade_data['confidence']}%
        - Risk Level: {trade_data['risk']}/10
        - RSI: {trade_data.get('rsi', 'N/A')}
        - Trend: {trade_data['trend']}
        """
        
        # Store alert
        self.notification_history.append({
            'type': 'trade_alert',
            'symbol': trade_data['symbol'],
            'signal': trade_data['signal'],
            'confidence': trade_data['confidence'],
            'time': timestamp,
            'message': alert_message
        })
        
        # Send email if configured
        if email_address and st.session_state.preferences['notification_channels']['email']:
            self.send_email(email_address, 
                          f"ICT Alert: {trade_data['signal']} {trade_data['symbol']}",
                          f"<pre>{alert_message}</pre>")
        
        # Show success message
        st.success(f"📢 Trade Alert Generated for {trade_data['symbol']}!")
        
        return alert_message
    
    def get_notification_history(self):
        """Get notification history"""
        return self.notification_history

# Initialize simplified notification system
notification_system = NotificationSystem()

# ═══════════════════════════════════════════════════════════════════════════════
# ENHANCED WATCHLIST SYSTEM (SIMPLIFIED)
# ═══════════════════════════════════════════════════════════════════════════════

class EnhancedWatchlist:
    def __init__(self):
        self.watchlist = st.session_state.watchlist
    
    def add_to_watchlist(self, asset: Dict, custom_name: str = None, notes: str = "") -> bool:
        """Add asset to watchlist with enhanced details"""
        if not any(w['symbol'] == asset['symbol'] for w in self.watchlist):
            watchlist_item = {
                'symbol': asset['symbol'],
                'name': custom_name or asset['name'],
                'asset_type': asset.get('asset_type', 'Unknown'),
                'current_price': asset.get('price', 0),
                'added_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'target_price': asset.get('price', 0) * 1.1,
                'stop_loss': asset.get('price', 0) * 0.95,
                'take_profit': asset.get('price', 0) * 1.15,
                'notes': notes,
                'alert_enabled': True,
                'price_change_since_added': 0,
                'high_since_added': asset.get('price', 0),
                'low_since_added': asset.get('price', 0),
                'priority': 'medium'
            }
            self.watchlist.append(watchlist_item)
            st.session_state.watchlist = self.watchlist
            return True
        return False
    
    def update_prices(self):
        """Update prices for all watchlist items"""
        updated_count = 0
        for item in self.watchlist:
            try:
                if 'Stock' in item.get('asset_type', ''):
                    ticker = item['symbol'] + ('.NS' if not item['symbol'].endswith('.NS') else '')
                    data = fetch_stock_data(ticker)
                elif 'Crypto' in item.get('asset_type', ''):
                    data = fetch_crypto_data(item['symbol'].lower())
                else:
                    continue
                
                if data and 'price' in data:
                    old_price = item['current_price']
                    new_price = data['price']
                    item['current_price'] = new_price
                    item['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M')
                    
                    # Update highs/lows
                    if new_price > item['high_since_added']:
                        item['high_since_added'] = new_price
                    if new_price < item['low_since_added']:
                        item['low_since_added'] = new_price
                    
                    # Calculate price change
                    if old_price > 0:
                        item['price_change_since_added'] = ((new_price - old_price) / old_price) * 100
                    
                    updated_count += 1
            except Exception as e:
                continue
        
        st.session_state.watchlist = self.watchlist
        return updated_count
    
    def display_enhanced_watchlist(self):
        """Display enhanced watchlist with more features"""
        if not self.watchlist:
            st.info("📋 Your watchlist is empty. Add assets from the Market Analysis page!")
            
            # Quick add section
            with st.expander("➕ Quick Add Asset", expanded=False):
                col1, col2, col3 = st.columns(3)
                with col1:
                    quick_symbol = st.text_input("Symbol", placeholder="RELIANCE")
                with col2:
                    quick_name = st.text_input("Name", placeholder="Reliance Industries")
                with col3:
                    quick_price = st.number_input("Current Price", value=1000.0, step=10.0)
                
                if st.button("Add to Watchlist", type="primary"):
                    if quick_symbol:
                        self.add_to_watchlist({
                            'symbol': quick_symbol,
                            'name': quick_name or quick_symbol,
                            'price': quick_price,
                            'asset_type': 'Stock'
                        })
                        st.success(f"Added {quick_symbol} to watchlist!")
                        st.rerun()
            
            return
        
        # Watchlist header with stats
        total_items = len(self.watchlist)
        stocks_count = sum(1 for item in self.watchlist if 'Stock' in item.get('asset_type', ''))
        crypto_count = sum(1 for item in self.watchlist if 'Crypto' in item.get('asset_type', ''))
        forex_count = sum(1 for item in self.watchlist if 'Forex' in item.get('asset_type', ''))
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Items", total_items)
        with col2:
            st.metric("Stocks", stocks_count)
        with col3:
            st.metric("Crypto", crypto_count)
        with col4:
            st.metric("Forex", forex_count)
        
        st.divider()
        
        # Update prices button
        col_update, col_filter = st.columns([1, 2])
        with col_update:
            if st.button("🔄 Update All Prices", type="secondary", use_container_width=True):
                with st.spinner("Updating prices..."):
                    updated = self.update_prices()
                    if updated > 0:
                        st.success(f"Updated {updated} prices!")
                    else:
                        st.info("No prices updated")
                    st.rerun()
        
        with col_filter:
            filter_option = st.selectbox("Filter by", ["All", "Stocks", "Crypto", "Forex", "High Priority"])
        
        # Watchlist items with enhanced view
        filtered_watchlist = self.watchlist
        if filter_option == "Stocks":
            filtered_watchlist = [w for w in self.watchlist if 'Stock' in w.get('asset_type', '')]
        elif filter_option == "Crypto":
            filtered_watchlist = [w for w in self.watchlist if 'Crypto' in w.get('asset_type', '')]
        elif filter_option == "Forex":
            filtered_watchlist = [w for w in self.watchlist if 'Forex' in w.get('asset_type', '')]
        elif filter_option == "High Priority":
            filtered_watchlist = [w for w in self.watchlist if w.get('priority') == 'high']
        
        for item in filtered_watchlist:
            with st.expander(f"📈 {item['name']} ({item['symbol']})", expanded=False):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.markdown(f"**{item['name']}**")
                    st.caption(f"{item['symbol']} • {item.get('asset_type', 'Unknown')}")
                    
                    if item.get('notes'):
                        st.info(f"📝 {item['notes']}")
                    
                    # Price change indicator
                    change = item.get('price_change_since_added', 0)
                    change_color = "positive-change" if change >= 0 else "negative-change"
                    change_icon = "📈" if change >= 0 else "📉"
                    
                    col_price1, col_price2 = st.columns(2)
                    with col_price1:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Current Price</div>
                            <div class="metric-value">₹{item['current_price']:.2f}</div>
                            <div class="metric-change {change_color}">
                                {change_icon} {change:+.2f}% since added
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_price2:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Price Range</div>
                            <div style="color: #ffffff; font-size: 16px; margin: 8px 0;">
                                High: ₹{item['high_since_added']:.2f}<br>
                                Low: ₹{item['low_since_added']:.2f}
                            </div>
                            <div style="color: #aaaaaa; font-size: 12px;">
                                Updated: {item['last_updated']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    # Price targets
                    st.markdown("**🎯 Price Targets**")
                    
                    target_diff = ((item['target_price'] - item['current_price']) / item['current_price']) * 100
                    stop_diff = ((item['current_price'] - item['stop_loss']) / item['current_price']) * 100
                    profit_diff = ((item['take_profit'] - item['current_price']) / item['current_price']) * 100
                    
                    st.metric("Target", f"₹{item['target_price']:.2f}", f"{target_diff:+.1f}%")
                    st.metric("Stop Loss", f"₹{item['stop_loss']:.2f}", f"{stop_diff:+.1f}%")
                    st.metric("Take Profit", f"₹{item['take_profit']:.2f}", f"{profit_diff:+.1f}%")
                
                with col3:
                    # Actions
                    st.markdown("**⚡ Actions**")
                    
                    # View chart button
                    if st.button("📊 Chart", key=f"chart_{item['symbol']}", use_container_width=True):
                        st.session_state.show_chart_for = item['symbol']
                    
                    # Edit button
                    if st.button("✏️ Edit", key=f"edit_{item['symbol']}", use_container_width=True):
                        st.session_state.editing_item = item['symbol']
                    
                    # Remove button
                    if st.button("🗑️ Remove", key=f"remove_{item['symbol']}", use_container_width=True):
                        self.watchlist = [w for w in self.watchlist if w['symbol'] != item['symbol']]
                        st.session_state.watchlist = self.watchlist
                        st.success(f"Removed {item['symbol']} from watchlist")
                        st.rerun()
                    
                    # Quick alert button
                    if st.button("🔔 Alert", key=f"alert_{item['symbol']}", use_container_width=True):
                        st.session_state.create_alert_for = item['symbol']
                
                # Price history chart if requested
                if st.session_state.get('show_chart_for') == item['symbol']:
                    try:
                        if 'Stock' in item.get('asset_type', ''):
                            ticker = item['symbol'] + ('.NS' if not item['symbol'].endswith('.NS') else '')
                            chart_data = yf.download(ticker, period='1mo')
                        else:
                            chart_data = yf.download(item['symbol'], period='1mo')
                        
                        if not chart_data.empty:
                            fig = go.Figure(data=[go.Candlestick(
                                x=chart_data.index,
                                open=chart_data['Open'],
                                high=chart_data['High'],
                                low=chart_data['Low'],
                                close=chart_data['Close']
                            )])
                            
                            # Add target lines
                            fig.add_hline(y=item['target_price'], line_dash="dash", 
                                         line_color="green", opacity=0.5,
                                         annotation_text="Target")
                            fig.add_hline(y=item['stop_loss'], line_dash="dash", 
                                         line_color="red", opacity=0.5,
                                         annotation_text="Stop Loss")
                            fig.add_hline(y=item['take_profit'], line_dash="dash", 
                                         line_color="blue", opacity=0.5,
                                         annotation_text="Take Profit")
                            
                            fig.update_layout(
                                template='plotly_dark',
                                height=300,
                                showlegend=False,
                                margin=dict(l=0, r=0, t=30, b=0),
                                title=f"{item['symbol']} - 1 Month Price Action"
                            )
                            st.plotly_chart(fig, use_container_width=True)
                    except Exception as e:
                        st.error(f"Could not load chart: {str(e)}")
        
        # Bulk actions
        st.divider()
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📥 Export Watchlist", use_container_width=True):
                df = pd.DataFrame(self.watchlist)
                csv = df.to_csv(index=False)
                st.download_button(
                    "Download CSV",
                    csv,
                    "watchlist.csv",
                    "text/csv"
                )
        
        with col2:
            if st.button("🔔 Bulk Alerts", use_container_width=True):
                st.session_state.show_bulk_alerts = True
        
        with col3:
            if st.button("🧹 Clear All", type="secondary", use_container_width=True):
                if st.checkbox("Confirm clear all items", key="confirm_clear"):
                    self.watchlist = []
                    st.session_state.watchlist = []
                    st.success("Watchlist cleared!")
                    st.rerun()

# Initialize enhanced watchlist
enhanced_watchlist = EnhancedWatchlist()

# ═══════════════════════════════════════════════════════════════════════════════
# ENHANCED ALERT SYSTEM (SIMPLIFIED)
# ═══════════════════════════════════════════════════════════════════════════════

class EnhancedAlertSystem:
    def __init__(self):
        self.alerts = st.session_state.alerts
    
    def create_advanced_alert(self, alert_data: Dict):
        """Create advanced alert with multiple conditions"""
        alert_id = len(self.alerts) + 1
        advanced_alert = {
            'id': alert_id,
            'symbol': alert_data['symbol'],
            'name': alert_data.get('name', alert_data['symbol']),
            'conditions': alert_data.get('conditions', []),
            'notification_email': alert_data.get('email', ''),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'triggered': False,
            'trigger_count': 0,
            'cooldown_minutes': alert_data.get('cooldown', 5),
            'last_triggered': None,
            'active': True,
            'priority': alert_data.get('priority', 'medium')
        }
        
        self.alerts.append(advanced_alert)
        st.session_state.alerts = self.alerts
        
        # Send confirmation
        if alert_data.get('email'):
            notification_system.send_email(
                alert_data['email'],
                f"Alert Created: {alert_data['symbol']}",
                f"Your alert for {alert_data['symbol']} has been created successfully!"
            )
        
        return alert_id
    
    def check_condition(self, condition: Dict, asset_data: Dict) -> bool:
        """Check individual condition"""
        condition_type = condition['type']
        target_value = condition['value']
        comparator = condition.get('comparator', '>=')
        
        if condition_type == 'price':
            current_value = asset_data.get('price', 0)
        elif condition_type == 'rsi':
            current_value = asset_data.get('rsi', 50)
        elif condition_type == 'volume':
            current_value = asset_data.get('volume', 0)
        elif condition_type == 'confidence':
            current_value = asset_data.get('confidence', 0)
        else:
            return False
        
        if comparator == '>=':
            return current_value >= target_value
        elif comparator == '<=':
            return current_value <= target_value
        elif comparator == '>':
            return current_value > target_value
        elif comparator == '<':
            return current_value < target_value
        elif comparator == '==':
            return abs(current_value - target_value) < 0.01
        
        return False
    
    def display_enhanced_alerts(self):
        """Display enhanced alert management interface"""
        st.header("🚨 Advanced Alert System")
        
        # Tabs for different alert types
        tab1, tab2, tab3 = st.tabs(["Create Alert", "Manage Alerts", "Alert History"])
        
        with tab1:
            self.display_alert_creator()
        
        with tab2:
            self.display_alerts_management()
        
        with tab3:
            self.display_alert_history()
    
    def display_alert_creator(self):
        """Display alert creation interface"""
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Symbol selection
            symbol = st.text_input("Asset Symbol", placeholder="e.g., RELIANCE, BTC-USD")
            asset_name = st.text_input("Asset Name (Optional)", placeholder="Reliance Industries")
            
            # Condition builder
            st.subheader("🔧 Add Conditions")
            
            conditions = st.session_state.get('alert_conditions', [])
            
            with st.container():
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    cond_type = st.selectbox("Metric", 
                        ["price", "rsi", "volume", "confidence"], 
                        key="cond_type")
                with col_b:
                    comparator = st.selectbox("Comparator", 
                        [">=", "<=", ">", "<", "=="], 
                        key="comparator")
                with col_c:
                    value = st.number_input("Value", 
                        key="cond_value",
                        min_value=0.0,
                        step=0.1)
                
                col_add, col_clear = st.columns(2)
                with col_add:
                    if st.button("➕ Add Condition", type="secondary", use_container_width=True):
                        conditions.append({
                            'type': cond_type,
                            'comparator': comparator,
                            'value': value
                        })
                        st.session_state.alert_conditions = conditions
                        st.success(f"Condition added: {cond_type} {comparator} {value}")
                
                with col_clear:
                    if st.button("🗑️ Clear All", type="secondary", use_container_width=True):
                        conditions.clear()
                        st.session_state.alert_conditions = []
                        st.info("All conditions cleared")
            
            # Display added conditions
            if conditions:
                st.write("**📋 Current Conditions:**")
                for i, cond in enumerate(conditions):
                    col_cond, col_del = st.columns([4, 1])
                    with col_cond:
                        st.write(f"{i+1}. {cond['type'].upper()} {cond['comparator']} {cond['value']}")
                    with col_del:
                        if st.button("❌", key=f"del_cond_{i}"):
                            conditions.pop(i)
                            st.session_state.alert_conditions = conditions
                            st.rerun()
        
        with col2:
            # Alert settings
            st.subheader("⚙️ Alert Settings")
            
            priority = st.selectbox("Priority", 
                ["low", "medium", "high", "critical"],
                help="Higher priority alerts are checked more frequently")
            
            coold
