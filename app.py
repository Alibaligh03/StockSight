from flask import Flask, render_template, request
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objs as go
import plotly.offline as pyo
import pandas as pd
from plotly.subplots import make_subplots

app = Flask(__name__)

# Add this function to search Yahoo Finance for any symbol (even if not in our list)
def is_valid_stock(ticker):
    """Check if a stock symbol is valid in Yahoo Finance"""
    try:
        stock = yf.Ticker(ticker)
        # Try to get some basic info to validate the symbol
        info = stock.info
        # If we get basic info without error, it's likely a valid symbol
        if info and 'symbol' in info:
            return True
    except:
        pass
    return False


stock_names = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corporation",
    "AMZN": "Amazon.com Inc.",
    "NVDA": "NVIDIA Corporation",
    "GOOGL": "Alphabet Inc. (Class A)",
    "GOOG": "Alphabet Inc. (Class C)",
    "META": "Meta Platforms Inc.",
    "TSLA": "Tesla Inc.",
    "BRK.B": "Berkshire Hathaway Inc. (Class B)",
    "UNH": "UnitedHealth Group Incorporated",
    "JNJ": "Johnson & Johnson",
    "XOM": "Exxon Mobil Corporation",
    "JPM": "JPMorgan Chase & Co.",
    "V": "Visa Inc.",
    "PG": "Procter & Gamble Company",
    "AVGO": "Broadcom Inc.",
    "MA": "Mastercard Incorporated",
    "HD": "Home Depot Inc.",
    "CVX": "Chevron Corporation",
    "LLY": "Eli Lilly and Company",
    "ABBV": "AbbVie Inc.",
    "MRK": "Merck & Co. Inc.",
    "KO": "Coca-Cola Company",
    "PEP": "PepsiCo Inc.",
    "WMT": "Walmart Inc.",
    "TMO": "Thermo Fisher Scientific Inc.",
    "COST": "Costco Wholesale Corporation",
    "BAC": "Bank of America Corporation",
    "ADBE": "Adobe Inc.",
    "CRM": "Salesforce Inc.",
    "DIS": "Walt Disney Company",
    "NFLX": "Netflix Inc.",
    "ACN": "Accenture plc",
    "CSCO": "Cisco Systems Inc.",
    "INTC": "Intel Corporation",
    "AMD": "Advanced Micro Devices Inc.",
    "TXN": "Texas Instruments Incorporated",
    "QCOM": "QUALCOMM Incorporated",
    "AMGN": "Amgen Inc.",
    "HON": "Honeywell International Inc.",
    "IBM": "International Business Machines Corporation",
    "UBER": "Uber Technologies Inc.",
    "PM": "Philip Morris International Inc.",
    "NEE": "NextEra Energy Inc.",
    "RTX": "RTX Corp",
    "LIN": "Linde plc",
    "WFC": "Wells Fargo & Company",
    "T": "AT&T Inc.",
    "SBUX": "Starbucks Corporation",
    "SPGI": "S&P Global Inc.",
    "GS": "Goldman Sachs Group Inc.",
    "VZ": "Verizon Communications Inc.",
    "AXP": "American Express Company",
    "LOW": "Lowe's Companies Inc.",
    "CAT": "Caterpillar Inc.",
    "ISRG": "Intuitive Surgical Inc.",
    "PLD": "Prologis Inc.",
    "DE": "Deere & Company",
    "NOW": "ServiceNow Inc.",
    "MS": "Morgan Stanley",
    "SYK": "Stryker Corporation",
    "UNP": "Union Pacific Corporation",
    "ELV": "Elevance Health Inc.",
    "LMT": "Lockheed Martin Corporation",
    "NKE": "Nike Inc.",
    "MDT": "Medtronic plc",
    "UPS": "United Parcel Service Inc.",
    "TGT": "Target Corporation",
    "BLK": "BlackRock Inc.",
    "C": "Citigroup Inc.",
    "INTU": "Intuit Inc.",
    "SCHW": "Charles Schwab Corporation",
    "AMT": "American Tower Corporation",
    "MO": "Altria Group Inc.",
    "PGR": "Progressive Corporation",
    "GILD": "Gilead Sciences Inc.",
    "BMY": "Bristol-Myers Squibb Company",
    "ADI": "Analog Devices Inc.",
    "CVS": "CVS Health Corporation",
    "CI": "Cigna Corporation",
    "ZTS": "Zoetis Inc.",
    "PYPL": "PayPal Holdings Inc.",
    "ABT": "Abbott Laboratories",
    "MMC": "Marsh & McLennan Companies Inc.",
    "TJX": "TJX Companies Inc.",
    "DUK": "Duke Energy Corporation",
    "SO": "Southern Company",
    "CMCSA": "Comcast Corporation",
    "BDX": "Becton Dickinson and Company",
    "NOC": "Northrop Grumman Corporation",
    "EOG": "EOG Resources Inc.",
    "CL": "Colgate-Palmolive Company",
    "ICE": "Intercontinental Exchange Inc.",
    "APD": "Air Products and Chemicals Inc.",
    "ITW": "Illinois Tool Works Inc.",
    "HCA": "HCA Healthcare Inc.",
    "PNC": "PNC Financial Services Group Inc.",
    "MPC": "Marathon Petroleum Corporation",
    "SLB": "Schlumberger Limited",
    "FIS": "Fidelity National Information Services Inc.",
    "FDX": "FedEx Corporation",
    "VRTX": "Vertex Pharmaceuticals Incorporated",
    "MU": "Micron Technology Inc.",
    "PXD": "Pioneer Natural Resources Company",
    "LRCX": "Lam Research Corporation",
    "ETN": "Eaton Corporation plc",
    "GM": "General Motors Company",
    "MCD": "McDonald's Corporation",
    "MMM": "3M Company",
    "AON": "Aon plc",
    "TFC": "Truist Financial Corporation",
    "NSC": "Norfolk Southern Corporation",
    "DHR": "Danaher Corporation",
    "USB": "U.S. Bancorp",
    "EMR": "Emerson Electric Co.",
    "BSX": "Boston Scientific Corporation",
    "ORCL": "Oracle Corporation",
    "PSX": "Phillips 66",
    "SHW": "Sherwin-Williams Company",
    "GD": "General Dynamics Corporation",
    "COF": "Capital One Financial Corporation",
    "MCK": "McKesson Corporation",
    "MCO": "Moody's Corporation",
    "ADP": "Automatic Data Processing Inc.",
    "CSX": "CSX Corporation",
    "BK": "Bank of New York Mellon Corporation",
    "CME": "CME Group Inc.",
    "SNPS": "Synopsys Inc.",
    "CCI": "Crown Castle Inc.",
    "AIG": "American International Group Inc.",
    "KLAC": "KLA Corporation",
    "NEM": "Newmont Corporation",
    "DXCM": "DexCom Inc.",
    "ROP": "Roper Technologies Inc.",
    "MCHP": "Microchip Technology Incorporated",
    "ADSK": "Autodesk Inc.",
    "APH": "Amphenol Corporation",
    "IDXX": "IDEXX Laboratories Inc.",
    "FCX": "Freeport-McMoRan Inc.",
    "WELL": "Welltower Inc.",
    "SRE": "Sempra Energy",
    "OXY": "Occidental Petroleum Corporation",
    "GIS": "General Mills Inc.",
    "PSA": "Public Storage",
    "AEP": "American Electric Power Company Inc.",
    "CDNS": "Cadence Design Systems Inc.",
    "CTAS": "Cintas Corporation",
    "VLO": "Valero Energy Corporation",
    "FISV": "Fiserv Inc.",
    "HUM": "Humana Inc.",
    "EW": "Edwards Lifesciences Corporation",
    "IQV": "IQVIA Holdings Inc.",
    "KMB": "Kimberly-Clark Corporation",
    "MSCI": "MSCI Inc.",
    "ORLY": "O'Reilly Automotive Inc.",
    "PCAR": "PACCAR Inc",
    "PPG": "PPG Industries Inc.",
    "RSG": "Republic Services Inc.",
    "SPG": "Simon Property Group Inc.",
    "STZ": "Constellation Brands Inc.",
    "WMB": "Williams Companies Inc.",
    "APO": "Apollo Global Management Inc.",
    "AZO": "AutoZone Inc.",
    "CB": "Chubb Limited",
    "CMG": "Chipotle Mexican Grill Inc.",
    "CPRT": "Copart Inc.",
    "CSGP": "CoStar Group Inc.",
    "DHI": "D.R. Horton Inc.",
    "DLR": "Digital Realty Trust Inc.",
    "EL": "Estée Lauder Companies Inc.",
    "FTNT": "Fortinet Inc.",
    "GWW": "W.W. Grainger Inc.",
    "HLT": "Hilton Worldwide Holdings Inc.",
    "ILMN": "Illumina Inc.",
    "LULU": "Lululemon Athletica Inc.",
    "MAR": "Marriott International Inc.",
    "MNST": "Monster Beverage Corporation",
    "NXPI": "NXP Semiconductors N.V.",
    "PAYX": "Paychex Inc.",
    "PEG": "Public Service Enterprise Group Incorporated",
    "PLTR": "Palantir Technologies Inc.",
    "REGN": "Regeneron Pharmaceuticals Inc.",
    "RMD": "ResMed Inc.",
    "ROST": "Ross Stores Inc.",
    "SBAC": "SBA Communications Corporation",
    "TDG": "TransDigm Group Incorporated",
    "TRV": "Travelers Companies Inc.",
    "TT": "Trane Technologies plc",
    "TXN": "Texas Instruments Incorporated",
    "WDAY": "Workday Inc.",
    "WST": "West Pharmaceutical Services Inc.",
    "XEL": "Xcel Energy Inc.",
    "YUM": "Yum! Brands Inc.",
    "ZBH": "Zimmer Biomet Holdings Inc.",
    "AJG": "Arthur J. Gallagher & Co.",
    "ALGN": "Align Technology Inc.",
    "AME": "AMETEK Inc.",
    "ANET": "Arista Networks Inc.",
    "ANSS": "ANSYS Inc.",
    "A": "Agilent Technologies Inc.",
    "BA": "Boeing Company",
    "BIIB": "Biogen Inc.",
    "BKNG": "Booking Holdings Inc.",
    "BKR": "Baker Hughes Company",
    "CARR": "Carrier Global Corporation",
    "CHTR": "Charter Communications Inc.",
    "CTSH": "Cognizant Technology Solutions Corporation",
    "D": "Dominion Energy Inc.",
    "DAL": "Delta Air Lines Inc.",
    "DD": "DuPont de Nemours Inc.",
    "DELL": "Dell Technologies Inc.",
    "DOW": "Dow Inc.",
    "DTE": "DTE Energy Company",
    "EA": "Electronic Arts Inc.",
    "EBAY": "eBay Inc.",
    "ECL": "Ecolab Inc.",
    "EFX": "Equifax Inc.",
    "EIX": "Edison International",
    "ELP": "Cia Paranaense De Energia Copel",
    "ENPH": "Enphase Energy Inc.",
    "EQIX": "Equinix Inc.",
    "EQR": "Equity Residential",
    "ES": "Eversource Energy",
    "EXC": "Exelon Corporation",
    "EXPE": "Expedia Group Inc.",
    "FANG": "Diamondback Energy Inc.",
    "FAST": "Fastenal Company",
    "FBHS": "Fortune Brands Home & Security Inc.",
    "FCNCA": "First Citizens BancShares Inc.",
    "FE": "FirstEnergy Corp.",
    "FFIV": "F5 Inc.",
    "FITB": "Fifth Third Bancorp",
    "FLT": "FleetCor Technologies Inc.",
    "FOX": "Fox Corporation",
    "FOXA": "Fox Corporation",
    "FRC": "First Republic Bank",
    "FTV": "Fortive Corporation",
    "GLW": "Corning Incorporated",
    "GPN": "Global Payments Inc.",
    "GRMN": "Garmin Ltd.",
    "HAL": "Halliburton Company",
    "HAS": "Hasbro Inc.",
    "HBAN": "Huntington Bancshares Incorporated",
    "HES": "Hess Corporation",
    "HIG": "Hartford Financial Services Group Inc.",
    "HOLX": "Hologic Inc.",
    "HPE": "Hewlett Packard Enterprise Company",
    "HPQ": "HP Inc.",
    "HRL": "Hormel Foods Corporation",
    "HSY": "Hershey Company",
    "HWM": "Howmet Aerospace Inc.",
    "IEX": "IDEX Corporation",
    "INCY": "Incyte Corporation",
    "IR": "Ingersoll Rand Inc.",
    "IRM": "Iron Mountain Incorporated",
    "J": "Jacobs Engineering Group Inc.",
    "JBHT": "J.B. Hunt Transport Services Inc.",
    "JCI": "Johnson Controls International plc",
    "JNPR": "Juniper Networks Inc.",
    "K": "Kellogg Company",
    "KEY": "KeyCorp",
    "KEYS": "Keysight Technologies Inc.",
    "KHC": "Kraft Heinz Company",
    "KMI": "Kinder Morgan Inc.",
    "KR": "Kroger Company",
    "L": "Loews Corporation",
    "LDOS": "Leidos Holdings Inc.",
    "LEN": "Lennar Corporation",
    "LH": "Laboratory Corporation of America Holdings",
    "LHX": "L3Harris Technologies Inc.",
    "LKQ": "LKQ Corporation",
    "LLY": "Eli Lilly and Company",
    "LNC": "Lincoln National Corporation",
    "LNT": "Alliant Energy Corporation",
    "LUV": "Southwest Airlines Co.",
    "LVS": "Las Vegas Sands Corp.",
    "LW": "Lamb Weston Holdings Inc.",
    "LYB": "LyondellBasell Industries N.V.",
    "MAA": "Mid-America Apartment Communities Inc.",
    "MAS": "Masco Corporation",
    "MDB": "MongoDB Inc.",
    "MDLZ": "Mondelez International Inc.",
    "MET": "MetLife Inc.",
    "MGM": "MGM Resorts International",
    "MHK": "Mohawk Industries Inc.",
    "MKC": "McCormick & Company Incorporated",
    "MLM": "Martin Marietta Materials Inc.",
    "MRNA": "Moderna Inc.",
    "MRO": "Marathon Oil Corporation",
    "MRVL": "Marvell Technology Inc.",
    "MSI": "Motorola Solutions Inc.",
    "MTB": "M&T Bank Corporation",
    "MTCH": "Match Group Inc.",
    "MTD": "Mettler-Toledo International Inc.",
    "NDAQ": "Nasdaq Inc.",
    "NEE": "NextEra Energy Inc.",
    "NFLX": "Netflix Inc.",
    "NI": "NiSource Inc.",
    "NKE": "Nike Inc.",
    "NOC": "Northrop Grumman Corporation",
    "NUE": "Nucor Corporation",
    "NVDA": "NVIDIA Corporation",
    "NVR": "NVR Inc.",
    "NWSA": "News Corporation",
    "NWS": "News Corporation",
    "O": "Realty Income Corporation",
    "ODFL": "Old Dominion Freight Line Inc.",
    "OKE": "ONEOK Inc.",
    "OMC": "Omnicom Group Inc.",
    "ON": "ON Semiconductor Corporation",
    "ORCL": "Oracle Corporation",
    "OTIS": "Otis Worldwide Corporation",
    "OXY": "Occidental Petroleum Corporation",
    "PARA": "Paramount Global",
    "PAYC": "Paycom Software Inc.",
    "PAYX": "Paychex Inc.",
    "PBA": "Pembina Pipeline Corporation",
    "PBR": "Petróleo Brasileiro S.A.",
    "PCG": "PG&E Corporation",
    "PEAK": "Healthpeak Properties Inc.",
    "PEG": "Public Service Enterprise Group Incorporated",
    "PFE": "Pfizer Inc.",
    "PFG": "Principal Financial Group Inc.",
    "PG": "Procter & Gamble Company",
    "PGR": "Progressive Corporation",
    "PH": "Parker-Hannifin Corporation",
    "PHM": "PulteGroup Inc.",
    "PKG": "Packaging Corporation of America",
    "PLD": "Prologis Inc.",
    "PM": "Philip Morris International Inc.",
    "PNC": "PNC Financial Services Group Inc.",
    "PNR": "Pentair plc",
    "PNW": "Pinnacle West Capital Corporation",
    "PPG": "PPG Industries Inc.",
    "PPL": "PPL Corporation",
    "PRU": "Prudential Financial Inc.",
    "PSA": "Public Storage",
    "PTC": "PTC Inc.",
    "PXD": "Pioneer Natural Resources Company",
    "PYPL": "PayPal Holdings Inc.",
    "QCOM": "QUALCOMM Incorporated",
    "QRVO": "Qorvo Inc.",
    "RCL": "Royal Caribbean Cruises Ltd.",
    "RE": "Everest Re Group Ltd.",
    "REG": "Regency Centers Corporation",
    "RF": "Regions Financial Corporation",
    "RHI": "Robert Half International Inc.",
    "RJF": "Raymond James Financial Inc.",
    "RL": "Ralph Lauren Corporation",
    "RMD": "ResMed Inc.",
    "ROK": "Rockwell Automation Inc.",
    "ROL": "Rollins Inc.",
    "ROP": "Roper Technologies Inc.",
    "ROST": "Ross Stores Inc.",
    "RSG": "Republic Services Inc.",
    "RTX": "RTX Corp",
    "SBUX": "Starbucks Corporation",
    "SCHW": "Charles Schwab Corporation",
    "SEE": "Sealed Air Corporation",
    "SHW": "Sherwin-Williams Company",
    "SIVB": "SVB Financial Group",
    "SJM": "J.M. Smucker Company",
    "SLB": "Schlumberger Limited",
    "SNA": "Snap-on Incorporated",
    "SNPS": "Synopsys Inc.",
    "SO": "Southern Company",
    "SPG": "Simon Property Group Inc.",
    "SPGI": "S&P Global Inc.",
    "SRE": "Sempra Energy",
    "STE": "STERIS plc",
    "STT": "State Street Corporation",
    "STX": "Seagate Technology Holdings plc",
    "STZ": "Constellation Brands Inc.",
    "SWK": "Stanley Black & Decker Inc.",
    "SWKS": "Skyworks Solutions Inc.",
    "SYF": "Synchrony Financial",
    "SYY": "Sysco Corporation",
    "T": "AT&T Inc.",
    "TAP": "Molson Coors Beverage Company",
    "TDG": "TransDigm Group Incorporated",
    "TDY": "Teledyne Technologies Incorporated",
    "TECH": "Bio-Techne Corporation",
    "TEL": "TE Connectivity Ltd.",
    "TER": "Teradyne Inc.",
    "TFC": "Truist Financial Corporation",
    "TFX": "Teleflex Incorporated",
    "TGT": "Target Corporation",
    "TJX": "TJX Companies Inc.",
    "TMO": "Thermo Fisher Scientific Inc.",
    "TMUS": "T-Mobile US Inc.",
    "TPR": "Tapestry Inc.",
    "TRMB": "Trimble Inc.",
    "TROW": "T. Rowe Price Group Inc.",
    "TRV": "Travelers Companies Inc.",
    "TSCO": "Tractor Supply Company",
    "TSLA": "Tesla Inc.",
    "TSN": "Tyson Foods Inc.",
    "TT": "Trane Technologies plc",
    "TTWO": "Take-Two Interactive Software Inc.",
    "TWTR": "Twitter Inc.",
    "TXN": "Texas Instruments Incorporated",
    "TXT": "Textron Inc.",
    "TYL": "Tyler Technologies Inc.",
    "UAL": "United Airlines Holdings Inc.",
    "UDR": "UDR Inc.",
    "UHS": "Universal Health Services Inc.",
    "ULTA": "Ulta Beauty Inc.",
    "UNH": "UnitedHealth Group Incorporated",
    "UNP": "Union Pacific Corporation",
    "UPS": "United Parcel Service Inc.",
    "URI": "United Rentals Inc.",
    "USB": "U.S. Bancorp",
    "V": "Visa Inc.",
    "VFC": "V.F. Corporation",
    "VLO": "Valero Energy Corporation",
    "VMC": "Vulcan Materials Company",
    "VRSK": "Verisk Analytics Inc.",
    "VRSN": "VeriSign Inc.",
    "VRTX": "Vertex Pharmaceuticals Incorporated",
    "VTR": "Ventas Inc.",
    "VZ": "Verizon Communications Inc.",
    "WAB": "Westinghouse Air Brake Technologies Corporation",
    "WAT": "Waters Corporation",
    "WBA": "Walgreens Boots Alliance Inc.",
    "WDC": "Western Digital Corporation",
    "WEC": "WEC Energy Group Inc.",
    "WELL": "Welltower Inc.",
    "WFC": "Wells Fargo & Company",
    "WHR": "Whirlpool Corporation",
    "WM": "Waste Management Inc.",
    "WMB": "Williams Companies Inc.",
    "WMT": "Walmart Inc.",
    "WRB": "W.R. Berkley Corporation",
    "WRK": "WestRock Company",
    "WST": "West Pharmaceutical Services Inc.",
    "WU": "Western Union Company",
    "WY": "Weyerhaeuser Company",
    "WYNN": "Wynn Resorts Limited",
    "XEL": "Xcel Energy Inc.",
    "XLNX": "Xilinx Inc.",
    "XOM": "Exxon Mobil Corporation",
    "XRAY": "DENTSPLY SIRONA Inc.",
    "XYL": "Xylem Inc.",
    "YUM": "Yum! Brands Inc.",
    "ZBH": "Zimmer Biomet Holdings Inc.",
    "ZBRA": "Zebra Technologies Corporation",
    "ZION": "Zions Bancorporation N.A.",
    "ZTS": "Zoetis Inc."
}

