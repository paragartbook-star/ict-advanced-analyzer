import React, { useState, useEffect, useRef } from 'react';
import { 
  TrendingUp, TrendingDown, AlertTriangle, Clock, Target, Zap, 
  Brain, ChevronDown, ChevronUp, BarChart3, Activity, Shield,
  DollarSign, Globe, Cpu, Database, Wallet, Users, Lock, 
  RadioTower, Satellite, CloudLightning, Sparkles, Robot,
  Mic, Video, MessageSquare, Bell, Settings, LogOut,
  RefreshCw, Download, Upload, Filter, Search,
  PieChart, LineChart, CandlestickChart, Eye, EyeOff, Star, Bookmark
} from 'lucide-react';

const ICTAdvancedAnalyzer2026 = () => {
  // State Management
  const [currentTime, setCurrentTime] = useState(new Date());
  const [selectedMarket, setSelectedMarket] = useState('AI Stocks');
  const [sortBy, setSortBy] = useState('Quantum Score');
  const [expandedAsset, setExpandedAsset] = useState(null);
  const [viewMode, setViewMode] = useState('grid');
  const [theme, setTheme] = useState('dark');
  const [userPreferences, setUserPreferences] = useState({
    notifications: true,
    autoRefresh: true,
    aiSuggestions: true,
    riskAlerts: true
  });
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedSectors, setSelectedSectors] = useState([]);
  const [riskFilter, setRiskFilter] = useState('all');
  const [timeFrame, setTimeFrame] = useState('1D');
  const [aiMode, setAiMode] = useState('aggressive');
  
  const audioRef = useRef(null);
  
  // Market Data
  const quantumMarkets2026 = {
    'AI Stocks': [
      { symbol: 'NVDA', name: 'NVIDIA Quantum', sector: 'Quantum AI/Semiconductors', marketCap: '3.2T' },
      { symbol: 'MSFT', name: 'Microsoft Copilot AI', sector: 'Enterprise AI/Quantum', marketCap: '4.1T' },
      { symbol: 'GOOGL', name: 'Google Gemini', sector: 'Quantum Search/AI', marketCap: '2.8T' },
      { symbol: 'META', name: 'Meta Metaverse AI', sector: 'Social VR/AI', marketCap: '1.9T' },
      { symbol: 'AAPL', name: 'Apple Vision AI', sector: 'Consumer Quantum Tech', marketCap: '3.5T' },
      { symbol: 'PLTR', name: 'Palantir AIP', sector: 'Gov AI/Quantum', marketCap: '120B' },
      { symbol: 'TSLA', name: 'Tesla Optimus', sector: 'Robotics/AI', marketCap: '900B' },
      { symbol: 'AMD', name: 'AMD MI300X', sector: 'AI Accelerators', marketCap: '350B' },
      { symbol: 'SNOW', name: 'Snowflake Cortex', sector: 'AI Data Cloud', marketCap: '85B' },
      { symbol: 'CRWD', name: 'CrowdStrike AI', sector: 'Cybersecurity AI', marketCap: '110B' }
    ],
    'Quantum Computing': [
      { symbol: 'IONQ', name: 'IonQ', sector: 'Quantum Hardware', marketCap: '8.5B' },
      { symbol: 'RGTI', name: 'Rigetti Computing', sector: 'Quantum Processors', marketCap: '3.2B' },
      { symbol: 'QBTS', name: 'D-Wave Quantum', sector: 'Quantum Annealing', marketCap: '2.8B' },
      { symbol: 'IBM', name: 'IBM Quantum', sector: 'Quantum Cloud', marketCap: '180B' },
      { symbol: 'GOOG', name: 'Google Quantum AI', sector: 'Quantum Supremacy', marketCap: '2.8T' }
    ],
    'Neural Tech': [
      { symbol: 'SYNX', name: 'Synaptics Neural', sector: 'Brain-Computer Interface', marketCap: '4.5B' },
      { symbol: 'AI', name: 'C3.ai Enterprise', sector: 'Enterprise AI Platform', marketCap: '4.8B' },
      { symbol: 'PATH', name: 'UiPath', sector: 'Process Automation AI', marketCap: '15B' },
      { symbol: 'ASAN', name: 'Asana AI', sector: 'Work Intelligence', marketCap: '6.5B' }
    ],
    'Crypto AI': [
      { symbol: 'TAO', name: 'Bittensor', sector: 'Decentralized AI', marketCap: '18B' },
      { symbol: 'RNDR', name: 'Render Network', sector: 'GPU AI Rendering', marketCap: '4.2B' },
      { symbol: 'AKT', name: 'Akash Network', sector: 'Decentralized Cloud AI', marketCap: '1.8B' },
      { symbol: 'FET', name: 'Fetch.ai', sector: 'AI Agents Platform', marketCap: '3.5B' },
      { symbol: 'AGIX', name: 'SingularityNET', sector: 'AI Marketplace', marketCap: '2.1B' }
    ],
    'Space Tech': [
      { symbol: 'SPCE', name: 'Virgin Galactic', sector: 'Space Tourism', marketCap: '2.1B' },
      { symbol: 'ASTS', name: 'AST SpaceMobile', sector: 'Satellite Internet', marketCap: '3.8B' },
      { symbol: 'RKLB', name: 'Rocket Lab', sector: 'Rocket Launch', marketCap: '2.4B' }
    ],
    'Energy AI': [
      { symbol: 'NEE', name: 'NextEra Energy AI', sector: 'Renewable AI Grid', marketCap: '150B' },
      { symbol: 'ENPH', name: 'Enphase AI', sector: 'Smart Solar AI', marketCap: '25B' },
      { symbol: 'PLUG', name: 'Plug Power AI', sector: 'Hydrogen AI', marketCap: '4.2B' }
    ]
  };

  // Trading Sessions
  const sessions2026 = [
    { 
      name: 'Quantum Asian KZ', 
      active: false, 
      time: '6:30-9:30 AM IST', 
      priority: 4,
      aiOptimization: '85%',
      volatility: 'Medium',
      bestPairs: ['USD/JPY', 'AUD/USD', 'Nifty 50']
    },
    { 
      name: 'AI London KZ', 
      active: true, 
      time: '12:30-3:30 PM IST', 
      priority: 5,
      aiOptimization: '92%',
      volatility: 'High',
      bestPairs: ['EUR/USD', 'GBP/USD', 'FTSE 100']
    },
    { 
      name: 'Neural NY KZ', 
      active: true, 
      time: '5:30-8:30 PM IST', 
      priority: 5,
      aiOptimization: '95%',
      volatility: 'Very High',
      bestPairs: ['US30', 'SPX500', 'NASDAQ']
    },
    { 
      name: 'Crypto Silver Bullet', 
      active: false, 
      time: '8:30-9:30 PM IST', 
      priority: 4,
      aiOptimization: '88%',
      volatility: 'Extreme',
      bestPairs: ['BTC/USD', 'ETH/USD', 'AI Tokens']
    },
    {
      name: '24/7 AI Session',
      active: true,
      time: 'Always Active',
      priority: 3,
      aiOptimization: '78%',
      volatility: 'Variable',
      bestPairs: ['AI Stocks', 'Quantum Computing']
    }
  ];

  // AI Models
  const aiModels = {
    'Quantum Neural Network': { accuracy: '94.7%', latency: '12ms', training: '2025-Q4' },
    'Deep Reinforcement Learning': { accuracy: '92.3%', latency: '18ms', training: '2025-Q3' },
    'Transformer Time-Series': { accuracy: '91.8%', latency: '22ms', training: '2026-Q1' },
    'Generative Market Sim': { accuracy: '89.5%', latency: '35ms', training: '2026-Q1' }
  };

  // Generate Asset Data
  const generateQuantumData = (baseList) => {
    return baseList.map((asset, idx) => {
      const quantumScore = (95 - idx * 1.5 + Math.random() * 8).toFixed(1);
      const aiPrediction = (90 + Math.random() * 10).toFixed(1);
      const riskLevel = (2 + Math.random() * 5).toFixed(1);
      
      return {
        ...asset,
        rank: idx + 1,
        quantumScore: quantumScore,
        aiPrediction2026: aiPrediction,
        neuralScore: (85 + Math.random() * 15).toFixed(1),
        sentimentScore: (75 + Math.random() * 25).toFixed(1),
        volumeProfile: ['Quantum High', 'AI High', 'Neural Medium'][Math.floor(Math.random() * 3)],
        signal: idx < 5 ? '⚡ QUANTUM BUY' : idx < 10 ? '🧠 AI STRONG BUY' : idx < 15 ? '🟢 BUY' : '🟡 NEUTRAL',
        trend: Math.random() > 0.25 ? '🚀 SUPER BULL' : '🔻 CORRECTION',
        riskScore: riskLevel,
        nextOptimal: ['Neural KZ', 'AI Silver Bullet', 'Quantum Entry'][Math.floor(Math.random() * 3)],
        institutionalFlow: Math.random() > 0.4 ? 'Heavy Buying' : 'Light Selling',
        darkPoolActivity: (Math.random() * 250 + 50).toFixed(1) + 'M',
        shortInterest: (Math.random() * 12).toFixed(1) + '%',
        optionsFlow: Math.random() > 0.5 ? 'Extreme Bullish' : 'Moderate',
        earningsDate: new Date(Date.now() + Math.random() * 60 * 24 * 60 * 60 * 1000).toLocaleDateString(),
        whaleActivity: Math.random() > 0.6 ? 'Multiple Whales' : 'Normal',
        aiInsights: [
          'Quantum breakout detected',
          'AI accumulation phase',
          'Neural support holding',
          'Institutional FOMO building'
        ][Math.floor(Math.random() * 4)],
        priceTargets: {
          short: (Math.random() * 20 + 5).toFixed(1) + '%',
          medium: (Math.random() * 40 + 10).toFixed(1) + '%',
          long: (Math.random() * 100 + 20).toFixed(1) + '%'
        },
        volatility: (Math.random() * 30 + 10).toFixed(1) + '%',
        correlation: {
          nvda: (Math.random() * 0.4 + 0.5).toFixed(2),
          spy: (Math.random() * 0.3 + 0.3).toFixed(2)
        },
        lastUpdated: new Date().toLocaleTimeString()
      };
    });
  };

  const [assets, setAssets] = useState(() => 
    generateQuantumData(quantumMarkets2026[selectedMarket])
  );

  const [portfolio] = useState([
    { symbol: 'NVDA', quantity: 50, avgPrice: 650, currentPrice: 950 },
    { symbol: 'MSFT', quantity: 100, avgPrice: 380, currentPrice: 520 },
    { symbol: 'TAO', quantity: 500, avgPrice: 250, currentPrice: 360 },
    { symbol: 'IONQ', quantity: 1000, avgPrice: 12, currentPrice: 18 }
  ]);

  // Live Data Simulation
  useEffect(() => {
    const simulateLiveData = () => {
      setAssets(prev => prev.map(asset => ({
        ...asset,
        quantumScore: (parseFloat(asset.quantumScore) + (Math.random() - 0.5) * 0.2).toFixed(1),
        lastUpdated: new Date().toLocaleTimeString()
      })));
    };

    const interval = setInterval(simulateLiveData, 3000);
    return () => clearInterval(interval);
  }, []);

  // Time Updates
  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  // Market Stats
  const marketStats2026 = {
    totalAssets: assets.length,
    quantumSignals: assets.filter(a => a.signal.includes('QUANTUM')).length,
    aiSignals: assets.filter(a => a.signal.includes('AI')).length,
    averageAccuracy: '94.2%',
    activeSession: sessions2026.find(s => s.active)?.name || 'AI Session',
    marketRegime: 'QUANTUM BULL',
    totalVolume: '4.2T',
    fearGreedIndex: '78 (Extreme Greed)',
    putCallRatio: '0.72',
    vix: '14.2'
  };

  // Portfolio Stats
  const portfolioStats = portfolio.reduce((acc, holding) => {
    const currentValue = holding.quantity * holding.currentPrice;
    const invested = holding.quantity * holding.avgPrice;
    const pnl = currentValue - invested;
    const pnlPercent = (pnl / invested) * 100;
    
    acc.totalInvested += invested;
    acc.totalValue += currentValue;
    acc.totalPnl += pnl;
    acc.bestPerformer = Math.max(acc.bestPerformer, pnlPercent);
    return acc;
  }, { totalInvested: 0, totalValue: 0, totalPnl: 0, bestPerformer: 0 });

  portfolioStats.pnlPercent = ((portfolioStats.totalPnl / portfolioStats.totalInvested) * 100).toFixed(2);

  // Filtering & Sorting
  const filteredAssets = assets.filter(asset => {
    const matchesSearch = asset.symbol.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         asset.name.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesSector = selectedSectors.length === 0 || selectedSectors.includes(asset.sector);
    const matchesRisk = riskFilter === 'all' || 
                       (riskFilter === 'low' && parseFloat(asset.riskScore) < 4) ||
                       (riskFilter === 'medium' && parseFloat(asset.riskScore) >= 4 && parseFloat(asset.riskScore) <= 6) ||
                       (riskFilter === 'high' && parseFloat(asset.riskScore) > 6);
    
    return matchesSearch && matchesSector && matchesRisk;
  }).sort((a, b) => {
    switch(sortBy) {
      case 'Quantum Score': return parseFloat(b.quantumScore) - parseFloat(a.quantumScore);
      case 'Risk Score': return parseFloat(a.riskScore) - parseFloat(b.riskScore);
      case 'AI Prediction': return parseFloat(b.aiPrediction2026) - parseFloat(a.aiPrediction2026);
      case 'Market Cap': {
        const getCapValue = (cap) => {
          if (!cap) return 0;
          const num = parseFloat(cap.replace(/[^0-9.]/g, ''));
          if (cap.includes('T')) return num * 1000;
          if (cap.includes('B')) return num;
          return num / 1000;
        };
        return getCapValue(b.marketCap) - getCapValue(a.marketCap);
      }
      default: return a.rank - b.rank;
    }
  });

  // Theme styles
  const themeStyles = {
    dark: {
      bg: 'bg-black',
      card: 'bg-gray-900',
      text: 'text-white',
      border: 'border-gray-800',
      accent: 'from-blue-500 to-purple-600'
    },
    light: {
      bg: 'bg-gray-50',
      card: 'bg-white',
      text: 'text-gray-900',
      border: 'border-gray-200',
      accent: 'from-blue-600 to-indigo-700'
    },
    cyberpunk: {
      bg: 'bg-gray-950',
      card: 'bg-gray-900',
      text: 'text-cyan-100',
      border: 'border-purple-500',
      accent: 'from-pink-500 to-cyan-500'
    }
  }[theme];

  return (
    <div className={`min-h-screen ${themeStyles.bg} ${themeStyles.text} p-2 sm:p-4 md:p-6 font-sans`}>
      
      {/* Top Navigation */}
      <div className={`sticky top-0 z-50 ${themeStyles.card} border-b ${themeStyles.border} p-4 mb-6 backdrop-blur-lg bg-opacity-95`}>
        <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
          <div className="flex items-center gap-4">
            <div className="relative">
              <div className={`w-12 h-12 bg-gradient-to-r ${themeStyles.accent} rounded-lg flex items-center justify-center`}>
                <Brain className="w-8 h-8 text-white" />
              </div>
              <div className="absolute -top-1 -right-1 w-5 h-5 bg-green-500 rounded-full border-2 border-black animate-pulse"></div>
            </div>
            <div>
              <h1 className={`text-2xl md:text-3xl font-bold bg-gradient-to-r ${themeStyles.accent} bg-clip-text text-transparent`}>
                QUANTUM AI TRADER 2026
              </h1>
              <p className="text-sm text-gray-500">Neural Market Intelligence v4.2</p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="hidden md:flex items-center gap-2">
              <Bell className={`w-5 h-5 cursor-pointer hover:text-blue-400 transition-colors ${userPreferences.notifications ? 'text-yellow-400' : 'text-gray-500'}`} 
                    onClick={() => setUserPreferences(prev => ({...prev, notifications: !prev.notifications}))} />
              <Settings className="w-5 h-5 cursor-pointer hover:text-blue-400 transition-colors" />
            </div>
            
            <div className="flex items-center gap-2">
              <div className={`w-10 h-10 bg-gradient-to-r ${themeStyles.accent} rounded-full flex items-center justify-center font-bold text-white`}>
                AI
              </div>
              <div className="hidden sm:block">
                <div className="font-bold text-sm">Quantum Trader</div>
                <div className="text-xs text-gray-500">Tier: Neural Pro</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Dashboard Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 mb-6">
        
        {/* Left Panel */}
        <div className="lg:col-span-1 space-y-4">
          {/* Portfolio Card */}
          <div className={`${themeStyles.card} rounded-xl p-4 border ${themeStyles.border}`}>
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-bold text-lg flex items-center gap-2">
                <Wallet className="w-5 h-5" /> Portfolio
              </h3>
              <span className={`px-2 py-1 text-xs rounded-full ${portfolioStats.pnlPercent >= 0 ? 'bg-green-900 text-green-400' : 'bg-red-900 text-red-400'}`}>
                {portfolioStats.pnlPercent >= 0 ? '▲' : '▼'} {Math.abs(portfolioStats.pnlPercent)}%
              </span>
            </div>
            
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-500">Total Value:</span>
                <span className="font-bold text-xl">${(portfolioStats.totalValue / 1000).toFixed(1)}K</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Today's P&L:</span>
                <span className={`font-bold ${portfolioStats.totalPnl >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                  ${portfolioStats.totalPnl.toFixed(0)}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Best Performer:</span>
                <span className="text-green-400">{portfolioStats.bestPerformer.toFixed(1)}%</span>
              </div>
            </div>

            <div className="mt-4 pt-4 border-t border-gray-800">
              <h4 className="font-bold mb-2 text-sm">Quick Actions</h4>
              <div className="grid grid-cols-2 gap-2">
                <button className="p-2 bg-green-900 hover:bg-green-800 rounded text-xs transition-colors">AI Rebalance</button>
                <button className="p-2 bg-blue-900 hover:bg-blue-800 rounded text-xs transition-colors">Hedge Now</button>
                <button className="p-2 bg-purple-900 hover:bg-purple-800 rounded text-xs transition-colors">Copy Trade</button>
                <button className="p-2 bg-gray-800 hover:bg-gray-700 rounded text-xs transition-colors">Risk Check</button>
              </div>
            </div>
          </div>

          {/* AI Models Card */}
          <div className={`${themeStyles.card} rounded-xl p-4 border ${themeStyles.border}`}>
            <h3 className="font-bold text-lg mb-4 flex items-center gap-2">
              <Cpu className="w-5 h-5" /> AI Models Live
            </h3>
            <div className="space-y-3">
              {Object.entries(aiModels).map(([model, data]) => (
                <div key={model} className="flex items-center justify-between p-2 hover:bg-gray-800 rounded transition-colors cursor-pointer">
                  <div className="flex-1 min-w-0">
                    <div className="font-medium text-sm truncate">{model}</div>
                    <div className="text-xs text-gray-500">Latency: {data.latency}</div>
                  </div>
                  <div className="text-right ml-2">
                    <div className={`text-sm font-bold ${parseFloat(data.accuracy) > 92 ? 'text-green-400' : 'text-yellow-400'}`}>
                      {data.accuracy}
                    </div>
                    <div className="text-xs text-gray-500">{data.training}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Main Content Area */}
        <div className="lg:col-span-3">
          {/* Market Stats Bar */}
          <div className={`${themeStyles.card} rounded-xl p-4 mb-4 border ${themeStyles.border}`}>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {[
                { label: 'QUANTUM', value: marketStats2026.quantumSignals, icon: Sparkles, color: 'text-purple-400' },
                { label: 'AI SIGNALS', value: marketStats2026.aiSignals, icon: Robot, color: 'text-blue-400' },
                { label: 'REGIME', value: marketStats2026.marketRegime, icon: Activity, color: 'text-green-400' },
                { label: 'VOLUME', value: marketStats2026.totalVolume, icon: BarChart3, color: 'text-cyan-400' },
              ].map((stat, idx) => (
                <div key={idx} className="text-center">
                  <stat.icon className={`w-6 h-6 mx-auto mb-2 ${stat.color}`} />
                  <div className="text-xs text-gray-500">{stat.label}</div>
                  <div className={`text-lg font-bold ${stat.color}`}>{stat.value}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Control Bar */}
          <div className={`${themeStyles.card} rounded-xl p-4 mb-6 border ${themeStyles.border}`}>
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div className="flex flex-wrap items-center gap-3">
                <select
                  value={selectedMarket}
                  onChange={(e) => {
                    setSelectedMarket(e.target.value);
                    setAssets(generateQuantumData(quantumMarkets2026[e.target.value]));
                  }}
                  className={`bg-gray-800 border ${themeStyles.border} rounded-lg px-4 py-2 text-sm ${themeStyles.text} focus:outline-none focus:ring-2 focus:ring-blue-500`}
                >
                  {Object.keys(quantumMarkets2026).map(market => (
                    <option key={market} value={market}>{market}</option>
                  ))}
                </select>

                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className={`bg-gray-800 border ${themeStyles.border} rounded-lg px-4 py-2 text-sm ${themeStyles.text} focus:outline-none focus:ring-2 focus:ring-blue-500`}
                >
                  <option>Quantum Score</option>
                  <option>AI Prediction</option>
                  <option>Risk Score</option>
                  <option>Market Cap</option>
                </select>

                <div className="flex items-center gap-2">
                  <Search className="w-5 h-5 text-gray-500" />
                  <input
                    type="text"
                    placeholder="Search..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className={`bg-gray-800 border ${themeStyles.border} rounded-lg px-4 py-2 text-sm ${themeStyles.text} focus:outline-none focus:ring-2 focus:ring-blue-500 w-40`}
                  />
                </div>
              </div>

              <div className="flex items-center gap-2">
                <button 
                  onClick={() => setViewMode('grid')} 
                  className={`p-2 rounded transition-colors ${viewMode === 'grid' ? 'bg-blue-600' : 'bg-gray-800 hover:bg-gray-700'}`}
                >
                  <BarChart3 className="w-5 h-5" />
                </button>
                <button 
                  onClick={() => setViewMode('list')} 
                  className={`p-2 rounded transition-colors ${viewMode === 'list' ? 'bg-blue-600' : 'bg-gray-800 hover:bg-gray-700'}`}
                >
                  <PieChart className="w-5 h-5" />
                </button>
                <button 
                  onClick={() => setTheme(theme === 'dark' ? 'light' : theme === 'light' ? 'cyberpunk' : 'dark')} 
                  className="p-2 bg-gray-800 hover:bg-gray-700 rounded transition-colors"
                >
                  <Sparkles className="w-5 h-5" />
                </button>
              </div>
            </div>

            {/* Filter Chips */}
            <div className="flex flex-wrap gap-2 mt-4">
              {['low', 'medium', 'high'].map(risk => (
                <button
                  key={risk}
                  onClick={() => setRiskFilter(riskFilter === risk ? 'all' : risk)}
                  className={`px-3 py-1 text-xs rounded-full transition-colors ${riskFilter === risk ? 'bg-blue-600' : 'bg-gray-800 hover:bg-gray-700'}`}
                >
                  Risk: {risk.charAt(0).toUpperCase() + risk.slice(1)}
                </button>
              ))}
            </div>
          </div>

          {/* Sessions */}
          <div className={`${themeStyles.card} rounded-xl p-4 mb-6 border ${themeStyles.border}`}>
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
              <Satellite className="w-6 h-6" /> Trading Sessions 2026
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
              {sessions2026.map((session, idx) => (
                <div key={idx} className={`p-4 rounded-xl border-2 transition-all ${session.active ? 'border-green-500 bg-green-900 bg-opacity-20' : 'border-gray-700 bg-gray-800 bg-opacity-30'}`}>
                  <div className="flex items-center justify-between mb-3">
                    <span className="font-bold text-sm">{session.name}</span>
                    <span className={`px-2 py-1 rounded text-xs ${session.active ? 'bg-green-500' : 'bg-gray-700'}`}>
                      {session.active ? 'LIVE' : 'CLOSED'}
                    </span>
                  </div>
                  <div className="space-y-2">
                    <div className="text-xs text-gray-400">{session.time}</div>
                    <div className="flex justify-between text-xs">
                      <span className="text-gray-500">AI Opt:</span>
                      <span className="text-green-400 font-bold">{session.aiOptimization}</span>
                    </div>
                    <div className="flex justify-between text-xs">
                      <span className="text-gray-500">Vol:</span>
                      <span className="text-yellow-400 font-bold">{session.volatility}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Assets Display */}
          {viewMode === 'grid' ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {filteredAssets.slice(0, 12).map((asset, idx) => (
                <div key={idx} className={`${themeStyles.card} rounded-xl border ${themeStyles.border} p-4 hover:border-blue-500 transition-all cursor-pointer`}>
                  <div className="flex justify-between items-start mb-3">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <span className={`font-bold ${idx < 3 ? 'text-yellow-400' : idx < 8 ? 'text-green-400' : 'text-gray-400'}`}>
                          #{asset.rank}
                        </span>
                        <div className="font-bold text-xl text-blue-400 truncate">{asset.symbol}</div>
                      </div>
                      <div className="text-sm text-gray-400 truncate">{asset.name}</div>
                      <div className="text-xs text-gray-500 truncate">{asset.sector}</div>
                    </div>
                    <div className="text-right ml-2">
                      <div className="text-3xl font-bold text-green-400">{asset.quantumScore}</div>
                      <div className={`px-2 py-1 rounded text-xs font-semibold mt-1 whitespace-nowrap ${
                        asset.signal.includes('QUANTUM') ? 'bg-gradient-to-r from-purple-600 to-pink-600' :
                        asset.signal.includes('AI') ? 'bg-gradient-to-r from-blue-600 to-cyan-600' :
                        'bg-gradient-to-r from-green-600 to-emerald-600'
                      }`}>
                        {asset.signal.split(' ')[0]}
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-2 mb-3">
                    <div className="text-sm">
                      AI: <span className="font-bold text-purple-400">{asset.aiPrediction2026}</span>
                    </div>
                    <div className="text-sm text-right truncate">
                      {asset.trend}
                    </div>
                    <div className="text-sm">
                      Risk: <span className={`font-bold ${parseFloat(asset.riskScore) < 3 ? 'text-green-400' : parseFloat(asset.riskScore) < 5 ? 'text-yellow-400' : 'text-red-400'}`}>
                        {asset.riskScore}
                      </span>
                    </div>
                    <div className="text-sm text-right">
                      <span className={`px-2 py-1 rounded text-xs ${
                        asset.volumeProfile.includes('Quantum') ? 'bg-purple-900' :
                        asset.volumeProfile.includes('AI') ? 'bg-blue-900' : 'bg-gray-700'
                      }`}>
                        {asset.volumeProfile.split(' ')[0]}
                      </span>
                    </div>
                  </div>

                  <button
                    onClick={() => setExpandedAsset(expandedAsset === idx ? null : idx)}
                    className="w-full py-2 bg-gray-800 hover:bg-gray-700 rounded-lg flex items-center justify-center gap-2 transition-colors text-sm"
                  >
                    Details {expandedAsset === idx ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                  </button>

                  {expandedAsset === idx && (
                    <div className="mt-4 pt-4 border-t border-gray-800 space-y-3 text-sm">
                      <div>
                        <h4 className="font-bold mb-2 text-blue-400 text-xs">🎯 Targets</h4>
                        <div className="space-y-1 text-xs">
                          <div className="flex justify-between">
                            <span>1M:</span>
                            <span className="font-bold text-green-400">+{asset.priceTargets.short}</span>
                          </div>
                          <div className="flex justify-between">
                            <span>3M:</span>
                            <span className="font-bold text-yellow-400">+{asset.priceTargets.medium}</span>
                          </div>
                          <div className="flex justify-between">
                            <span>1Y:</span>
                            <span className="font-bold text-purple-400">+{asset.priceTargets.long}</span>
                          </div>
                        </div>
                      </div>
                      <div>
                        <h4 className="font-bold mb-2 text-purple-400 text-xs">🏦 Institutional</h4>
                        <div className="space-y-1 text-xs">
                          <div className="flex justify-between">
                            <span>Dark Pool:</span>
                            <span className="font-bold">{asset.darkPoolActivity}</span>
                          </div>
                          <div className="flex justify-between">
                            <span>Flow:</span>
                            <span className={`font-bold ${asset.institutionalFlow.includes('Buying') ? 'text-green-400' : 'text-red-400'}`}>
                              {asset.institutionalFlow}
                            </span>
                          </div>
                        </div>
                      </div>
                      <div>
                        <h4 className="font-bold mb-2 text-green-400 text-xs">🧠 AI Insight</h4>
                        <p className="text-xs text-gray-300">{asset.aiInsights}</p>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div className={`${themeStyles.card} rounded-xl border ${themeStyles.border} overflow-hidden`}>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-800">
                    <tr>
                      <th className="p-3 text-left text-sm">#</th>
                      <th className="p-3 text-left text-sm">Asset</th>
                      <th className="p-3 text-left text-sm">Score</th>
                      <th className="p-3 text-left text-sm">AI</th>
                      <th className="p-3 text-left text-sm">Signal</th>
                      <th className="p-3 text-left text-sm">Risk</th>
                      <th className="p-3 text-left text-sm">Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredAssets.map((asset, idx) => (
                      <tr key={idx} className={`border-b ${themeStyles.border} hover:bg-gray-800 transition-colors`}>
                        <td className="p-3">
                          <span className={`font-bold text-sm ${idx < 3 ? 'text-yellow-400' : idx < 8 ? 'text-green-400' : ''}`}>
                            #{asset.rank}
                          </span>
                        </td>
                        <td className="p-3">
                          <div className="font-bold text-blue-400">{asset.symbol}</div>
                          <div className="text-xs text-gray-400">{asset.name}</div>
                        </td>
                        <td className="p-3">
                          <span className="text-xl font-bold text-green-400">{asset.quantumScore}</span>
                        </td>
                        <td className="p-3">
                          <span className="font-bold text-purple-400">{asset.aiPrediction2026}</span>
                        </td>
                        <td className="p-3">
                          <span className={`px-2 py-1 rounded text-xs font-semibold ${
                            asset.signal.includes('QUANTUM') ? 'bg-purple-600' :
                            asset.signal.includes('AI') ? 'bg-blue-600' : 'bg-green-600'
                          }`}>
                            {asset.signal.split(' ')[1] || asset.signal}
                          </span>
                        </td>
                        <td className="p-3">
                          <span className={`font-bold ${parseFloat(asset.riskScore) < 3 ? 'text-green-400' : parseFloat(asset.riskScore) < 5 ? 'text-yellow-400' : 'text-red-400'}`}>
                            {asset.riskScore}
                          </span>
                        </td>
                        <td className="p-3">
                          <button className="px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded text-xs transition-colors">
                            Trade
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Bottom Info */}
          <div className={`${themeStyles.card} rounded-xl p-4 mt-6 border ${themeStyles.border}`}>
            <div className="flex flex-col md:flex-row justify-between items-center gap-4">
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                  <span className="text-sm">Live Streaming</span>
                </div>
                <div className="text-sm text-gray-500">
                  Updated: {currentTime.toLocaleTimeString()}
                </div>
              </div>
              <div className="flex items-center gap-4">
                <button className="px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg hover:opacity-90 transition-opacity text-sm">
                  <RefreshCw className="w-4 h-4 inline mr-2" />
                  Refresh
                </button>
                <button className="px-4 py-2 bg-gradient-to-r from-green-600 to-emerald-600 rounded-lg hover:opacity-90 transition-opacity text-sm">
                  <Download className="w-4 h-4 inline mr-2" />
                  Export
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className={`mt-8 text-center text-sm border-t ${themeStyles.border} pt-6`}>
        <div className="flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="text-gray-500">
            <p>⚡ QUANTUM AI TRADER 2026 | v4.2.1 | Neural Intelligence Active</p>
            <p className="mt-1 text-xs">🎯 Focus on Top Quantum Signals during AI Kill Zones</p>
          </div>
          <div className="flex flex-wrap items-center gap-2 justify-center">
            <span className="text-xs px-3 py-1 bg-gradient-to-r from-blue-900 to-purple-900 rounded-full">
              AI: 94.2%
            </span>
            <span className="text-xs px-3 py-1 bg-gradient-to-r from-green-900 to-emerald-900 rounded-full">
              Live
            </span>
            <span className="text-xs px-3 py-1 bg-gradient-to-r from-yellow-900 to-orange-900 rounded-full">
              Risk Managed
            </span>
          </div>
        </div>
        <div className="mt-4 text-xs text-gray-600">
          <p>⚠️ AI predictions are probabilistic. Trade responsibly. Past performance doesn't guarantee future results.</p>
        </div>
      </div>
    </div>
  );
};

export default ICTAdvancedAnalyzer2026;
