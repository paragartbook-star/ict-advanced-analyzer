# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION WITH ENHANCED NAVIGATION
# ═══════════════════════════════════════════════════════════════════════════════

def create_sidebar_navigation():
    with st.sidebar:
        # Logo and Header
        st.markdown("""
        <div style="padding: 20px 0 16px 0; text-align: center;">
            <div style="font-size: 32px; margin-bottom: 8px;">📈</div>
            <h3 style="color: #FFFFFF; margin: 0; font-weight: 600;">ICT Pro</h3>
            <p style="color: #9CA3AF; font-size: 12px; margin: 4px 0 0 0; letter-spacing: 1px;">TRADING ANALYZER</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Navigation Header
        st.markdown('<p class="nav-section-header">NAVIGATION</p>', unsafe_allow_html=True)
        
        # Navigation Items
        nav_items = [
            ("📊", "Market Analysis", "Market Analysis"),
            ("👁️", "Watchlist", "Watchlist"),
            ("💼", "Portfolio", "Portfolio"),
            ("🔔", "Alerts", "Alerts"),
            ("⏮️", "Backtesting", "Backtesting"),
            ("📈", "Correlation", "Correlation"),
            ("⚙️", "Settings", "Settings")
        ]
        
        # Create navigation buttons
        for icon, label, page_key in nav_items:
            is_active = (st.session_state.current_page == page_key)
            
            if is_active:
                # Portfolio के लिए special indicator
                if page_key == "Portfolio":
                    button_html = f"""
                    <div style="
                        background: linear-gradient(135deg, rgba(37, 99, 235, 0.15) 0%, rgba(29, 78, 216, 0.15) 100%);
                        color: #2563EB;
                        padding: 12px 16px;
                        margin: 4px 0;
                        border-radius: 8px;
                        border-left: 3px solid #2563EB;
                        display: flex;
                        align-items: center;
                        gap: 12px;
                        font-weight: 500;
                    ">
                        <span>{icon}</span>
                        <span style="flex-grow: 1;">{label}</span>
                        <span style="background: rgba(37, 99, 235, 0.2); color: #2563EB; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 500;">●</span>
                    </div>
                    """
                else:
                    button_html = f"""
                    <div style="
                        background: linear-gradient(135deg, rgba(37, 99, 235, 0.15) 0%, rgba(29, 78, 216, 0.15) 100%);
                        color: #2563EB;
                        padding: 12px 16px;
                        margin: 4px 0;
                        border-radius: 8px;
                        border-left: 3px solid #2563EB;
                        display: flex;
                        align-items: center;
                        gap: 12px;
                        font-weight: 500;
                    ">
                        <span>{icon}</span>
                        <span>{label}</span>
                    </div>
                    """
            else:
                button_html = f"""
                <div style="
                    color: #9CA3AF;
                    padding: 12px 16px;
                    margin: 4px 0;
                    border-radius: 8px;
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    transition: all 0.2s ease;
                    cursor: pointer;
                " onmouseover="this.style.backgroundColor='rgba(255,255,255,0.05)'; this.style.color='#E0E0E0';" 
                     onmouseout="this.style.backgroundColor='transparent'; this.style.color='#9CA3AF';">
                    <span>{icon}</span>
                    <span>{label}</span>
                </div>
                """
            
            st.markdown(button_html, unsafe_allow_html=True)
            
            # Add invisible button for click handling
            if st.button(label, key=f"nav_{page_key}", 
                        type="primary" if is_active else "secondary",
                        use_container_width=True, label_visibility="collapsed"):
                st.session_state.current_page = page_key
                st.rerun()
        
        st.divider()
        
        # Quick Stats
        st.markdown('<p class="nav-section-header">QUICK STATS</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Watchlist", len(st.session_state.watchlist), label_visibility="visible")
        with col2:
            st.metric("Portfolio", len(st.session_state.portfolio), label_visibility="visible")
        
        # Active Portfolio Indicator
        if st.session_state.current_page == "Portfolio" and st.session_state.portfolio:
            total_value, total_pnl = calculate_portfolio_value()
            pnl_color = "positive" if total_pnl >= 0 else "negative"
            
            st.markdown(f"""
            <div class="active-portfolio-indicator">
                <div class="active-dot"></div>
                <div style="flex-grow: 1;">
                    <div style="font-size: 13px; font-weight: 500; color: #2563EB;">Portfolio Active</div>
                    <div style="font-size: 11px; color: #9CA3AF;">{len(st.session_state.portfolio)} positions</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 14px; font-weight: 600; color: #FFFFFF;">${total_value:,.0f}</div>
                    <div class="{pnl_color}" style="font-size: 11px;">${total_pnl:+,.0f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # System Status
        kill_zone = get_kill_zone()
        status_color = "#10B981" if kill_zone['active'] else "#6B7280"
        
        st.markdown('<p class="nav-section-header">SYSTEM STATUS</p>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="
            background-color: #1A1D29;
            border: 1px solid #2A2D3A;
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 8px;
        ">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <span style="color: #E0E0E0; font-size: 13px; font-weight: 500;">Kill Zone</span>
                <span style="color: {status_color}; font-size: 12px; display: flex; align-items: center; gap: 4px;">
                    <span style="display: inline-block; width: 6px; height: 6px; background: {status_color}; border-radius: 50%;"></span>
                    {kill_zone['name']}
                </span>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <span style="color: #9CA3AF; font-size: 12px;">Multiplier</span>
                <span style="color: #E0E0E0; font-size: 12px; font-weight: 500;">{kill_zone['multiplier']}x</span>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 8px;">
                <span style="color: #9CA3AF; font-size: 12px;">Priority</span>
                <span style="color: #E0E0E0; font-size: 12px; font-weight: 500;">{kill_zone['priority']}/5</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Footer
        st.markdown(f"""
        <div style="
            text-align: center;
            color: #6B7280;
            font-size: 11px;
            padding: 16px 0 8px 0;
            margin-top: 16px;
            border-top: 1px solid #2A2D3A;
        ">
            {datetime.now().strftime('%Y-%m-%d %H:%M')}
        </div>
        """, unsafe_allow_html=True)

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
    
    # Create Sidebar Navigation
    create_sidebar_navigation()
    
    # Page Routing based on current_page
    current_page = st.session_state.current_page
    
    if current_page == "Market Analysis":
        display_market_analysis_page(kill_zone)
    elif current_page == "Watchlist":
        display_watchlist_page()
    elif current_page == "Portfolio":
        display_portfolio_page()
    elif current_page == "Alerts":
        display_alerts_page()
    elif current_page == "Backtesting":
        display_backtesting_page()
    elif current_page == "Correlation":
        display_correlation_page()
    elif current_page == "Settings":
        display_settings_page()

def display_market_analysis_page(kill_zone):
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

def display_watchlist_page():
    display_watchlist()

def display_portfolio_page():
    display_portfolio()

def display_alerts_page():
    display_alerts()

def display_backtesting_page():
    display_backtesting()

def display_correlation_page():
    display_correlation_analysis()

def display_settings_page():
    display_settings()

if __name__ == "__main__":
    main()
