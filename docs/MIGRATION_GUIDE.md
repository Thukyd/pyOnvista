# pyOnvista v1.0 to v2.0 Migration Guide

## Overview

pyOnvista v2.0 is **fully backward compatible** with v1.0. Your existing code will continue to work without any changes. This guide shows you how to take advantage of the new v2.0 features.

## 🔄 What Stays the Same

All existing v1.0 functionality remains unchanged:

```python
# ✅ This v1.0 code continues to work in v2.0
import asyncio
import aiohttp
from pyonvista.api import PyOnVista

async def v1_compatible():
    async with aiohttp.ClientSession() as session:
        api = PyOnVista()
        await api.install_client(session)
        
        # All v1.0 methods work exactly the same
        results = await api.search_instrument("Apple")
        instrument = await api.request_instrument(isin="US0378331005")
        print(f"Price: €{instrument.quote.close:.2f}")

asyncio.run(v1_compatible())
```

## 🆕 What's New in v2.0

### 1. Enhanced Search Capabilities

**v1.0**: Basic text search only
```python
# v1.0 - Basic search
results = await api.search_instrument("Apple")
```

**v2.0**: Advanced filtering and international support
```python
# v2.0 - Enhanced search with filters
results = await api.search_instrument("Apple", 
                                    instrument_type="STOCK", 
                                    country="US", 
                                    limit=5)

# New: International stock symbol search
apple_stocks = await api.search_international_stocks("AAPL")

# New: Direct ISIN lookup
apple = await api.search_by_isin("US0378331005")
```

### 2. Fundamental Data Extraction

**v1.0**: Only basic quote data
```python
# v1.0 - Limited to basic quote information
instrument = await api.request_instrument(isin="DE0007164600")
print(f"Name: {instrument.name}")
print(f"Price: €{instrument.quote.close:.2f}")
print(f"Volume: {instrument.quote.volume}")
# That's all the data available in v1.0
```

**v2.0**: Comprehensive fundamental analysis
```python
# v2.0 - Rich fundamental data extraction
instrument = await api.request_instrument(isin="DE0007164600")

# NEW: Financial ratios
ratios = instrument.get_financial_ratios()
print(f"P/E Ratio: {ratios.pe_ratio:.2f}")
print(f"Market Cap: €{ratios.market_cap:,.0f}")
print(f"Dividend Yield: {ratios.dividend_yield:.2f}%")
print(f"EPS: €{ratios.eps:.2f}")

# NEW: Performance metrics
performance = instrument.get_performance_metrics()
print(f"1-Year Return: {performance.performance_1y:+.2f}%")
print(f"30-Day Volatility: {performance.volatility_30d:.2f}%")
print(f"Beta: {performance.beta:.2f}")

# NEW: Technical indicators
technical = instrument.get_technical_indicators()
print(f"20-Day MA: €{technical.moving_avg_20d:.2f}")
print(f"200-Day MA: €{technical.moving_avg_200d:.2f}")
print(f"RSI (14): {technical.rsi_14d:.1f}")

# NEW: Company information
company = instrument.get_company_info()
print(f"Sector: {company.sector}")
print(f"Industry: {company.industry}")
print(f"Employees: {company.employees:,}")
print(f"Headquarters: {company.headquarters}")

# NEW: ESG/Sustainability data
esg = instrument.get_sustainability_data()
print(f"ESG Score: {esg.esg_score:.1f}")
print(f"Environmental: {esg.environmental_score:.1f}")
print(f"Social: {esg.social_score:.1f}")
print(f"Governance: {esg.governance_score:.1f}")
```

### 3. Error Handling & Reliability

**v1.0**: Basic error handling
```python
# v1.0 - Manual error handling required
try:
    instrument = await api.request_instrument(isin="INVALID")
except Exception as e:
    print(f"Error: {e}")
```

**v2.0**: Enhanced error handling with graceful degradation
```python
# v2.0 - Robust error handling built-in
instrument = await api.request_instrument(isin="DE0007164600")

# Data extraction methods gracefully handle missing data
ratios = instrument.get_financial_ratios()
if ratios.pe_ratio:
    print(f"P/E Ratio: {ratios.pe_ratio:.2f}")
else:
    print("P/E Ratio: Not available")

# Built-in rate limiting prevents API abuse
# Automatic retry on rate limit responses
# Comprehensive logging for debugging
```

## 📋 Step-by-Step Migration

### Step 1: Update Your Installation (Optional)
Your existing installation will work, but to get the latest features:
```bash
pip install --upgrade pyonvista
```

### Step 2: Test Existing Code
Run your existing v1.0 code - everything should work exactly as before.

### Step 3: Gradually Add v2.0 Features
Start adding new capabilities to your existing code:

```python
# Your existing v1.0 code
async def existing_function():
    async with aiohttp.ClientSession() as session:
        api = PyOnVista()
        await api.install_client(session)
        
        instrument = await api.request_instrument(isin="DE0007164600")
        print(f"Price: €{instrument.quote.close:.2f}")
        
        # ADD: New v2.0 fundamental data
        ratios = instrument.get_financial_ratios()
        if ratios.pe_ratio:
            print(f"P/E Ratio: {ratios.pe_ratio:.2f}")
        
        performance = instrument.get_performance_metrics()
        if performance.performance_1y:
            print(f"1-Year Return: {performance.performance_1y:+.2f}%")
```

### Step 4: Leverage New Search Features

