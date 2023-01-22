import json 
from dash import dcc, html, dash
from dash.dependencies import Input, Output
import plotly.express as px
from utils import *




# --- DATA EXTRACTION ---

timestamp, symbol, price, market = [], [], [], []

def parseFile(path: str) -> None:
    f = open(path)
    data = json.load(f)
    for i in data:
        if i["MessageType"] == "NewOrderRequest":
            price.append(i["OrderPrice"])
            timestamp.append(i["TimeStampEpoch"])
            symbol.append(i["Symbol"])
            market.append(i["Exchange"])
    f.close()

parseFile("data/AequitasData.json")
parseFile("data/AlphaData.json")
parseFile("data/TSXData.json")



# --- DASH ---


def generateOptions():
    options = [{"label": "All", "value": "All"}]

    for k in set(symbol):
        options.append({"label": k, "value": k})
    return options

options = generateOptions()

    
g1 = dash.Dash(__name__)
g1.layout = html.Div(className="g1_container", children=[

    html.H1("Graph 1", className="g1_h1"),

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
                 style={'width':"300px", "background-color": "#D5D5D5"}
                 )]),
    html.Div(className="g1_label", children=[
        html.P(children=["Symbol: "], style={"color":"#ffffff", "margin": "10px"}),
        dcc.Dropdown(id="symbol_selected",
        className="dropdown",
                 options=options,
                 multi=False,
                 value="All",
                 style={'width':"300px", "background-color": "#D5D5D5"}
                 )]),
    

    html.Br(),
    html.Br(),

    dcc.Graph(id='graph1', figure={}, style={'height': '500px', "margin": "0px 30px 30px 30px"})

])



@g1.callback(
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
        fig = px.area(title="This stock is not traded in the selected market")
    else:
        fig = px.area(x=display_dt, y=copy2_price, title="Stock order requests over time",labels=dict(x="Time ", y="Price ($) "))


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


if (__name__ == "__main__"):
    g1.run_server(debug=True)