available_stocks = list(stock_names.keys())

def get_stock_name(ticker):
    """Get stock name from our dictionary"""
    return stock_names.get(ticker, ticker)

def get_stock_price(ticker):
    """Get current stock price"""
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period='1d', interval='1m')
        if not data.empty:
            return f"${data['Close'].iloc[-1]:.2f}"
    except:
        pass
    return "Loading..."

def get_quick_access_stocks():
    """Get the 4 predefined quick access stocks"""
    quick_stocks = ["AAPL", "GOOGL", "TSLA", "META"]
    stock_info = []
    
    for ticker in quick_stocks:
        stock_info.append({
            'symbol': ticker,
            'name': get_stock_name(ticker),
            'price': get_stock_price(ticker)
        })
    
    return stock_info



# Available period options
period_options = {
    '1d': '1 Day',
    '5d': '5 Days', 
    '1mo': '1 Month',
    '3mo': '3 Months',
    '6mo': '6 Months',
    '1y': '1 Year',
    '2y': '2 Years',
    '5y': '5 Years',
    '10y': '10 Years',
    'ytd': 'Year to Date',
    'max': 'Max History'
}

# Available interval options
interval_options = {
    '1d': 'Daily',
    '1wk': 'Weekly',
    '1mo': 'Monthly',
    '1h': '1 Hour',
    '30m': '30 Minutes',
    '15m': '15 Minutes',
    '5m': '5 Minutes',
    '1m': '1 Minute'
}

