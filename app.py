import dash
from dash import html, dcc, Output, Input
import plotly.graph_objects as go
import plotly.express as px

from utils import *
import pandas as pd

from trade_duration import generate_duration_graph_df

from g1 import generateOptions, price, timestamp, symbol, remove_outliers


app = dash.Dash()

app.layout = html.Div(className="g1_container", children=[

    html.Div(className="hero", style={"height":"90vh"}, children=[
        html.Img(src="assets/logo2.png", className="logo"),
        html.H2("Visualization deriving crucial trading insights", style={"color": "#CBCBCB", "padding-top": "15px", "font-size":"23px","transform":"translateY(-75px)"})

    ]),
 html.Div(style={"height":"10vh"}),
  html.Div(style={"height":"10vh"}),

    # Graph 1
    html.H1("Graph 1", className="g_h1 g1_h1"),

    html.Div(className="g1_label", children=[
        html.P(children=["Market: "], style={"color":"#ffffff", "margin": "10px"}),
        dcc.Dropdown(id="market_selected",
        className="dropdown",
                 options=[
                    {"label": "Aequitas", "value": "Aequitas"},
                    {"label": "Alpha", "value": "Alpha"},
                     {"label": "TSX", "value": "TSX"}
                     ],
                 multi=False,
                 value="Aequitas",
                 style={'width':"200px", "background-color": "#D5D5D5"}
                 )]),
    html.Div(className="g1_label", children=[
        html.P(children=["Symbol: "], style={"color":"#ffffff", "margin": "10px"}),
        dcc.Dropdown(id="symbol_selected",
        className="dropdown",
                 options=generateOptions(),
                 multi=False,
                 value="All",
                 style={'width':"200px", "background-color": "#D5D5D5"}
                 )]),
    

    html.Br(),
    html.Br(),

    dcc.Graph(id='graph1', figure={}, style={'height': '500px', "margin": "0px 30px 30px 30px"}),


    html.Div(style={"height":"11vh"}),


    html.Div(className="parralax", style={"height":"85vh"}, children=[
        html.H4("Price evolution for given trade symbols can be analyzed with Graph 1. Since price evolution over small time intervals tends to follow continuous trends, these plots allow the detection of anomalies in the trading data. With continuous live data, this graph has the potential to be used to train predictive models for anomaly detection.", className="parralax_text")
    ]),
    html.Div(style={"height":"10vh"}),


    # Graph 2

    html.H1("Graph 2", className="g_h1 g2_h1"),
    html.P(children=["Market: "], style={"color":"#ffffff", "margin": "10px"}),
    dcc.Dropdown(id='market_selected',
      className="dropdown",
                options=[
                    {'label': 'Aequitas', 'value': 'Aequitas'},
                    {'label': 'Alpha', 'value': 'Alpha'},
                    {'label': 'TSX', 'value': 'TSX'}],
                multi=False,
                value='Aequitas',
                style={
                    'width':'220px'
                }),
                html.P(children=["Message type: "], style={"color":"#ffffff", "margin": "35px 0px 20px 10px"}),

    # Don't know if we'll need all types of messages. Can change later.
    html.Div(className="radio_div", children=[
    dcc.RadioItems(id='message_selected',
                className="radio",
                options=[
                    {'label': '   NewOrderRequest', 'value': 'NewOrderRequest'},
                    {'label': '   NewOrderAcknowledged', 'value': 'NewOrderAcknowledged'},
                    {'label': '   CancelRequest', 'value': 'CancelRequest'},
                    {'label': '   Cancel', 'value': 'Cancel'},
                    {'label': '   Trade', 'value': 'Trade'}],
                    value='Trade')]),

    dcc.Input(id='top_x', className="inputt", type='number', min=0, placeholder='# of Symbols'),
    html.Br(),
    html.Br(),
    html.Br(),
    dcc.Graph(
        id='stock_distribution',
        figure={}
    ),

    html.Div(style={"height":"11vh"}),

    html.Div(className="parralax", style={"height":"85vh"}, children=[
        html.H4("Graph 2, in the form of a tree map, demonstrates the distribution of traded symbols in a given market. Allowing for at-a-glance comparisons, graph 2 can provide insight on the user portfolio efficiently and effectively.", className="parralax_text")
    ]),
    html.Div(style={"height":"14vh"}),

    # Graph 3


    html.H1("Graph 3", className="g_h1 g3_h1"),
    html.P(children=["Market: "], style={"color":"#ffffff", "margin": "10px"}),
    dcc.Dropdown(["TSX", "Aequitas", "Alpha"], "Aequitas", id='exchange-dropdown-menu', style={"width": "220px"}, className="dropdown", ),
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

    html.Div(style={"height":"11vh"}),


    html.Div(className="parralax", style={"height":"85vh"}, children=[
        html.H4("Graph 3 shows aggregate data in the form of a heatmap to represent the distribution of order completion over the 4 minute period from 9:28:00 to 9:32:00. Order completion time peaks around 9:30:00 for all 3 exchanges, which corresponds to the peak in order requests at market opening.", className="parralax_text")
    ]),
    html.Div(style={"height":"16vh"}),

    # Graph 4

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
        )
    ]),
    html.Br(),
    html.Div(className="graph_container", children=[dcc.Graph(id="time-volume-price-graph", figure={})]),

    html.Div(className="parralax", style={"height":"85vh"}, children=[
        html.H4("Graph 4 shows the relationship between the number of orders and prices in smaller time intervals between 9:28:00 and 9:32:00. The number of orders tends to increase as the price of stock options decrease in relation to its respective time interval.", className="parralax_text")
    ]),

])


