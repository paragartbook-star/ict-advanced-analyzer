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
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import schedule
import asyncio
import websockets
import aiohttp
from twilio.rest import Client
import discord

warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════════════════════
# ENHANCED NOTIFICATION SYSTEM CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

# Configuration dictionary for notification services
NOTIFICATION_CONFIG = {
    'email': {
        'enabled': False,
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'sender_email': '',
        'sender_password': '',
        'recipients': []
    },
    'telegram': {
        'enabled': False,
        'bot_token': '',
        'chat_id': ''
    },
    'whatsapp': {
        'enabled': False,
        'twilio_sid': '',
        'twilio_token': '',
        'twilio_number': '',
        'recipients': []
    },
    'sms': {
        'enabled': False,
        'twilio_sid': '',
        'twilio_token': '',
        'twilio_number': '',
        'recipients': []
    },
    'discord': {
        'enabled': False,
        'webhook_url': ''
    },
    'push': {
        'enabled': False,
        'onesignal_app_id': '',
        'onesignal_api_key': ''
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# ICT PROFESSIONAL ANALYZER - CLEAN DARK THEME WITH ALERT SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="ICT Pro Analyzer with Alerts",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - TradingView Dark Theme
st.markdown("""
<style>
    /* Main Background - Deep TradingView Black */
    .stApp {
        background: #0d0d0d !important;
    }
    
    /* Sidebar - TradingView Style */
    [data-testid="stSidebar"] {
        background: #131722 !important;
        border-right: 1px solid #2a2e39 !important;
    }
    
    /* Metric Cards - TradingView Cards */
    [data-testid="stMetric"] {
        background: #1e222d !important;
        padding: 15px;
        border-radius: 4px;
        border: 1px solid #2a2e39;
    }
    
    /* Headers - TradingView White Text */
    h1, h2, h3 {
        color: #d1d4dc !important;
        font-weight: 600;
    }
    
    /* Tables - TradingView Style */
    .dataframe {
        background: #1e222d !important;
        color: #d1d4dc !important;
        border: 1px solid #2a2e39;
        border-radius: 4px;
    }
    
    .dataframe thead tr th {
        background: #131722 !important;
        color: #787b86 !important;
        font-weight: 600;
        border-bottom: 1px solid #2a2e39;
        text-transform: uppercase;
        font-size: 11px;
    }
    
    .dataframe tbody tr:hover {
        background: #2a2e39 !important;
    }
    
    /* Buttons - TradingView Blue */
    .stButton>button {
        background: #2962ff !important;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton>button:hover {
        background: #1e53e5 !important;
    }

# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATE INITIALIZATION WITH ALERT SYSTEM
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

# ═══════════════════════════════════════════════════════════════════════════════
# ENHANCED NOTIFICATION SYSTEM FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

class NotificationManager:
    def __init__(self):
        self.config = NOTIFICATION_CONFIG
        
    def send_email_alert(self, subject: str, message: str, html_message: str = None):
        """Send email notification"""
        if not self.config['email']['enabled']:
            return False
            
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.config['email']['sender_email']
            msg['To'] = ', '.join(self.config['email']['recipients'])
            
            part1 = MIMEText(message, 'plain')
            msg.attach(part1)
            
            if html_message:
                part2 = MIMEText(html_message, 'html')
                msg.attach(part2)
            
            with smtplib.SMTP(self.config['email']['smtp_server'], 
                            self.config['email']['smtp_port']) as server:
                server.starttls()
                server.login(self.config['email']['sender_email'], 
                           self.config['email']['sender_password'])
                server.send_message(msg)
            
            return True
        except Exception as e:
            st.error(f"Email error: {str(e)}")
            return False
    
    def send_telegram_alert(self, message: str):
        """Send Telegram notification"""
        if not self.config['telegram']['enabled']:
            return False
            
        try:
            url = f"https://api.telegram.org/bot{self.config['telegram']['bot_token']}/sendMessage"
            payload = {
                'chat_id': self.config['telegram']['chat_id'],
                'text': message,
                'parse_mode': 'HTML'
            }
            response = requests.post(url, json=payload)
            return response.status_code == 200
        except Exception as e:
            st.error(f"Telegram error: {str(e)}")
            return False
    
    def send_whatsapp_alert(self, message: str):
        """Send WhatsApp notification via Twilio"""
        if not self.config['whatsapp']['enabled']:
            return False
            
        try:
            client = Client(self.config['whatsapp']['twilio_sid'], 
                          self.config['whatsapp']['twilio_token'])
            
            for recipient in self.config['whatsapp']['recipients']:
                message = client.messages.create(
                    body=message,
                    from_=f"whatsapp:{self.config['whatsapp']['twilio_number']}",
                    to=f"whatsapp:{recipient}"
                )
            
            return True
        except Exception as e:
            st.error(f"WhatsApp error: {str(e)}")
            return False
    
    def send_sms_alert(self, message: str):
        """Send SMS notification via Twilio"""
        if not self.config['sms']['enabled']:
            return False
            
        try:
            client = Client(self.config['sms']['twilio_sid'], 
                          self.config['sms']['twilio_token'])
            
            for recipient in self.config['sms']['recipients']:
                message = client.messages.create(
                    body=message,
                    from_=self.config['sms']['twilio_number'],
                    to=recipient
                )
            
            return True
        except Exception as e:
            st.error(f"SMS error: {str(e)}")
            return False
    
    def send_discord_alert(self, message: str, title: str = None):
        """Send Discord webhook notification"""
        if not self.config['discord']['enabled']:
            return False
            
        try:
            webhook = discord.Webhook.from_url(
                self.config['discord']['webhook_url'],
                adapter=discord.RequestsWebhookAdapter()
            )
            
            embed = discord.Embed(
                title=title or "ICT Trading Alert",
                description=message,
                color=discord.Color.red() if "SELL" in message else discord.Color.green(),
                timestamp=datetime.now()
            )
            
            webhook.send(embed=embed)
            return True
        except Exception as e:
            st.error(f"Discord error: {str(e)}")
            return False
    
    def send_browser_push(self, title: str, message: str):
        """Send browser push notification via OneSignal"""
        if not self.config['push']['enabled']:
            return False
            
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Basic {self.config['push']['onesignal_api_key']}"
            }
            
            payload = {
                "app_id": self.config['push']['onesignal_app_id'],
                "included_segments": ["All"],
                "contents": {"en": message},
                "headings": {"en": title}
            }
            
            response = requests.post(
                "https://onesignal.com/api/v1/notifications",
                headers=headers,
                json=payload
            )
            
            return response.status_code == 200
        except Exception as e:
            st.error(f"Push notification error: {str(e)}")
            return False
    
    def play_sound_alert(self, alert_type: str = "info"):
        """Play sound alert based on type"""
        if not st.session_state.preferences.get('sound_alerts', True):
            return
            
        # In a real implementation, you would play actual sound files
        # For Streamlit, we can use JavaScript audio
        sound_js = """
        <audio autoplay>
            <source src="https://assets.mixkit.co/sfx/preview/mixkit-alarm-digital-clock-beep-989.mp3" type="audio/mpeg">
        </audio>
        """
        st.components.v1.html(sound_js, height=0)
    
    def send_multichannel_alert(self, alert_data: Dict):
        """Send alert through all enabled channels"""
        try:
            # Format message based on alert type
            if alert_data['type'] == 'trade_signal':
                message = self.format_trade_alert(alert_data)
                subject = f"🚨 TRADE SIGNAL: {alert_data['symbol']} - {alert_data['signal']}"
            elif alert_data['type'] == 'kill_zone':
                message = self.format_kill_zone_alert(alert_data)
                subject = f"⏰ KILL ZONE ACTIVE: {alert_data['zone_name']}"
            elif alert_data['type'] == 'price_alert':
                message = self.format_price_alert(alert_data)
                subject = f"📈 PRICE ALERT: {alert_data['symbol']}"
            else:
                message = alert_data.get('message', 'Alert triggered')
                subject = "ICT Analyzer Alert"
            
            # Send through all enabled channels
            results = {}
            
            if self.config['email']['enabled']:
                html_msg = self.format_html_alert(alert_data)
                results['email'] = self.send_email_alert(subject, message, html_msg)
            
            if self.config['telegram']['enabled']:
                results['telegram'] = self.send_telegram_alert(message)
            
            if self.config['whatsapp']['enabled']:
                results['whatsapp'] = self.send_whatsapp_alert(message)
            
            if self.config['sms']['enabled']:
                results['sms'] = self.send_sms_alert(message[:160])  # SMS character limit
            
            if self.config['discord']['enabled']:
                results['discord'] = self.send_discord_alert(message, subject)
            
            if self.config['push']['enabled']:
                results['push'] = self.send_browser_push(subject, message)
            
            # Play sound if enabled
            if st.session_state.preferences.get('sound_alerts', True):
                self.play_sound_alert(alert_data.get('alert_type', 'info'))
            
            return results
            
        except Exception as e:
            st.error(f"Multichannel alert error: {str(e)}")
            return {}
    
    def format_trade_alert(self, alert_data: Dict) -> str:
        """Format trade signal alert message"""
        symbol = alert_data.get('symbol', '')
        signal = alert_data.get('signal', '')
        confidence = alert_data.get('confidence', 0)
        price = alert_data.get('current_price', 0)
        
        message = f"""
📊 *ICT TRADING ALERT* 📊

🔸 *Symbol:* {symbol}
🔸 *Signal:* {signal}
🔸 *Confidence:* {confidence}%
🔸 *Current Price:* ${price:.2f}
🔸 *Time:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📈 *Trade Setup:*
Entry: ${alert_data.get('entry_price', 0):.2f}
Stop Loss: ${alert_data.get('stop_loss', 0):.2f} ({alert_data.get('stop_loss_pct', 0):.1f}%)
Take Profit: ${alert_data.get('take_profit', 0):.2f} ({alert_data.get('take_profit_pct', 0):.1f}%)
Risk/Reward: 1:{alert_data.get('risk_reward', 0):.1f}

📊 *Analysis:*
{alert_data.get('analysis', 'No analysis available')}

💡 *Recommendation:* {alert_data.get('recommendation', '')}

⚠️ *Risk Level:* {alert_data.get('risk_level', 'Medium')}/10
        """
        
        return message
    
    def format_kill_zone_alert(self, alert_data: Dict) -> str:
        """Format kill zone activation alert"""
        return f"""
⏰ *KILL ZONE ACTIVATED* ⏰

Zone: {alert_data.get('zone_name', '')}
Status: {alert_data.get('status', 'ACTIVE')}
Multiplier: {alert_data.get('multiplier', 1.0)}x
Priority: {alert_data.get('priority', 0)}/5

Description: {alert_data.get('description', '')}

Expected: High volatility and liquidity
Time: {datetime.now().strftime('%H:%M')} IST
Duration: {alert_data.get('duration', '2 hours')}

Action: Monitor for trade setups
        """
    
    def format_price_alert(self, alert_data: Dict) -> str:
        """Format price alert message"""
        return f"""
📈 *PRICE ALERT TRIGGERED* 📈

Symbol: {alert_data.get('symbol', '')}
Condition: {alert_data.get('condition', '')}
Target: ${alert_data.get('target_price', 0):.2f}
Current: ${alert_data.get('current_price', 0):.2f}
Change: {alert_data.get('price_change', 0):.2f}%

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Action: Check chart for potential trade
        """
    
    def format_html_alert(self, alert_data: Dict) -> str:
        """Format HTML email alert"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .alert-container {{ background: #f8f9fa; padding: 20px; border-radius: 10px; }}
                .header {{ background: {'#28a745' if 'BUY' in alert_data.get('signal', '') else '#dc3545'}; 
                         color: white; padding: 15px; border-radius: 5px; }}
                .trade-details {{ background: white; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                .metric {{ display: inline-block; margin: 10px; padding: 10px; background: #e9ecef; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="alert-container">
                <div class="header">
                    <h2>🚨 ICT Trading Alert</h2>
                    <h3>{alert_data.get('symbol', '')} - {alert_data.get('signal', '')}</h3>
                </div>
                
                <div class="trade-details">
                    <h4>Trade Parameters</h4>
                    <div class="metric"><strong>Entry:</strong> ${alert_data.get('entry_price', 0):.2f}</div>
                    <div class="metric"><strong>Stop Loss:</strong> ${alert_data.get('stop_loss', 0):.2f}</div>
                    <div class="metric"><strong>Take Profit:</strong> ${alert_data.get('take_profit', 0):.2f}</div>
                    <div class="metric"><strong>Risk/Reward:</strong> 1:{alert_data.get('risk_reward', 0):.1f}</div>
                </div>
                
                <div class="trade-details">
                    <h4>Analysis</h4>
                    <p>{alert_data.get('analysis', '')}</p>
                </div>
                
                <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Confidence:</strong> {alert_data.get('confidence', 0)}%</p>
                <p><strong>Risk Level:</strong> {alert_data.get('risk_level', 'Medium')}/10</p>
            </div>
        </body>
        </html>
        """
        return html

# Initialize notification manager
notification_manager = NotificationManager()

# ═══════════════════════════════════════════════════════════════════════════════
# ENHANCED ALERT PROCESSING FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def calculate_trade_parameters(asset_data: Dict, signal: str) -> Dict:
    """Calculate detailed trade parameters including SL, TP, and position size"""
    current_price = asset_data.get('price', 0)
    volatility = abs(asset_data.get('price_change_24h', 2))
    risk_tolerance = st.session_state.preferences.get('risk_tolerance', 'medium')
    
    # Risk tolerance mapping
    risk_multiplier = {
        'very low': 0.5,
        'low': 0.75,
        'medium': 1.0,
        'high': 1.5,
        'very high': 2.0
    }.get(risk_tolerance, 1.0)
    
    # Calculate stop loss percentage based on volatility
    base_sl_pct = min(5.0, max(1.0, volatility * 0.5))
    sl_pct = base_sl_pct * risk_multiplier
    
    # Calculate take profit based on risk-reward
    risk_reward = 2.0 if confidence >= 85 else 1.5
    tp_pct = sl_pct * risk_reward
    
    if 'BUY' in signal:
        stop_loss = current_price * (1 - sl_pct/100)
        take_profit = current_price * (1 + tp_pct/100)
        entry_price = current_price * 0.995  # Slightly below current for buy
    else:  # SELL signal
        stop_loss = current_price * (1 + sl_pct/100)
        take_profit = current_price * (1 - tp_pct/100)
        entry_price = current_price * 1.005  # Slightly above current for sell
    
    # Calculate position size (simplified)
    account_size = 10000  # Default account size
    risk_per_trade = account_size * 0.01  # 1% risk per trade
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
    """Generate detailed analysis summary for alerts"""
    summary = []
    
    # Technical analysis
    rsi = asset_data.get('rsi', 50)
    if rsi < 30:
        summary.append("RSI indicates oversold conditions")
    elif rsi > 70:
        summary.append("RSI indicates overbought conditions")
    else:
        summary.append("RSI in neutral range")
    
    # Market structure
    if ict_scores.get('Market Structure', 0) > 80:
        summary.append("Strong market structure alignment")
    
    # Order blocks
    if ict_scores.get('Order Blocks', 0) > 85:
        summary.append("Clear order block formation detected")
    
    # Fair Value Gaps
    if ict_scores.get('Fair Value Gaps', 0) > 80:
        summary.append("Fair value gaps present for potential fills")
    
    # Kill zone
    kill_zone = get_kill_zone()
    if kill_zone['active']:
        summary.append(f"Active kill zone: {kill_zone['name']}")
    
    return " | ".join(summary)

def create_trade_alert(asset_data: Dict, analysis: Dict) -> Dict:
    """Create comprehensive trade alert"""
    trade_params = calculate_trade_parameters(asset_data, analysis['signal'])
    analysis_summary = generate_analysis_summary(asset_data, analysis.get('ict_scores', {}))
    
    alert_data = {
        'type': 'trade_signal',
        'symbol': asset_data.get('symbol', ''),
        'name': asset_data.get('name', ''),
        'asset_type': asset_data.get('asset_type', ''),
        'signal': analysis['signal'],
        'current_price': asset_data.get('price', 0),
        'confidence': analysis['confidence'],
        'trend': analysis['trend'],
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'timeframe': 'Intraday',
        **trade_params,
        'analysis': analysis_summary,
        'recommendation': f"Consider {analysis['signal'].lower()} position with tight risk management",
        'risk_level': analysis['risk'],
        'priority': 'HIGH' if analysis['confidence'] >= 90 else 'MEDIUM',
        'kill_zone': get_kill_zone()['name'],
        'market_condition': 'Volatile' if abs(asset_data.get('price_change_24h', 0)) > 3 else 'Normal'
    }
    
    return alert_data

def check_and_send_alerts(asset_data: Dict, analysis: Dict):
    """Check if alerts should be sent and send them"""
    threshold = st.session_state.preferences.get('alert_threshold', 90)
    
    # Check confidence threshold
    if analysis['confidence'] >= threshold:
        # Create trade alert
        trade_alert = create_trade_alert(asset_data, analysis)
        
        # Add to sent alerts history
        st.session_state.sent_alerts.append({
            **trade_alert,
            'sent_time': datetime.now().isoformat()
        })
        
        # Keep only last 100 alerts
        if len(st.session_state.sent_alerts) > 100:
            st.session_state.sent_alerts = st.session_state.sent_alerts[-100:]
        
        # Send notifications
        notification_manager.config = st.session_state.preferences['notification_services']
        results = notification_manager.send_multichannel_alert(trade_alert)
        
        # Log results
        if any(results.values()):
            st.success(f"Alert sent for {asset_data['symbol']} with {analysis['confidence']}% confidence")
        else:
            st.warning(f"Alert created but not sent (check notification settings)")
        
        return trade_alert
    
    return None

def monitor_kill_zones():
    """Monitor and alert for kill zone activations"""
    kill_zone = get_kill_zone()
    
    if kill_zone['active'] and st.session_state.preferences.get('kill_zone_alerts', True):
        # Check if we already sent an alert for this zone
        last_alert_time = None
        for alert in reversed(st.session_state.sent_alerts):
            if alert.get('type') == 'kill_zone' and alert.get('zone_name') == kill_zone['name']:
                last_alert_time = datetime.fromisoformat(alert.get('sent_time', ''))
                break
        
        # Send alert if not sent in last 30 minutes
        if not last_alert_time or (datetime.now() - last_alert_time).total_seconds() > 1800:
            kill_zone_alert = {
                'type': 'kill_zone',
                'zone_name': kill_zone['name'],
                'status': 'ACTIVE',
                'multiplier': kill_zone['multiplier'],
                'priority': kill_zone['priority'],
                'description': kill_zone['description'],
                'duration': '2 hours',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            notification_manager.config = st.session_state.preferences['notification_services']
            notification_manager.send_multichannel_alert(kill_zone_alert)
            
            st.session_state.sent_alerts.append({
                **kill_zone_alert,
                'sent_time': datetime.now().isoformat()
            })

# ═══════════════════════════════════════════════════════════════════════════════
# ENHANCED UI COMPONENTS FOR ALERT SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════

def display_alert_settings():
    """Display alert configuration settings"""
    st.subheader("🔔 Alert System Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state.preferences['alert_threshold'] = st.slider(
            "Confidence Threshold for Alerts",
            min_value=70,
            max_value=99,
            value=st.session_state.preferences.get('alert_threshold', 90),
            help="Only send alerts when confidence is above this percentage"
        )
        
        st.session_state.preferences['sound_alerts'] = st.checkbox(
            "Enable Sound Alerts",
            value=st.session_state.preferences.get('sound_alerts', True)
        )
        
        st.session_state.preferences['kill_zone_alerts'] = st.checkbox(
            "Enable Kill Zone Alerts",
            value=st.session_state.preferences.get('kill_zone_alerts', True)
        )
    
    with col2:
        # Alert frequency
        alert_frequency = st.selectbox(
            "Alert Frequency",
            ['All Signals', 'High Confidence Only', 'Daily Digest'],
            index=0
        )
        
        # Market hours filter
        market_hours = st.multiselect(
            "Alert During Market Hours",
            ['Pre-Market', 'Regular Hours', 'After-Hours', '24/7'],
            default=['Regular Hours', 'Pre-Market']
        )
    
    st.write("---")
    st.subheader("📱 Notification Channels")
    
    # Email Configuration
    with st.expander("Email Settings", expanded=False):
        email_config = st.session_state.preferences['notification_services']['email']
        email_config['enabled'] = st.checkbox("Enable Email Alerts", value=email_config['enabled'])
        
        if email_config['enabled']:
            col1, col2 = st.columns(2)
            with col1:
                email_config['sender_email'] = st.text_input(
                    "Sender Email",
                    value=email_config['sender_email'],
                    type="password"
                )
                email_config['sender_password'] = st.text_input(
                    "App Password",
                    value=email_config['sender_password'],
                    type="password"
                )
            with col2:
                recipients = st.text_area(
                    "Recipient Emails (one per line)",
                    value="\n".join(email_config['recipients'])
                )
                email_config['recipients'] = [r.strip() for r in recipients.split('\n') if r.strip()]
    
    # Telegram Configuration
    with st.expander("Telegram Settings", expanded=False):
        telegram_config = st.session_state.preferences['notification_services']['telegram']
        telegram_config['enabled'] = st.checkbox("Enable Telegram Alerts", value=telegram_config['enabled'])
        
        if telegram_config['enabled']:
            telegram_config['bot_token'] = st.text_input(
                "Bot Token",
                value=telegram_config['bot_token'],
                type="password"
            )
            telegram_config['chat_id'] = st.text_input(
                "Chat ID",
                value=telegram_config['chat_id']
            )
            
            if st.button("Test Telegram Connection"):
                if telegram_config['bot_token'] and telegram_config['chat_id']:
                    test_msg = "✅ ICT Analyzer Telegram connection test successful!"
                    if notification_manager.send_telegram_alert(test_msg):
                        st.success("Telegram test message sent!")
                    else:
                        st.error("Failed to send test message")
    
    # WhatsApp Configuration
    with st.expander("WhatsApp Settings", expanded=False):
        whatsapp_config = st.session_state.preferences['notification_services']['whatsapp']
        whatsapp_config['enabled'] = st.checkbox("Enable WhatsApp Alerts", value=whatsapp_config['enabled'])
        
        if whatsapp_config['enabled']:
            col1, col2 = st.columns(2)
            with col1:
                whatsapp_config['twilio_sid'] = st.text_input(
                    "Twilio SID",
                    value=whatsapp_config['twilio_sid'],
                    type="password"
                )
                whatsapp_config['twilio_token'] = st.text_input(
                    "Twilio Token",
                    value=whatsapp_config['twilio_token'],
                    type="password"
                )
            with col2:
                whatsapp_config['twilio_number'] = st.text_input(
                    "Twilio Number",
                    value=whatsapp_config['twilio_number']
                )
                recipients = st.text_area(
                    "WhatsApp Numbers (with country code)",
                    value="\n".join(whatsapp_config['recipients'])
                )
                whatsapp_config['recipients'] = [r.strip() for r in recipients.split('\n') if r.strip()]
    
    # SMS Configuration
    with st.expander("SMS Settings", expanded=False):
        sms_config = st.session_state.preferences['notification_services']['sms']
        sms_config['enabled'] = st.checkbox("Enable SMS Alerts", value=sms_config['enabled'])
        
        if sms_config['enabled']:
            col1, col2 = st.columns(2)
            with col1:
                sms_config['twilio_sid'] = st.text_input(
                    "Twilio SID (SMS)",
                    value=sms_config['twilio_sid'],
                    type="password"
                )
                sms_config['twilio_token'] = st.text_input(
                    "Twilio Token (SMS)",
                    value=sms_config['twilio_token'],
                    type="password"
                )
            with col2:
                sms_config['twilio_number'] = st.text_input(
                    "Twilio Number (SMS)",
                    value=sms_config['twilio_number']
                )
                recipients = st.text_area(
                    "Phone Numbers (with country code)",
                    value="\n".join(sms_config['recipients'])
                )
                sms_config['recipients'] = [r.strip() for r in recipients.split('\n') if r.strip()]
    
    # Discord Configuration
    with st.expander("Discord Settings", expanded=False):
        discord_config = st.session_state.preferences['notification_services']['discord']
        discord_config['enabled'] = st.checkbox("Enable Discord Alerts", value=discord_config['enabled'])
        
        if discord_config['enabled']:
            discord_config['webhook_url'] = st.text_input(
                "Discord Webhook URL",
                value=discord_config['webhook_url'],
                type="password"
            )
            
            if st.button("Test Discord Webhook"):
                if discord_config['webhook_url']:
                    test_msg = "✅ ICT Analyzer Discord webhook test successful!"
                    if notification_manager.send_discord_alert(test_msg, "Test Notification"):
                        st.success("Discord test message sent!")
                    else:
                        st.error("Failed to send test message")
    
    # Push Notification Configuration
    with st.expander("Push Notification Settings", expanded=False):
        push_config = st.session_state.preferences['notification_services']['push']
        push_config['enabled'] = st.checkbox("Enable Browser Push Alerts", value=push_config['enabled'])
        
        if push_config['enabled']:
            push_config['onesignal_app_id'] = st.text_input(
                "OneSignal App ID",
                value=push_config['onesignal_app_id'],
                type="password"
            )
            push_config['onesignal_api_key'] = st.text_input(
                "OneSignal API Key",
                value=push_config['onesignal_api_key'],
                type="password"
            )
    
    st.write("---")
    
    # Test all notifications
    if st.button("🚨 Test All Notification Channels"):
        test_alert = {
            'type': 'trade_signal',
            'symbol': 'TEST',
            'signal': 'TEST BUY',
            'confidence': 95,
            'current_price': 100.50,
            'entry_price': 100.00,
            'stop_loss': 98.00,
            'take_profit': 104.00,
            'analysis': 'This is a test alert to verify all notification channels are working properly.',
            'risk_level': 3
        }
        
        notification_manager.config = st.session_state.preferences['notification_services']
        results = notification_manager.send_multichannel_alert(test_alert)
        
        success_count = sum(1 for r in results.values() if r)
        st.success(f"Test alerts sent: {success_count}/{len(results)} channels successful")

def display_sent_alerts():
    """Display history of sent alerts"""
    st.subheader("📨 Alert History")
    
    if not st.session_state.sent_alerts:
        st.info("No alerts have been sent yet.")
        return
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_type = st.selectbox("Filter by Type", ['All', 'Trade Signal', 'Kill Zone', 'Price Alert'])
    with col2:
        filter_symbol = st.text_input("Filter by Symbol", "")
    with col3:
        filter_days = st.slider("Last N Days", 1, 30, 7)
    
    # Filter alerts
    filtered_alerts = st.session_state.sent_alerts.copy()
    
    # Filter by date
    cutoff_date = datetime.now() - timedelta(days=filter_days)
    filtered_alerts = [
        a for a in filtered_alerts 
        if datetime.fromisoformat(a.get('sent_time', '2000-01-01')) >= cutoff_date
    ]
    
    # Filter by type
    if filter_type != 'All':
        type_map = {
            'Trade Signal': 'trade_signal',
            'Kill Zone': 'kill_zone',
            'Price Alert': 'price_alert'
        }
        filtered_alerts = [a for a in filtered_alerts if a.get('type') == type_map[filter_type]]
    
    # Filter by symbol
    if filter_symbol:
        filtered_alerts = [a for a in filtered_alerts if filter_symbol.lower() in a.get('symbol', '').lower()]
    
    if not filtered_alerts:
        st.info("No alerts match the selected filters.")
        return
    
    # Display alerts in reverse chronological order
    filtered_alerts.sort(key=lambda x: x.get('sent_time', ''), reverse=True)
    
    for alert in filtered_alerts[:20]:  # Show last 20 alerts
        with st.container():
            if alert.get('type') == 'trade_signal':
                signal_class = "buy" if "BUY" in alert.get('signal', '') else "sell"
                st.markdown(f"""
                <div class="trade-card {signal_class}">
                    <h4>🚨 {alert.get('symbol', '')} - {alert.get('signal', '')}</h4>
                    <p><strong>Time:</strong> {alert.get('timestamp', '')}</p>
                    <p><strong>Confidence:</strong> {alert.get('confidence', 0)}%</p>
                    <p><strong>Entry:</strong> ${alert.get('entry_price', 0):.2f} | 
                    <strong>SL:</strong> ${alert.get('stop_loss', 0):.2f} | 
                    <strong>TP:</strong> ${alert.get('take_profit', 0):.2f}</p>
                    <p><strong>Analysis:</strong> {alert.get('analysis', '')}</p>
                </div>
                """, unsafe_allow_html=True)
            
            elif alert.get('type') == 'kill_zone':
                st.markdown(f"""
                <div class="status-box">
                    <h3>⏰ {alert.get('zone_name', '')}</h3>
                    <p><strong>Time:</strong> {alert.get('timestamp', '')}</p>
                    <p>{alert.get('description', '')}</p>
                    <p>Multiplier: {alert.get('multiplier', 1.0)}x | Priority: {alert.get('priority', 0)}/5</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Export alerts option
    if st.button("Export Alert History to CSV"):
        df = pd.DataFrame(filtered_alerts)
        csv = df.to_csv(index=False)
        st.download_button(
            "Download CSV",
            csv,
            f"alert_history_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )

def display_realtime_alerts():
    """Display real-time alert monitoring dashboard"""
    st.subheader("🔍 Real-time Alert Monitor")
    
    # Auto-refresh toggle
    auto_refresh = st.checkbox("Auto-refresh every 30 seconds", value=True)
    
    if auto_refresh:
        st.write("Monitoring for high-confidence signals...")
        
        # In a real implementation, you would have a background thread
        # For demo, we'll simulate with a button
        if st.button("Check for New Alerts Now"):
            # Simulate checking for alerts
            st.info("Scanning top 10 assets for high-confidence signals...")
            
            # Get current kill zone
            kill_zone = get_kill_zone()
            
            # Display current monitoring status
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Confidence Threshold", f"{st.session_state.preferences.get('alert_threshold', 90)}%")
            with col2:
                st.metric("Active Kill Zone", kill_zone['name'])
            with col3:
                st.metric("Alert Channels", 
                         sum(1 for service in st.session_state.preferences['notification_services'].values() 
                             if service.get('enabled', False)))
            
            # Show last sent alert
            if st.session_state.sent_alerts:
                last_alert = st.session_state.sent_alerts[-1]
                st.markdown(f"""
                <div class="alert-box">
                    <h4>📨 Last Alert Sent</h4>
                    <p><strong>{last_alert.get('symbol', '')}</strong> - {last_alert.get('signal', '')}</p>
                    <p>Time: {last_alert.get('timestamp', '')} | Confidence: {last_alert.get('confidence', 0)}%</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Quick alert creation
    st.write("---")
    st.subheader("📝 Create Manual Alert")
    
    col1, col2 = st.columns(2)
    with col1:
        manual_symbol = st.text_input("Symbol", placeholder="AAPL, BTC, etc.")
        manual_signal = st.selectbox("Signal Type", ["BUY", "SELL", "STRONG BUY", "STRONG SELL"])
        manual_confidence = st.slider("Confidence", 70, 99, 85)
    
    with col2:
        manual_price = st.number_input("Current Price", min_value=0.01, step=0.01)
        manual_sl = st.number_input("Stop Loss", min_value=0.01, step=0.01)
        manual_tp = st.number_input("Take Profit", min_value=0.01, step=0.01)
    
    manual_analysis = st.text_area("Analysis Notes", placeholder="Enter your analysis here...")
    
    if st.button("Send Manual Alert"):
        if manual_symbol and manual_price > 0:
            manual_alert = {
                'type': 'trade_signal',
                'symbol': manual_symbol,
                'signal': manual_signal,
                'confidence': manual_confidence,
                'current_price': manual_price,
                'entry_price': manual_price,
                'stop_loss': manual_sl,
                'take_profit': manual_tp,
                'analysis': manual_analysis or "Manual alert created by user",
                'risk_level': 5,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            notification_manager.config = st.session_state.preferences['notification_services']
            results = notification_manager.send_multichannel_alert(manual_alert)
            
            st.session_state.sent_alerts.append({
                **manual_alert,
                'sent_time': datetime.now().isoformat()
            })
            
            success_count = sum(1 for r in results.values() if r)
            st.success(f"Manual alert sent via {success_count} channel(s)!")

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
                assets_to_analyze = NIFTY_50[:analyze_count]

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


if __name__ == "__main__":
    main()
