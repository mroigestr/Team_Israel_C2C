import dash
from dash import dcc
from dash import html
import plotly.express as px


app = dash.Dash()
df = px.data.stocks()

print(df.head(10))
print(df.tail(10))

def stock_prices():
    """Function to create a line chart representing Google stock prices over time."""
    fig = px.line(df, x=df['date'], y=df['GOOG']) 
    fig2 = px.line(df, x=df['date'], y=df['AMZN'])
    return fig, fig2


# app.layout = html.Div(
#     children=[
#         html.H1(id='H1',
#                 children='HTML Component',
#                 style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 40}),
#         html.H1(id='H2',
#                 children='2nd HTML Component'),
#         html.Div(children='Ein ganz normaler Container (div) für Fließende Objekte'),
#         dcc.Graph(id='line_plot', figure=stock_prices()),
#         # dcc.Graph(id='line_plot', figure=stock_prices()),
#     ]
# )


# if __name__ == '__main__':
#     app.run_server(debug=True)
