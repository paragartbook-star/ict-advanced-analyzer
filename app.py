<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Trading Dashboard</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            /* Primary Colors - Professional Blue Theme */
            --primary-dark: #0c1a2d;
            --primary-blue: #1a2b3c;
            --secondary-blue: #2d3b4e;
            --accent-blue: #4a9eff;
            --accent-green: #10b981;
            --accent-red: #ef4444;
            --accent-orange: #f59e0b;
            --accent-purple: #8b5cf6;
            
            /* Text Colors */
            --text-primary: #ffffff;
            --text-secondary: #b0c7e8;
            --text-muted: #8a9bb8;
            
            /* Background Colors */
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --bg-card: rgba(30, 41, 59, 0.8);
            --bg-hover: rgba(255, 255, 255, 0.05);
            
            /* Borders */
            --border-color: rgba(74, 158, 255, 0.2);
            --border-light: rgba(255, 255, 255, 0.1);
            
            /* Spacing */
            --spacing-xs: 4px;
            --spacing-sm: 8px;
            --spacing-md: 16px;
            --spacing-lg: 24px;
            --spacing-xl: 32px;
            --spacing-xxl: 48px;
            
            /* Typography */
            --font-size-xs: 12px;
            --font-size-sm: 14px;
            --font-size-md: 16px;
            --font-size-lg: 20px;
            --font-size-xl: 24px;
            --font-size-xxl: 32px;
            
            /* Border Radius */
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
            --radius-xl: 20px;
            
            /* Shadows */
            --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.1);
            --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.2);
            --shadow-xl: 0 20px 40px rgba(0, 0, 0, 0.3);
            
            /* Transitions */
            --transition-fast: 150ms ease;
            --transition-normal: 300ms ease;
            --transition-slow: 500ms ease;
        }
        
        /* Base Styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-blue) 100%);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
            padding: var(--spacing-lg);
            letter-spacing: 0.3px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: var(--spacing-xl);
        }
        
        /* Header Styles */
        .header {
            background: linear-gradient(135deg, 
                rgba(19, 28, 46, 0.95) 0%,
                rgba(26, 43, 60, 0.95) 100%);
            backdrop-filter: blur(10px);
            border-radius: var(--radius-lg);
            padding: var(--spacing-lg) var(--spacing-xl);
            border: 1px solid var(--border-color);
            box-shadow: var(--shadow-xl);
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all var(--transition-normal);
        }
        
        .header:hover {
            border-color: rgba(74, 158, 255, 0.4);
            box-shadow: var(--shadow-xl), 0 0 30px rgba(74, 158, 255, 0.1);
        }
        
        .logo-container {
            display: flex;
            align-items: center;
            gap: var(--spacing-md);
        }
        
        .logo-icon {
            color: var(--accent-blue);
            font-size: 28px;
            background: rgba(74, 158, 255, 0.1);
            width: 52px;
            height: 52px;
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px solid rgba(74, 158, 255, 0.3);
            transition: all var(--transition-normal);
        }
        
        .logo-icon:hover {
            transform: rotate(10deg);
            background: rgba(74, 158, 255, 0.2);
            border-color: var(--accent-blue);
        }
        
        .logo-text {
            display: flex;
            flex-direction: column;
            gap: var(--spacing-xs);
        }
        
        .logo-main {
            font-size: var(--font-size-xl);
            font-weight: 700;
            background: linear-gradient(90deg, var(--accent-blue), #6bb5ff);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            letter-spacing: 0.5px;
        }
        
        .logo-sub {
            font-size: var(--font-size-sm);
            color: var(--text-muted);
            font-weight: 400;
        }
        
        .nav-controls {
            display: flex;
            gap: var(--spacing-md);
            align-items: center;
        }
        
        /* Button Styles */
        .btn {
            padding: 12px 24px;
            border-radius: var(--radius-md);
            border: none;
            font-weight: 600;
            font-size: var(--font-size-sm);
            cursor: pointer;
            transition: all var(--transition-normal);
            display: inline-flex;
            align-items: center;
            gap: var(--spacing-sm);
            letter-spacing: 0.3px;
            font-family: inherit;
            outline: none;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, var(--accent-blue) 0%, #2d7dd2 100%);
            color: white;
            box-shadow: 0 4px 15px rgba(74, 158, 255, 0.3);
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(74, 158, 255, 0.4);
        }
        
        .btn-primary:active {
            transform: translateY(0);
        }
        
        .btn-secondary {
            background: rgba(255, 255, 255, 0.08);
            color: var(--text-secondary);
            border: 1px solid var(--border-light);
        }
        
        .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.12);
            border-color: rgba(74, 158, 255, 0.4);
        }
        
        .btn-icon {
            padding: 10px;
            width: 40px;
            height: 40px;
            justify-content: center;
        }
        
        /* Main Content Layout */
        .main-content {
            display: grid;
            grid-template-columns: 1fr 350px;
            gap: var(--spacing-xl);
        }
        
        /* Chart Container */
        .chart-container {
            background: linear-gradient(135deg, 
                rgba(19, 28, 46, 0.95) 0%,
                rgba(26, 43, 60, 0.95) 100%);
            backdrop-filter: blur(10px);
            border-radius: var(--radius-lg);
            padding: var(--spacing-lg);
            border: 1px solid var(--border-color);
            box-shadow: var(--shadow-xl);
        }
        
        .chart-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: var(--spacing-lg);
            padding-bottom: var(--spacing-md);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }
        
        .chart-title {
            font-size: var(--font-size-lg);
            font-weight: 600;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: var(--spacing-sm);
        }
        
        .chart-title i {
            color: var(--accent-blue);
        }
        
        .timeframe-selector {
            display: flex;
            gap: var(--spacing-xs);
            background: rgba(255, 255, 255, 0.05);
            padding: 6px;
            border-radius: var(--radius-md);
        }
        
        .timeframe-btn {
            padding: 8px 16px;
            border-radius: var(--radius-sm);
            background: transparent;
            color: var(--text-secondary);
            border: none;
            font-size: var(--font-size-sm);
            font-weight: 500;
            cursor: pointer;
            transition: all var(--transition-fast);
            font-family: inherit;
        }
        
        .timeframe-btn:hover {
            background: rgba(255, 255, 255, 0.1);
        }
        
        .timeframe-btn.active {
            background: rgba(74, 158, 255, 0.2);
            color: var(--accent-blue);
        }
        
        /* Chart Area */
        .chart-placeholder {
            background: rgba(10, 18, 30, 0.7);
            height: 500px;
            border-radius: var(--radius-md);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: var(--text-muted);
            border: 1px dashed var(--border-light);
            transition: all var(--transition-normal);
        }
        
        .chart-placeholder:hover {
            border-color: rgba(74, 158, 255, 0.4);
        }
        
        .chart-icon {
            font-size: 64px;
            margin-bottom: var(--spacing-md);
            color: rgba(74, 158, 255, 0.3);
        }
        
        /* Sidebar */
        .sidebar {
            display: flex;
            flex-direction: column;
            gap: var(--spacing-xl);
        }
        
        /* Widget Styles */
        .widget {
            background: linear-gradient(135deg, 
                rgba(19, 28, 46, 0.95) 0%,
                rgba(26, 43, 60, 0.95) 100%);
            backdrop-filter: blur(10px);
            border-radius: var(--radius-lg);
            padding: var(--spacing-lg);
            border: 1px solid var(--border-color);
            box-shadow: var(--shadow-xl);
            transition: all var(--transition-normal);
        }
        
        .widget:hover {
            transform: translateY(-2px);
            border-color: rgba(74, 158, 255, 0.4);
        }
        
        .widget-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: var(--spacing-lg);
        }
        
        .widget-title {
            font-size: var(--font-size-md);
            font-weight: 600;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: var(--spacing-sm);
        }
        
        .widget-title i {
            color: var(--accent-blue);
        }
        
        /* Market Data */
        .market-list {
            display: flex;
            flex-direction: column;
            gap: var(--spacing-md);
        }
        
        .market-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: var(--spacing-sm) 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            transition: all var(--transition-fast);
        }
        
        .market-item:hover {
            background: var(--bg-hover);
            border-radius: var(--radius-sm);
            padding: var(--spacing-sm) var(--spacing-md);
        }
        
        .market-item:last-child {
            border-bottom: none;
        }
        
        .market-name {
            display: flex;
            align-items: center;
            gap: var(--spacing-md);
        }
        
        .market-icon {
            width: 32px;
            height: 32px;
            background: rgba(74, 158, 255, 0.1);
            border-radius: var(--radius-sm);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--accent-blue);
        }
        
        .market-symbol {
            font-weight: 600;
            color: var(--text-primary);
            font-size: var(--font-size-sm);
        }
        
        .market-fullname {
            font-size: var(--font-size-xs);
            color: var(--text-muted);
        }
        
        .market-price {
            font-weight: 600;
            color: var(--text-primary);
            font-size: var(--font-size-sm);
        }
        
        .market-change {
            padding: 4px 10px;
            border-radius: var(--radius-sm);
            font-size: var(--font-size-xs);
            font-weight: 600;
            min-width: 60px;
            text-align: center;
        }
        
        .positive {
            background: rgba(16, 185, 129, 0.15);
            color: var(--accent-green);
        }
        
        .negative {
            background: rgba(239, 68, 68, 0.15);
            color: var(--accent-red);
        }
        
        /* Trade Panel */
        .trade-panel {
            display: flex;
            flex-direction: column;
            gap: var(--spacing-lg);
        }
        
        .trade-input-group {
            display: flex;
            flex-direction: column;
            gap: var(--spacing-sm);
        }
        
        .input-label {
            font-size: var(--font-size-sm);
            color: var(--text-secondary);
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: var(--spacing-xs);
        }
        
        .input-label i {
            color: var(--accent-blue);
            font-size: 12px;
        }
        
        .input-field {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-md);
            padding: 14px 16px;
            color: var(--text-primary);
            font-size: var(--font-size-md);
            transition: all var(--transition-normal);
            font-family: inherit;
            outline: none;
        }
        
        .input-field:focus {
            outline: none;
            border-color: var(--accent-blue);
            background: rgba(255, 255, 255, 0.08);
            box-shadow: 0 0 0 3px rgba(74, 158, 255, 0.1);
        }
        
        .input-field::placeholder {
            color: var(--text-muted);
        }
        
        .input-row {
            display: flex;
            gap: var(--spacing-md);
        }
        
        .input-row .trade-input-group {
            flex: 1;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: var(--spacing-lg);
            color: var(--text-muted);
            font-size: var(--font-size-sm);
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            margin-top: var(--spacing-lg);
        }
        
        /* Responsive Design */
        @media (max-width: 1200px) {
            .main-content {
                grid-template-columns: 1fr;
            }
            
            .container {
                gap: var(--spacing-lg);
            }
        }
        
        @media (max-width: 768px) {
            .header {
                flex-direction: column;
                gap: var(--spacing-md);
                text-align: center;
                padding: var(--spacing-md);
            }
            
            .logo-container {
                flex-direction: column;
                text-align: center;
            }
            
            .input-row {
                flex-direction: column;
                gap: var(--spacing-md);
            }
            
            .nav-controls {
                flex-wrap: wrap;
                justify-content: center;
            }
            
            .btn {
                padding: 10px 18px;
                font-size: var(--font-size-sm);
            }
            
            .chart-placeholder {
                height: 400px;
            }
            
            body {
                padding: var(--spacing-md);
            }
        }
        
        @media (max-width: 480px) {
            :root {
                --spacing-lg: 16px;
                --spacing-xl: 20px;
            }
            
            .widget {
                padding: var(--spacing-md);
            }
            
            .market-item {
                flex-direction: column;
                align-items: flex-start;
                gap: var(--spacing-sm);
            }
            
            .market-name {
                width: 100%;
                justify-content: space-between;
            }
        }
        
        /* Utility Classes */
        .text-center { text-align: center; }
        .text-right { text-align: right; }
        .mb-sm { margin-bottom: var(--spacing-sm); }
        .mb-md { margin-bottom: var(--spacing-md); }
        .mb-lg { margin-bottom: var(--spacing-lg); }
        .mt-sm { margin-top: var(--spacing-sm); }
        .mt-md { margin-top: var(--spacing-md); }
        .mt-lg { margin-top: var(--spacing-lg); }
        .p-sm { padding: var(--spacing-sm); }
        .p-md { padding: var(--spacing-md); }
        .p-lg { padding: var(--spacing-lg); }
        
        /* Animation Classes */
        .fade-in {
            animation: fadeIn var(--transition-slow) ease-in;
        }
        
        .slide-up {
            animation: slideUp var(--transition-normal) ease-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes slideUp {
            from { 
                opacity: 0;
                transform: translateY(20px);
            }
            to { 
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: rgba(74, 158, 255, 0.3);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(74, 158, 255, 0.5);
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header class="header slide-up">
            <div class="logo-container">
                <div class="logo-icon">
                    <i class="fas fa-chart-line"></i>
                </div>
                <div class="logo-text">
                    <div class="logo-main">SmartTrade Pro</div>
                    <div class="logo-sub">Professional Trading Dashboard</div>
                </div>
            </div>
            
            <div class="nav-controls">
                <button class="btn btn-secondary">
                    <i class="fas fa-cog"></i> Settings
                </button>
                <button class="btn btn-primary">
                    <i class="fas fa-user-circle"></i> Account
                </button>
                <button class="btn btn-icon btn-secondary">
                    <i class="fas fa-bell"></i>
                </button>
            </div>
        </header>
        
        <!-- Main Content -->
        <div class="main-content fade-in">
            <!-- Main Chart Area -->
            <div class="chart-container">
                <div class="chart-header">
                    <div class="chart-title">
                        <i class="fas fa-chart-candlestick"></i>
                        BTC/USD Chart
                    </div>
                    <div class="timeframe-selector">
                        <button class="timeframe-btn active">1D</button>
                        <button class="timeframe-btn">1W</button>
                        <button class="timeframe-btn">1M</button>
                        <button class="timeframe-btn">3M</button>
                        <button class="timeframe-btn">1Y</button>
                    </div>
                </div>
                
                <div class="chart-placeholder">
                    <i class="fas fa-chart-area chart-icon"></i>
                    <p class="mb-sm">Interactive Chart Area</p>
                    <p style="font-size: 14px; color: var(--text-muted);">Real-time price data visualization with technical indicators</p>
                </div>
                
                <div class="chart-footer mt-md">
                    <div class="input-row">
                        <div class="trade-input-group">
                            <label class="input-label">
                                <i class="fas fa-info-circle"></i>
                                Chart Settings
                            </label>
                            <select class="input-field">
                                <option>Show All Indicators</option>
                                <option>RSI Only</option>
                                <option>MACD Only</option>
                                <option>Volume Only</option>
                            </select>
                        </div>
                        <div class="trade-input-group">
                            <label class="input-label">
                                <i class="fas fa-palette"></i>
                                Theme
                            </label>
                            <select class="input-field">
                                <option>Dark Theme</option>
                                <option>Light Theme</option>
                                <option>High Contrast</option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Sidebar -->
            <div class="sidebar">
                <!-- Market Overview -->
                <div class="widget slide-up" style="animation-delay: 100ms">
                    <div class="widget-header">
                        <div class="widget-title">
                            <i class="fas fa-globe"></i>
                            Market Overview
                        </div>
                        <button class="btn btn-icon btn-secondary">
                            <i class="fas fa-sync-alt"></i>
                        </button>
                    </div>
                    
                    <div class="market-list">
                        <div class="market-item">
                            <div class="market-name">
                                <div class="market-icon">
                                    <i class="fab fa-bitcoin"></i>
                                </div>
                                <div>
                                    <div class="market-symbol">BTC/USD</div>
                                    <div class="market-fullname">Bitcoin</div>
                                </div>
                            </div>
                            <div class="market-price">$42,850.30</div>
                            <div class="market-change positive">+2.4%</div>
                        </div>
                        
                        <div class="market-item">
                            <div class="market-name">
                                <div class="market-icon">
                                    <i class="fab fa-ethereum"></i>
                                </div>
                                <div>
                                    <div class="market-symbol">ETH/USD</div>
                                    <div class="market-fullname">Ethereum</div>
                                </div>
                            </div>
                            <div class="market-price">$2,340.50</div>
                            <div class="market-change positive">+1.8%</div>
                        </div>
                        
                        <div class="market-item">
                            <div class="market-name">
                                <div class="market-icon">
                                    <i class="fas fa-chart-line"></i>
                                </div>
                                <div>
                                    <div class="market-symbol">SPX</div>
                                    <div class="market-fullname">S&P 500</div>
                                </div>
                            </div>
                            <div class="market-price">$4,780.23</div>
                            <div class="market-change negative">-0.5%</div>
                        </div>
                        
                        <div class="market-item">
                            <div class="market-name">
                                <div class="market-icon">
                                    <i class="fas fa-dollar-sign"></i>
                                </div>
                                <div>
                                    <div class="market-symbol">EUR/USD</div>
                                    <div class="market-fullname">Euro Dollar</div>
                                </div>
                            </div>
                            <div class="market-price">1.0854</div>
                            <div class="market-change positive">+0.2%</div>
                        </div>
                        
                        <div class="market-item">
                            <div class="market-name">
                                <div class="market-icon">
                                    <i class="fas fa-gem"></i>
                                </div>
                                <div>
                                    <div class="market-symbol">GOLD</div>
                                    <div class="market-fullname">Gold Spot</div>
                                </div>
                            </div>
                            <div class="market-price">$2,034.80</div>
                            <div class="market-change positive">+0.8%</div>
                        </div>
                    </div>
                </div>
                
                <!-- Trade Panel -->
                <div class="widget slide-up" style="animation-delay: 200ms">
                    <div class="widget-header">
                        <div class="widget-title">
                            <i class="fas fa-exchange-alt"></i>
                            Quick Trade
                        </div>
                        <div class="market-change positive">Live</div>
                    </div>
                    
                    <div class="trade-panel">
                        <div class="trade-input-group">
                            <label class="input-label">
                                <i class="fas fa-coins"></i>
                                Asset
                            </label>
                            <select class="input-field">
                                <option>BTC/USD</option>
                                <option>ETH/USD</option>
                                <option>SOL/USD</option>
                                <option>SPX</option>
                                <option>EUR/USD</option>
                            </select>
                        </div>
                        
                        <div class="input-row">
                            <div class="trade-input-group">
                                <label class="input-label">
                                    <i class="fas fa-money-bill-wave"></i>
                                    Amount
                                </label>
                                <input type="number" class="input-field" placeholder="0.00" step="0.01">
                            </div>
                            <div class="trade-input-group">
                                <label class="input-label">
                                    <i class="fas fa-balance-scale"></i>
                                    Leverage
                                </label>
                                <select class="input-field">
                                    <option>1x</option>
                                    <option>3x</option>
                                    <option>5x</option>
                                    <option>10x</option>
                                </select>
                            </div>
                        </div>
                        
                        <div class="trade-input-group">
                            <label class="input-label">
                                <i class="fas fa-sliders-h"></i>
                                Risk Percentage
                                <span style="color: var(--accent-blue); margin-left: auto;">25%</span>
                            </label>
                            <input type="range" class="slider" min="1" max="100" value="25">
                            <div class="value-display">
                                <span>Low Risk</span>
                                <span>High Risk</span>
                            </div>
                        </div>
                        
                        <div class="input-row">
                            <button class="btn btn-primary" style="flex: 1;">
                                <i class="fas fa-arrow-up"></i>
                                Buy/Long
                            </button>
                            <button class="btn" style="flex: 1; background: rgba(239, 68, 68, 0.1); color: var(--accent-red); border: 1px solid rgba(239, 68, 68, 0.3);">
                                <i class="fas fa-arrow-down"></i>
                                Sell/Short
                            </button>
                        </div>
                    </div>
                </div>
                
                <!-- Account Summary -->
                <div class="widget slide-up" style="animation-delay: 300ms">
                    <div class="widget-header">
                        <div class="widget-title">
                            <i class="fas fa-wallet"></i>
                            Account Summary
                        </div>
                        <i class="fas fa-eye" style="color: var(--accent-blue); cursor: pointer;"></i>
                    </div>
                    
                    <div class="market-list">
                        <div class="market-item">
                            <div class="market-name">
                                <div>Balance</div>
                            </div>
                            <div class="market-price">$24,850.30</div>
                        </div>
                        
                        <div class="market-item">
                            <div class="market-name">
                                <div>Equity</div>
                            </div>
                            <div class="market-price">$26,340.50</div>
                        </div>
                        
                        <div class="market-item">
                            <div class="market-name">
                                <div>Free Margin</div>
                            </div>
                            <div class="market-price">$18,780.23</div>
                        </div>
                        
                        <div class="market-item">
                            <div class="market-name">
                                <div>Daily P&L</div>
                            </div>
                            <div class="market-change positive">+$1,234.56</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Footer -->
        <footer class="footer">
            <div class="container">
                <p>© 2024 SmartTrade Pro. Professional Trading Dashboard. All market data is simulated for demonstration purposes.</p>
                <p style="margin-top: var(--spacing-sm); font-size: 12px; color: var(--text-muted);">
                    <i class="fas fa-shield-alt"></i> Secure Connection | 
                    <i class="fas fa-bolt"></i> Real-time Data | 
                    <i class="fas fa-chart-bar"></i> Advanced Analytics
                </p>
            </div>
        </footer>
    </div>

    <script>
        // Initialize animations
        document.addEventListener('DOMContentLoaded', function() {
            // Add hover effects to all interactive elements
            const interactiveElements = document.querySelectorAll('.btn, .market-item, .timeframe-btn');
            interactiveElements.forEach(el => {
                el.addEventListener('mouseenter', () => {
                    el.style.transform = 'translateY(-2px)';
                });
                el.addEventListener('mouseleave', () => {
                    el.style.transform = 'translateY(0)';
                });
            });
            
            // Timeframe selector functionality
            const timeframeButtons = document.querySelectorAll('.timeframe-btn');
            timeframeButtons.forEach(btn => {
                btn.addEventListener('click', function() {
                    timeframeButtons.forEach(b => b.classList.remove('active'));
                    this.classList.add('active');
                });
            });
            
            // Simulate live data updates
            function updateMarketData() {
                const prices = document.querySelectorAll('.market-price');
                const changes = document.querySelectorAll('.market-change');
                
                prices.forEach(price => {
                    const current = parseFloat(price.textContent.replace(/[^0-9.]/g, ''));
                    const change = (Math.random() - 0.5) * 0.02 * current;
                    const newPrice = current + change;
                    price.textContent = '$' + newPrice.toLocaleString('en-US', {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2
                    });
                });
                
                changes.forEach(change => {
                    const currentChange = parseFloat(change.textContent.replace(/[^0-9.-]/g, ''));
                    const newChange = currentChange + (Math.random() - 0.5) * 0.5;
                    change.textContent = (newChange >= 0 ? '+' : '') + newChange.toFixed(2) + '%';
                    change.className = 'market-change ' + (newChange >= 0 ? 'positive' : 'negative');
                });
            }
            
            // Update data every 5 seconds (simulated)
            setInterval(updateMarketData, 5000);
        });
    </script>
</body>
</html>
