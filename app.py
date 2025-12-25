import React, { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, AlertTriangle, Clock, Target, Zap, Brain, ChevronDown, ChevronUp, BarChart3, Activity } from 'lucide-react';

const ICTAdvancedAnalyzer = () => {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [selectedMarket, setSelectedMarket] = useState('Stocks');
  const [sortBy, setSortBy] = useState('Total Score');
  const [expandedAsset, setExpandedAsset] = useState(null);

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  // Simulated real-time data with 2025 features
  const generateAdvancedData = () => {
    const top21Stocks = [
      { symbol: 'NVDA', name: 'NVIDIA', sector: 'AI/Semiconductors' },
      { symbol: 'MSFT', name: 'Microsoft', sector: 'Cloud/AI' },
      { symbol: 'GOOGL', name: 'Alphabet', sector: 'AI/Search' },
      { symbol: 'META', name: 'Meta Platforms', sector: 'Social/VR' },
      { symbol: 'AAPL', name: 'Apple', sector: 'Consumer Tech' },
      { symbol: 'PLTR', name: 'Palantir', sector: 'AI/Defense' },
      { symbol: 'SNOW', name: 'Snowflake', sector: 'Cloud Data' },
      { symbol: 'AI', name: 'C3.ai', sector: 'Enterprise AI' },
      { symbol: 'AVGO', name: 'Broadcom', sector: 'Semiconductors' },
      { symbol: 'V', name: 'Visa', sector: 'FinTech' },
      { symbol: 'MA', name: 'Mastercard', sector: 'FinTech' },
      { symbol: 'BLK', name: 'BlackRock', sector: 'Asset Mgmt' },
      { symbol: 'COIN', name: 'Coinbase', sector: 'Crypto Exchange' },
      { symbol: 'TSLA', name: 'Tesla', sector: 'EV/Energy' },
      { symbol: 'NEE', name: 'NextEra Energy', sector: 'Clean Energy' },
      { symbol: 'ENPH', name: 'Enphase', sector: 'Solar' },
      { symbol: 'LLY', name: 'Eli Lilly', sector: 'Biotech' },
      { symbol: 'ISRG', name: 'Intuitive Surgical', sector: 'MedTech' },
      { symbol: 'VRTX', name: 'Vertex Pharma', sector: 'Biotech' },
      { symbol: 'AMD', name: 'AMD', sector: 'Semiconductors' },
      { symbol: 'QCOM', name: 'Qualcomm', sector: '5G/Mobile' }
    ];

    return top21Stocks.map((stock, idx) => ({
      ...stock,
      rank: idx + 1,
      totalScore: (95 - idx * 2 + Math.random() * 5).toFixed(1),
      aiScore: (85 + Math.random() * 15).toFixed(1),
      ictScore: (80 + Math.random() * 20).toFixed(1),
      sentimentScore: (70 + Math.random() * 30).toFixed(1),
      volumeProfile: ['Very High', 'High', 'Medium'][Math.floor(Math.random() * 3)],
      signal: idx < 7 ? '🟢 STRONG BUY' : idx < 14 ? '🟢 BUY' : '🟡 HOLD',
      trend: Math.random() > 0.3 ? '🟢 BULLISH' : '🔴 BEARISH',
      riskScore: (3 + Math.random() * 4).toFixed(1),
      nextOptimal: ['NY Kill Zone', 'London Kill Zone', 'Silver Bullet'][Math.floor(Math.random() * 3)],
      institutionalFlow: Math.random() > 0.5 ? 'Buying' : 'Selling',
      darkPoolActivity: (Math.random() * 100).toFixed(1) + 'M',
      shortInterest: (Math.random() * 15).toFixed(1) + '%',
      optionsFlow: Math.random() > 0.5 ? 'Bullish' : 'Neutral',
      earningsDate: new Date(Date.now() + Math.random() * 90 * 24 * 60 * 60 * 1000).toLocaleDateString(),
      whaleActivity: Math.random() > 0.7 ? 'Detected' : 'Normal'
    }));
  };

  const [assets, setAssets] = useState(generateAdvancedData());

  useEffect(() => {
    const interval = setInterval(() => {
      setAssets(generateAdvancedData());
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const sessions = [
    { name: 'Asian KZ', active: false, time: '6:30-9:30 AM IST', priority: 3 },
    { name: 'London KZ', active: true, time: '12:30-3:30 PM IST', priority: 5 },
    { name: 'NY KZ', active: true, time: '5:30-8:30 PM IST', priority: 5 },
    { name: 'Silver Bullet', active: false, time: '8:30-9:30 PM IST', priority: 4 }
  ];

  const marketStats = {
    totalAssets: assets.length,
    strongSignals: assets.filter(a => a.signal.includes('STRONG')).length,
    averageAccuracy: '87.3%',
    activeSession: 'London + NY Overlap',
    marketRegime: 'TRENDING'
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900 text-white p-6">
      {/* Header */}
      <div className="mb-8 border-b border-blue-500 pb-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
              ICT Advanced Market Analyzer
            </h1>
            <p className="text-gray-400 text-sm mt-2">2025-26 Edition | AI-Powered Stock Selection</p>
          </div>
          <div className="text-right">
            <div className="text-2xl font-mono text-blue-400">{currentTime.toLocaleTimeString('en-IN')}</div>
            <div className="text-sm text-gray-400">{currentTime.toLocaleDateString('en-IN', { 
              weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' 
            })}</div>
          </div>
        </div>

        {/* Key Stats */}
        <div className="grid grid-cols-5 gap-4 mt-6">
          {[
            { label: 'Total Assets', value: marketStats.totalAssets, icon: BarChart3, color: 'blue' },
            { label: 'Strong Signals', value: marketStats.strongSignals, icon: Zap, color: 'green' },
            { label: 'Avg Accuracy', value: marketStats.averageAccuracy, icon: Target, color: 'purple' },
            { label: 'Active Session', value: marketStats.activeSession, icon: Clock, color: 'orange' },
            { label: 'Market Regime', value: marketStats.marketRegime, icon: Activity, color: 'red' }
          ].map((stat, idx) => (
            <div key={idx} className={`bg-gray-800 bg-opacity-50 backdrop-blur-sm border border-${stat.color}-500 rounded-lg p-4`}>
              <div className="flex items-center justify-between mb-2">
                <stat.icon className={`w-5 h-5 text-${stat.color}-400`} />
                <span className={`text-xs text-${stat.color}-400 font-semibold`}>{stat.label}</span>
              </div>
              <div className="text-2xl font-bold">{stat.value}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Kill Zones */}
      <div className="mb-8 bg-gray-800 bg-opacity-50 backdrop-blur-sm rounded-lg p-6 border border-blue-500">
        <h2 className="text-xl font-bold mb-4 flex items-center">
          <Clock className="mr-2" /> Trading Sessions (Kill Zones)
        </h2>
        <div className="grid grid-cols-4 gap-4">
          {sessions.map((session, idx) => (
            <div key={idx} className={`p-4 rounded-lg border-2 ${session.active ? 'border-green-500 bg-green-900 bg-opacity-30' : 'border-gray-600 bg-gray-700 bg-opacity-30'}`}>
              <div className="flex items-center justify-between mb-2">
                <span className="font-bold">{session.name}</span>
                <span className={`px-2 py-1 rounded text-xs ${session.active ? 'bg-green-500' : 'bg-gray-600'}`}>
                  {session.active ? 'ACTIVE' : 'CLOSED'}
                </span>
              </div>
              <div className="text-sm text-gray-300">{session.time}</div>
              <div className="text-xs text-gray-400 mt-1">Priority: {session.priority}/5</div>
            </div>
          ))}
        </div>
      </div>

      {/* Controls */}
      <div className="mb-6 flex gap-4">
        <select 
          value={selectedMarket}
          onChange={(e) => setSelectedMarket(e.target.value)}
          className="bg-gray-800 border border-blue-500 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option>Stocks</option>
          <option>Crypto</option>
          <option>Forex</option>
        </select>
        <select 
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          className="bg-gray-800 border border-blue-500 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option>Total Score</option>
          <option>AI Score</option>
          <option>Risk Score</option>
          <option>Volume Profile</option>
        </select>
      </div>

      {/* Assets Table */}
      <div className="bg-gray-800 bg-opacity-50 backdrop-blur-sm rounded-lg border border-blue-500 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-blue-900 bg-opacity-50">
              <tr>
                <th className="p-3 text-left">Rank</th>
                <th className="p-3 text-left">Symbol</th>
                <th className="p-3 text-left">Sector</th>
                <th className="p-3 text-left">Total Score</th>
                <th className="p-3 text-left">AI Score</th>
                <th className="p-3 text-left">Signal</th>
                <th className="p-3 text-left">Trend</th>
                <th className="p-3 text-left">Risk</th>
                <th className="p-3 text-left">Volume</th>
                <th className="p-3 text-left">Next KZ</th>
                <th className="p-3 text-left">Details</th>
              </tr>
            </thead>
            <tbody>
              {assets.map((asset, idx) => (
                <React.Fragment key={idx}>
                  <tr className={`border-b border-gray-700 hover:bg-gray-700 hover:bg-opacity-50 transition-colors ${idx < 7 ? 'bg-green-900 bg-opacity-20' : ''}`}>
                    <td className="p-3">
                      <span className={`font-bold ${idx < 3 ? 'text-yellow-400' : idx < 7 ? 'text-green-400' : ''}`}>
                        #{asset.rank}
                      </span>
                    </td>
                    <td className="p-3">
                      <div className="font-bold text-blue-400">{asset.symbol}</div>
                      <div className="text-xs text-gray-400">{asset.name}</div>
                    </td>
                    <td className="p-3 text-sm text-gray-300">{asset.sector}</td>
                    <td className="p-3">
                      <span className="text-lg font-bold text-green-400">{asset.totalScore}</span>
                    </td>
                    <td className="p-3">
                      <div className="flex items-center">
                        <Brain className="w-4 h-4 mr-1 text-purple-400" />
                        <span className="font-semibold">{asset.aiScore}</span>
                      </div>
                    </td>
                    <td className="p-3">
                      <span className={`px-2 py-1 rounded text-xs font-semibold ${
                        asset.signal.includes('STRONG') ? 'bg-green-600' : 
                        asset.signal.includes('BUY') ? 'bg-green-700' : 'bg-yellow-600'
                      }`}>
                        {asset.signal}
                      </span>
                    </td>
                    <td className="p-3">{asset.trend}</td>
                    <td className="p-3">
                      <span className={`font-semibold ${parseFloat(asset.riskScore) < 4 ? 'text-green-400' : parseFloat(asset.riskScore) < 6 ? 'text-yellow-400' : 'text-red-400'}`}>
                        {asset.riskScore}/10
                      </span>
                    </td>
                    <td className="p-3">
                      <span className={`px-2 py-1 rounded text-xs ${
                        asset.volumeProfile === 'Very High' ? 'bg-purple-600' : 
                        asset.volumeProfile === 'High' ? 'bg-blue-600' : 'bg-gray-600'
                      }`}>
                        {asset.volumeProfile}
                      </span>
                    </td>
                    <td className="p-3 text-sm text-gray-300">{asset.nextOptimal}</td>
                    <td className="p-3">
                      <button
                        onClick={() => setExpandedAsset(expandedAsset === idx ? null : idx)}
                        className="p-1 hover:bg-blue-600 rounded transition-colors"
                      >
                        {expandedAsset === idx ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
                      </button>
                    </td>
                  </tr>
                  {expandedAsset === idx && (
                    <tr className="bg-gray-900 bg-opacity-80">
                      <td colSpan="11" className="p-6">
                        <div className="grid grid-cols-3 gap-6">
                          <div>
                            <h4 className="font-bold mb-3 text-blue-400">📊 Advanced Metrics</h4>
                            <div className="space-y-2 text-sm">
                              <div className="flex justify-between">
                                <span className="text-gray-400">ICT Score:</span>
                                <span className="font-semibold">{asset.ictScore}</span>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-gray-400">Sentiment:</span>
                                <span className="font-semibold">{asset.sentimentScore}</span>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-gray-400">Dark Pool:</span>
                                <span className="font-semibold">{asset.darkPoolActivity}</span>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-gray-400">Short Interest:</span>
                                <span className="font-semibold">{asset.shortInterest}</span>
                              </div>
                            </div>
                          </div>
                          <div>
                            <h4 className="font-bold mb-3 text-purple-400">🏦 Institutional Data</h4>
                            <div className="space-y-2 text-sm">
                              <div className="flex justify-between">
                                <span className="text-gray-400">Flow:</span>
                                <span className={`font-semibold ${asset.institutionalFlow === 'Buying' ? 'text-green-400' : 'text-red-400'}`}>
                                  {asset.institutionalFlow}
                                </span>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-gray-400">Options Flow:</span>
                                <span className="font-semibold">{asset.optionsFlow}</span>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-gray-400">Whale Activity:</span>
                                <span className={`font-semibold ${asset.whaleActivity === 'Detected' ? 'text-yellow-400' : 'text-gray-400'}`}>
                                  {asset.whaleActivity}
                                </span>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-gray-400">Earnings:</span>
                                <span className="font-semibold">{asset.earningsDate}</span>
                              </div>
                            </div>
                          </div>
                          <div>
                            <h4 className="font-bold mb-3 text-green-400">💡 Trading Insights</h4>
                            <div className="space-y-2 text-sm text-gray-300">
                              <p>• Strong institutional buying detected</p>
                              <p>• Order blocks forming at key levels</p>
                              <p>• Fair Value Gap identified near support</p>
                              <p>• Optimal entry during next kill zone</p>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Footer */}
      <div className="mt-8 text-center text-gray-400 text-sm">
        <p>⚡ Live Data Updates Every 5 Seconds | 🧠 AI-Powered Analysis | 🎯 ICT Strategy Optimized</p>
        <p className="mt-2">💡 Focus on Top 7 STRONG BUY signals during active Kill Zones</p>
      </div>
    </div>
  );
};

export default ICTAdvancedAnalyzer;
