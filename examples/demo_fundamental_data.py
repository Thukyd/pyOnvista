"""
PyOnvista v2.0 - Fundamental Data Extraction Demo

This demo showcases the enhanced PyOnvista v2.0 capabilities for extracting
comprehensive fundamental data from OnVista snapshot responses.

Features demonstrated:
- Financial ratios (P/E, P/B, EPS, dividend yield, etc.)
- Performance metrics (returns, volatility, beta)
- Technical indicators (moving averages, RSI)
- Company information (sector, employees, headquarters)
- Sustainability/ESG data

Original PyOnvista by cloasdata
Enhanced v2.0 by Thukyd
"""

import asyncio
import aiohttp
import logging
import sys
import os

# Add parent directory to path to import pyonvista
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.pyonvista.api import PyOnVista

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def demo_fundamental_data():
    """Demonstrate fundamental data extraction from OnVista snapshots."""
    
    # Test ISINs for different types of instruments
    test_isins = {
        "SAP SE (German Stock)": "DE0007164600",
        "Apple Inc. (US Stock)": "US0378331005", 
        "Siemens AG (German Stock)": "DE0007236101"
    }
    
    async with aiohttp.ClientSession() as session:
        api = PyOnVista()
        await api.install_client(session)
        
        print("=" * 80)
        print("PyOnvista v2.0 - Fundamental Data Extraction Demo")
        print("=" * 80)
        print()
        
        for company_name, isin in test_isins.items():
            print(f"Analyzing: {company_name} (ISIN: {isin})")
            print("-" * 60)
            
            try:
                # Request instrument with full snapshot data
                instrument = await api.request_instrument(isin=isin)
                
                print(f"Basic Info: {instrument.name} ({instrument.symbol})")
                print(f"Type: {instrument.type}")
                print(f"Current Price: €{instrument.quote.close:.2f}" if instrument.quote else "Price: N/A")
                print()
                
                # Extract financial ratios
                ratios = instrument.get_financial_ratios()
                print("Financial Ratios:")
                if ratios.pe_ratio:
                    print(f"  P/E Ratio: {ratios.pe_ratio:.2f}")
                if ratios.pb_ratio:
                    print(f"  P/B Ratio: {ratios.pb_ratio:.2f}")
                if ratios.eps:
                    print(f"  EPS: €{ratios.eps:.2f}")
                if ratios.dividend_yield:
                    print(f"  Dividend Yield: {ratios.dividend_yield:.2f}%")
                if ratios.market_cap:
                    print(f"  Market Cap: €{ratios.market_cap:,.0f}")
                if not any([ratios.pe_ratio, ratios.pb_ratio, ratios.eps, ratios.dividend_yield, ratios.market_cap]):
                    print("  No financial ratio data available in snapshot")
                print()
                
                # Extract performance metrics
                performance = instrument.get_performance_metrics()
                print("Performance Metrics:")
                if performance.performance_1d:
                    print(f"  1 Day: {performance.performance_1d:+.2f}%")
                if performance.performance_1w:
                    print(f"  1 Week: {performance.performance_1w:+.2f}%")
                if performance.performance_1m:
                    print(f"  1 Month: {performance.performance_1m:+.2f}%")
                if performance.performance_1y:
                    print(f"  1 Year: {performance.performance_1y:+.2f}%")
                if performance.volatility_30d:
                    print(f"  30D Volatility: {performance.volatility_30d:.2f}%")
                if performance.beta:
                    print(f"  Beta: {performance.beta:.2f}")
                if not any([performance.performance_1d, performance.performance_1w, performance.performance_1m, 
                           performance.performance_1y, performance.volatility_30d, performance.beta]):
                    print("  No performance data available in snapshot")
                print()
                
                # Extract technical indicators
                technical = instrument.get_technical_indicators()
                print("Technical Indicators:")
                if technical.moving_avg_20d:
                    print(f"  20-Day MA: €{technical.moving_avg_20d:.2f}")
                if technical.moving_avg_200d:
                    print(f"  200-Day MA: €{technical.moving_avg_200d:.2f}")
                if technical.rsi_14d:
                    print(f"  RSI (14): {technical.rsi_14d:.1f}")
                if technical.bollinger_upper and technical.bollinger_lower:
                    print(f"  Bollinger Bands: €{technical.bollinger_lower:.2f} - €{technical.bollinger_upper:.2f}")
                if not any([technical.moving_avg_20d, technical.moving_avg_200d, technical.rsi_14d]):
                    print("  No technical indicator data available in snapshot")
                print()
                
                # Extract company information
                company = instrument.get_company_info()
                print("Company Information:")
                if company.sector:
                    print(f"  Sector: {company.sector}")
                if company.industry:
                    print(f"  Industry: {company.industry}")
                if company.country:
                    print(f"  Country: {company.country}")
                if company.employees:
                    print(f"  Employees: {company.employees:,}")
                if company.headquarters:
                    print(f"  Headquarters: {company.headquarters}")
                if company.founded:
                    print(f"  Founded: {company.founded}")
                if not any([company.sector, company.industry, company.country, company.employees]):
                    print("  No company data available in snapshot")
                print()
                
                # Extract sustainability data
                sustainability = instrument.get_sustainability_data()
                print("Sustainability/ESG Data:")
                if sustainability.esg_score:
                    print(f"  ESG Score: {sustainability.esg_score:.1f}")
                if sustainability.environmental_score:
                    print(f"  Environmental: {sustainability.environmental_score:.1f}")
                if sustainability.social_score:
                    print(f"  Social: {sustainability.social_score:.1f}")
                if sustainability.governance_score:
                    print(f"  Governance: {sustainability.governance_score:.1f}")
                if sustainability.sustainability_rating:
                    print(f"  Rating: {sustainability.sustainability_rating}")
                if not any([sustainability.esg_score, sustainability.environmental_score, 
                           sustainability.social_score, sustainability.governance_score]):
                    print("  No sustainability data available in snapshot")
                print()
                
                # Show raw snapshot data structure for debugging
                print("Snapshot Data Structure Analysis:")
                if instrument._snapshot_json:
                    snapshot = instrument._snapshot_json
                    print(f"  Top-level keys: {list(snapshot.keys())}")
                    if 'instrument' in snapshot:
                        inst_keys = list(snapshot['instrument'].keys())
                        print(f"  Instrument keys: {inst_keys}")
                        
                        # Look for potential data sections
                        data_sections = []
                        for key in inst_keys:
                            if isinstance(snapshot['instrument'].get(key), dict):
                                data_sections.append(key)
                        if data_sections:
                            print(f"  Data sections found: {data_sections}")
                else:
                    print("  No snapshot data stored")
                
            except Exception as e:
                logger.error(f"Error analyzing {company_name}: {str(e)}")
                print(f"Error: {str(e)}")
            
            print("\n" + "=" * 80 + "\n")
            
            # Add delay between requests
            await asyncio.sleep(0.5)


