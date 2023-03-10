import pandas as pd
import utils

from collections import defaultdict

from dash import Dash, dcc, html, Input, Output
import plotly.express as px

app = Dash(__name__)

app.layout = html.Div(className="g1_container", children=[
    html.H1("Graph 4", className="g_h1 g4_h1"),
    html.P(children=["Market: "], style={"color":"#ffffff", "margin": "10px"}),
    dcc.Dropdown(id="dropdown", className="dropdown", options=[{'label': 'TSX', 'value': 'TSX'}, {'label': 'Aequitas', 'value': 'Aequitas'}, {
                 'label': 'Alpha', 'value': 'Alpha'}], value='TSX', style={'width':'220px', "margin-bottom": "20px"}),
    html.Div(className="radio_div", children=[
        dcc.RadioItems(
        id = "radio",
        className="radio",
        options=[
            {'label': 'New Order Request', 'value': 'NOR'},
            {'label': 'Orders Filled', 'value': 'OF'}
        ],
        value='NOR'
)]),
html.Br(),
    html.Div(className="graph_container", children=[dcc.Graph(id="time-volume-price-graph", figure={})])
])

@app.callback(
    Output("time-volume-price-graph", "figure"),
    [Input("radio", "value"), Input("dropdown", "value")]
)
def update_graph(radio_value, dropdown_value):
    if radio_value == 'NOR':
        obj = utils.load_json(dropdown_value + "Data.json" )
        num_intervals = 100

        end = utils.END_EPOCH/(10**9)
        start = utils.START_EPOCH/10**9
        diff = (end - start) / num_intervals

        df = pd.DataFrame(columns=["Interval", "Price", "Number of Orders"])
        intervals = []
        volume = defaultdict(int)
        prices = defaultdict(list)

        for i in range(1, num_intervals + 1):
            interval = str(start + i * diff)
            intervals.append(interval)

        for i in range(len(obj)):
            if obj[i]["MessageType"] == "NewOrderRequest":
                for j in intervals:
                    epoch_timestamp = int(obj[i]["TimeStampEpoch"]) / 10**9
                    if epoch_timestamp < float(j):
                        volume[j] += 1
                        prices[j].append(obj[i]["OrderPrice"])

                        break

        avg_prices = defaultdict(float)
        for i in prices:
            avg_prices[i] = sum(prices[i]) / len(prices[i])

        for i in intervals:
            price = avg_prices[i]
            num_orders = volume[i]
            date_obj = utils.epoch_seconds_to_datetime(int(float(i))).strftime("%H:%M:%S")
            new_row = pd.DataFrame(
                {"Interval": [date_obj], "Price": [price], "Number of Orders": [num_orders]})
            df = pd.concat([new_row, df.loc[:]]).reset_index(drop=True)
        fig = px.scatter_3d(df, x='Interval', y='Price', z='Number of Orders', height=750, width=750, opacity=0.7, title="Order volume and price evolution", template="plotly_dark")
        fig.update_layout(title_font_color="#4e4e4e"),
        return fig
    elif radio_value == 'OF':
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
        fig = px.scatter_3d(df, x='Interval', y='Price', z='Order Filled', opacity=0.7, title="Order volume and price evolution", template="plotly_dark")
        fig.update_layout(title_font_color="#4e4e4e"),
        return fig


if __name__ == "__main__":
    pass
    #app.run_server(debug=True)
