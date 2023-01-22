# This graph will show the distribution of stocks at a given time interval
# The impact is that the brokers will be able to see their portfolio at a glance 
# (both desired and actual)
 
import json
import plotly.express as px
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='ConUHacks VII'),

    dcc.Dropdown(id='market_selected',
                options=[
                    {'label': 'Aequitas', 'value': 'Aequitas'},
                    {'label': 'Alpha', 'value': 'Alpha'},
                    {'label': 'TSX', 'value': 'TSX'}],
                multi=False,
                value='Aequitas',
                style={
                    'background-color':'#283747',
                    'border-color':'white',
                    'width':'50%'
                }),

    # Don't know if we'll need all types of messages. Can change later.
    dcc.RadioItems(id='message_selected',
                options=[
                    {'label': 'NewOrderRequest', 'value': 'NewOrderRequest'},
                    {'label': 'NewOrderAcknowledged', 'value': 'NewOrderAcknowledged'},
                    {'label': 'CancelRequest', 'value': 'CancelRequest'},
                    {'label': 'Cancel', 'value': 'Cancel'},
                    {'label': 'Trade', 'value': 'Trade'}],
                    value='Trade'),

    dcc.Input(id='top_x', type='number', min=0, placeholder='Find top X symbols'),

    dcc.Graph(
        id='stock_distribution',
        figure={}
    )
], style={
    'background-color':'#283747'
})

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

    fig.update_traces(root_color="#6D8388")

    return fig
        
if __name__ == '__main__':
    app.run_server(debug=True)