# Available chart type options
chart_type_options = {
    'candlestick': 'Candlestick',
    'line': 'Line Chart',
    'ohlc': 'OHLC Chart',
    'area': 'Area Chart'
}

# Most Popular Technical Indicators
technical_indicators = {
    'Moving Averages': {
        'sma_20': 'SMA 20',
        'sma_50': 'SMA 50', 
        'sma_200': 'SMA 200',
        'ema_20': 'EMA 20',
        'ema_50': 'EMA 50'
    },
    'Momentum': {
        'rsi': 'RSI (14)',
        'macd': 'MACD',
        'stoch': 'Stochastic',
        'cci': 'CCI',
        'willr': 'Williams %R'
    },
    'Volatility': {
        'bbands': 'Bollinger Bands',
        'atr': 'ATR'
    },
    'Volume': {
        'obv': 'OBV',
        'volume': 'Volume Bars',
        'mfi': 'Money Flow Index'
    },
    'Trend': {
        'adx': 'ADX',
        'ichimoku': 'Ichimoku Cloud'
    }
}

@app.route("/")
def home():
    # Get quick access stocks
    quick_stocks = get_quick_access_stocks()
    
    return render_template("home.html", 
                         quick_stocks=quick_stocks,
                         available_stocks=available_stocks)


@app.route("/search")
def search_stock():
    ticker = request.args.get('ticker', '').upper().strip()
    if ticker:
        # First check if it's in our predefined list
        if ticker in available_stocks:
            return redirect(url_for('stock_page', ticker=ticker))
        else:
            # If not in our list, validate with Yahoo Finance
            if is_valid_stock(ticker):
                return redirect(url_for('stock_page', ticker=ticker))
            else:
                flash(f"Stock symbol '{ticker}' not found in Yahoo Finance", "danger")
                return redirect(url_for('home'))
    return redirect(url_for('home'))

