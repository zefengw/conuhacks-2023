import pandas as pd
from dash import dcc, html, dash
from dash.dependencies import Input, Output
import plotly.express as px

# --- DATA EXTRACTION ---
import json 
timestamp, symbol, price, market = [], [], [], []

def parseFile(path):
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


g1 = dash.Dash()



g1.layout = html.Div([

    html.H1("Graph 1", style={}),

    dcc.Dropdown(id="span_selected",
                 options=[
                     {"label": "5 minutes", "value": 0},
                     {"label": "1 minute", "value": 1},
                     {"label": "30 seconds", "value": 2},
                     {"label": "15 seconds", "value": 3}],
                 multi=False,
                 value=0,
                 style={'width': "50%"}
                 ),
    dcc.Dropdown(id="market_selected",
                 options=[
                    {"label": "Aequitas", "value": "Aequitas"},
                    {"label": "Alpha", "value": "Alpha"},
                     {"label": "TSX", "value": "TSX"}
                     ],
                 multi=False,
                 value="Aequitas",
                 style={'width': "50%"}
                 ),

    html.Br(),
    html.Br(),

    dcc.Graph(id='graph1', figure={})

])



@g1.callback(
    Output(component_id='graph1', component_property='figure'),
    [Input(component_id='span_selected', component_property='value'), 
    Input(component_id='market_selected', component_property='value')]
)
def update_graph(s_selected, m_selected):
    
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
    copy_market = market[i:j]



    fig = px.line(x=copy_timestamp, y=copy_price)
    '''
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='Pct of Colonies Impacted',
        hover_data=['State', 'Pct of Colonies Impacted'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
        template='plotly_dark'
    )
    '''

    return fig

#print(timestamp)
#print(price)

if (__name__ == "__main__"):
    g1.run_server(debug=True)