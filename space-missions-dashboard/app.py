import dash
from dash import html, dcc, dash_table, Input, Output
import pandas as pd
import plotly.express as px

from src.analytics import (
    getMissionCountByCompany, 
    getSuccessRate, 
    getMissionsByDateRange, 
    getTopCompaniesByMissionCount, 
    getMissionStatusCount, 
    getMissionsByYear, 
    getMostUsedRocket, 
    getAverageMissionsPerYear
)

# Load data
df = pd.read_csv("data/space_missions.csv", parse_dates=["Date"])

# Initialize app
app = dash.Dash(__name__)
app.title = "Space Missions Dashboard"

# Dropdown style
dropdown_style = {"minWidth": "300px", "height": "auto"}

# Filters
filters = html.Div([
    dcc.Dropdown(
        id='company-filter',
        options=[{'label': c, 'value': c} for c in sorted(df['Company'].dropna().unique())],
        placeholder="Select Company",
        multi=True,
        style=dropdown_style,
        optionHeight=60
    ),
    dcc.Dropdown(
        id='status-filter',
        options=[{'label': s, 'value': s} for s in sorted(df['MissionStatus'].dropna().unique())],
        placeholder="Select Mission Status",
        multi=True,
        style=dropdown_style,
        optionHeight=60
    ),
    dcc.DatePickerRange(
        id='date-filter',
        min_date_allowed=df["Date"].min(),
        max_date_allowed=df["Date"].max(),
        start_date=df["Date"].min(),
        end_date=df["Date"].max(),
    )
], style={'display': 'flex', 'gap': '20px', 'margin-bottom': '30px'})

# Summary stats as simple cards
summary_stats = html.Div(id='summary-stats', style={'display': 'flex', 'gap': '20px', 'margin-bottom': '30px'})

# Graphs
visuals = html.Div([
    dcc.Graph(id='missions-by-company'),
    dcc.Graph(id='missions-over-time'),
    dcc.Graph(id='missions-by-location')
], style={'display': 'grid', 'grid-template-columns': '1fr', 'gap': '30px'})

# Data table
data_table = dash_table.DataTable(
    id='missions-table',
    columns=[{"name": i, "id": i} for i in df.columns],
    page_size=10,
    sort_action="native",
    filter_action="native",
    style_table={'overflowX': 'auto'},
    style_header={'backgroundColor': '#1f77b4', 'color': 'white'},
    style_cell={'textAlign': 'left', 'padding': '5px'}
)

# App layout
app.layout = html.Div([
    html.H1("Space Missions Dashboard", style={'textAlign': 'center', 'margin-bottom': '30px'}),
    filters,
    summary_stats,
    visuals,
    html.H2("Mission Data Table", style={'margin-top': '40px'}),
    data_table
], style={'padding': '20px', 'font-family': 'Arial, sans-serif', 'backgroundColor': '#f9f9f9'})

# Callback to update dashboard
@app.callback(
    Output('summary-stats', 'children'),
    Output('missions-by-company', 'figure'),
    Output('missions-over-time', 'figure'),
    Output('missions-by-location', 'figure'),
    Output('missions-table', 'data'),
    Input('company-filter', 'value'),
    Input('status-filter', 'value'),
    Input('date-filter', 'start_date'),
    Input('date-filter', 'end_date')
)
def update_dashboard(companies, statuses, start_date, end_date):
    dff = df.copy()
    if companies:
        dff = dff[dff['Company'].isin(companies)]
    if statuses:
        dff = dff[dff['MissionStatus'].isin(statuses)]
    if start_date and end_date:
        dff = dff[(dff['Date'] >= start_date) & (dff['Date'] <= end_date)]

    # Summary cards
    total_missions = len(dff)
    success_count = len(dff[dff['MissionStatus'] == "Success"])
    success_rate = round(success_count / total_missions * 100, 2) if total_missions > 0 else 0

    summary = [
        html.Div([
            html.H3("Total Missions"),
            html.H2(f"{total_missions}", style={'color':"#3E6987"})
        ], style={'padding': '10px', 'borderRadius': '10px', 'backgroundColor': 'white', 'flex': 0.5, 'textAlign': 'center'}),
        
        html.Div([
            html.H3("Success Rate"),
            html.H2(f"{success_rate}%", style={'color': "#204d20"})
        ], style={'padding': '20px', 'borderRadius': '1px', 'backgroundColor': 'white', 'flex': 0.5, 'textAlign': 'center'})
    ]

    # Graphs
    fig_company = px.bar(
        dff.groupby("Company").size().reset_index(name='Missions'),
        x='Company', y='Missions',
        title='Missions by Company',
        color='Missions'
    )

    fig_time = px.line(
        dff.groupby(dff['Date'].dt.year).size().reset_index(name='Missions'),
        x='Date', y='Missions',
        title='Missions Over Time',
        markers=True
    )

    fig_location = px.bar(
        dff.groupby("Location").size().reset_index(name='Missions'),
        x='Location', y='Missions',
        title='Missions by Location',
        color= 'Missions'
    )

    # Table data
    table_data = dff.to_dict('records')

    return summary, fig_company, fig_time, fig_location, table_data

# Run app
if __name__ == '__main__':
    app.run(debug=True)