@app.route("/stock/<ticker>")
def stock_page(ticker):
    # Get parameters from query
    period = request.args.get('period', '6mo')
    interval = request.args.get('interval', '1d')
    chart_type = request.args.get('chart_type', 'candlestick')
    
    # Get selected indicators
    selected_indicators = request.args.getlist('indicators')
    
    # Validate parameters
    if period not in period_options:
        period = '6mo'
    if interval not in interval_options:
        interval = '1d'
    if chart_type not in chart_type_options:
        chart_type = 'candlestick'
    
    # Auto-adjust period for intraday intervals
    if interval in ['1m', '5m', '15m', '30m', '1h']:
        if period not in ['1d', '5d', '1mo']:
            period = '5d'
    
    # Get stock data
    stock = yf.Ticker(ticker)
    
    try:
        data = stock.history(period=period, interval=interval)
        
        if data.empty or len(data) == 0:
            raise ValueError("No data available")
            
    except Exception as e:
        error_message = f"Data not available for {period} period with {interval} interval."
        return render_template("stock.html", 
                             graph_html=f"<div class='alert alert-danger text-center' style='padding: 20px;'><h4>Data Not Available</h4><p>{error_message}</p></div>",
                             ticker=ticker,
                             period=period,
                             interval=interval,
                             chart_type=chart_type,
                             period_options=period_options,
                             interval_options=interval_options,
                             chart_type_options=chart_type_options,
                             technical_indicators=technical_indicators,
                             selected_indicators=selected_indicators,
                             current_price=None,
                             price_change=None,
                             percent_change=None)
    
    # Calculate selected technical indicators
    data = calculate_indicators(data, selected_indicators)
    
    # Create main chart with subplots
    fig = create_chart_with_subplots(data, ticker, period, interval, chart_type, selected_indicators)
    
    # Get current price info
    current_price = None
    price_change = None
    percent_change = None
    
    if not data.empty and len(data) > 0:
        current_price = data['Close'].iloc[-1]
        if len(data) > 1:
            prev_close = data['Close'].iloc[-2]
            price_change = current_price - prev_close
            percent_change = (price_change / prev_close) * 100
    
    graph_html = pyo.plot(fig, output_type='div')
    
    return render_template("stock.html", 
                         graph_html=graph_html, 
                         ticker=ticker,
                         period=period,
                         interval=interval,
                         chart_type=chart_type,
                         period_options=period_options,
                         interval_options=interval_options,
                         chart_type_options=chart_type_options,
                         technical_indicators=technical_indicators,
                         selected_indicators=selected_indicators,
                         current_price=current_price,
                         price_change=price_change,
                         percent_change=percent_change)

