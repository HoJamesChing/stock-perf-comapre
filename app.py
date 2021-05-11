# EXPAND STOCK SYMBOL INPUT TO PERMIT MULTIPLE STOCK SELECTION
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import yfinance as yf
from datetime import datetime
import pandas as pd
import os
from stocker import Stocker
import base64
import matplotlib.pyplot as plt
from io import BytesIO

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
    ),
    html.Div([
        html.H1('Prediction'),
        html.H3('Select a stock')
    ]),
    html.Div(
        [
            dcc.Dropdown(
            id='pred-ticker',
            options=dropdown_list,
            value=['AAPL'],
            multi = False
        )
        ],
        style={'width':'30%','verticalAlign':'top','display':'inline-block'}
    ),
    html.Div([
        html.Button(
            id='pred-submit-button',
            n_clicks=0,
            children='See the prediction',
            style={'fontSize':18, 'marginLeft':'30px'}
        ),
    ], style={'display':'inline-block'}),
    html.Div([
        html.Img(
                id='stock-pred-img',
                src=''
            )
    ])
])

# The callback function that generates the original stock line graph
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

# Encode the matplotlib figure to html image
def fig_to_uri(in_fig, close_all=True, **save_args):
    # type: (plt.Figure) -> str
    """
    Save a figure as a URI
    :param in_fig:
    :return:
    """
    out_img = BytesIO()
    in_fig.savefig(out_img, format='png', **save_args)
    if close_all:
        in_fig.clf()
        plt.close('all')
    out_img.seek(0)  # rewind file
    encoded = base64.b64encode(out_img.read()).decode("ascii").replace("\n", "")
    return "data:image/png;base64,{}".format(encoded)

# The callback function that predicts tomorrow's close price of the chosen stock
@app.callback(
    Output('stock-pred-img','src'),
    [Input('pred-submit-button','n_clicks')],
    [State('pred-ticker','value')]
)
def predict_stock_price_fig(n_clicks,stock_ticker):
    stockNo = stock_ticker
    ticker = yf.Ticker(stockNo)
    df = ticker.history(period='max')
    df = df.reset_index()
    stock = Stocker(stockNo,df)
    future, fig = stock.create_prophet_model(days=1)
    pred = round(future.loc[future.index[-1], 'yhat'],2)
    out_url = fig_to_uri(fig) 
    return out_url 



# The callback function that generates the forecast graph of the chosen stock
# @app.callback(
#     Output('stock-pred','children'),
#     [Input('pred-submit-button','n_clicks')],
#     [State('pred-ticker','value')]
# )
# def predict_stock_price(n_clicks,stock_ticker):
#     stockNo = stock_ticker
#     ticker = yf.Ticker(stockNo)
#     df = ticker.history(period='max')
#     df = df.reset_index()
#     stock = Stocker(stockNo,df)
#     future, fig = stock.create_prophet_model(days=1)
#     pred = round(future.loc[future.index[-1], 'yhat'],2)
#     return f"Tomorrow's close price of {stockNo} is predicted as {pred}"

if __name__ == '__main__':
    app.run_server()
