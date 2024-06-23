
from dash import html, dcc, Output, Input, Dash, State
import dash_bootstrap_components as dbc
import sqlite3
import time
import math

update_frequency = 200

default_fig = dict(
                data=[{'x':[],'y':[]}],
                layout=dict(
                    xaxis=dict(range=[-1,1], visible = False),
                    yaxis=dict(range=[0,8000], color="white"),
                    paper_bgcolor="#2D2D2D",
                    plot_bgcolor="#2D2D2D"
                    ))

app = Dash(external_stylesheets=[dbc.themes.CYBORG])

app.layout = html.Div([

    html.H1(id="price-ticker",
        style={"text-align":"center",
               "padding-top":"120px",
               "padding-bottom":"40px"}),
    dcc.Graph(id="graph", figure = default_fig ),
    dcc.Interval(id="update", interval = update_frequency),

    ])

@app.callback(
        Output("graph", "extendData"),
        Output("price-ticker", "children"),
        Input("update", "n_intervals"),
        )
def update_data(intervals):

    connection = sqlite3.connect("./data.db")
    cursor = connection.cursor()

    time_from = math.floor((time.time() - 60) *1000)

    data = cursor.execute(
            f"SELECT * FROM trades WHERE time > {time_from} ORDER BY time DESC").fetchall()

    current_price = data[0][3]
    total_trades = len(data)

    # (new data, trace to add data to, number of elements to keep)
    return (dict(x=[[time.time()]], y=[[total_trades]]), [0], 100), current_price












if __name__ == "__main__":
    app.run_server(debug=True)