def calculate_indicators(data, selected_indicators):
    """Calculate selected technical indicators"""
    if not selected_indicators:
        return data
    
    for indicator in selected_indicators:
        try:
            if indicator == 'sma_20':
                data.ta.sma(length=20, append=True)
            elif indicator == 'sma_50':
                data.ta.sma(length=50, append=True)
            elif indicator == 'sma_200':
                data.ta.sma(length=200, append=True)
            elif indicator == 'ema_20':
                data.ta.ema(length=20, append=True)
            elif indicator == 'ema_50':
                data.ta.ema(length=50, append=True)
            elif indicator == 'rsi':
                data.ta.rsi(length=14, append=True)
            elif indicator == 'macd':
                data.ta.macd(append=True)
            elif indicator == 'stoch':
                data.ta.stoch(append=True)
            elif indicator == 'bbands':
                # Bollinger Bands with specific column names
                bb = data.ta.bbands(length=20, std=2, append=True)
            elif indicator == 'atr':
                data.ta.atr(append=True)
            elif indicator == 'obv':
                data.ta.obv(append=True)
            elif indicator == 'volume':
                # Volume is already in the data, we'll handle it in visualization
                pass
            elif indicator == 'mfi':
                data.ta.mfi(append=True)
            elif indicator == 'adx':
                data.ta.adx(append=True)
            elif indicator == 'cci':
                data.ta.cci(append=True)
            elif indicator == 'willr':
                data.ta.willr(append=True)
            elif indicator == 'ichimoku':
                # Ichimoku Cloud with specific parameters
                ichimoku = data.ta.ichimoku(append=True)
                
        except Exception as e:
            print(f"Error calculating {indicator}: {e}")
            continue
    
    return data

