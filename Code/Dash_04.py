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
import numpy as np


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

df_fp1 = pd.read_csv('Log-Datei_BaseCar_fp1.csv', header=0)
df_fp2 = pd.read_csv('Log-Datei_BaseCar_fp2.csv', header=0)
df_fp3 = pd.read_csv('Log-Datei_SonicCar_fp3.csv', header=0)
df_fp4 = pd.read_csv('Log-Datei_SonicCar_fp4.csv', header=0)
df_fp5 = pd.read_csv('Log-Datei_SonicCar_fp5.csv', header=0)
df_fp6 = pd.read_csv('Log-Datei_SonicCar_fp6.csv', header=0)

def driving_data(data):

    t_end= datetime.strptime(data["t_now"].iloc[-1], '%H:%M:%S.%f')
    t_start= datetime.strptime(data["t_now"].iloc[0], '%H:%M:%S.%f') 
    t_gesamt= t_end - t_start

    s_gesamt = 0
    for i in range(len(data["t_now"])-1):

        t_end_i = datetime.strptime(data["t_now"].iloc[i+1], '%H:%M:%S.%f')
        t_start_i = datetime.strptime(data["t_now"].iloc[i], '%H:%M:%S.%f')
        t_diff = t_end_i - t_start_i
        t_diff_s = t_diff.total_seconds()
        s_diff = t_diff_s * data["speed"].iloc[i]
        s_gesamt +=  s_diff


    speed_max = data['speed'].max()
    speed_min = data['speed'].min()
    speed_mean = data['speed'].mean()

    speed_stat = [speed_max, speed_min, speed_mean, s_gesamt]

    dfs = pd.DataFrame({
        "Statistik": ["v_Max", "v_Min", "vMean","Strecke"],
        "Werte": speed_stat
    })

    

    dfs = {
        "v_Max": speed_max,
        "v_Min": speed_min,
        "v_Mean": speed_mean,
        "Strecke": s_gesamt
    }

    return(dfs)





drivestats = driving_data(df_fp1)


app.layout = html.Div(
    children=[
        html.H1(id='H1',
                children='Gruppe 2 - Team Israel',
                style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 40}),
        html.H1(id='H2',
                children='PiCar - Fahrdaten:'),
        
        dcc.Dropdown(id='dropdown_fp',
                     options=[
                         {'label': 'Fahrpacours 1', 'value': 'df_fp1'},
                         {'label': 'Fahrpacours 2', 'value': 'df_fp2'},
                         {'label': 'Fahrpacours 3', 'value': 'df_fp3'},
                         {'label': 'Fahrpacours 4', 'value': 'df_fp4'},
                         {'label': 'Fahrpacours 5', 'value': 'df_fp5'},
                         {'label': 'Fahrpacours 6', 'value': 'df_fp6'},
                     ],
                     value='df_fp1'),
        dcc.Dropdown(id='dropdown',
                     options=[
                         {'label': 'Geschwindigkeit', 'value': 'speed'},
                         {'label': 'Richtung', 'value': 'direction'},
                         {'label': 'Lenkwinkel', 'value': 'steering_angle'},
                     ],
                     value='speed'),
        dcc.Graph(id='line_plot'),
        html.H5(id='H3',
                children=('Gesamtstrecke: ',drivestats["Strecke"])),
        html.Br(),


    ]
)


# Callback für den Plot als Ausgabe (siehe 'line_plot') und den Wert des Dropdown Menüs als Eingabe
@app.callback([Output(component_id='line_plot', component_property='figure'),
               Output('H3', 'children')],
              [Input(component_id='dropdown_fp', component_property='value'),
              Input(component_id='dropdown', component_property='value')])
def graph_update(value_of_dropdown_fp, value_of_dropdown):
    data = eval(value_of_dropdown_fp)
    drivestats = driving_data(data)

    fig_plot = px.line(data, x=data['t_now'], y=data[value_of_dropdown])
    s_gesamt = 'Gesamtstrecke: ',drivestats["Strecke"]
    return fig_plot, s_gesamt


if __name__ == '__main__':
    app.run_server(debug=True)
