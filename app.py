
# coding: utf-8

# In[4]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)
server = app.server


r = pd.read_csv('nama_10_gdp_1_Data.csv')

#clean countries values
countries_only = r[(r.GEO != 'European Union (current composition)')&(r.GEO != 'European Union (without United Kingdom)')&
   (r.GEO != 'European Union (15 countries)')&(r.GEO != 'Euro area (EA11-2000, EA12-2006, EA13-2007, EA15-2008, EA16-2010, EA17-2013, EA18-2014, EA19)')
   &(r.GEO != 'Euro area (19 countries)')&(r.GEO != 'Euro area (12 countries)')]
data = countries_only.replace({'GEO': {'Germany (until 1990 former territory of the FRG)': 'Germany', 'Former Yugoslav Republic of Macedonia, the': 'Macedonia',
                              'Kosovo (under United Nations Security Council Resolution 1244/99)':'Kososvo'}})

#clean units (only 1 unit left)
data = data[data['UNIT']=='Current prices, million euro']
#drop 'Flag and Footnotes'
cleaned_data = data.drop('Flag and Footnotes', axis=1)
a = cleaned_data.drop('UNIT', axis=1)
a = a.rename(columns={'TIME': 'Year', 'GEO': 'Country Name', 'NA_ITEM': 'Indicator Name'}).reset_index()
df = a.drop('index', axis=1)

available_indicators = df['Indicator Name'].unique()
countries = df['Country Name'].unique()

app.layout = html.Div([
    html.Div([
    html.H1('Graph number 1'),
    ]),
    
    html.Div([

        html.Div(
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Final consumption expenditure'
            ),
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div(
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )
        ,style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='year--slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].max(),
        step=None,
        marks={str(year): str(year) for year in df['Year'].unique()}
    ),
        
    html.Div([
    html.H1('Graph number 2'),
    ]),
    html.Div(
            dcc.Dropdown(
                id='b_xaxis-column',
                options=[{'label': i, 'value': i} for i in countries],
                value='Hungary'
            ),
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div(
            dcc.Dropdown(
                id='b_yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )
        ,style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

    dcc.Graph(id='b_indicator-graphic')
])
])
@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('year--slider', 'value')])
def a_update_graph(xaxis_column_name, yaxis_column_name,
                 year_value):
    dff = df[df['Year'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name
            },
            yaxis={
                'title': yaxis_column_name
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }
    
@app.callback(
    dash.dependencies.Output('b_indicator-graphic', 'figure'),
    [dash.dependencies.Input('b_xaxis-column', 'value'),
     dash.dependencies.Input('b_yaxis-column', 'value'),
    ])
def b_update_graph(b_xaxis_column_name, b_yaxis_column_name):
    
    return {
        'data': [go.Scatter(
            x=df[df['Country Name'] == b_xaxis_column_name]['Year'].unique(),
            y=df[(df['Indicator Name'] == b_yaxis_column_name)&(df['Country Name'] == b_xaxis_column_name)]['Value'],
            text=df[df['Indicator Name'] == b_yaxis_column_name]['Country Name'],
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': b_xaxis_column_name
            },
            yaxis={
                'title': b_yaxis_column_name
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()    

