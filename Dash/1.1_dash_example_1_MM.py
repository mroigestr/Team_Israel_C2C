import dash
from dash import dcc
from dash import html

# Inizialisierung der dash app
app = dash.Dash()

# Erstellen des Layouts
app.layout = html.Div(
    children=[
        html.H1(id='H1',
                children='HTML Titel',
                style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 20}),
        html.H2(id='H2',
                children='2nd HTML Component'),
        html.Div(children='Ein ganz normaler Container (div) für Fließende Objekte'),
        html.H3(children='Ein weiterer Container'),
    ]
)

# Starten der dash app
if __name__ == '__main__':
    app.run_server(debug=True)