# Graph 1 callbacks
@app.callback(
    Output(component_id='graph1', component_property='figure'),
    [Input(component_id='market_selected', component_property='value'), Input(component_id='symbol_selected', component_property='value')]
)
def update_graph(m_selected, s_selected):
    #dff = dff[dff["Year"] == span_selected]
    #dff = dff[dff["Affected by"] == "Varroa_mites"]

    # Plotly Express
    match m_selected:
        case "Aequitas":
            i, j = 0, 3917
        case "Alpha":
            i, j = 3918, 3949
        case "TSX":
            i, j = 3950, 45900

# Aequitas 0 - 3917
# Alpha 3918 - 3949
# TSX 3950 - 45900

    copy_price = price[i:j]
    copy_timestamp = timestamp[i:j]
    copy_symbol = symbol[i:j]
    copy2_price = []
    copy2_timestamp = []


    if s_selected != "All":
        for index, value in enumerate(copy_symbol):
            if value == s_selected:
                copy2_price.append(copy_price[index])
                copy2_timestamp.append(copy_timestamp[index])
    else:
        copy2_price = copy_price
        copy2_timestamp = copy_timestamp
        
    display_dt = []
    for k in copy2_timestamp:
        display_dt.append(epoch_to_datetime(int(k)))

    if len(display_dt) == 0 or len(copy2_price) == 0:
        fig = px.area(title="This symbol is not traded in the selected market")
    else:

        processed_data = remove_outliers(display_dt, copy2_price)
        clean_df = processed_data[0]
        outliers_df = processed_data[1]

        fig = px.area(x=clean_df["Time"], y=clean_df["Price"], title=f"Order requests over time for {s_selected}",labels=dict(x="Time ", y="Price ($) "))

        fig.add_scatter(x=outliers_df["Time"], y=outliers_df["Price"], showlegend=False, mode="markers")
        #fig.add_trace(px.scatter(outliers_df))


    fig.update_layout(paper_bgcolor="#303030",
    plot_bgcolor="#303030",
    font_color="#919191",
    margin_pad=30,
    )
    fig.layout.yaxis.gridcolor = "#4A4A4A"
    fig.layout.yaxis.dividercolor = "#4A4A4A"
    fig.layout.xaxis.gridcolor = "#4A4A4A"
    fig.layout.xaxis.gridcolor = "#4A4A4A"


    return fig



# Graph 2 callbacks