def create_chart_with_subplots(data, ticker, period, interval, chart_type, selected_indicators):
    """Create chart with subplots for all oscillators and separate indicators"""
    
    # Determine how many subplots we need
    has_rsi = 'rsi' in selected_indicators and 'RSI_14' in data.columns
    has_macd = 'macd' in selected_indicators and 'MACD_12_26_9' in data.columns
    has_stoch = 'stoch' in selected_indicators and 'STOCHk_14_3_3' in data.columns
    has_cci = 'cci' in selected_indicators and 'CCI_14_0.015' in data.columns
    has_willr = 'willr' in selected_indicators and 'WILLR_14' in data.columns
    has_mfi = 'mfi' in selected_indicators and 'MFI_14' in data.columns
    has_adx = 'adx' in selected_indicators and 'ADX_14' in data.columns
    has_obv = 'obv' in selected_indicators and 'OBV' in data.columns
    has_atr = 'atr' in selected_indicators and 'ATRr_14' in data.columns
    
    # Calculate number of rows
    rows = 1  # Start with main chart
    
    # Count each subplot indicator
    subplot_indicators = [has_rsi, has_macd, has_stoch, has_cci, has_willr, has_mfi, has_adx, has_obv, has_atr]
    rows += sum(subplot_indicators)
    
    # Adjust row heights dynamically based on number of subplots
    if rows == 1:  # Only main chart
        row_heights = [1.0]
    elif rows == 2:  # Main + 1 indicator
        row_heights = [0.75, 0.25]
    elif rows == 3:  # Main + 2 indicators
        row_heights = [0.65, 0.175, 0.175]
    elif rows == 4:  # Main + 3 indicators
        row_heights = [0.6, 0.133, 0.133, 0.134]
    elif rows == 5:  # Main + 4 indicators
        row_heights = [0.55, 0.1125, 0.1125, 0.1125, 0.1125]
    elif rows == 6:  # Main + 5 indicators
        row_heights = [0.5, 0.1, 0.1, 0.1, 0.1, 0.1]
    elif rows == 7:  # Main + 6 indicators
        row_heights = [0.45, 0.092, 0.092, 0.092, 0.092, 0.092, 0.092]
    elif rows == 8:  # Main + 7 indicators
        row_heights = [0.4, 0.085, 0.085, 0.085, 0.085, 0.085, 0.085, 0.085]
    else:  # Main + 8+ indicators
        row_heights = [0.35] + [0.065] * (rows - 1)
    
    # Create subplot titles
    subplot_titles = [f"{ticker} Price Chart"]
    if has_rsi: subplot_titles.append("RSI")
    if has_macd: subplot_titles.append("MACD")
    if has_stoch: subplot_titles.append("Stochastic")
    if has_cci: subplot_titles.append("CCI")
    if has_willr: subplot_titles.append("Williams %R")
    if has_mfi: subplot_titles.append("Money Flow Index")
    if has_adx: subplot_titles.append("ADX")
    if has_obv: subplot_titles.append("OBV")
    if has_atr: subplot_titles.append("ATR")
    
    # Create subplots with secondary y-axis for volume if needed
    has_volume = 'volume' in selected_indicators
    
    if has_volume:
        # Create subplots with secondary y-axis specification
        fig = make_subplots(
            rows=rows, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.015,
            subplot_titles=subplot_titles,
            row_heights=row_heights,
            specs=[[{"secondary_y": True}]] + [[{"secondary_y": False}]] * (rows - 1)
        )
    else:
        # Create regular subplots without secondary y-axis
        fig = make_subplots(
            rows=rows, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.015,
            subplot_titles=subplot_titles,
            row_heights=row_heights
        )
    
    # Main price chart (row 1)
    if chart_type == 'candlestick':
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Price'
        ), row=1, col=1, secondary_y=False)
    elif chart_type == 'line':
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Close'],
            mode='lines',
            line=dict(color='black', width=2),
            name='Close Price'
        ), row=1, col=1, secondary_y=False)
    elif chart_type == 'ohlc':
        fig.add_trace(go.Ohlc(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='OHLC'
        ), row=1, col=1, secondary_y=False)
    elif chart_type == 'area':
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Close'],
            fill='tozeroy',
            mode='lines',
            line=dict(color='blue', width=2),
            name='Close Price'
        ), row=1, col=1, secondary_y=False)
    
    # Add volume if selected (on main chart with secondary y-axis)
    if has_volume:
        fig.add_trace(go.Bar(
            x=data.index,
            y=data['Volume'],
            name='Volume',
            marker_color='rgba(100, 100, 100, 0.5)',
            opacity=0.7
        ), row=1, col=1, secondary_y=True)
    
    # Add overlay indicators to main chart (moving averages, Bollinger Bands, Ichimoku)
    fig = add_indicators_to_main_chart(fig, data, selected_indicators, has_volume)
    
    # Add subplots in order
    current_row = 2
    
    # RSI Subplot
    if has_rsi:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['RSI_14'],
            line=dict(color='purple', width=1.2),
            name='RSI',
            showlegend=False
        ), row=current_row, col=1)
        
        fig.add_hline(y=70, line_dash="dash", line_color="red", line_width=0.8, row=current_row, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", line_width=0.8, row=current_row, col=1)
        fig.add_hline(y=50, line_dash="dot", line_color="gray", line_width=0.3, row=current_row, col=1)
        
        fig.update_yaxes(range=[0, 100], row=current_row, col=1, title_text="RSI", title_font=dict(size=9), tickfont=dict(size=7))
        current_row += 1
    
    # MACD Subplot
    if has_macd:
        fig.add_trace(go.Scatter(x=data.index, y=data['MACD_12_26_9'], line=dict(color='blue', width=0.8), name='MACD', showlegend=False), row=current_row, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=data['MACDs_12_26_9'], line=dict(color='red', width=0.8), name='Signal', showlegend=False), row=current_row, col=1)
        
        colors_histogram = ['green' if val >= 0 else 'red' for val in data['MACDh_12_26_9']]
        fig.add_trace(go.Bar(x=data.index, y=data['MACDh_12_26_9'], name='Histogram', marker_color=colors_histogram, opacity=0.6, showlegend=False), row=current_row, col=1)
        
        fig.add_hline(y=0, line_color="black", line_width=0.5, row=current_row, col=1)
        fig.update_yaxes(title_text="MACD", row=current_row, col=1, title_font=dict(size=9), tickfont=dict(size=7))
        current_row += 1
    
    # Stochastic Subplot
    if has_stoch:
        fig.add_trace(go.Scatter(x=data.index, y=data['STOCHk_14_3_3'], line=dict(color='blue', width=1.0), name='%K', showlegend=False), row=current_row, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=data['STOCHd_14_3_3'], line=dict(color='red', width=1.0), name='%D', showlegend=False), row=current_row, col=1)
        
        fig.add_hline(y=80, line_dash="dash", line_color="red", line_width=0.8, row=current_row, col=1)
        fig.add_hline(y=20, line_dash="dash", line_color="green", line_width=0.8, row=current_row, col=1)
        fig.add_hline(y=50, line_dash="dot", line_color="gray", line_width=0.3, row=current_row, col=1)
        
        fig.update_yaxes(range=[0, 100], row=current_row, col=1, title_text="Stochastic", title_font=dict(size=9), tickfont=dict(size=7))
        current_row += 1
    
    # CCI Subplot
    if has_cci:
        fig.add_trace(go.Scatter(x=data.index, y=data['CCI_14_0.015'], line=dict(color='orange', width=1.2), name='CCI', showlegend=False), row=current_row, col=1)
        
        fig.add_hline(y=100, line_dash="dash", line_color="red", line_width=0.8, row=current_row, col=1)
        fig.add_hline(y=-100, line_dash="dash", line_color="green", line_width=0.8, row=current_row, col=1)
        fig.add_hline(y=0, line_color="black", line_width=0.5, row=current_row, col=1)
        
        fig.update_yaxes(range=[-200, 200], row=current_row, col=1, title_text="CCI", title_font=dict(size=9), tickfont=dict(size=7))
        current_row += 1
    
    # Williams %R Subplot
    if has_willr:
        fig.add_trace(go.Scatter(x=data.index, y=data['WILLR_14'], line=dict(color='brown', width=1.2), name='Williams %R', showlegend=False), row=current_row, col=1)
        
        fig.add_hline(y=-20, line_dash="dash", line_color="red", line_width=0.8, row=current_row, col=1)
        fig.add_hline(y=-80, line_dash="dash", line_color="green", line_width=0.8, row=current_row, col=1)
        fig.add_hline(y=-50, line_dash="dot", line_color="gray", line_width=0.3, row=current_row, col=1)
        
        fig.update_yaxes(range=[-100, 0], row=current_row, col=1, title_text="Williams %R", title_font=dict(size=9), tickfont=dict(size=7))
        current_row += 1
    
    # Money Flow Index (MFI) Subplot
    if has_mfi:
        fig.add_trace(go.Scatter(x=data.index, y=data['MFI_14'], line=dict(color='teal', width=1.2), name='MFI', showlegend=False), row=current_row, col=1)
        
        fig.add_hline(y=80, line_dash="dash", line_color="red", line_width=0.8, row=current_row, col=1)
        fig.add_hline(y=20, line_dash="dash", line_color="green", line_width=0.8, row=current_row, col=1)
        fig.add_hline(y=50, line_dash="dot", line_color="gray", line_width=0.3, row=current_row, col=1)
        
        fig.update_yaxes(range=[0, 100], row=current_row, col=1, title_text="MFI", title_font=dict(size=9), tickfont=dict(size=7))
        current_row += 1
    
    # ADX Subplot
    if has_adx:
        fig.add_trace(go.Scatter(x=data.index, y=data['ADX_14'], line=dict(color='darkblue', width=1.2), name='ADX', showlegend=False), row=current_row, col=1)
        
        # ADX reference lines
        fig.add_hline(y=25, line_dash="dash", line_color="orange", line_width=0.8, row=current_row, col=1)
        fig.add_hline(y=50, line_dash="dash", line_color="red", line_width=0.8, row=current_row, col=1)
        
        fig.update_yaxes(range=[0, 100], row=current_row, col=1, title_text="ADX", title_font=dict(size=9), tickfont=dict(size=7))
        current_row += 1
    
    # OBV Subplot
    if has_obv:
        fig.add_trace(go.Scatter(x=data.index, y=data['OBV'], line=dict(color='darkgreen', width=1.2), name='OBV', showlegend=False), row=current_row, col=1)
        
        fig.update_yaxes(row=current_row, col=1, title_text="OBV", title_font=dict(size=9), tickfont=dict(size=7))
        current_row += 1
    
    # ATR Subplot
    if has_atr:
        fig.add_trace(go.Scatter(x=data.index, y=data['ATRr_14'], line=dict(color='darkred', width=1.2), name='ATR', showlegend=False), row=current_row, col=1)
        
        fig.update_yaxes(row=current_row, col=1, title_text="ATR", title_font=dict(size=9), tickfont=dict(size=7))
    
    # Update layout
    layout_updates = {
        'title': f"{ticker} - {period_options[period]} ({interval_options[interval]})",
        'xaxis_title': "Date",
        'template': "plotly_white",
        'height': max(500, 400 + (rows * 80)),  # Dynamic height based on rows
        'showlegend': True,
        'legend': dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    }
    
    # Configure secondary y-axis for volume if present
    if has_volume:
        layout_updates['yaxis2'] = dict(
            title="Volume",
            overlaying="y",
            side="right",
            showgrid=False,
            showticklabels=True
        )
        
        # Make sure the primary y-axis shows price
        fig.update_yaxes(title_text="Price", row=1, col=1, secondary_y=False)
        fig.update_yaxes(title_text="Volume", row=1, col=1, secondary_y=True)
    
    fig.update_layout(**layout_updates)
    
    # Update subplot titles to be smaller
    for i in range(rows):
        fig.layout.annotations[i].font.size = 10
    
    # Remove range slider from all but the bottom subplot
    fig.update_xaxes(rangeslider_visible=False)
    
    # Add range slider to bottom subplot only
    bottom_row = rows
    fig.update_xaxes(rangeslider_visible=True, row=bottom_row, col=1, rangeslider_thickness=0.04)
    
    return fig

