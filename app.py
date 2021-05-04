# EXPAND STOCK SYMBOL INPUT TO PERMIT MULTIPLE STOCK SELECTION
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import yfinance as yf
from datetime import datetime
import pandas as pd
import os

app = dash.Dash()
server = app.server
nsdq = pd.read_csv('data/NASDAQcompanylist.csv')
nsdq.set_index('Symbol', inplace=True)
dropdown_list = []
for tic in nsdq.index:
    dropdown_list.append({'label':'{} {}'.format(tic,nsdq.loc[tic]['Name']), 'value':tic})

app.layout = html.Div([
    html.H1('Stock Ticker Dashboard'),
    html.Div([
        html.H3('Select stock symbols:', style={'paddingRight':'30px'}),
        dcc.Dropdown(
            id='ticker',
            options=dropdown_list,
            value=['AAPL'],
            multi=True
        )
    ], style={'display':'inline-block', 'verticalAlign':'top', 'width':'30%'}),
    html.Div([
        html.H3('Select a time range'),
        dcc.DatePickerRange(
            id='date_picker',
            min_date_allowed=datetime(2015, 1, 1),
            max_date_allowed=datetime.today(),
            start_date=datetime(2018, 1, 1),
            end_date=datetime.today()
        )
    ], style={'display':'inline-block'}),
    html.Div([
        html.Button(
            id='submit-button',
            n_clicks=0,
            children='Update the graph',
            style={'fontSize':24, 'marginLeft':'30px'}
        ),
    ], style={'display':'inline-block'}),
    dcc.Graph(
        id='stock_graph',
        figure={
            'data': [
                {'x': [1,2], 'y': [3,1]}
            ]
        }
    )
])

@app.callback(
    Output('stock_graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [
        State('ticker', 'value'),
        State('date_picker', 'start_date'),
        State('date_picker', 'end_date')
    ]
    )
def update_graph(n_clicks, stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    traces = []
    for tic in stock_ticker:
        stock = yf.Ticker(tic)
        df = stock.history(start=start,end=end)
        traces.append({'x':df.index, 'y': df['Close'], 'name':tic})
    fig = {
        'data': traces,
        'layout': {'title':', '.join(stock_ticker)+' Closing Prices'}
    }
    return fig

if __name__ == '__main__':
    app.run_server()
