from dash import Dash, dcc, html, Input, Output, State, Patch, MATCH, ALL    
import dash_bootstrap_components as dbc         
import plotly.express as px
import pandas as pd
import DataScienceAndVis.dashboard.vis as vis

df = pd.read_csv("netflix_processed.csv")
genres = {}
for genre in df['listed_in']:
    for names in genre.split(','):
        names = names.strip()
        if names in genres:
            genres[names] += 1
        else:
            genres[names] = 1

gen_df = pd.DataFrame(list(genres.items()), columns= ['Genre', 'Number of Movies'])
gen_df

casts = {}
for cast in df['cast']:
    for names in cast.split(','):
        names = names.strip()
        if names in genres:
            casts[names] += 1
        else:
            casts[names] = 1

cast_df = pd.DataFrame(list(casts.items()), columns= ['cast', 'Number of Movies'])
cast_df

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

search_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Netflix search", className="card-title",),
                dbc.CardImg(src="/assets/Netflix logo.jpg", title="netflix logo"),
                #https://www.panchayiti.com/wp-content/uploads/2023/04/Netflix-1000x500.jpg

                html.Br(),
                html.Br(),
                html.Br(),

                html.H6("Movie/TV Show:", className="card-text"),
                dcc.Dropdown(id='movie_tv', options=[{'label': d, "value": d} for d in df["type"].unique()],
                              value="Movie", style={"color": "#000000"}), 
                html.Hr(),

                #html.H6("Origin:", className="card-text"),
                #dcc.Dropdown(id='country', options=[{'label': d, "value": d} for d in df["country"].unique()],
                #              value="Unknown", style={"color": "#000000"}), 
                #html.Hr(),

                html.H6("Cast:", className="card-text"),
                dcc.Dropdown(id='cast', options=[{'label': d, "value": d} for d in cast_df["cast"].unique()],
                              value="Unknown", style={"color": "#000000"}), 
                html.Hr(),

                html.H6("Genre:", className="card-text"),
                dcc.Dropdown(id='listed_in', options=[{'label': d, "value": d} for d in gen_df["Genre"].unique()],
                              value="Documentaries", style={"color": "#000000"}), 
                html.Hr(),

                dbc.Button(
                    "Search", id="search_button", color="info", n_clicks=0, style={'background': 'black', 'color': 'red'}
                ),
            ]
        ),
    ],
    color="light",
)

list_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Movie list", className="card-title", style={"text-align": "center"}),
                html.Div(id="container", children=[]),
                dbc.Button("Clear", id="clear", color="info", n_clicks=0, 
                           style={'background': 'black', 'color': 'red'}, 
                           )
            ]
        ),
    ],
    color="light",
)

app.layout = html.Div([
    html.Br(),
    html.H4("N e t f l i x - S e a r c h C a r d", className="card-title", style={'padding': '30px', 'text-align': 'center', 'background': 'black', 'color': 'red', 'font-size': '40px', }),
    html.Br(),
    dbc.Row([dbc.Col(search_card, width=3), dbc.Col(list_card, width=8)], justify="around")
])


@app.callback(
    Output("container","children", allow_duplicate=True),
    [Input("search_button", "n_clicks"),
     Input("movie_tv", "value"),
     Input("cast","value"),
     Input("listed_in","value"),],
    [State("container", "children")],
    prevent_initial_call=True,
)
def add_to_list(clicks, show_type, cast, listed_in, div_children): 
    

    div_children = Patch()

    if clicks != 0:

        df_read = vis.read_titles(show_type, cast, listed_in)

        title_list = df_read["title"]
        description = df_read["description"]
        show = df_read["type"]
        country = df_read["country"]
        all_cast = []

        for i in range(len(title_list)):
            for title in df_read['title']:
                all_cast.append(df['cast'].loc[(df['title'] == title)])

            container = html.Div(
            [
                html.H4(title_list[i], style={'padding': '10px', 'text-align': 'center', 'background': 'black', 'color': 'red', 'font-size': '20px', }),
                html.Div(
                    [
                        html.H6(description[i]),
                        html.H6("Cast: "+all_cast[i]),
                        html.H6("Show type: "+show[i]),
                        html.H6("Origin: "+country[i])
                    ],style={'padding': '10px', 'background': '#e5e4e2', 'color': 'black', 'font-size': '20px', }      
                ),

                ]
            )

            div_children.append(container)

        #clicks = 0

    return div_children

@app.callback(
    Output("container","children", allow_duplicate=True),
    [Input("clear","n_clicks")],
    [State("container", "children")],
    prevent_initial_call=True,
)

def clear(clear_clicked, div_children):
    if clear_clicked is not None:
        div_children = ""

    return div_children


if __name__ == "__main__":
    app.run_server(debug=True)