@app.callback(
    Output(component_id='stock_distribution', component_property='figure'),
    Input(component_id='market_selected', component_property='value'),
    Input(component_id='message_selected', component_property='value'),
    Input(component_id='top_x', component_property='value')
)
def generate_treemap(m_selected, message, top_x):
    if m_selected == 'Aequitas':
        with open('data/AequitasData.json') as f:
            data = json.load(f)
    elif m_selected == 'Alpha':
        with open('data/AlphaData.json') as f:
            data = json.load(f)
    elif m_selected == 'TSX':
        with open('data/TSXData.json') as f:
            data = json.load(f)
    
    # Create a dictionary of successful trades where the key is the symbol and the value is the count
    symbol_dict = {}

    for data_point in data:
        # Computing TRADED symbols
        if data_point['MessageType'] == message:

            # If the symbol is already in the dictionary, add to count
            symbol = data_point['Symbol']
            if symbol in symbol_dict.keys():
                symbol_dict[symbol] += 1

            # If symbol is not in the dict, set default to 1
            else:
                symbol_dict[symbol] = 1

    # Plotting the data into tree map
    if len(symbol_dict.keys()) == 0:
        fig = px.treemap(names=['No symbols available'], parents=[m_selected],
                        title='Distribution of Stocks by Market ({})'.format(message),
                        labels={
                            'names': 'Symbol',
                            'values': 'Traded',
                            'parents': 'Market'
                            })
    
    else:
        # Might want to add a note if top_x is larger than num of keys
        if top_x is not None and top_x <= len(symbol_dict.keys()):
            sorted_sym_dict = dict(sorted(symbol_dict.items(), key=lambda x:x[1], reverse=True))
            l = list(sorted_sym_dict.items())

            while len(l) != top_x:
                l.pop()
            
            sorted_sym_dict = dict(l)

            fig = px.treemap(names=sorted_sym_dict.keys(), parents=[m_selected] * top_x, values=sorted_sym_dict.values(), title='Distribution of Stocks by Market ({}, Top {} Symbols)'.format(message, top_x),
            labels={
                'names': 'Symbol',
                'values': 'Traded',
                'parents': 'Market'
                })

        else:
            fig = px.treemap(names=symbol_dict.keys(), parents=[m_selected] * len(symbol_dict.keys()), values=symbol_dict.values(), title='Distribution of Stocks by Market ({})'.format(message),
            labels={
                'names': 'Symbol',
                'values': 'Traded',
                'parents': 'Market'
                })
    fig.update_layout(paper_bgcolor="#303030",
    plot_bgcolor="#303030",
    font_color="#919191",
    margin_pad=10
    )
    return fig






# Graph 3 callbacks

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

    return fig




# Graph 4 callbacks

@app.callback(
    Output("time-volume-price-graph", "figure"),
    [Input("radio", "value"), Input("dropdown", "value")]
)
def update_graph(radio_value, dropdown_value):
    if radio_value == 'NOR':
        obj = load_json(dropdown_value + "Data.json" )
        num_intervals = 100

        end = END_EPOCH/(10**9)
        start = START_EPOCH/10**9
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
            date_obj = epoch_seconds_to_datetime(int(float(i))).strftime("%H:%M:%S")
            new_row = pd.DataFrame(
                {"Interval": [date_obj], "Price": [price], "Number of Orders": [num_orders]})
            df = pd.concat([new_row, df.loc[:]]).reset_index(drop=True)
        fig = px.scatter_3d(df, x='Interval', y='Price', z='Number of Orders', height=750, width=750, opacity=0.7, title="Order volume and price evolution", template="plotly_dark")
        fig.update_layout(title_font_color="#4e4e4e"),
        return fig
    elif radio_value == 'OF':
        obj = load_json(dropdown_value + "DataByOrderID.json" )
        num_intervals = 100

        end = END_EPOCH/(10**9)
        start = START_EPOCH/10**9
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
            date_obj = epoch_seconds_to_datetime(int(float(i))).strftime("%H:%M:%S")
            new_row = pd.DataFrame(
                {"Interval": [date_obj], "Price": [price], "Order Filled": [num_orders]})
            df = pd.concat([new_row, df.loc[:]]).reset_index(drop=True)
        fig = px.scatter_3d(df, x='Interval', y='Price', z='Order Filled', opacity=0.7, title="Order volume and price evolution", template="plotly_dark")
        fig.update_layout(title_font_color="#4e4e4e"),
        return fig


if __name__ == "__main__":
    app.run_server(debug=True)