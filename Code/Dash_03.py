import dash
from dash import dcc
from dash import html
import plotly.express as px
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from pickle import POP
from re import T
import csv
from datetime import datetime


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_csv('Log-Datei_SonicCar_fp6.csv', header=0)

t_end_str= df["t_now"].iloc[-1]
t_start_str= df["t_now"].iloc[0]
t_end= datetime.strptime(t_end_str, '%H:%M:%S.%f')
t_start= datetime.strptime(t_start_str, '%H:%M:%S.%f') 
t_gesamt= t_end - t_start


s_gesamt = 0
for i in range(len(df["t_now"])-1):

    t_end_i = datetime.strptime(df["t_now"].iloc[i+1], '%H:%M:%S.%f')
    t_start_i = datetime.strptime(df["t_now"].iloc[i], '%H:%M:%S.%f')
    t_diff = t_end_i - t_start_i
    t_diff_s = t_diff.total_seconds()
    s_diff = t_diff_s * df["speed"].iloc[i]
    s_gesamt +=  s_diff

speed_max = df['speed'].max()
speed_min = df['speed'].min()
speed_mean = df['speed'].mean()

speed_stat = [speed_max, speed_min, speed_mean]

dfs = pd.DataFrame({
    "Statistik": ["Max", "Min", "MW"],
    "Werte": speed_stat
})



app.layout = html.Div(
    children=[
        html.H1(id='H1',
                children='Gruppe 2 - Team Israel',
                style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 40}),
        html.H1(id='H2',
                children='PiCar - Fahrdaten: Fahrpacours 6'),
        dcc.Dropdown(id='dropdown',
                     options=[
                         {'label': 'Geschwindigkeit', 'value': 'speed'},
                         {'label': 'Richtung', 'value': 'direction'},
                         {'label': 'Lenkwinkel', 'value': 'steering_angle'},
                     ],
                     value='speed'),
        dcc.Graph(id='line_plot'),
        html.H5(id='H3',
                children=('Gesamtstrecke: ',s_gesamt)),
        html.Br(),

    ]
)


# Callback für den Plot als Ausgabe (siehe 'line_plot') und den Wert des Dropdown Menüs als Eingabe
@app.callback(Output(component_id='line_plot', component_property='figure'),
              [Input(component_id='dropdown', component_property='value')])
def graph_update(value_of_input_component):
    print(value_of_input_component)
    fig = px.line(df, x=df['t_now'], y=df[value_of_input_component])
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
