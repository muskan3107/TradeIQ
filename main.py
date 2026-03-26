"""
AlphaScout AI - Opportunity Radar Engine
FINAL PRODUCTION VERSION - Optimized for ET Hackathon Demo
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class OpportunityRadar:
    """Core engine for detecting high-confidence trading opportunities"""
    
    def __init__(self, ticker: str, lookback_days: int = 180):
        self.ticker = self._normalize_ticker(ticker)
        self.original_ticker = ticker.upper().strip()
        self.lookback_days = lookback_days
        self.data = None
        self.signals = {}
        self.confidence_score = 0
        self.backtest_results = {}
        
    def _normalize_ticker(self, ticker: str) -> str:
        """Smart ticker normalization for Indian and US markets"""
        ticker = ticker.upper().strip()
        
        # List of known US stock suffixes/patterns
        us_indicators = ['.', '^', '-']
        common_us_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX']
        
        # If already has suffix, return as-is
        if any(ind in ticker for ind in us_indicators):
            return ticker
            
        # If it's a known US stock, don't add .NS
        if ticker in common_us_stocks:
            return ticker
            
        # If ticker is 1-4 letters, likely US stock
        if len(ticker) <= 4 and ticker.isalpha():
            return ticker
            
        # Otherwise, assume Indian stock
        return f"{ticker}.NS"
    
    def fetch_data(self) -> bool:
        """Fetch historical price data with multiple fallback mechanisms"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=self.lookback_days + 60)
            
            # Try primary ticker first
            try:
                self.data = yf.download(
                    self.ticker,
                    start=start_date,
                    end=end_date,
                    progress=False,
                    auto_adjust=True
                )
            except:
                # If that fails and it tried .NS, try without
                if '.NS' in self.ticker:
                    base_ticker = self.ticker.replace('.NS', '')
                    print(f"   Retrying without .NS suffix...")
                    self.data = yf.download(
                        base_ticker,
                        start=start_date,
                        end=end_date,
                        progress=False,
                        auto_adjust=True
                    )
                    self.ticker = base_ticker
                else:
                    raise
            
            if self.data is None or self.data.empty:
                print(f"❌ Error: No data returned for {self.ticker}")
                return False
            
            self.data = self.data.dropna()
            
            if len(self.data) < 50:
                print(f"❌ Error: Insufficient data ({len(self.data)} days)")
                return False
            
            self._calculate_indicators()
            print(f"✅ Loaded {len(self.data)} days of data for {self.ticker}")
            return True
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def _calculate_indicators(self):
        """Calculate technical indicators - OPTIMIZED THRESHOLDS"""
        self.data['SMA_10'] = self.data['Close'].rolling(window=10, min_periods=10).mean()
        self.data['SMA_20'] = self.data['Close'].rolling(window=20, min_periods=20).mean()
        self.data['SMA_50'] = self.data['Close'].rolling(window=50, min_periods=50).mean()
        
        self.data['Avg_Volume'] = self.data['Volume'].rolling(window=20, min_periods=20).mean()
        self.data['High_20'] = self.data['High'].rolling(window=20, min_periods=20).max()
        self.data['Low_20'] = self.data['Low'].rolling(window=20, min_periods=20).min()
        
        self.data['Volume_Ratio'] = self.data['Volume'] / self.data['Avg_Volume']
        
        # Price change metrics
        self.data['Returns_5d'] = self.data['Close'].pct_change(5) * 100
        
        self.data = self.data.fillna(method='ffill').fillna(method='bfill')
    
    def detect_signals(self) -> Dict[str, bool]:
        """OPTIMIZED signal detection with realistic thresholds"""
        if self.data is None or len(self.data) < 2:
            return {}
        
        try:
            latest = self.data.iloc[-1]
            prev = self.data.iloc[-2]
            
            # SIGNAL 1: Breakout (RELAXED to 95% of 20-day high)
            breakout = (latest['Close'] >= latest['High_20'] * 0.95) and \
                       (not pd.isna(latest['High_20']))
            
            # SIGNAL 2: Volume Spike (RELAXED to 1.5x average)
            volume_spike = (latest['Volume_Ratio'] >= 1.5) and \
                          (not pd.isna(latest['Volume_Ratio']))
            
            # SIGNAL 3: Moving Average Bullish Trend
            ma_bullish = False
            if not pd.isna(latest['SMA_10']) and not pd.isna(latest['SMA_20']):
                # Bullish if: 10-day > 20-day AND trending up
                ma_bullish = (latest['SMA_10'] > latest['SMA_20']) and \
                            (latest['SMA_10'] > prev['SMA_10'])
            
            # BONUS SIGNAL 4: Strong Uptrend (price above 50-day MA)
            strong_trend = False
            if not pd.isna(latest['SMA_50']):
                strong_trend = latest['Close'] > latest['SMA_50'] * 1.02  # 2% above
            
            self.signals = {
                'breakout': bool(breakout),
                'volume_spike': bool(volume_spike),
                'ma_bullish': bool(ma_bullish),
                'strong_trend': bool(strong_trend)
            }
            
            return self.signals
            
        except Exception as e:
            print(f"⚠️ Signal detection error: {e}")
            return {}
    
    def calculate_confidence(self) -> float:
        """Enhanced confidence calculation"""
        if not self.signals:
            return 0.0
        
        # Updated scoring
        scores = {
            'breakout': 3.0,
            'volume_spike': 2.5,
            'ma_bullish': 2.5,
            'strong_trend': 2.0
        }
        
        base_score = sum(scores[sig] for sig, active in self.signals.items() if active)
        active_count = sum(self.signals.values())
        
        # Confluence bonus
        if active_count >= 3:
            confluence_bonus = 2.5
        elif active_count == 2:
            confluence_bonus = 1.5
        else:
            confluence_bonus = 0.0
        
        self.confidence_score = min(base_score + confluence_bonus, 10.0)
        return self.confidence_score
    
    def backtest_signals(self, forward_days: int = 10) -> Dict:
        """IMPROVED backtesting with 10-day forward returns"""
        if self.data is None or len(self.data) < 60:
            return {}
        
        try:
            occurrences = []
            
            for i in range(55, len(self.data) - forward_days):
                try:
                    # Historical indicators
                    close = self.data['Close'].iloc[i]
                    high_20 = self.data['High'].iloc[max(0, i-20):i].max()
                    avg_vol = self.data['Volume'].iloc[max(0, i-20):i].mean()
                    vol = self.data['Volume'].iloc[i]
                    sma_10 = self.data['Close'].iloc[max(0, i-10):i+1].mean()
                    sma_20 = self.data['Close'].iloc[max(0, i-20):i+1].mean()
                    sma_50 = self.data['Close'].iloc[max(0, i-50):i+1].mean()
                    
                    if pd.isna([high_20, avg_vol, sma_10, sma_20, sma_50]).any():
                        continue
                    
                    # Check signals (SAME relaxed thresholds)
                    vol_ratio = vol / avg_vol if avg_vol > 0 else 0
                    breakout_hist = close >= high_20 * 0.95
                    volume_spike_hist = vol_ratio >= 1.5
                    ma_bullish_hist = sma_10 > sma_20
                    strong_trend_hist = close > sma_50 * 1.02
                    
                    signals = [breakout_hist, volume_spike_hist, ma_bullish_hist, strong_trend_hist]
                    signal_count = sum(signals)
                    
                    # Require at least 2 signals
                    if signal_count >= 2:
                        entry = self.data['Close'].iloc[i]
                        exit_price = self.data['Close'].iloc[i + forward_days]
                        
                        if pd.isna([entry, exit_price]).any() or entry == 0:
                            continue
                        
                        pct_return = ((exit_price - entry) / entry) * 100
                        
                        occurrences.append({
                            'date': self.data.index[i],
                            'signals': signal_count,
                            'return': pct_return,
                            'win': pct_return > 0
                        })
                except:
                    continue
            
            if not occurrences:
                return {
                    'total_occurrences': 0,
                    'win_rate': 0.0,
                    'avg_return': 0.0,
                    'avg_win': 0.0,
                    'avg_loss': 0.0,
                    'best_return': 0.0,
                    'worst_return': 0.0
                }
            
            df = pd.DataFrame(occurrences)
            wins = df[df['win'] == True]
            losses = df[df['win'] == False]
            
            self.backtest_results = {
                'total_occurrences': len(df),
                'win_rate': (len(wins) / len(df)) * 100,
                'avg_return': df['return'].mean(),
                'avg_win': wins['return'].mean() if len(wins) > 0 else 0,
                'avg_loss': losses['return'].mean() if len(losses) > 0 else 0,
                'best_return': df['return'].max(),
                'worst_return': df['return'].min()
            }
            
            return self.backtest_results
            
        except Exception as e:
            print(f"⚠️ Backtest error: {e}")
            return {}
    
    def generate_recommendation(self) -> str:
        """Generate recommendation"""
        active_count = sum(self.signals.values())
        confidence = self.confidence_score
        
        if active_count >= 3 and confidence >= 7.0:
            return "🟢 BUY"
        elif active_count >= 2 and confidence >= 4.0:
            return "🟡 WATCH"
        else:
            return "🔴 AVOID"
    
    def generate_reasoning(self) -> str:
        """Generate AI reasoning"""
        active = [name for name, state in self.signals.items() if state]
        active_count = len(active)
        
        if active_count == 0:
            return "No significant signals detected. Market conditions do not favor entry."
        
        reasoning = []
        reasoning.append(f"✅ Detected {active_count}/4 signals:")
        
        if self.signals.get('breakout'):
            reasoning.append("   • BREAKOUT: Price near 20-day high resistance")
        if self.signals.get('volume_spike'):
            reasoning.append("   • VOLUME: 1.5x+ above average - strong interest")
        if self.signals.get('ma_bullish'):
            reasoning.append("   • TREND: Bullish MA crossover confirmed")
        if self.signals.get('strong_trend'):
            reasoning.append("   • MOMENTUM: Price above 50-day MA - strong uptrend")
        
        if active_count >= 2:
            reasoning.append(f"\n🎯 CONFLUENCE: {active_count} signals align - high probability setup")
        
        if self.backtest_results and self.backtest_results.get('total_occurrences', 0) > 0:
            bt = self.backtest_results
            reasoning.append(f"\n📊 HISTORICAL PERFORMANCE (10-day holding period):")
            reasoning.append(f"   • {bt['total_occurrences']} similar setups found")
            reasoning.append(f"   • Win Rate: {bt['win_rate']:.1f}%")
            reasoning.append(f"   • Avg Return: {bt['avg_return']:+.2f}%")
            
            if bt['win_rate'] >= 60:
                reasoning.append(f"   ✅ Strong historical performance")
            elif bt['win_rate'] >= 50:
                reasoning.append(f"   🟡 Moderate historical success")
        
        return "\n".join(reasoning)
    
    def run_full_analysis(self) -> Dict:
        """Execute full analysis"""
        if not self.fetch_data():
            return {'error': 'Failed to fetch data'}
        
        self.detect_signals()
        confidence = self.calculate_confidence()
        backtest = self.backtest_signals()
        recommendation = self.generate_recommendation()
        reasoning = self.generate_reasoning()
        
        return {
            'ticker': self.ticker,
            'signals': self.signals,
            'confidence_score': confidence,
            'backtest': backtest,
            'recommendation': recommendation,
            'reasoning': reasoning,
            'current_price': float(self.data['Close'].iloc[-1])
        }


