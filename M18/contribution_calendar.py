import streamlit as st
import pandas as pd
import numpy as np
from plotly_calplot import calplot


st.write("## Calendar")


dates = pd.date_range("2026-01-01", "2026-12-31")

df = pd.DataFrame({
	"date":dates,
	"value":np.random.randint(0,10, len(dates))})

df.iloc[0:10, 1] = 10

st.write(df)

colorscales = [
    [0.0, "#ebedf0"],
    [0.25, "#9be9a8"],
    [0.5, "#40c463"],
    [0.75, "#30a14e"],
    [1.0, "#216e39"]
]

fig = calplot(
	df, 
	x="date",
	y="value",
	colorscale=colorscales,
	dark_theme=True
	)
fig.update_xaxes(visible=True)
fig.update_yaxes(visible=False)

fig.update_layout(
    margin=dict(l=0, r=0, t=10, b=0)
)

st.plotly_chart(fig, use_container_width=True)