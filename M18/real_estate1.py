import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events
import streamlit as st 

df_2023 = pd.read_csv('cleaned_df.csv')


fig = go.Figure()

# fig = px.scatter_map(
# 	df_2023,
# 	lat='Latitude',
# 	lon='Longitude',
# 	color='ListedPrice',
# 	hover_name='ListedPrice',
# 	zoom=3,
# 	center={
# 	'lat': df_2023['Latitude'].mean(),
# 	'lon': df_2023['Longitude'].mean()
# 	},
# 	height=500,
# 	width=700,
# 	title='US Real Estate (2023)'
# )


# this works, you can use a dict, but not recommended
# fig.add_trace(
# 	{
# 		"lat":df_2023["Latitude"],
# 		"lon":df_2023["Longitude"],
# 		"color":df_2023["ListedPrice"]
#       ...	
# 	})

fig.add_trace(
	go.Scattermap(
		lat = df_2023["Latitude"],
		lon = df_2023["Longitude"],
		mode = "markers",
		marker = dict(
			color=df_2023["ListedPrice"],
			size = 10,
			colorscale="Viridis",
			showscale=True
			),
		hovertext = df_2023["ListedPrice"],
		hovertemplate="Price: %{hovertext}<extra></extra>",
		customdata=df_2023.index
		
		
		
	))

fig.update_layout(
	map=dict(
		zoom = 3,
		center = {
		'lat': df_2023['Latitude'].mean(),
 		'lon': df_2023['Longitude'].mean()
		},
		style='open-street-map',
		),
	height=500, width=700,
	title="US Real Estate (2023)",
	margin=dict(l=0,r=0,t=50,b=0)
	)



#fig.show()
st.title('US Real Estate (2023)')
st.plotly_chart(fig, use_container_width=True)

state_df = df_2023[['State', 'Bedroom', 'Bathroom', 'Area', 'MarketEstimate', 'RentEstimate', 'Latitude',
       'Longitude', 'ListedPrice']].groupby('State').mean().round(2)
state_df['RentalYield'] = state_df['RentEstimate'] * 12 /state_df['ListedPrice']
st.write(state_df.head())
st.write(state_df[['ListedPrice','RentEstimate','RentalYield']])

fig1 = px.scatter_map(
    state_df,
    lat='Latitude',
    lon='Longitude',
    color='ListedPrice',
    color_continuous_scale="Plasma_r",
    size="ListedPrice",              # Bubble size
    size_max=40,
    hover_name="ListedPrice",
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

st.title('State Average Price')
st.plotly_chart(fig1, use_container_width=True)

state_df2 = state_df.sort_values('ListedPrice')
state_df2 = state_df2.reset_index()
fig2 = px.bar(
	state_df2.tail(10),
	x='State',
	y='ListedPrice',
	title='Top 10 Average House Prices by State',
	)
fig2.update_layout(
	width=1400,
	height=600
	)

st.plotly_chart(fig2, use_container_width=False)



# ===================================================================
# ===================================================================

# print("Print Statedf2\n",state_df2.tail(10))
temp_dict = {"type":"bar", 
             "y": state_df2.loc[40:, "State"],
             "x": state_df2.loc[40:, "ListedPrice"],
             "orientation": "h",
             "marker_color": "crimson",
             "width": 0.3
             
             }

fig2 = go.Figure(
	temp_dict
    # go.Bar(
    #     state_df2.tail(10),
    #     y='ListedPrice',
    #     x='State',
    #     orientation="h"
    # )
)
fig2.update_layout(title="Horizontal Bar Chart")
st.plotly_chart(fig2, use_container_width=False)
# ===================================================================

fig = go.Figure()
# white bar background
fig.add_trace(go.Bar(
	x = [state_df2["ListedPrice"].max() for i in range(40)],
	y = state_df2.loc[10:, "State"],
	orientation ="h",
	marker_color="#E5E7EB",
	hoverinfo="skip",
	showlegend=False
	))
# blue bar in the middle
fig.add_trace(go.Bar(
    x=state_df2.loc[10:, "ListedPrice"],
    y=state_df2.loc[10:, "State"],
    orientation="h",
    marker_color="#3B82F6",
    text=state_df2.loc[10:, "ListedPrice"],
    textposition="inside",
    showlegend=False,
    ))
# red bar on the top
fig.add_trace(go.Bar(
    x=state_df2.loc[10:, "RentEstimate"]*12,
    y=state_df2.loc[10:, "State"],
    orientation="h",
    marker_color="red",
    text=state_df2.loc[10:, "RentEstimate"],
    textposition="inside",
    showlegend=False,
    ))
fig.update_layout(
	title="Horizontal Bar Chart",
	barmode="overlay",
	bargap=0.4,
	xaxis_range=[0,state_df2["ListedPrice"].max()],
	template="simple_white",
	barcornerradius=15,
	height=1000
	)
st.plotly_chart(fig, use_container_width=False)

state_df3 = state_df2[['State','ListedPrice','RentalYield']].sort_values('ListedPrice', ascending=False)
max_price = state_df3['ListedPrice'].max()

st.dataframe(
	state_df3,
	hide_index=True,
	use_container_width=True,
	column_config={
		'ListedPrice': st.column_config.ProgressColumn(
				'Average House Price',
				format='$%d',
				min_value=0,
				max_value=max_price,
			)

		}

	)