def print_analysis_report(results: Dict):
    """Pretty print results"""
    if 'error' in results:
        print(f"\n❌ Analysis failed: {results['error']}")
        return
    
    print("\n" + "="*70)
    print(f"📈 ALPHASCOUT AI - OPPORTUNITY RADAR REPORT")
    print("="*70)
    
    print(f"\n🎯 STOCK: {results['ticker']}")
    print(f"💰 Current Price: ${results['current_price']:.2f}")
    
    print(f"\n🔍 SIGNAL DETECTION:")
    for signal, active in results['signals'].items():
        status = "✅ ACTIVE" if active else "❌ INACTIVE"
        print(f"   {signal.replace('_', ' ').title()}: {status}")
    
    print(f"\n⚡ CONFIDENCE SCORE: {results['confidence_score']:.1f}/10.0")
    
    if results['backtest'] and results['backtest'].get('total_occurrences', 0) > 0:
        bt = results['backtest']
        print(f"\n📊 BACKTEST RESULTS (10-day forward returns):")
        print(f"   Total Occurrences: {bt['total_occurrences']}")
        print(f"   Win Rate: {bt['win_rate']:.1f}%")
        print(f"   Avg Return: {bt['avg_return']:+.2f}%")
        print(f"   Best Return: {bt['best_return']:+.2f}%")
        print(f"   Worst Return: {bt['worst_return']:+.2f}%")
    
    print(f"\n🎯 RECOMMENDATION: {results['recommendation']}")
    print(f"\n💭 AI REASONING:")
    print(results['reasoning'])
    print("\n" + "="*70)


def main():
    """Main CLI"""
    print("\n" + "="*70)
    print("🚀 ALPHASCOUT AI - OPPORTUNITY RADAR ENGINE")
    print("   Multi-Signal Confluence Detection with Backtested Confidence")
    print("="*70)
    
    print("\n💡 EXAMPLE TICKERS:")
    print("   Indian: TCS, RELIANCE, INFY, HDFCBANK, WIPRO")
    print("   US: AAPL, MSFT, GOOGL, TSLA, NVDA")
    print("   (System auto-detects market)")
    
    ticker = input("\n📝 Enter stock ticker: ").strip()
    
    if not ticker:
        print("❌ Invalid ticker.")
        return
    
    print(f"\n🔄 Analyzing {ticker}...\n")
    
    radar = OpportunityRadar(ticker, lookback_days=180)
    results = radar.run_full_analysis()
    print_analysis_report(results)
    
    another = input("\n\nAnalyze another stock? (y/n): ").strip().lower()
    if another == 'y':
        main()
    else:
        print("\n✅ Thank you for using AlphaScout AI!\n")


if __name__ == "__main__":
    main()