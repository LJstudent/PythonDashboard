import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import plotly.graph_objs as go
import pandas as pd
import downloadFile as db

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H3(children='Hello Dash'),

    dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'Microsoft', 'value': 'MSFT'},
            {'label': 'Apple', 'value': 'AAPL'}
        ],
        value='AAPL'
    ),
    html.Br(),

    html.Div(id='dd-output-container'),

    html.Div(id='Company-info'),


    dcc.Graph(id='stock-graph'),

    html.Div(id='Company-financials')

])


@app.callback(
    [Output(component_id='stock-graph', component_property='figure'),
     Output(component_id='Company-info', component_property='children'),
     Output(component_id='Company-financials', component_property='children')],
    [Input(component_id='demo-dropdown', component_property='value')]
)
def update_output_div(input_value):
    df = db.yahoo_download(input_value)
    companyInfo = db.profile_download(input_value)
    dividend = db.dividend_download(input_value)
    companyFinancial = db.financial_statements(input_value)


    company = html.Div([
        'Company name: {}'.format(companyInfo['companyName']),
        html.Br(),
        'Sector: {}'.format(companyInfo['sector']), '({})'.format(companyInfo['industry']),
        html.Br(),
        '52w range: {}'.format(companyInfo['range']),
        html.Br(),
        'Dividend {}'.format(dividend.get('dividend')),
        ' 5year {}'.format(dividend.get('5year'))
    ])

    GraphData = {'data': [
                go.Scatter(
                    x = df.index,
                    y = df['Close'],
                    mode = 'lines'
                )
            ],
            'layout': {
                'title': 'stock data'
            }
    }

    financial = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in companyFinancial.columns],
        data=companyFinancial.to_dict('records'),
    )

    return GraphData, company, financial



if __name__ == '__main__':
    app.run_server(debug=True)