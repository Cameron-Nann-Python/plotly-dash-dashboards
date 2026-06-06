import yfinance as yf
import pandas as pd

import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc

import plotly.express as px

# Ticker 
meta = yf.Ticker("META")
nvda = yf.Ticker("NVDA")
msft = yf.Ticker("MSFT")
ibm = yf.Ticker("IBM")

# Stock DataFrames
meta_data = meta.history(start='2020-01-01', end='2020-12-31').reset_index()
nvda_data = nvda.history(start='2020-01-01', end='2020-12-31').reset_index()
msft_data = msft.history(start='2020-01-01', end='2020-12-31').reset_index()
ibm_data = ibm.history(start='2020-01-01', end='2020-12-31').reset_index()

# Add a column for stock name
meta_data.insert(loc=1, column='Name', value='META')
nvda_data.insert(loc=1, column='Name', value='NVDA')
msft_data.insert(loc=1, column='Name', value='MSFT')
ibm_data.insert(loc=1, column='Name', value='IBM')

# Create consolidated DataFrame
stock_df = pd.concat([meta_data, nvda_data, msft_data, ibm_data]).sort_values(by="Date")

# Instantiate app
app = dash.Dash(
    __name__,
    # Get Bootstrap themes
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    # Allow app to work for mobile
    meta_tags=[{'name':'viewport', 'content': 'width=device-width, initial-scale=1.0'}]
    )

# Drawing modes
drawing_modes = ['drawline','drawopenpath','drawclosedpath','drawcircle','eraseshape']

# App layout
app.layout = dbc.Container([
    dbc.Row([
        # Dashboard title
        dbc.Col(html.H1('Tech Company Stock Dashboard',
                        style={'textAlign':'center','color':'blue', 'padding':'10px'}),
                        width=12)
    ]),

    dbc.Row([ 
        dbc.Col([
           # Stock name dropdown 
            dcc.Dropdown(
                id='ind-stock-name', 
                multi=False, 
                value='IBM',
                options=[
                    {'label':x, 'value':x} 
                    for x in sorted(stock_df['Name'].unique())
                    ]
                ),

            # Individual stock price graph
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(
                        id='ind-stock-price',
                        figure={},
                        config={'modeBarButtonsToAdd':drawing_modes}
                        )
                ])
            ], class_name='mb-4')              
           # Change width according to device
        ], xs=12, sm=6, md=6, lg=5, xl=5),

        dbc.Col([
            # Multi-select name dropdown
            dcc.Dropdown(
                id='mul-stock-name', 
                multi=True, 
                value=['IBM', 'NVDA'],
                options=[
                    {'label':x, 'value':x}
                    for x in sorted(stock_df['Name'].unique())
                    ]
                ),

            # Multiple stock price graph
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(
                        id='mul-stock-price',
                        figure={},
                        config={'modeBarButtonsToAdd':drawing_modes}
                        )
                ])
            ], class_name='mb-4')
            
        ], xs=12, sm=6, md=6, lg=5, xl=5)
    ]),

    dbc.Row([
        dbc.Col([
            # Stock name dropdown title
            html.P(
                'Select Company Stock: ', 
                style={'textDecoration':'underline'}
                ),

            # Stock name dropdown
            dcc.Checklist(
                id='check-stock-name', 
                value=sorted(stock_df['Name'].unique()),
                options=[
                    {'label':x, 'value':x}
                    for x in sorted(stock_df['Name'].unique())],
                    inline=True,
                    labelStyle={'color':'green'}
                ),
            
            # Stock close graph
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(
                        id='stock-sum-close',
                        figure={},
                        config={'modeBarButtonsToAdd':drawing_modes}
                        )
                ])
            ], class_name='mb-4')
            
        ], xs=12, sm=6, md=6, lg=5, xl=5),

        dbc.Col([
            # RAM card image
            dbc.Card([
                dbc.CardBody(
                    html.P(
                        "These are pretty expensive now!",
                        className="card-text"
                    )
                ),
                # Insert image
                dbc.CardImg(
                    src='assets/ram.jpg',
                    bottom=True
                )
            ], class_name='mb-4')

        ],xs=12, sm=6, md=6, lg=5, xl=5)
    ], align='center')

], fluid=True)

@app.callback(
    [Output(component_id='ind-stock-price', component_property='figure'),
     Output(component_id='mul-stock-price', component_property='figure'),
     Output(component_id='stock-sum-close', component_property='figure')],
    [Input(component_id='ind-stock-name', component_property='value'),
     Input(component_id='mul-stock-name', component_property='value'),
     Input(component_id='check-stock-name', component_property='value')]
)

def graph_stocks(company_name, company_list, check_list):
    """
    Returns a graph of stock data based on company
        Parameters:
            company_name (str): company name for stock
        Returns:
            ind_stock_fig (Figure): plotly graph
    """
    # Get df of company stock
    df_ind = stock_df[stock_df['Name'] == company_name]

    # Get df of multiple company stocks
    df_mul = stock_df[stock_df['Name'].isin(company_list)]
    df_check = stock_df[stock_df['Name'].isin(check_list)]

    ### Individual Stock Name Graph
    
    # Make a line chart of high over time
    ind_price = px.line(
        df_ind,
        x='Date',
        y='High',
        title=f'High Price for {company_name}'
        )
    
    ### Multiple Stock Name Graph
    mul_price = px.line(
        df_mul,
        x='Date',
        y='High',
        color='Name',
        title='High Price for Tech Companies'
    )

    ### Multiple Stock Volume Bar Graph

    # Make a grouped data frame for closing price by name 
    df_close = df_check.groupby(['Name'])['Close'].sum().reset_index()

    mul_close = px.bar(
        df_close,
        x='Name',
        y='Close',
        title='Sum of Close'
    )
    
    return[ind_price, mul_price, mul_close]

# Run app
if __name__ == '__main__':
    app.run()