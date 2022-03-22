import dash
from dash import dcc
from dash import html

# Inizialisierung der dash app
app = dash.Dash()

# Erstellen des Layouts
app.layout = html.Div(
    children=[
        html.H1(id='H1',
                children='HTML Component',
                style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 40}),
        html.H2(id='H2',
                children='2nd HTML Component'),
        html.Div(children='Ein ganz normaler Container (div) für Fließende Objekte'),
    ]
)

# Starten der dash app
if __name__ == '__main__':
    app.run_server(debug=True)
