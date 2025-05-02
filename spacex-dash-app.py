import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Load data
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Initialize app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("SpaceX Launch Records Dashboard",
            style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 40}),

    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] + 
                [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
        value='ALL',
        placeholder='Select a Launch Site',
        style={'width': '50%', 'margin': 'auto'}
    ),

    html.Br(),

    dcc.Graph(id='success-pie-chart'),

    html.P("Payload range (Kg):", style={'marginTop': 30}),
    dcc.RangeSlider(
        id='payload-slider',
        min=int(min_payload),
        max=int(max_payload),
        step=100,
        marks={i: f'{i}' for i in range(int(min_payload), int(max_payload)+1, 2000)},
        value=[min_payload, max_payload]
    ),

    html.Br(),

    dcc.Graph(id='success-payload-scatter-chart')
])

# Callback for pie chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie(site):
    if site == 'ALL':
        fig = px.pie(spacex_df, names='Launch Site', values='class',
                     title='Total Success Launches By Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == site]
        fig = px.pie(filtered_df, names='class',
                     title=f'Total Success vs Failure for {site}')
    return fig

# Callback for scatter plot
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter(site, payload):
    low, high = payload
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & 
                            (spacex_df['Payload Mass (kg)'] <= high)]
    if site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == site]

    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                     color='Booster Version Category',
                     title='Payload vs. Outcome')
    return fig

# Run app
if __name__ == '__main__':
    app.run(debug=True)
