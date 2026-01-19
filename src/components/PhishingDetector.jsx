import React, { useState } from 'react';
import { Shield, AlertTriangle, CheckCircle, Search, X, Info, Link2 } from 'lucide-react';

const PhishingDetector = () => {
    const [url, setUrl] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const analyzeURL = async (inputUrl) => {
        if (!inputUrl || !inputUrl.trim()) return;

        setLoading(true);
        setResult(null);

        try {
            // Call your Python XGBoost Backend
            const response = await fetch('http://localhost:8000/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: inputUrl.trim() }),
            });

            if (!response.ok) {
                throw new Error('Backend server error');
            }

            const data = await response.json();

            setResult({
                url: inputUrl,
                isSafe: data.isSafe,
                riskScore: data.riskScore,
                checks: [
                    {
                        name: 'XGBoost Analysis',
                        status: data.isSafe ? 'safe' : 'danger',
                        message: data.message || (data.isSafe ? 'Model classified this URL as safe.' : 'Model detected phishing patterns.'),
                        risk: data.riskScore
                    }
                ]
            });
        } catch (error) {
            console.error("Backend error:", error);
            alert("Please start your Python backend (uvicorn app:app)!");
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = () => {
        if (url.trim()) {
            analyzeURL(url.trim());
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            handleSubmit();
        }
    };

    const handleClear = () => {
        setUrl('');
        setResult(null);
    };

    const getRiskLevel = (score) => {
        if (score < 20) return { level: 'Low', color: 'text-green-400', bgColor: 'bg-green-500' };
        if (score < 40) return { level: 'Medium', color: 'text-yellow-400', bgColor: 'bg-yellow-500' };
        if (score < 70) return { level: 'High', color: 'text-orange-400', bgColor: 'bg-orange-500' };
        return { level: 'Critical', color: 'text-red-400', bgColor: 'bg-red-500' };
    };

    const getStatusIcon = (status) => {
        if (status === 'safe') {
            return <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />;
        } else if (status === 'warning') {
            return <AlertTriangle className="w-5 h-5 text-yellow-400 flex-shrink-0 mt-0.5" />;
        } else {
            return <AlertTriangle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />;
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-4 sm:p-6">
            <div className="max-w-4xl mx-auto">
                <div className="text-center mb-8 sm:mb-12 pt-4 sm:pt-8">
                    <div className="inline-flex items-center justify-center w-16 h-16 sm:w-20 sm:h-20 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl mb-4 shadow-lg shadow-purple-500/50">
                        <Shield className="w-8 h-8 sm:w-10 sm:h-10 text-white" />
                    </div>
                    <h1 className="text-4xl sm:text-5xl font-bold text-white mb-3">PhishGuard</h1>
                    <p className="text-gray-300 text-base sm:text-lg">Advanced URL Security Scanner</p>
                </div>

                <div className="mb-8">
                    <div className="relative">
                        <div className="absolute inset-y-0 left-0 pl-4 sm:pl-6 flex items-center pointer-events-none">
                            <Link2 className="h-5 w-5 text-gray-400" />
                        </div>
                        <input
                            type="text"
                            value={url}
                            onChange={(e) => setUrl(e.target.value)}
                            onKeyDown={handleKeyDown}
                            placeholder="Enter URL to analyze (e.g., https://example.com)"
                            className="w-full pl-12 sm:pl-14 pr-24 sm:pr-32 py-4 sm:py-5 bg-white/10 backdrop-blur-lg border border-white/20 rounded-2xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all text-base sm:text-lg"
                        />
                        {url && (
                            <button
                                type="button"
                                onClick={handleClear}
                                className="absolute right-20 sm:right-28 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white transition-colors p-2"
                            >
                                <X className="w-5 h-5" />
                            </button>
                        )}
                        <button
                            type="button"
                            onClick={handleSubmit}
                            disabled={!url.trim() || loading}
                            className="absolute right-2 top-1/2 -translate-y-1/2 px-4 sm:px-6 py-2 sm:py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl font-semibold hover:shadow-lg hover:shadow-purple-500/50 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center gap-2"
                        >
                            {loading ? (
                                <>
                                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                                    <span className="hidden sm:inline">Scanning</span>
                                </>
                            ) : (
                                <>
                                    <Search className="w-4 h-4" />
                                    <span className="hidden sm:inline">Scan</span>
                                </>
                            )}
                        </button>
                    </div>
                </div>

                {result && (
                    <div className="space-y-6">
                        <div className={`p-6 sm:p-8 rounded-2xl backdrop-blur-lg border-2 ${result.isSafe ? 'bg-green-500/10 border-green-500/30' : 'bg-red-500/10 border-red-500/30'
                            }`}>
                            <div className="flex items-start gap-4">
                                {result.isSafe ? (
                                    <CheckCircle className="w-10 h-10 sm:w-12 sm:h-12 text-green-400 flex-shrink-0" />
                                ) : (
                                    <AlertTriangle className="w-10 h-10 sm:w-12 sm:h-12 text-red-400 flex-shrink-0" />
                                )}
                                <div className="flex-1 min-w-0">
                                    <h2 className="text-xl sm:text-2xl font-bold text-white mb-2">
                                        {result.isSafe ? 'URL Appears Safe' : 'Potential Threat Detected'}
                                    </h2>
                                    <p className="text-gray-300 mb-3 break-all text-sm sm:text-base">{result.url}</p>
                                    <div className="flex flex-col sm:flex-row sm:items-center gap-3 sm:gap-4">
                                        <div>
                                            <span className="text-gray-400 text-sm">Risk Score: </span>
                                            <span className={`text-xl sm:text-2xl font-bold ${getRiskLevel(result.riskScore).color}`}>
                                                {result.riskScore}
                                            </span>
                                            <span className="text-gray-400 text-sm">/100</span>
                                        </div>
                                        <div className="hidden sm:block h-8 w-px bg-white/20" />
                                        <div>
                                            <span className="text-gray-400 text-sm">Risk Level: </span>
                                            <span className={`font-bold ${getRiskLevel(result.riskScore).color}`}>
                                                {getRiskLevel(result.riskScore).level}
                                            </span>
                                        </div>
                                    </div>
                                    <div className="mt-4">
                                        <div className="w-full bg-white/10 rounded-full h-2">
                                            <div
                                                className={`h-2 rounded-full transition-all duration-1000 ${getRiskLevel(result.riskScore).bgColor}`}
                                                style={{ width: `${Math.min(result.riskScore, 100)}%` }}
                                            />
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl p-4 sm:p-6">
                            <h3 className="text-lg sm:text-xl font-bold text-white mb-4 flex items-center gap-2">
                                <Info className="w-5 h-5 text-purple-400" />
                                Security Analysis Details
                            </h3>
                            <div className="space-y-3">
                                {result.checks.map((check, index) => (
                                    <div
                                        key={index}
                                        className={`p-3 sm:p-4 rounded-xl border ${check.status === 'safe' ? 'bg-green-500/5 border-green-500/20' :
                                            check.status === 'warning' ? 'bg-yellow-500/5 border-yellow-500/20' :
                                                'bg-red-500/5 border-red-500/20'
                                            }`}
                                    >
                                        <div className="flex items-start justify-between gap-4">
                                            <div className="flex items-start gap-3 flex-1">
                                                {getStatusIcon(check.status)}
                                                <div className="flex-1">
                                                    <h4 className="font-semibold text-white mb-1">{check.name}</h4>
                                                    <p className="text-sm text-gray-300">{check.message}</p>
                                                </div>
                                            </div>
                                            {check.risk > 0 && (
                                                <div className="text-right">
                                                    <div className={`text-sm font-semibold ${check.status === 'warning' ? 'text-yellow-400' : 'text-red-400'
                                                        }`}>
                                                        +{check.risk}
                                                    </div>
                                                    <div className="text-xs text-gray-400">risk</div>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="bg-purple-500/10 backdrop-blur-lg border border-purple-500/20 rounded-2xl p-4 sm:p-6">
                            <h3 className="text-base sm:text-lg font-bold text-white mb-3">Recommendation</h3>
                            <p className="text-sm sm:text-base text-gray-300">
                                {result.isSafe ? (
                                    "This URL appears to be safe based on our analysis. However, always exercise caution when entering sensitive information online."
                                ) : (
                                    "⚠️ We strongly recommend avoiding this URL. The detected risk factors suggest it may be malicious or unsafe."
                                )}
                            </p>
                        </div>

                        <button
                            onClick={handleClear}
                            className="w-full px-6 py-3 bg-white/10 hover:bg-white/20 border border-white/20 text-white rounded-xl font-semibold transition-all"
                        >
                            Analyze Another URL
                        </button>
                    </div>
                )}

                {!result && (
                    <div className="mt-12 grid sm:grid-cols-3 gap-4">
                        <div className="bg-white/5 backdrop-blur-lg border border-white/10 rounded-xl p-6">
                            <div className="w-12 h-12 bg-purple-500/20 rounded-lg flex items-center justify-center mb-4">
                                <Shield className="w-6 h-6 text-purple-400" />
                            </div>
                            <h3 className="text-white font-semibold mb-2">Real-time Analysis</h3>
                            <p className="text-gray-400 text-sm">Instant security checks</p>
                        </div>
                        <div className="bg-white/5 backdrop-blur-lg border border-white/10 rounded-xl p-6">
                            <div className="w-12 h-12 bg-pink-500/20 rounded-lg flex items-center justify-center mb-4">
                                <CheckCircle className="w-6 h-6 text-pink-400" />
                            </div>
                            <h3 className="text-white font-semibold mb-2">Multiple Checks</h3>
                            <p className="text-gray-400 text-sm">8 validation rules</p>
                        </div>
                        <div className="bg-white/5 backdrop-blur-lg border border-white/10 rounded-xl p-6">
                            <div className="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center mb-4">
                                <Info className="w-6 h-6 text-blue-400" />
                            </div>
                            <h3 className="text-white font-semibold mb-2">Detailed Reports</h3>
                            <p className="text-gray-400 text-sm">Clear risk breakdown</p>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default PhishingDetector;