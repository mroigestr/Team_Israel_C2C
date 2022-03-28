from pickle import POP
from re import T
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
#df["t_now_dt"]= datetime.strptime(df["t_now"] , '%H:%M:%S.%f')
t_end_str= df["t_now"].iloc[-1]
t_start_str= df["t_now"].iloc[0]
t_end= datetime.strptime(t_end_str, '%H:%M:%S.%f')
t_start= datetime.strptime(t_start_str, '%H:%M:%S.%f') 
t_gesamt= t_end - t_start
print (t_start, t_end, t_gesamt)
#print(type(df['t_now']))
'''print(df.head())
print(df['speed'].max())
print(df['speed'].min())
print(df['speed'].mean())'''
s_gesamt = 0

for i in range(len(df["t_now"])-1):
    # print(i+1)
    # print(type(i))

    t_end_i = datetime.strptime(df["t_now"].iloc[i+1], '%H:%M:%S.%f')
    t_start_i = datetime.strptime(df["t_now"].iloc[i], '%H:%M:%S.%f')
    t_diff = t_end_i - t_start_i
    #t_diff = df["t_now"].iloc[i+1] - df["t_now"].iloc[i]
    #t_diff_s = float(t_diff.seconds)
    t_diff_s = t_diff.total_seconds()
    s_diff = t_diff_s * df["speed"].iloc[i]
    # print(t_diff_s, type(t_diff_s))
    s_gesamt +=  s_diff
print (s_gesamt)
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
        html.H1(id='H3',
                children=('Gesamtstrecke: ',s_gesamt)),

    ]   
)

# Starten der dash app
if __name__ == '__main__':
    app.run_server(debug=True)


