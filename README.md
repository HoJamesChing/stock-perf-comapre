This is a milestone project following an online course on udemy, with a little change of the data source API. It focuses on the funtionality rather than aesthetic design.



This dashboard enables you to select multiple stocks and desired time range, then returns the historical performance of each stock on the same graph.

The whole dashboard is written in python. The functional divisions are built with dash, whereas the graph is generated using plotly. And it is deployed on Heroku. You can visit the site [here](https://stock-perf-compare.herokuapp.com/).


### Steps to run locally (codes are for Linux and MacOS users)
Firstly, clone the repos to your local machine and cd to the directory.

Create a python virtual environment (requires python 3.6 or later)
```
python -m venv venv
```

Activate the virtual environment
```
source venv/bin/activate
```

Install the required packages
```
python -m pip install -r requirements.txt
```

Run the application. By default, dash will run on port 8050 (localhost:8050)
```
python app.py
```

### About the data source
The course uses pandas_datareader library to get stock data from IEX's API. However, IEX's API is now key required and only has very limited free access. I found the library provided by yahoo, yfinance, quite easy to use. You can find more information at [yfinance](https://pypi.org/project/yfinance/).


Reference: [Interactive Python Dashboards with Plotly and Dash](https://www.udemy.com/course/interactive-python-dashboards-with-plotly-and-dash/).
