import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st 
import joblib

st.set_page_config(layout="wide")

df_2023 = pd.read_csv('cleaned_df.csv')

state_df = df_2023[['State', 'Bedroom', 'Bathroom', 'Area', 'MarketEstimate', 'RentEstimate', 'Latitude',
       'Longitude', 'ListedPrice']].groupby('State').mean().round(2)
state_df['RentalYield'] = state_df['RentEstimate'] * 12 /state_df['ListedPrice']

state_df3 = state_df[['ListedPrice','RentEstimate','RentalYield']].sort_values('ListedPrice', ascending=False)
max_price = state_df3['ListedPrice'].max()

fig1 = px.scatter_map(
    state_df,
    lat='Latitude',
    lon='Longitude',
    color='ListedPrice',
    color_continuous_scale="Plasma_r",
    size="ListedPrice",              # Bubble size
    size_max=40,
    hover_name=state_df.index,
    hover_data={'ListedPrice':':,.0f','Latitude': False,'Longitude':False},
    labels={'ListedPrice':'AveragePrice'},
    zoom=3,
    center={
        "lat": state_df["Latitude"].mean(),
        "lon": state_df["Longitude"].mean()
    },
    height=500,
    width=700,
    title="US Real Estate Average Price(2023)"
)
fig1.update_layout(
    map_style="open-street-map",
    margin=dict(l=0, r=0, t=50, b=0)
)


col1,col2 = st.columns([3,1])
with col1:

	st.title('State Average Price')
	st.plotly_chart(fig1, use_container_width=True)
	
	st.title('MA House Price Prediction')
	#st.write('Linear Regression and Lasso Model')
	model = joblib.load('best_lasso_Jul21.pkl')
	st.write(model)

	c1,c2,c3 = st.columns(3)
	with c1:
		bedroom = st.number_input(label='Bedroom',value=3.0,key='b1')
		bathroom = st.number_input('Bathroom',value=2.0)
	with c2:
		area = st.number_input('Area',value=2000.0)
		lotarea = st.number_input('LotArea',value=0.45)
		rentestimate = st.number_input('RentEstimate',value=3000.0)
	with c3:
		latitude = st.number_input('Latitude',value=42.5)
		longitude = st.number_input('Longitude',value=-71.0)
	data = [[bedroom,bathroom,area,lotarea,rentestimate,latitude,longitude]]
	predict_result = model.predict(data)[0]
	#st.write(predict_result)
	st.metric(
    	label="🏠 Predicted MA House Price",
    	value=f"${predict_result:,.0f}"
	)

	# CA
	st.title('CA House Price Prediction')
	ca_ridge_model = joblib.load('ca_ridge_July26.pkl')
	st.write(ca_ridge_model)

	c1,c2,c3 = st.columns(3)
	with c1:
		bedroom = st.number_input(label='Bedroom',value=3,key='b2',step=1,min_value=1)
		bathroom2 = st.number_input(label='Bathroom2',value=2,key='bath2',step=1,min_value=0)
	with c2:
		area2 = st.number_input('Area2',value=2000.0)
		lotarea2 = st.number_input('LotArea2',value=0.45)
		#rentestimate = st.number_input('RentEstimate',value=3000.0)
	with c3:
		latitude2 = st.number_input('Latitude2',value=34.0)
		longitude2 = st.number_input('Longitude2',value=-118.3)

	data2 = [[bedroom,bathroom2,area2,lotarea2,latitude2,longitude2]]
	predict_result2 = ca_ridge_model.predict(data2)[0]
	#st.write(predict_result)
	st.metric(
    	label="🏠 Predicted CA House Price",
    	value=f"${predict_result2:,.0f}"
	)


with col2:

	st.dataframe(
		state_df3,
		hide_index=False,
		use_container_width=True,
		height=600, #increase height
		column_config={
			'ListedPrice': st.column_config.ProgressColumn(
					'Average House Price',
					format='$%d',
					min_value=0,
					max_value=max_price,
				)})


