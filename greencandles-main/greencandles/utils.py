from greencandles.models import Stockbasics,Stock
import csv,json,os
from greencandles import db,app
import pandas as pd
import yfinance as yf

def import_data_from_csv(file_path):
    with open(file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip the header row
        print(csv_reader)

        for row in csv_reader:
            symbol, country, company = row
            stock = Stockbasics(symbol=symbol, country=country, company=company)
            db.session.add(stock)
        db.session.commit()

def return_stocks_info(symbol):
    keys = ['longName',
 'sector',
 'website',
 'address1',
 'address2',
 'city',
 'country',
 'zip',
 'phone',
 'fullTimeEmployees',
 'longBusinessSummary',
 'totalCash',
 'totalDebt',
 'totalRevenue',
 'symbol',
 'currentPrice',
 'marketCap',
 'open',
 'dayLow',
 'dayHigh',
 'previousClose',
 'fiftyTwoWeekHigh',
 'fiftyTwoWeekLow',
 '52WeekChange',
 'fiftyDayAverage',
 'twoHundredDayAverage',
 'overallRisk',
 'recommendationKey',
 'volume',
 'averageVolume',
 'returnOnEquity',
 'returnOnAssets',
 'pegRatio',
 'priceToBook',
 'trailingEps',
 'revenuePerShare',
 'totalCashPerShare',
 'bid','ask']
    stock = Stock.query.filter_by(symbol=symbol).first()
    if not stock:
        ticker = yf.Ticker(symbol)
        data = {}
        for i in range(len(keys)):
            key = keys[i]
            value = ticker.info.get(keys[i])
            if type(value) != 'str':
                value = str(value)
            value = value.replace("'","")
            data[key] = value

  

        
        # Specify the file path
        file_path = os.path.join(app.root_path, 'static', 'data','stockinfo', f'{symbol}.json')
        # Write JSON data to the file
        with open(file_path, "w") as file:
            json.dump(data, file)

        with open(file_path, "r") as file:
            # Load the JSON data
            data = json.load(file)            
    return f"{data}"

def pie_data(symbol):
    ticker = yf.Ticker(symbol)
    data = {}
    share_holders = ticker.major_holders[1].to_list()[:3]
    holding_percentages = ticker.major_holders[0].to_list()[:3]
    for i in range(len(share_holders)):
        data[share_holders[i]] = holding_percentages[i]
    return data 



def return_csv(symbol):
    file_path = os.path.join(app.root_path, 'static', 'data','stockscsv', f'{symbol}.csv')
    try:
        with open(file_path, "r") as file:
            pass
    except:
        ticker = yf.Ticker(symbol)  
        history = ticker.history("5y")
        history.reset_index(inplace=True)
        history.Date = history['Date'].dt.strftime('%Y-%m-%d')
        history = history[['Date', 'Open', 'High', 'Low', 'Close']]
        history.to_csv(file_path,index=False,header=False)

    json_data = []
    with open(file_path, "r") as file:
        for row in file:
            row = row.strip('\n')
            row = row.split(',')
            # print('##'*100)
            # print(row)
            json_row = {}
            json_row['time'] = row[0]
            json_row['open'] = row[1]
            json_row['high'] = row[2]
            json_row['low'] = row[3]
            json_row['close'] = row[4]
            json_data.append(json_row)
        
        return json_data   

