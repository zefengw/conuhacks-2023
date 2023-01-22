import pandas as pd
import utils

from collections import defaultdict

from dash import Dash, dcc, html, Input, Output
import plotly.express as px

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Trade/Cancel Graph"),
    dcc.Graph(id="time-volume-price-graph"),
    dcc.Dropdown(id="dropdown", options=[{'label': 'TSX', 'value': 'TSX'}, {'label': 'Aequitas', 'value': 'Aequitas'}, {
                 'label': 'Alpha', 'value': 'Alpha'}], value='TSX'),
])

@app.callback(
    Output("time-volume-price-graph", "figure"),
    Input("dropdown", "value")
)
def update_graph(dropdown_value):
    obj = utils.load_json(dropdown_value + "DataByOrderID.json" )
    num_intervals = 100

    end = utils.END_EPOCH/(10**9)
    start = utils.START_EPOCH/10**9
    diff = (end - start) / num_intervals

    df = pd.DataFrame(columns=["Interval", "Price", "Order Filled"])
    intervals = []
    volume = defaultdict(int)
    prices = defaultdict(list)

    for i in range(1, num_intervals + 1):
        interval = str(start + i * diff)
        intervals.append(interval)

    for i in obj:
        for j in range(len(obj[i])):
            if obj[i][j]["MessageType"] == "Trade":
                for k in intervals:
                    epoch_timestamp = int(obj[i][j]["TimeStampEpoch"]) / 10**9
                    if epoch_timestamp < float(k):
                        volume[k] += 1
                        prices[k].append(obj[i][j]["OrderPrice"])
                        break

    avg_prices = defaultdict(float)
    for i in prices:
        avg_prices[i] = sum(prices[i]) / len(prices[i])

    for i in intervals:
        price = avg_prices[i]
        num_orders = volume[i]
        date_obj = utils.epoch_seconds_to_datetime(int(float(i))).strftime("%H:%M:%S")
        new_row = pd.DataFrame(
            {"Interval": [date_obj], "Price": [price], "Order Filled": [num_orders]})
        df = pd.concat([new_row, df.loc[:]]).reset_index(drop=True)
    fig = px.scatter_3d(df, x='Interval', y='Price', z='Order Filled', height=750, width=750)
    return fig


#if __name__ == "__main__":
#    app.run_server(debug=True)

