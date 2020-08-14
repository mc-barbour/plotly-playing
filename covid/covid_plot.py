import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from state_names import *

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

"""
Script to plot clortpleth math of covid-19 cases. 

Pulling data from Johns Hopkins Database. 

Eventually want to make this a time-series 

"""


#-------------------------------------------------------
# Load and Clean Data
daily_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/08-12-2020.csv'

df_daily = pd.read_csv(daily_url,delimiter=',')
print(df_daily.head(5))

df_daily = df_daily.drop(df_daily[df_daily['FIPS'] > 60.0].index)

abbrev_state_names=us_state_abbrev(df_daily['Province_State'])
df_daily["State_Abberviated"] = abbrev_state_names

#---------------------------------------------------------


metrics=['Confirmed','Deaths','Recocvered','Active','FIPS','Incident_Rate','People_Tested',
'People_Hospitalized','Mortality_Rate','UID','Testing_Rate','Hospitalization_Rate']

metric='Mortality_Rate'

fig=px.choropleth(
		data_frame=df_daily,
		locationmode='USA-states',
		locations='State_Abberviated',
		scope="usa",
		color=metric,
		color_continuous_scale=px.colors.sequential.Viridis,
		hover_data=['Confirmed','Deaths','Recovered','Active'],
		template='plotly_white',
		title=metric

)

fig.show()