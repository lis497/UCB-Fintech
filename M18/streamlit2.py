import streamlit as st                                                                            # to several arguments ()# M4 Project Risk Return Analysisimport streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

st.set_page_config(layout="wide")
st.title('Risk Return Analysis')

#st.write('### Input Data')

whale_df = pd.read_csv('whale_navs.csv',
        index_col ='date',
        parse_dates = True
    )


sec1, spacing, sec2 = st.columns([4,0.4,4])


with sec1:
    st.write('### Input Data')
    col1,col2 = sec1.columns(2)
    time_range = {"min_value":whale_df.index[0],"max_value":whale_df.index[-1], "format":"MM-DD-YYYY"}

    with col1:
        # start_date = col1.date_input('Start Date',min_value=whale_df.index[0],max_value=whale_df.index[-1])
        # end_date = col2.date_input('End Date',min_value=whale_df.index[0],max_value=whale_df.index[-1])
        start_date = col1.date_input("Start Date", value=date(2020,9,1), min_value = whale_df.index[0],
                                     max_value=whale_df.index[-1], format="MM-DD-YYYY")
    with col2:
        end_date = col2.date_input("end Date", value=date(2020,9,11), **time_range) # ** unpack a dict
                                                                                    # to several arguments ()
    st.write(whale_df.loc[start_date:end_date].head())


    st.write('### Whale Daily Returns 2014-2020')
    whale_daily_returns = whale_df.loc[start_date:end_date].pct_change().dropna()
    #st.write(whale_daily_returns.head(2))
    st.line_chart(whale_daily_returns)


with sec2:
    st.write('### Whale Cumulative Returns')
    whale_cumulative_returns = (1+whale_daily_returns).cumprod()
    st.line_chart(whale_cumulative_returns)

    fig = px.box(whale_daily_returns)
    st.plotly_chart(fig, theme='streamlit')