async def demo_search_capabilities():
    """Demonstrate enhanced search capabilities."""
    
    async with aiohttp.ClientSession() as session:
        api = PyOnVista()
        await api.install_client(session)
        
        print("Enhanced Search Capabilities Demo")
        print("-" * 40)
        
        # Test enhanced search
        print("Searching for 'Apple' stocks...")
        results = await api.search_instrument("Apple", instrument_type="STOCK", limit=5)
        
        for i, instrument in enumerate(results, 1):
            print(f"{i}. {instrument.name} ({instrument.isin})")
            print(f"   Symbol: {instrument.symbol}, Type: {instrument.type}")
        
        print("\nSearching for German stocks with 'SAP'...")
        results = await api.search_instrument("SAP", instrument_type="STOCK", country="DE", limit=3)
        
        for i, instrument in enumerate(results, 1):
            print(f"{i}. {instrument.name} ({instrument.isin})")
            print(f"   Symbol: {instrument.symbol}, Country: {instrument.isin[:2]}")
        
        print("\nDirect ISIN lookup...")
        instrument = await api.search_by_isin("US0378331005")  # Apple
        if instrument:
            print(f"Found: {instrument.name} ({instrument.symbol})")
        else:
            print("Instrument not found")


async def main():
    """Run the complete demo."""
    print("""
PyOnvista v2.0 Enhanced Features Demo
====================================

This demo showcases the new fundamental data extraction capabilities
that unlock the rich financial data hidden in OnVista snapshot responses.

Original PyOnvista: Basic quotes and search
Enhanced v2.0: Comprehensive financial analysis

""")
    
    try:
        await demo_search_capabilities()
        print("\n" + "=" * 80 + "\n")
        await demo_fundamental_data()
        
        print("""
Demo Complete!

Key v2.0 Enhancements:
- Financial ratios extracted from snapshot data
- Performance metrics and volatility analysis  
- Technical indicators (moving averages, RSI)
- Company information and sector data
- ESG/sustainability metrics
- Enhanced international stock search
- Improved error handling and rate limiting

The rich fundamental data was there all along in the OnVista API responses,
just not exposed through the original interface. PyOnvista v2.0 unlocks
this hidden treasure trove of financial information!
""")
        
    except Exception as e:
        logger.error(f"Demo failed: {str(e)}")
        print(f"Demo failed with error: {str(e)}")
        print("This might be due to network issues or API changes.")


if __name__ == "__main__":
    asyncio.run(main())
