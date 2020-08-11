import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

"""
This app ic copied from https://www.youtube.com/watch?v=hSPmj7mK6ng

The code is taken from https://github.com/Coding-with-Adam/Dash-by-Plotly/blob/master/Other/Dash_Introduction/intro.py

It is an introduction into dash web app creation

It covers the main components of a dash app: components, figure, callback

"""

app = dash.Dash(__name__)

#--------------------------------------
# First Step is import and clean the data

df = pd.read_csv("intro_bees.csv")
df = df.groupby(['State','ANSI','Affected by','Year','state_code'])[['Pct of Colonies Impacted']].mean()
print(df.head(5))

df.reset_index(inplace=True)

#--------------------------------------
# Create App layout: Div is the generic wrapper for the contents of the app: the components and figure
# Components either come from dcc or html
app.layout = html.Div([


	#html.H1(children="Web Appliction with Dash",style={'text-align':'center'}),
	# H1 is the highest level header in html

	dcc.Dropdown(id='select_year',
		options=[
			{"label": "2015", "value": 2015},
			{"label": "2016", "value": 2016},
			{"label": "2017", "value": 2017},
			{"label": "2018", "value": 2018}],
		multi=False,
		value=2015, # default value
		style={'width': "40%"}

		),

	html.Br(),

	dcc.Dropdown(id='select_death',
		options=[
			{"label": "Disease", "value": "Disease"},
			{"label": "Other", "value": "Other"},
			{"label": "Pesticides", "value": "Pesticides"},
			{"label": "Pests exclusing Varroa", "value": "Pests_excl_Varroa"},
			{"label": "Unknown", "value": "Unknown"},
			{"label": "Varroa Mites", "value": "Varroa_mites"}],
		multi=False,
		value="Disease",
		style={'width':'40%'}

		),


	html.Br(),
	html.Div(id='output_container_year',children=[]),
	html.Br(),
	html.Div(id='output_container_affect',children=[]),
	html.Br(),

	dcc.Graph(id='my_bee_map',figure={})

])


#-------------------------------------------------------------
# Connect the plotly graphs with Dash Components 

@app.callback(
	[Output(component_id='output_container_year',component_property='children'),
	 Output(component_id='output_container_affect',component_property='children'),
	 Output(component_id='my_bee_map',component_property='figure')],
	[Input(component_id='select_year',component_property='value'),
	Input(component_id='select_death',component_property='value')]
)

def update_graph(option_selected,death_selected):
	print(option_selected,death_selected)

	#text_continer feeds into the first div - will be the first item returned 
	text_container = "The year chosen by the user was: {}".format(option_selected)
	affect_container = "The method of colony death selected by user was: {}".format(death_selected)

	dff=df.copy()
	dff=dff[dff["Year"]==option_selected]
	dff=dff[dff["Affected by"]==death_selected]


	fig=px.choropleth(
		data_frame=dff,
		locationmode='USA-states',
		locations='state_code',
		scope="usa",
		color="Pct of Colonies Impacted",
		hover_data=['State','Pct of Colonies Impacted'],
		color_continuous_scale=px.colors.sequential.Viridis,
		labels={'Pct of Colonies Destroyed'},
		title='Percentage of colonies Destroyed',
		template='plotly_white'

	)

	fig.update_layout(title={	
        'x':0.85,
        'xanchor': 'center',
        'yanchor': 'top'})

	return text_container,affect_container,fig

#-------------------------------------------------------------
if __name__ == '__main__':
	app.run_server(debug=True)