```python
# Enhance your search capabilities
async def enhanced_search():
    async with aiohttp.ClientSession() as session:
        api = PyOnVista()
        await api.install_client(session)
        
        # OLD: Basic search
        results = await api.search_instrument("Apple")
        
        # NEW: Filtered search
        us_stocks = await api.search_instrument("Apple", 
                                              country="US", 
                                              instrument_type="STOCK")
        
        # NEW: International symbol search
        apple_stocks = await api.search_international_stocks("AAPL")
        
        # NEW: Direct ISIN lookup
        apple = await api.search_by_isin("US0378331005")
```

## 🔧 Common Migration Patterns

### Pattern 1: Enhancing Existing Data Display

**Before (v1.0):**
```python
def display_stock_info(instrument):
    print(f"Stock: {instrument.name}")
    print(f"Symbol: {instrument.symbol}")
    print(f"Price: €{instrument.quote.close:.2f}")
    print(f"Volume: {instrument.quote.volume:,}")
```

**After (v2.0):**
```python
def display_stock_info(instrument):
    # Keep existing v1.0 functionality
    print(f"Stock: {instrument.name}")
    print(f"Symbol: {instrument.symbol}")
    print(f"Price: €{instrument.quote.close:.2f}")
    print(f"Volume: {instrument.quote.volume:,}")
    
    # Add new v2.0 fundamental data
    ratios = instrument.get_financial_ratios()
    performance = instrument.get_performance_metrics()
    company = instrument.get_company_info()
    
    if ratios.pe_ratio:
        print(f"P/E Ratio: {ratios.pe_ratio:.2f}")
    if ratios.dividend_yield:
        print(f"Dividend Yield: {ratios.dividend_yield:.2f}%")
    if performance.performance_1y:
        print(f"1-Year Return: {performance.performance_1y:+.2f}%")
    if company.sector:
        print(f"Sector: {company.sector}")
```

### Pattern 2: Enhanced Portfolio Analysis

**Before (v1.0):**
```python
async def analyze_portfolio(isins):
    for isin in isins:
        instrument = await api.request_instrument(isin=isin)
        print(f"{instrument.name}: €{instrument.quote.close:.2f}")
```

**After (v2.0):**
```python
async def analyze_portfolio(isins):
    for isin in isins:
        instrument = await api.request_instrument(isin=isin)
        ratios = instrument.get_financial_ratios()
        performance = instrument.get_performance_metrics()
        
        print(f"{instrument.name}: €{instrument.quote.close:.2f}")
        
        # NEW: Rich fundamental analysis
        if ratios.pe_ratio:
            print(f"  P/E: {ratios.pe_ratio:.2f}")
        if ratios.dividend_yield:
            print(f"  Dividend: {ratios.dividend_yield:.2f}%")
        if performance.performance_1y:
            print(f"  1Y Return: {performance.performance_1y:+.2f}%")
        if ratios.market_cap:
            print(f"  Market Cap: €{ratios.market_cap:,.0f}")
```

### Pattern 3: Screening and Filtering

**New v2.0 Capability:**
```python
async def value_stock_screener():
    """Find undervalued stocks using v2.0 fundamental data."""
    candidates = ["DE0007164600", "DE0007236101", "DE0008469008"]
    
    value_stocks = []
    for isin in candidates:
        instrument = await api.request_instrument(isin=isin)
        ratios = instrument.get_financial_ratios()
        
        # Screen for value: Low P/E, High dividend yield
        if (ratios.pe_ratio and ratios.pe_ratio < 20 and 
            ratios.dividend_yield and ratios.dividend_yield > 2.0):
            
            value_stocks.append({
                'name': instrument.name,
                'pe_ratio': ratios.pe_ratio,
                'dividend_yield': ratios.dividend_yield,
                'price': instrument.quote.close
            })
    
    return value_stocks
```

## ⚠️ Breaking Changes

**None!** v2.0 introduces zero breaking changes. All v1.0 code continues to work.

## 🚨 Common Issues

### Issue 1: Import Errors
If you see import errors, make sure you're using the correct class name:
```python
# ✅ Correct (note the capital 'V')
from pyonvista.api import PyOnVista

# ❌ Wrong (lowercase 'v')
from pyonvista.api import PyOnvista
```

### Issue 2: Missing Data
Not all instruments have all fundamental data. Always check for None values:
```python
# ✅ Safe approach
ratios = instrument.get_financial_ratios()
if ratios.pe_ratio:
    print(f"P/E Ratio: {ratios.pe_ratio:.2f}")
else:
    print("P/E Ratio: Not available")

# ❌ Unsafe - may cause errors
print(f"P/E Ratio: {ratios.pe_ratio:.2f}")  # Could be None
```

### Issue 3: Rate Limiting
v2.0 includes built-in rate limiting, but for heavy usage:
```python
# Configure rate limiting for your needs
api = PyOnVista(request_delay=0.2, timeout=60)
```

## 🎯 Next Steps

1. **Test your existing code** - ensure everything works as expected
2. **Explore new features** - run the demo scripts to see v2.0 capabilities
3. **Enhance gradually** - add new features incrementally to your applications
4. **Leverage comprehensive data** - build more sophisticated financial analysis tools

## 📚 Additional Resources

- **Demo Scripts**: See `examples/` directory for comprehensive usage examples
- **API Documentation**: All new methods are documented in the source code
- **Issues**: Report any migration issues on GitHub

---

**Welcome to pyOnvista v2.0 - Unlock the hidden potential of German financial data!**
