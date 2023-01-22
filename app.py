import pandas as pd
import utils

from collections import defaultdict

from dash import Dash, dcc, html, Input, Output
import plotly.express as px

obj = utils.load_json("TSXData.json")
num_intervals = 10

end = utils.END_EPOCH/(10**9)
start = utils.START_EPOCH/10**9
diff = (end - start) / num_intervals
# date_time = datetime.datetime.fromtimestamp(e_epoch)
# print("Converted Datetime:", date_time)
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
    obj = utils.epoch_seconds_to_datetime(int(float(i))).strftime("%H:%M:%S")
    new_row = pd.DataFrame(
        {"Interval": [obj], "Price": [price], "Number of Orders": [num_orders]})
    df = pd.concat([new_row, df.loc[:]]).reset_index(drop=True)

# 3. volume = len(df[df["MessageType"] == "NewOrderRequest"])
# start epoch (epoch at 09:28) / end epoch (epoch at 09:32), end - start / # of intervals = duration of intervals,
# epoch(start) + (end-beg/n),
# 4. store order ids
# find average prices by appending prices of certain key intervals (k1, k2...) and dividing by # of elements in that interval

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Time/Volume/Price Graph"),
    dcc.Graph(id="time-volume-price-graph"),
    # html.H3(id="time-volume-price-graph"),
    dcc.Dropdown(id="dropdown", options=[{'label': 'Total', 'value': 'Total'}, {'label': 'Trade', 'value': 'Trade'}, {
                 'label': 'Cancelled', 'value': 'Cancelled'}], value='Total'),
])


@app.callback(
    Output("time-volume-price-graph", "figure"),
    Input("dropdown", "value")
)
def update_graph(dropdown_value):

    fig = px.scatter_3d(df, x='Interval', y='Price', z='Number of Orders')
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)

obj.close()
