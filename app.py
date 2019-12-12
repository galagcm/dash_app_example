#!/usr/bin/env python
# coding: utf-8

# In[17]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output


app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

gdp = pd.read_csv('nama_10_gdp_1_Data.csv')
gdp['Value'] = gdp['Value'].str.replace('.', '')
gdp['Value'] = gdp['Value'].str.replace(',', '.')
gdp['Value'] = pd.to_numeric(gdp['Value'], errors='coerce')
gdp = gdp.dropna()

available_indicators = gdp['NA_ITEM'].unique()
units = gdp['UNIT'].unique()
country = gdp['GEO'].unique()
years = gdp['TIME'].unique()

app.layout = html.Div([
    html.H1('Dashboard: Eurostat, gdp and main components'),
    html.H2('First Graph'),
    html.Div('The first graph is a scatterplot with two DropDown boxes for the different indicators. It has also a slide for the different years in the data.'),
    html.Div([
        html.Hr(),
        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value= available_indicators[0]
            ),
            html.Hr(),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            ),
            html.Hr(),
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value= available_indicators[0]
            ),
            html.Hr(),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            ),
            html.Hr(),

        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
        
        dcc.Dropdown(id = "units", options = [{"label" : i, "value": i} for i in units],
                                                 style = {"marginTop" : "1.5em", 'text-align': 'justify'}, value = units[0], 
                                                ),
        html.Hr(),
    
    ]),
    
    

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='year--slider',
        min=gdp['TIME'].min(),
        max=gdp['TIME'].max(),
        value=gdp['TIME'].max(),
        step=None,
        marks={str(time): str(time) for time in gdp['TIME'].unique()}
    ),
    
    html.Br(),
    html.Br(),
    html.Br(),
    html.H2('Second Graph'),
    html.Div('The second graph will be a line chart with two DropDown boxes, one for the country and the other for selecting one of the indicators.'),
    html.Hr(),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='country-dropdown',
                options = [{'label': i, 'value': i} for i in country],
                value= 'European Union - 28 countries'),
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='indicators-dropdown',
                options = [{'label': i, 'value': i} for i in available_indicators],
                value= 'Gross domestic product at market prices'),
            
        ],
        style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
        
        dcc.RadioItems(
            id='yaxis-type2',
            options=[{'label': i, 'value': i} for i in units],
            style = {"marginTop" : "1.5em", 'text-align': 'justify'},
            value= units[0],
            labelStyle={'display': 'inline-block', 'margin-right': 20}),
        
    ]),
    html.Hr(),
    html.Br(),
    html.Br(),
    dcc.Graph(id='country-graphic'),
])


@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('units', 'value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type, units,
                 year_value):
    gdpf = gdp[gdp['TIME'] == year_value]
    gdpf = gdpf[gdpf['UNIT'] == units]
    
   
    
    return {
        'data': [go.Scatter(
            x=gdpf[gdpf['NA_ITEM'] == xaxis_column_name]['Value'],
            y=gdpf[gdpf['NA_ITEM'] == yaxis_column_name]['Value'],
            text=gdpf[gdpf['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 60, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('country-graphic', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value'),
     dash.dependencies.Input('indicators-dropdown', 'value'),
     dash.dependencies.Input('yaxis-type2', 'value')])
def update_graph2(country_dropdown, indicators_dropdown, yaxis_type2):
    gdpf2 = gdp[gdp['GEO'] == country_dropdown]
    gdpf2 = gdpf2[gdpf2['NA_ITEM'] == indicators_dropdown]
    gdpf2 = gdpf2[gdpf2['UNIT'] == yaxis_type2]
   
    
    return {
        'data': [go.Scatter(
            x=gdpf2['TIME'],
            y=gdpf2['Value'],
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': country_dropdown
            },
            yaxis={
                'title': indicators_dropdown,
                'type': 'linear' if yaxis_type2 == 'Linear' else 'log'
            },
            margin={'l': 60, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }
  

if __name__ == '__main__':
    app.run_server()



# In[ ]:




