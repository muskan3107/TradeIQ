"""
AlphaScout AI - System Validator
FINAL OPTIMIZED VERSION
"""

from main import OpportunityRadar
import pandas as pd
import time


class SystemValidator:
    
    def __init__(self, test_stocks):
        self.test_stocks = test_stocks
        self.results = []
        
    def run_validation(self):
        print("\n" + "="*70)
        print("🧪 ALPHASCOUT AI - SYSTEM VALIDATION")
        print("="*70)
        print(f"\n📋 Testing {len(self.test_stocks)} stocks...\n")
        
        for idx, ticker in enumerate(self.test_stocks, 1):
            print(f"[{idx}/{len(self.test_stocks)}] {ticker}...", end=" ")
            
            try:
                radar = OpportunityRadar(ticker, lookback_days=180)
                result = radar.run_full_analysis()
                
                if 'error' not in result:
                    self.results.append(result)
                    conf = result['confidence_score']
                    signals = sum(result['signals'].values())
                    print(f"✅ {signals} signals | {conf:.1f}/10 confidence")
                else:
                    print(f"❌ Failed")
                    
            except Exception as e:
                print(f"❌ Error")
        
        return self.results
    
    def generate_performance_report(self):
        if not self.results:
            print("\n❌ No results")
            return
        
        print("\n" + "="*70)
        print("📊 PERFORMANCE REPORT")
        print("="*70)
        
        # Per-stock analysis
        print("\n🎯 PER-STOCK ANALYSIS:")
        print("-"*70)
        
        for r in self.results:
            bt = r.get('backtest', {})
            active = sum(r['signals'].values())
            
            print(f"\n📈 {r['ticker']}")
            print(f"   Signals: {active}/4")
            print(f"   Confidence: {r['confidence_score']:.1f}/10")
            print(f"   Recommendation: {r['recommendation']}")
            
            if bt.get('total_occurrences', 0) > 0:
                print(f"   Backtest: {bt['total_occurrences']} trades | {bt['win_rate']:.1f}% WR | {bt['avg_return']:+.2f}% avg")
        
        # Aggregate stats
        stocks_with_bt = [r for r in self.results if r.get('backtest', {}).get('total_occurrences', 0) > 0]
        
        if not stocks_with_bt:
            print("\n⚠️ No backtest data")
            return
        
        print("\n" + "="*70)
        print("🧮 AGGREGATE STATISTICS")
        print("="*70)
        
        avg_wr = sum(r['backtest']['win_rate'] for r in stocks_with_bt) / len(stocks_with_bt)
        avg_ret = sum(r['backtest']['avg_return'] for r in stocks_with_bt) / len(stocks_with_bt)
        total_occ = sum(r['backtest']['total_occurrences'] for r in stocks_with_bt)
        
        print(f"\n📊 Overall Performance:")
        print(f"   Stocks Analyzed: {len(self.results)}")
        print(f"   Average Win Rate: {avg_wr:.1f}%")
        print(f"   Average Return: {avg_ret:+.2f}%")
        print(f"   Total Opportunities: {total_occ}")
        
        # Best/worst
        best = max(stocks_with_bt, key=lambda x: x['backtest']['avg_return'])
        worst = min(stocks_with_bt, key=lambda x: x['backtest']['avg_return'])
        
        print(f"\n🏆 Best: {best['ticker']} ({best['backtest']['avg_return']:+.2f}%)")
        print(f"⚠️ Worst: {worst['ticker']} ({worst['backtest']['avg_return']:+.2f}%)")
        
        # Final verdict
        print("\n" + "="*70)
        print("🏁 VERDICT")
        print("="*70)
        
        if avg_wr >= 55 and avg_ret >= 1.0:
            verdict = "✅ SYSTEM VALIDATED - Good signal quality"
        elif avg_wr >= 50:
            verdict = "🟡 SYSTEM SHOWS PROMISE - Acceptable performance"
        else:
            verdict = "⚠️ NEEDS TUNING - Recalibrate thresholds"
        
        print(f"\n{verdict}")
        print(f"Win Rate: {avg_wr:.1f}% | Avg Return: {avg_ret:+.2f}%")
        print("\n" + "="*70 + "\n")


def main():
    # OPTIMIZED test set
    test_stocks = [
        'RELIANCE',  # Will auto-add .NS
        'TCS',
        'INFY',
        'HDFCBANK',
        'AAPL',      # Won't add .NS
        'MSFT',
        'NVDA'
    ]
    
    print("\n🚀 AlphaScout AI - System Validation")
    print(f"📅 {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
    
    start = time.time()
    
    validator = SystemValidator(test_stocks)
    validator.run_validation()
    validator.generate_performance_report()
    
    print(f"⏱️ Completed in {time.time() - start:.1f}s")


if __name__ == "__main__":
    main()