def add_indicators_to_main_chart(fig, data, selected_indicators, has_volume=False):
    """Add technical indicators to the main price chart"""
    if not selected_indicators:
        return fig
    
    # Color palette for indicators
    colors = {
        'sma_20': 'blue',
        'sma_50': 'red', 
        'sma_200': 'green',
        'ema_20': 'orange',
        'ema_50': 'purple',
        'bb_upper': 'rgba(255,0,0,0.3)',
        'bb_middle': 'rgba(255,0,0,0.6)',
        'bb_lower': 'rgba(255,0,0,0.3)',
        'atr': 'orange',
        'obv': 'purple',
        'mfi': 'green',
        'adx': 'red',
        'cci': 'blue',
        'willr': 'orange',
        'ichimoku_a': 'green',
        'ichimoku_b': 'red',
        'ichimoku_base': 'blue',
        'ichimoku_conversion': 'purple'
    }
    
    for indicator in selected_indicators:
        try:
            # Moving Averages
            if indicator == 'sma_20' and 'SMA_20' in data.columns:
                fig.add_trace(go.Scatter(
                    x=data.index, y=data['SMA_20'],
                    line=dict(color=colors['sma_20'], width=1.5),
                    name='SMA 20'
                ), row=1, col=1, secondary_y=False)
                
            elif indicator == 'sma_50' and 'SMA_50' in data.columns:
                fig.add_trace(go.Scatter(
                    x=data.index, y=data['SMA_50'],
                    line=dict(color=colors['sma_50'], width=1.5),
                    name='SMA 50'
                ), row=1, col=1, secondary_y=False)
                
            elif indicator == 'sma_200' and 'SMA_200' in data.columns:
                fig.add_trace(go.Scatter(
                    x=data.index, y=data['SMA_200'],
                    line=dict(color=colors['sma_200'], width=1.5),
                    name='SMA 200'
                ), row=1, col=1, secondary_y=False)
                
            elif indicator == 'ema_20' and 'EMA_20' in data.columns:
                fig.add_trace(go.Scatter(
                    x=data.index, y=data['EMA_20'],
                    line=dict(color=colors['ema_20'], width=1.5),
                    name='EMA 20'
                ), row=1, col=1, secondary_y=False)
                
            elif indicator == 'ema_50' and 'EMA_50' in data.columns:
                fig.add_trace(go.Scatter(
                    x=data.index, y=data['EMA_50'],
                    line=dict(color=colors['ema_50'], width=1.5),
                    name='EMA 50'
                ), row=1, col=1, secondary_y=False)
                
            # Bollinger Bands
            elif indicator == 'bbands':
                # Check for different possible column names for Bollinger Bands
                bb_upper_col = None
                bb_middle_col = None
                bb_lower_col = None
                
                # Try different possible column naming conventions
                possible_upper = ['BBU_20_2.0', 'BBU_20_2', 'BBU_20', 'BB_UPPER']
                possible_middle = ['BBM_20_2.0', 'BBM_20_2', 'BBM_20', 'BB_MIDDLE']
                possible_lower = ['BBL_20_2.0', 'BBL_20_2', 'BBL_20', 'BB_LOWER']
                
                for col in possible_upper:
                    if col in data.columns:
                        bb_upper_col = col
                        break
                
                for col in possible_middle:
                    if col in data.columns:
                        bb_middle_col = col
                        break
                
                for col in possible_lower:
                    if col in data.columns:
                        bb_lower_col = col
                        break
                
                if bb_upper_col and bb_middle_col and bb_lower_col:
                    # Add Bollinger Bands - CORRECTED: shade from lower to upper
                    # First add the lower band
                    fig.add_trace(go.Scatter(
                        x=data.index, y=data[bb_lower_col],
                        line=dict(color=colors['bb_lower'], width=1, dash='dash'),
                        name='BB Lower',
                        showlegend=True
                    ), row=1, col=1, secondary_y=False)
                    
                    # Then add the upper band and fill from lower to upper
                    fig.add_trace(go.Scatter(
                        x=data.index, y=data[bb_upper_col],
                        line=dict(color=colors['bb_upper'], width=1, dash='dash'),
                        name='BB Upper',
                        fill='tonexty',  # This fills from the previous trace (lower band) to this one (upper band)
                        fillcolor='rgba(255,0,0,0.1)',
                        showlegend=True
                    ), row=1, col=1, secondary_y=False)
                    
                    # Finally add the middle band on top
                    fig.add_trace(go.Scatter(
                        x=data.index, y=data[bb_middle_col],
                        line=dict(color=colors['bb_middle'], width=1),
                        name='BB Middle',
                        showlegend=True
                    ), row=1, col=1, secondary_y=False)
                
            # Ichimoku Cloud
            elif indicator == 'ichimoku':
                # Check for Ichimoku columns
                ichimoku_columns = {
                    'conversion': ['ISA_9', 'ICS_9', 'ITS_9'],
                    'base': ['ISB_26', 'IBS_26', 'IKS_26'],
                    'span_a': ['ISA_9', 'ICS_9', 'ITS_9'],  # Leading Span A
                    'span_b': ['ISB_26', 'IBS_26', 'IKS_26'],  # Leading Span B
                    'lagging': ['ILS_26', 'ILS_52', 'ICS_26']  # Lagging Span
                }
                
                # Find available columns
                available_cols = {}
                for key, possible_cols in ichimoku_columns.items():
                    for col in possible_cols:
                        if col in data.columns:
                            available_cols[key] = col
                            break
                
                # Add Ichimoku components if found
                if 'conversion' in available_cols:
                    fig.add_trace(go.Scatter(
                        x=data.index, y=data[available_cols['conversion']],
                        line=dict(color=colors['ichimoku_conversion'], width=1),
                        name='Ichimoku Conversion',
                        showlegend=True
                    ), row=1, col=1, secondary_y=False)
                
                if 'base' in available_cols:
                    fig.add_trace(go.Scatter(
                        x=data.index, y=data[available_cols['base']],
                        line=dict(color=colors['ichimoku_base'], width=1),
                        name='Ichimoku Base',
                        showlegend=True
                    ), row=1, col=1, secondary_y=False)
                
                # Add Ichimoku Cloud (the shaded area between Span A and Span B)
                if 'span_a' in available_cols and 'span_b' in available_cols:
                    span_a_col = available_cols['span_a']
                    span_b_col = available_cols['span_b']
                    
                    # Determine which span is on top for proper filling
                    # We need to fill between the two spans regardless of which is higher
                    fig.add_trace(go.Scatter(
                        x=data.index, 
                        y=data[span_a_col],
                        line=dict(color='rgba(0,0,0,0)'),  # Invisible line
                        showlegend=False,
                        hoverinfo='skip'
                    ), row=1, col=1, secondary_y=False)
                    
                    fig.add_trace(go.Scatter(
                        x=data.index, 
                        y=data[span_b_col],
                        line=dict(color='rgba(0,0,0,0)'),  # Invisible line
                        fill='tonexty',
                        fillcolor='rgba(0,150,255,0.2)',
                        name='Ichimoku Cloud',
                        showlegend=True
                    ), row=1, col=1, secondary_y=False)
                    
                if 'lagging' in available_cols:
                    fig.add_trace(go.Scatter(
                        x=data.index, y=data[available_cols['lagging']],
                        line=dict(color='orange', width=1, dash='dot'),
                        name='Ichimoku Lagging',
                        showlegend=True
                    ), row=1, col=1, secondary_y=False)
                
        except Exception as e:
            print(f"Error adding {indicator} to chart: {e}")
            continue
    
    return fig

if __name__ == "__main__":
    app.run(debug=True)