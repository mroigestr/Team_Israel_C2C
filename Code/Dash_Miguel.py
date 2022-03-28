import plotly.express as px
import dash
import csv
import pandas as pd
from dash import dcc
from dash import html
from datetime import datetime

# Inizialisierung der dash app
app = dash.Dash()

df = pd.read_csv('Log-Datei.csv', header=0)
#Ende vom Freitag Zeit
#t_gesamt = df['t_now'].
'''print(df.head())
print(df['speed'].max())
print(df['speed'].min())
print(df['speed'].mean())'''

t_end_str = df["t_now"].iloc[-1]
t_start_str = df["t_now"].iloc[0]

t_end = datetime.strptime(t_end_str, '%H:%M:%S.%f')
t_end1 = t_end.strftime('%H:%M:%S.%f')
t_start = datetime.strptime(t_start_str, '%H:%M:%S.%f')
t_gesamt = t_end - t_start
print(type(t_end1))
print(t_end1[:-3])
print(type(t_end))

print(t_start, t_end, t_gesamt)

speed_max = df['speed'].max()
speed_min = df['speed'].min()
speed_mean = df['speed'].mean()

speed_stat = [speed_max, speed_min, speed_mean]

dfs = pd.DataFrame({
    "Statistik": ["Max", "Min", "MW"],
    "Werte": speed_stat
})

def speed_values():
    """Function to create a line chart representing Google stock prices over time."""
    fig = px.line(df, x=df['t_now'], y=df['speed'])
    return fig

def speed_stats():
    """Function to create a line chart representing Google stock prices over time."""
    fig = px.bar(dfs, x=dfs['Statistik'], y=dfs['Werte'])
    return fig

# Erstellen des Layouts
'''app.layout = html.Div(
    children=[
        html.H1(id='H1',
                children='Team_Israel',
                style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 40}),
        html.H2(id='H2',
                children='Fahrspur'),
        html.Div(children='--'),
    ]  
)'''

'''app.layout = html.Div(
    children=[
        html.H1(id='H1',
                children='Team_Israel',
                style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 40}),
        html.H1(id='H2',
                children='Fahrspur'),
        html.Div(children='Aufzeichnung'),
        dcc.Graph(id='line_plot', figure=speed_values()),
    ]   
)'''

app.layout = html.Div(
    children=[
        html.H1(id='H1',
                children='Team_Israel',
                style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 40}),
        html.H1(id='H2',
                children='Fahrspur'),
        html.Div(children='Statistik'),
        dcc.Graph(id='bar_plot', figure=speed_stats()),
    ]   
)

# Starten der dash app
if __name__ == '__main__':
    app.run_server(debug=True)