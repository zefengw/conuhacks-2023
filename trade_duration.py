import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd

import os
import json

from collections import defaultdict

import datetime
import time

from decimal import Decimal


from utils import timestamp_to_datetime, datetime_to_epoch, epoch_to_datetime, load_json, START_EPOCH, END_EPOCH


# time interval vs trade fill/cancel duration vs price



def generate_duration_graph_df(exchange: str, num_intervals: int, request_type: str):


# beginning time of each time interval
#order_timestamps = []

# corresponding order ids
#order_ids = []


# trade only
#order_durations = []

    diff = (END_EPOCH - START_EPOCH) / (10**9)
    dt = diff / num_intervals

    interval_timestamps = []
    durations = set()

    num_orders = defaultdict(int)


    # right hand side
    for i in range(1, num_intervals + 1):
        interval_timestamps.append(START_EPOCH/(10**9) + i * dt)



    df = pd.DataFrame(columns=["Order Time", "Response Time", "Number of Orders"])

    data_by_order_id = load_json(f"{exchange}DataByOrderID.json")

    data = load_json(f"{exchange}Data.json")

    interval_index = 0

    for i in range(len(data)):
        original_msg = data[i]

        timestamp = int(original_msg["TimeStampEpoch"]) / 10**9


        if timestamp < interval_timestamps[interval_index]:
            msg_type = original_msg["MessageType"]
            

            if msg_type == f"{request_type}Request":
                order_id = original_msg["OrderID"]
                start_time = original_msg["TimeStampEpoch"]
                for msg in data_by_order_id[order_id]:
                    if msg["MessageType"] == f"{request_type}Acknowledged" or msg["MessageType"] == "Trade" or msg["MessageType"] == "Cancelled":
                        
                        start_time = original_msg["TimeStampEpoch"]
                        end_time = msg["TimeStampEpoch"]
                        duration = (int(end_time) - int(start_time)) / 1000000000
                        
                        #symbol = msg["Symbol"]

                        durations.add(int(duration*500)/500)

                        num_orders[(interval_timestamps[interval_index], int(duration*500)/500)] += 1



                        #new_row = pd.DataFrame({"orderID": [order_id], "orderDuration": [duration], "orderTimestamp": [epoch_to_datetime(interval_timestamps[interval_index])], "Symbol": [msg["Symbol"]], "Exchange": [msg["Exchange"]]})
                        #df = pd.concat([new_row, df.loc[:]]).reset_index(drop=True)
                        break

        else:
            while timestamp >= interval_timestamps[interval_index]:
                interval_index += 1

            msg_type = original_msg["MessageType"]
            

            if msg_type == f"{request_type}Request":
                order_id = original_msg["OrderID"]
                start_time = original_msg["TimeStampEpoch"]
                for msg in data_by_order_id[order_id]:
                    if msg["MessageType"] == f"{request_type}Acknowledged" or msg["MessageType"] == "Trade" or msg["MessageType"] == "Cancelled":
                        
                        start_time = original_msg["TimeStampEpoch"]
                        end_time = msg["TimeStampEpoch"]
                        duration = (int(end_time) - int(start_time)) / 1000000000
                        
                        #symbol = msg["Symbol"]
                        durations.add(int(duration*500)/500)

                        num_orders[(interval_timestamps[interval_index], int(duration*500)/500)] += 1



                        #new_row = pd.DataFrame({"orderID": [order_id], "orderDuration": [duration], "orderTimestamp": [epoch_to_datetime(interval_timestamps[interval_index])], "Symbol": [msg["Symbol"]], "Exchange": [msg["Exchange"]]})
                        #df = pd.concat([new_row, df.loc[:]]).reset_index(drop=True)
                        break

    for i in range(len(interval_timestamps)):
        for j in durations:

            new_row = pd.DataFrame({"Order Time": [epoch_to_datetime(interval_timestamps[i]*1000000000)], "Response Time": [j], "Number of Orders": [num_orders[(interval_timestamps[i], j)]]})

            df = pd.concat([new_row, df.loc[:]]).reset_index(drop=True)


    #print(df)

    
    return df

    """
    for order_id in data_by_order_id:
        start_time, end_time = "", ""

        for msg in data_by_order_id[order_id]:

            if msg["MessageType"] == f"{request_type}Request":
                start_time = msg["TimeStampEpoch"]
                start_time_string = msg["TimeStamp"]
                
            elif msg["MessageType"] == f"{request_type}Acknowledged":

                
                #order_ids.append(order_id)
                end_time = msg["TimeStampEpoch"]

        print(start_time, end_time)

        if start_time and end_time:

            duration = (int(end_time) - int(start_time)) / 1000000000
                #order_durations.append(duration)
                #order_timestamps.append(timestamp_to_datetime(order_request_msg["TimeStamp"]))

            new_row = pd.DataFrame({"orderID": [order_id], "orderDuration": [duration], "orderTimestamp": [timestamp_to_datetime(start_time_string)], "Symbol": [msg["Symbol"]], "Exchange": [msg["Exchange"]]})
            df = pd.concat([new_row, df.loc[:]]).reset_index(drop=True)

        """


app = dash.Dash()


app.layout = html.Div(className="g1_container", children=[
    html.H1("Graph 3", className="g_h1 g3_h1"),
    html.P(children=["Market: "], style={"color":"#ffffff", "margin": "10px"}),
    dcc.Dropdown(["TSX", "Aequitas", "Alpha"], "Alpha", id='exchange-dropdown-menu', style={"width": "220px"}),
    html.Br(),
    html.P(children=["Transaction type: "], style={"color":"#ffffff", "margin": "10px"}),
    html.Div(className="radio_div", children=[
    dcc.RadioItems(options=[
        {"label": "    New Order Requests", "value": "NewOrder"},
        {"label": "    Cancel Requests", "value": "Cancel"}
        ],
        className="radio",
        value="NewOrder",
        id='request-type'
        )]),

    html.Br(),
    html.Br(),
    dcc.Graph(id="duration-graph"),

    dcc.Slider(10, 500, value=10, id="num-intervals-slider"),

])



@app.callback(
    Output('duration-graph', 'figure'),
    Input('num-intervals-slider', 'value'),
    Input('exchange-dropdown-menu', 'value'),
    Input('request-type', 'value')
)
def display_selected_intervals(selected_intervals, selected_exchange, request_type):

    


    df = generate_duration_graph_df(selected_exchange, selected_intervals, request_type)

    fig = go.Figure(data=go.Heatmap(
        z=df["Number of Orders"],
        x=df["Order Time"],
        y=df["Response Time"],
        colorscale='RdBu_r'))
    
    fig.update_layout(paper_bgcolor="#303030",
    title="Distribution of average request completion times",
    xaxis_title="Time",
    yaxis_title="Request completion time",
    plot_bgcolor="#303030",
    font_color="#919191",
    margin_pad=30,
    )


    #fig = px.scatter(df, x="orderTimestamp", y="orderDuration", color="Symbol", hover_name="Symbol")


    return fig






#if (__name__ == "__main__"):
    #app.run_server(debug=True)




