from analysis import StockPrice
import streamlit as st
import pandas as pd
from datetime import datetime



ibov_tickers = pd.read_csv('./data/ibov_tickers.csv')


from catch_clean import BrazilianIndicators
from analysis import AnalysisSeriesMontly, StockPrice
import streamlit as st
import pandas as pd


data = BrazilianIndicators()
data.clean_data_bcb()
data.clean_data_ibge()
data = data.data_frame_indicators()
ibov = pd.read_csv('./data/ibov.csv')
ibov['date'] = pd.to_datetime(ibov['date'])
ibov.columns = ibov.columns.str.lstrip()
# Indexers description
description = pd.DataFrame({'Savings': ['SAVINGS: Profitability on the 1st day of the month (BCB-Demab)'],
                            'CDI': ['CDI: Monthly Accumulated Interest Rate (BCB-Demab)'],
                            'IPCA': ['IPCA: Covers families with income from 1 to 40 minimum wages (IBGE)'],
                            'INPC': ['INPC: Covers families with income from 1 a 5 minimum wages (IBGE)'],
                            'Selic': ['Selic: Monthly Accumulated Interest Rate (BCB-Demab)']})

def main():
    st.set_page_config(layout='wide')
    stocks_ibov = ibov.columns[1:]
    indexers = ['Savings', 'CDI', 'IPCA', 'INPC', 'Selic']
    st.markdown("<h1 style='text-align: right; font-size: 15px; font-weight: normal'>Version 1.5</h1>", 
                unsafe_allow_html=True)
    st.title('Financial Data Analysis')
    st.sidebar.selectbox('Country', ['Brazil'])
    indicators = ['Indexers', 'Stocks']
    indicator = st.sidebar.selectbox('Indicator', indicators)
    if indicator == 'Indexers':
        st.subheader('Brazilian Economic Indices')
        start_year = str(st.sidebar.selectbox('Start Year', sorted(data['date'].dt.year.unique(), reverse=True)))
        indexer = st.sidebar.multiselect('Indexer', indexers, default=['Savings'])
        if indexer:
            analyze = AnalysisSeriesMontly(data, start_year)
            analyze.visualize_indicator(indexer)
            analyze.acumulated(indexer)
        else:
            st.write('Please select a indexer!')
    elif indicator == 'Stocks':
        st.subheader('Brazilian Stock Price')
        start_date = str(st.sidebar.date_input('Initial Date', datetime(2021, 1, 1)))
        visualize_stocks = st.sidebar.multiselect('Stocks', stocks_ibov, default='ABEV3.SA')
        if visualize_stocks:
            candle_data = StockPrice(tickers=visualize_stocks)
            candle_data.request_data(start_date=start_date)
            candle_data.candlestick()
        else:
            st.write('Please select a stock option!')
    if indicator == 'Indexers':
        for index in indexer:
            st.text(description[index][0])
    st.markdown('[GitHub](https://github.com/MarcosRMG/Investimentos)')

if __name__ == '__main__':
    main()
