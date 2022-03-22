import dash
from dash import dcc
from dash import html
import plotly.express as px
from dash.dependencies import Input, Output


app = dash.Dash()
df = px.data.stocks()

app.layout = html.Div(
    children=[
        html.H1(id='H1',
                children='HTML Component',
                style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 40}),
        html.H1(id='H2',
                children='2nd HTML Component'),
        html.Div(children='Ein ganz normaler Container (div) für Fließende Objekte'),
        dcc.Dropdown(id='dropdown',
                     options=[
                         {'label': 'Google', 'value': 'GOOG'},
                         {'label': 'Apple', 'value': 'AAPL'},
                         {'label': 'Amazon', 'value': 'AMZN'},
                     ],
                     value='GOOG'),
        dcc.Graph(id='line_plot'),
    ]
)


@app.callback(Output(component_id='line_plot', component_property='figure'),
              [Input(component_id='dropdown', component_property='value')])
def graph_update(value_of_input_component):
    print(value_of_input_component)
    fig = px.line(df, x=df['date'], y=df[value_of_input_component])
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
