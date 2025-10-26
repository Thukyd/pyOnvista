"""
PyOnvista v2.0 - Enhanced Features Demo

This script demonstrates the enhanced search and filtering capabilities
of PyOnvista v2.0, including international stock search, advanced filtering,
and ISIN-based lookups.

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


async def demo_enhanced_search():
    """Demonstrate enhanced search capabilities."""
    
    async with aiohttp.ClientSession() as session:
        api = PyOnVista()
        await api.install_client(session)
        
        print("Enhanced Search Features Demo")
        print("=" * 40)
        print()
        
        # Basic search with filtering
        print("1. Search with instrument type filter:")
        results = await api.search_instrument("Apple", instrument_type="STOCK", limit=5)
        print(f"Found {len(results)} Apple stocks:")
        for i, instrument in enumerate(results, 1):
            print(f"  {i}. {instrument.name} ({instrument.isin})")
            print(f"     Symbol: {instrument.symbol}, Type: {instrument.type}")
        print()
        
        # Country-specific search
        print("2. Search with country filter (German stocks):")
        results = await api.search_instrument("SAP", country="DE", limit=3)
        print(f"Found {len(results)} German SAP instruments:")
        for i, instrument in enumerate(results, 1):
            print(f"  {i}. {instrument.name} ({instrument.isin})")
            print(f"     Symbol: {instrument.symbol}")
        print()
        
        # Combined filters
        print("3. Combined filters (US stocks only):")
        results = await api.search_instrument("Tesla", country="US", instrument_type="STOCK", limit=3)
        print(f"Found {len(results)} US Tesla stocks:")
        for i, instrument in enumerate(results, 1):
            print(f"  {i}. {instrument.name} ({instrument.isin})")
            print(f"     Symbol: {instrument.symbol}")
        print()
        
        # Direct ISIN lookup
        print("4. Direct ISIN lookup:")
        test_isins = {
            "SAP SE": "DE0007164600",
            "Apple Inc.": "US0378331005",
            "Microsoft": "US5949181045"
        }
        
        for company, isin in test_isins.items():
            try:
                instrument = await api.search_by_isin(isin)
                if instrument:
                    print(f"  {company}: Found {instrument.name} ({instrument.symbol})")
                else:
                    print(f"  {company}: Not found")
            except Exception as e:
                print(f"  {company}: Error - {str(e)}")
        print()
        
        # International stock search
        print("5. International stock search by symbol:")
        symbols = ["AAPL", "TSLA", "MSFT"]
        
        for symbol in symbols:
            try:
                print(f"  Searching for {symbol}:")
                stocks = await api.search_international_stocks(symbol, limit=3)
                if stocks:
                    for i, stock in enumerate(stocks, 1):
                        print(f"    {i}. {stock.name} ({stock.isin}) - {stock.symbol}")
                else:
                    print(f"    No international stocks found for {symbol}")
            except Exception as e:
                print(f"    Error searching for {symbol}: {str(e)}")
        print()


async def demo_data_extraction():
    """Demonstrate basic data extraction capabilities."""
    
    async with aiohttp.ClientSession() as session:
        api = PyOnVista()
        await api.install_client(session)
        
        print("Data Extraction Demo")
        print("=" * 20)
        print()
        
        # Get detailed instrument data
        print("Getting detailed data for SAP SE...")
        try:
            instrument = await api.request_instrument(isin="DE0007164600")
            
            print(f"Name: {instrument.name}")
            print(f"Symbol: {instrument.symbol}")
            print(f"Type: {instrument.type}")
            print(f"ISIN: {instrument.isin}")
            
            if instrument.quote:
                print(f"Current Price: €{instrument.quote.close:.2f}")
                print(f"Volume: {instrument.quote.volume:,}")
                print(f"Last Update: {instrument.quote.timestamp}")
            
            print()
            
            # Test fundamental data extraction
            print("Testing v2.0 fundamental data extraction...")
            ratios = instrument.get_financial_ratios()
            performance = instrument.get_performance_metrics()
            company = instrument.get_company_info()
            
            print("Financial Ratios Available:")
            print(f"  P/E Ratio: {'Yes' if ratios.pe_ratio else 'No'}")
            print(f"  Market Cap: {'Yes' if ratios.market_cap else 'No'}")
            print(f"  Dividend Yield: {'Yes' if ratios.dividend_yield else 'No'}")
            
            print("Performance Data Available:")
            print(f"  1-Year Return: {'Yes' if performance.performance_1y else 'No'}")
            print(f"  Volatility: {'Yes' if performance.volatility_30d else 'No'}")
            
            print("Company Data Available:")
            print(f"  Sector: {'Yes' if company.sector else 'No'}")
            print(f"  Employees: {'Yes' if company.employees else 'No'}")
            
        except Exception as e:
            print(f"Error getting SAP data: {str(e)}")
        
        print()


async def demo_error_handling():
    """Demonstrate error handling capabilities."""
    
    async with aiohttp.ClientSession() as session:
        api = PyOnVista()
        await api.install_client(session)
        
        print("Error Handling Demo")
        print("=" * 20)
        print()
        
        # Test invalid search
        print("1. Testing invalid search parameters:")
        try:
            results = await api.search_instrument("")
            print(f"  Empty search returned {len(results)} results")
        except ValueError as e:
            print(f"  Caught expected error: {e}")
        
        # Test invalid ISIN
        print("2. Testing invalid ISIN:")
        try:
            instrument = await api.search_by_isin("INVALID_ISIN")
            if instrument:
                print(f"  Unexpected: Found instrument {instrument.name}")
            else:
                print("  As expected: No instrument found for invalid ISIN")
        except ValueError as e:
            print(f"  Caught expected error: {e}")
        
        # Test network error handling
        print("3. Testing graceful handling of API errors:")
        try:
            instrument = await api.request_instrument(isin="NONEXISTENT123456")
            print("  Unexpected: Found instrument for non-existent ISIN")
        except Exception as e:
            print(f"  Handled API error gracefully: {type(e).__name__}")
        
        print()


async def main():
    """Run the complete enhanced features demo."""
    print("""
PyOnvista v2.0 - Enhanced Features Demo
======================================

This demo showcases the enhanced search, filtering, and error handling
capabilities of PyOnvista v2.0.

Key Enhancements:
- Advanced search with multiple filters
- International stock symbol lookup
- Direct ISIN-based instrument lookup
- Robust error handling and validation
- Rate limiting for respectful API usage

""")
    
    try:
        await demo_enhanced_search()
        print("\n" + "=" * 60 + "\n")
        
        await demo_data_extraction()
        print("\n" + "=" * 60 + "\n")
        
        await demo_error_handling()
        
        print("""
Enhanced Features Demo Complete!

The enhanced PyOnvista v2.0 provides:
- More sophisticated search and filtering
- Better international market support
- Comprehensive error handling
- Production-ready reliability features
- Full backward compatibility with v1.0

Ready for comprehensive financial analysis!
""")
        
    except Exception as e:
        logger.error(f"Demo failed: {str(e)}")
        print(f"Demo failed with error: {str(e)}")
        print("This might be due to network issues or API changes.")


if __name__ == "__main__":
    asyncio.run(main())
