from __future__ import print_function
import pickle
import os.path
import threading
import sys
import math

import yfinance as yf
from notionpy.notion.client import NotionClient
from datetime import datetime

# start - CHANGE THESE
NOTION_V2_TOKEN = "<YOUR_NOTION_TOKEN_V2>" 
NOTION_PAGE_LINK = "<YOUR_NOTION_PAGE_LINK>"

STOCK_SYMBOLS_LIST = 1
REFRESH_BUTTON_POSITION = 3
UPDATING_POSITION = 4
DATABASE_POSITION = 6
# end   - CHANGE THESE

def get_stock_symbols():
    client = NotionClient(token_v2=NOTION_V2_TOKEN)
    page = client.get_block(NOTION_PAGE_LINK)
    refresh_button = page.children[STOCK_SYMBOLS_LIST]

    clear_table()

    raw_symbols = refresh_button.title
    symbols = [x.strip() for x in raw_symbols.split(",")]

    return symbols

def clear_table():
    client = NotionClient(token_v2=NOTION_V2_TOKEN)
    page = client.get_block(NOTION_PAGE_LINK)
    database = page.children[DATABASE_POSITION].collection
    updating_indicator = page.children[UPDATING_POSITION]

    updating_indicator.title = "🗑  Clearing Stocks table"

    rows = database.get_rows()
    for row in rows:
        row.remove()

    updating_indicator.title = "🌱  Stocks table is ready to go"

def enter_symbols(symbols):
    client = NotionClient(token_v2=NOTION_V2_TOKEN)
    page = client.get_block(NOTION_PAGE_LINK)
    database = page.children[DATABASE_POSITION].collection
    updating_indicator = page.children[UPDATING_POSITION]

    updating_indicator.title = "🔥 Updating Symbols -- progress: %s/%s" % (str(0), str(len(symbols)))

    for i, symbol in enumerate(symbols):
        row = database.add_row()
        row.symbol = symbol
        updating_indicator.title = "🔥  Updating Symbols -- progress: %s/%s" % (str(i+1), str(len(symbols)))

    updating_indicator.title = "👀  Symbols updated!"

def populate_stock_data():
    client = NotionClient(token_v2=NOTION_V2_TOKEN)
    page = client.get_block(NOTION_PAGE_LINK)
    database = page.children[DATABASE_POSITION].collection
    rows = database.get_rows()

    updating_indicator = page.children[UPDATING_POSITION]

    success = True
    failed_to_load = []
    for i, row in enumerate(rows):
        symbol = row.title
        stock = yf.Ticker(symbol)

        updating_indicator.title = "🟡  _Stocks are currently updating -- progress: %s/%s_" % (str(i+1), str(len(rows)))

        try:
            info = stock.info
            hist = stock.history(period="1y")

            name = info['shortName']
            descr = info['longBusinessSummary'] 
            price = info['open']
            category = info['category']
            min52Week = min(hist['Close'])
            max52Week = max(hist['Close'])
            latestPrice = hist['Close'].values.tolist()[-1]
            ratio = (latestPrice - min52Week) / (max52Week - min52Week)
            sector = info['sector']
            dividend_rate = info['trailingAnnualDividendYield'] if 'trailingAnnualDividendYield' in info else 0.0
            pe_ratio = info['forwardPE'] if 'forwardPE' in info else -1
            market_cap = info['marketCap'] if 'marketCap' in info else 0
            price_to_sales_ratio = info['priceToSalesTrailing12Months'] if 'priceToSalesTrailing12Months' in info else 0.0
            eps = info['forwardEps'] if 'forwardEps' in info else 0.0

            row.set_property('name', name)
            row.set_property('price', price)
            row.set_property('52-week Low', min52Week)
            row.set_property('52-week High', max52Week)
            row.set_property('ratio', round(ratio or -1, 2))
            row.set_property('dividend', dividend_rate and round(dividend_rate * 1000, 2) / 1000)
            row.set_property('sector', sector or "")
            row.set_property('description', descr[0:150] + "...")
            row.set_property('pe', round(pe_ratio or -1, 2))
            row.set_property('market_cap', '$' + str(round(market_cap / 1000000000 or -1, 1)) + ' B')
            row.set_property('price_to_sales', round(price_to_sales_ratio or -1, 2))
            row.set_property('eps', eps)
        except:
            success = False
            failed_to_load.append(symbol)

    if success:
        updating_indicator.title = "✅  Stocks have been updated as of `%s`" % get_datetime()
    else:
        updating_indicator.title = "🚨  Error loading %s" % ', '.join(failed_to_load)


def callback():
    client = NotionClient(token_v2=NOTION_V2_TOKEN)
    page = client.get_block(NOTION_PAGE_LINK)
    refresh_button = page.children[REFRESH_BUTTON_POSITION]
    updating_indicator = page.children[UPDATING_POSITION]

    if refresh_button.checked == True:
        refresh_button.checked = False
        main()

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def get_datetime():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y at %I:%M %p")
    return dt_string

def main():
    client = NotionClient(token_v2=NOTION_V2_TOKEN)
    page = client.get_block(NOTION_PAGE_LINK)
    refresh_button = page.children[REFRESH_BUTTON_POSITION]

    symbols = get_stock_symbols()
    enter_symbols(symbols)
    populate_stock_data()

if __name__ == '__main__':
    main()
    set_interval(callback, 2)
    set_interval(main, 60 * 60 * 6)
