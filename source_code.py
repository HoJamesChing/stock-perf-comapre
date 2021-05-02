import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import pandas_datareader.data as web
#import yfinance as yf
from datetime import datetime
import numpy as np
import json
import os

app = dash.Dash()

df = pd.read_csv('data/NASDAQcompanylist.csv')
df.set_index('Symbol',inplace=True)

dropdown_list = []
for tick in df.index:
    dropdown_list.append({'label':f"{tick}: {df.loc[tick]['Name']}",'value':tick})

app.layout = html.Div([
    html.H1('Stock Ticker Dashboard'),
    html.Div([html.H3('Select a stock'),
                dcc.Dropdown(
                            id='ticker',
                            options=dropdown_list,
                            multi=True,
                            value='AAPL'
                        )
                ],style = {'width':'30%','display':'inline-block','verticalAlign':'top'}
            ),
    html.Div(
        [
            html.H3('Select a time span'),
            dcc.DatePickerRange(
                id='date-picker',
                min_date_allowed=datetime(2001,1,1),
                max_date_allowed=datetime.today(),
                start_date=datetime(2021,1,1),
                end_date=datetime.today()
            )
    ],
    style={'display':'inline-block'}
    ),
    html.Div([
        html.Button(
            id='submit-button',
            n_clicks=0,
            children='Update the graph',
            style={'fontSize':24, 'marginLeft':'30px'}
        )],
        style={'display':'inline-block'}
    ),
    html.Div(
        dcc.Graph(
            id='stock-graph',
            figure={
                'data':[{
                    'x':[1,2],'y':[3,1]
                }]
            }
        )
    )
])

token = os.environ.get('IEX_TOKEN')

@app.callback(
    Output('stock-graph','figure'),
    [Input('submit-button','n_clicks')],
    [
        State('ticker','value'),
        State('date-picker','start_date'),
        State('date-picker','end_date')
    ]
)
def update_graph(n_clicks, stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    traces = []
    for tic in stock_ticker:
        #ticker = yf.Ticker(stock_ticker)
        #df = ticker.history(start=start,end=end)
        df = web.DataReader(tic,'iex',start, end, api_key=token)
        traces.append({'x':df.index, 'y': df.close, 'name':tic})
    fig = {
        'data': traces,
        'layout': {'title':token}
    }
    return fig


if __name__=='__main__':
    app.run_server()