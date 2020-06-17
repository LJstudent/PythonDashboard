import pandas_datareader as pdr
import datetime as dt
import json
from urllib.request import urlopen
import CheckFile as ch
import pandas as pd


def yahoo_download(name):
    df = pdr.DataReader(name, "yahoo", dt.datetime(2018, 1, 1), dt.datetime.now())
    return df


def profile_download(name):
    url = ("https://financialmodelingprep.com/api/v3/company/profile/" + name + "?apikey=f4316d749878bafa2b5d132402cd3c16")
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)['profile']

def dividend_download(name):
    url = ("https://financialmodelingprep.com/api/v3/historical-price-full/stock_dividend/" + name + "?apikey=f4316d749878bafa2b5d132402cd3c16")
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return ch.dividend(json.loads(data)['historical'])

    # For next time make a list or dict and check in other div if dividend ratio is long and steady at least 5 years
    # how much each year

def financial_statements(name):
    urls_list = []
    frames = []
    # disable chained assignments
    pd.options.mode.chained_assignment = None  # needed otherwise error about copy / slicing

    url_income_statement = ("https://financialmodelingprep.com/api/v3/financials/income-statement/" + name + "?apikey=f4316d749878bafa2b5d132402cd3c16")
    url_cash_flow_statement = ("https://financialmodelingprep.com/api/v3/financials/cash-flow-statement/" + name + "?apikey=f4316d749878bafa2b5d132402cd3c16")
    url_balance_sheet_statement = ("https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/" + name + "?apikey=f4316d749878bafa2b5d132402cd3c16")

    urls_list.append(url_income_statement)
    urls_list.append(url_cash_flow_statement)
    urls_list.append(url_balance_sheet_statement)

    for url in urls_list:
        response = urlopen(url)
        data = response.read().decode("utf-8")
        data = (json.loads(data)['financials'])
        df = pd.DataFrame.from_dict(data, orient='columns')
        frames.append(df)

    total_dataframe = pd.merge(pd.merge(frames[0], frames[1], how='right', on=['date']), frames[2], how='right', on=['date'])
    revenue_dataframe = total_dataframe[['date', 'Revenue', 'Cost of Revenue', 'Net Income']]
    revenue_dataframe = revenue_dataframe.drop(revenue_dataframe.index[5:])  # houd alleen de eerste 5 rijen

    return revenue_dataframe


# make structure table later on data
