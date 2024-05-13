import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from dash import dcc, html, register_page, callback, Output, Input, callback_context
from .data.loader import load_dashboard_data, load_cities_data, DataSchemaTJ
from .components.ids import ids_tjs
from pathlib import Path

THIS_FOLDER = Path(__file__).parent.resolve()
DATA_JURIDICO = THIS_FOLDER / 'data/Planilha BI FINAL.xlsx'
DATA_CITIES = THIS_FOLDER / 'data/brazil_cities.csv'
data = load_dashboard_data(DATA_JURIDICO, "Planilha1")
df_cities = load_cities_data(DATA_CITIES)

unique_tribunais = sorted(set(data[DataSchemaTJ.TRIBUNAL_ORIGEM].unique().tolist()), key = str)

register_page(
    __name__,
    path = '/tj_stj',
    name = 'Dashboard TJS',
    title = 'Dashboard TJS')

layout = html.Div(
    children = [
        dbc.Container([
            dbc.Row([
                html.H4("TJS"),
                dcc.Dropdown(
                    id = ids_tjs.TRIBUNAL_TJS_DROPDOWN,
                    options = [{"label": tribunal, "value": tribunal} for tribunal in unique_tribunais],
                    value = unique_tribunais,
                    multi = True
                ),
                html.Button(
                    className = "dropdown-button",
                    children = ["Selecionar Todos"],
                    id = ids_tjs.SELECT_ALL_TRIBUNAIS_TJS_BUTTON,
                    n_clicks = 0
                ), 
            ]),
            dbc.Row([
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id = ids_tjs.ESTADOS_BUBBLE_MAP,
                        ),
                        id = ids_tjs.CONTAINER_ESTADOS_TJ,
                    )
                ),
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id = ids_tjs.DURACAO_TJS_GAUGE_CHART,
                        ),
                        id = ids_tjs.CONTAINER_DURACAO_TJ,
                    )
                )
            ]),
            dbc.Row([
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id = ids_tjs.RUBRICA_TJS_PIE_CHART,
                        ),
                        id = ids_tjs.CONTAINER_RUBRICAS_TJ,
                    )
                ),
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id = ids_tjs.DECISOES_TJS_PIE_CHART,
                        ),
                        id = ids_tjs.CONTAINER_DECISOES_TJ,
                    )
                )
            ]),
            dbc.Row([
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id = ids_tjs.PROPOSITURA_TJS_BAR_CHART,
                        ),
                        id = ids_tjs.CONTAINER_PROPOSITURA_TJ,
                    )
                ),
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id = ids_tjs.JULGAMENTO_TJS_BAR_CHART,
                        ),
                        id = ids_tjs.CONTAINER_JULGAMENTO_TJ,
                    )
                )
            ])
        ]),
    ]
)

@callback(
    Output(ids_tjs.TRIBUNAL_TJS_DROPDOWN, "value"),
    Output(ids_tjs.ESTADOS_BUBBLE_MAP, "clickData"),
    Output(ids_tjs.RUBRICA_TJS_PIE_CHART, "clickData"),
    Output(ids_tjs.DECISOES_TJS_PIE_CHART, "clickData"),
    Output(ids_tjs.JULGAMENTO_TJS_BAR_CHART, "clickData"),
    Output(ids_tjs.PROPOSITURA_TJS_BAR_CHART, "clickData"),
    Input(ids_tjs.SELECT_ALL_TRIBUNAIS_TJS_BUTTON, "n_clicks"),
)
def select_all_tribunais(_:str, *args) -> list[str]:
    return unique_tribunais, None, None, None, None, None


@callback(
    Output(ids_tjs.DURACAO_TJS_GAUGE_CHART, "figure"),
    Input(ids_tjs.TRIBUNAL_TJS_DROPDOWN, "value"),
    Input(ids_tjs.ESTADOS_BUBBLE_MAP, "clickData"),
    Input(ids_tjs.RUBRICA_TJS_PIE_CHART, "clickData"),
    Input(ids_tjs.DECISOES_TJS_PIE_CHART, "clickData"),
    Input(ids_tjs.JULGAMENTO_TJS_BAR_CHART, "clickData"),
    Input(ids_tjs.PROPOSITURA_TJS_BAR_CHART, "clickData"),
)
# def update_duracao_chart(tribunais:list[str]) -> go.Figure:
def update_duracao_chart(tribunais:list[str], *args) -> go.Figure:
    
    if not tribunais:
        filtered_data = data.copy()
    else:
        filtered_data = data[data[DataSchemaTJ.TRIBUNAL_ORIGEM].isin(tribunais)].copy()
    
    ctx = callback_context

    if not ctx.triggered[0]["value"]:
        pass
    else:
        if ids_tjs.ESTADOS_BUBBLE_MAP in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["customdata"][0]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.TRIBUNAL_ORIGEM] == selected]
            pass
        if ids_tjs.RUBRICA_TJS_PIE_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.RUBRICA] == selected]
            pass
        if ids_tjs.DECISOES_TJS_PIE_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.ECAD] == selected]
            pass
        if ids_tjs.JULGAMENTO_TJS_BAR_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.DATA_JULGAMENTO].dt.year == int(selected)]
            pass
        if ids_tjs.PROPOSITURA_TJS_BAR_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.ANO_PROPOSITURA].dt.year == int(selected)]
            pass

    minimo_duracao = filtered_data[DataSchemaTJ.TEMPO_MEDIO].min()
    maximo_duracao = filtered_data[DataSchemaTJ.TEMPO_MEDIO].max()
    medio_duracao = filtered_data[DataSchemaTJ.TEMPO_MEDIO].mean()

    duracao_gauge = go.Indicator(
        mode = "gauge+number",
        value = medio_duracao,
        number = {
            'font':{
                'size':50,
            },
        },
        title = {
            'text':'Duração Média (anos)',
            'font':{
                'size': 18,
            },
        },
        domain = {
            'x':[0,1],
            'y':[0,1]
        },
        gauge = {
            'axis':{
                'range':[minimo_duracao, maximo_duracao],
                'tickmode':'array',
                'tickvals':list(range(minimo_duracao, maximo_duracao + 1)),
                'tickfont':{
                    'size':15
                },
            },
            'bar':{
                'color':'lightgreen',
                'thickness':1
            }
        }
    )

    fig = go.Figure(
        data = [duracao_gauge]
    )

    return fig

@callback(
    Output(ids_tjs.RUBRICA_TJS_PIE_CHART, "figure"),
    Input(ids_tjs.TRIBUNAL_TJS_DROPDOWN, "value"),
    Input(ids_tjs.RUBRICA_TJS_PIE_CHART, "clickData"),
    Input(ids_tjs.ESTADOS_BUBBLE_MAP, "clickData"),
    Input(ids_tjs.DECISOES_TJS_PIE_CHART, "clickData"),
    Input(ids_tjs.JULGAMENTO_TJS_BAR_CHART, "clickData"),
    Input(ids_tjs.PROPOSITURA_TJS_BAR_CHART, "clickData"),
)
def update_rubrica_chart(tribunais:list[str], click_data, *args) -> go.Figure:
    ctx = callback_context

    if not tribunais:
        filtered_data = data.copy()
    else:
        filtered_data = data[data[DataSchemaTJ.TRIBUNAL_ORIGEM].isin(tribunais)].copy()

    if not ctx.triggered[0]["value"]:
        pass
    else:
        if ids_tjs.ESTADOS_BUBBLE_MAP in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["customdata"][0]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.TRIBUNAL_ORIGEM] == selected]
            pass
        if ids_tjs.DECISOES_TJS_PIE_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.ECAD] == selected]
            pass
        if ids_tjs.JULGAMENTO_TJS_BAR_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.DATA_JULGAMENTO].dt.year == int(selected)]
            pass
        if ids_tjs.PROPOSITURA_TJS_BAR_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.ANO_PROPOSITURA].dt.year == int(selected)]
            pass

    df_rubrica = filtered_data.groupby([DataSchemaTJ.RUBRICA])[DataSchemaTJ.RUBRICA].count().reset_index(name = 'Total')

    if click_data and ids_tjs.RUBRICA_TJS_PIE_CHART in ctx.triggered[0]["prop_id"] and ctx.triggered[0]["value"]:
        rubrica = ctx.triggered[0]["value"]["points"][0]["label"]
        lista_rubricas = df_rubrica[DataSchemaTJ.RUBRICA].unique().tolist()
        lista_rubricas.remove(rubrica)
        lista_rubricas.insert(0, rubrica)
        df_rubrica[DataSchemaTJ.RUBRICA] = pd.Categorical(df_rubrica[DataSchemaTJ.RUBRICA], categories = lista_rubricas)
        df_rubrica = df_rubrica.sort_values(DataSchemaTJ.RUBRICA)

        rubrica_donut = go.Pie(
            labels = df_rubrica[DataSchemaTJ.RUBRICA].tolist(),
            values = df_rubrica['Total'],
            pull = [0.2],
            textinfo = 'percent',
            textposition = 'outside',
            hole = 0.5,
            sort = False
        )
    else:
        rubrica_donut = go.Pie(
            labels = df_rubrica[DataSchemaTJ.RUBRICA].tolist(),
            values = df_rubrica['Total'],
            textinfo = 'percent',
            textposition = 'outside',
            hole = 0.5
        )

    fig = go.Figure(
        data = [rubrica_donut],
        layout = {
            'title': {
                'text': 'Quantidade de Rubricas',
                'x': 0.5,
                'xanchor': 'center',
                'y': 1,
                'yanchor': 'top',
                'font':{
                    'size': 18
                },
            },
            'legend':{
                'title': 'Rubrica'
            }
        }
    )

    fig.update_layout(
        margin = {"t":40, "b":0, "l":0, "r":0, "autoexpand": True},
        
    )
    fig.update_traces(hovertemplate = "%{label}<br>%{value}<extra></extra>")

    return fig

@callback(
    Output(ids_tjs.DECISOES_TJS_PIE_CHART, "figure"),
    Input(ids_tjs.TRIBUNAL_TJS_DROPDOWN, "value"),
    Input(ids_tjs.DECISOES_TJS_PIE_CHART, "clickData"),
    Input(ids_tjs.RUBRICA_TJS_PIE_CHART, "clickData"),
    Input(ids_tjs.ESTADOS_BUBBLE_MAP, "clickData"),
    Input(ids_tjs.JULGAMENTO_TJS_BAR_CHART, "clickData"),
    Input(ids_tjs.PROPOSITURA_TJS_BAR_CHART, "clickData"),
)
def update_decisao_chart(tribunais:list[str], click_data, *args) -> go.Figure:
    ctx = callback_context

    if not tribunais:
        filtered_data = data.copy()
    else:  
        filtered_data = data[data[DataSchemaTJ.TRIBUNAL_ORIGEM].isin(tribunais)].copy()

    if not ctx.triggered[0]["value"]:
        pass
    else:
        if ids_tjs.ESTADOS_BUBBLE_MAP in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["customdata"][0]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.TRIBUNAL_ORIGEM] == selected]
            pass
        if ids_tjs.RUBRICA_TJS_PIE_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.RUBRICA] == selected]
            pass
        if ids_tjs.JULGAMENTO_TJS_BAR_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.DATA_JULGAMENTO].dt.year == int(selected)]
            pass
        if ids_tjs.PROPOSITURA_TJS_BAR_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.ANO_PROPOSITURA].dt.year == int(selected)]
            pass

    df_decisoes = filtered_data.groupby([DataSchemaTJ.ECAD])[DataSchemaTJ.ECAD].count().reset_index(name = 'Total')

    if click_data and ids_tjs.DECISOES_TJS_PIE_CHART in ctx.triggered[0]["prop_id"] and ctx.triggered[0]["value"]:
        decisao = ctx.triggered[0]["value"]["points"][0]["label"]
        lista_decisoes = df_decisoes[DataSchemaTJ.ECAD].unique().tolist()
        lista_decisoes.remove(decisao)
        lista_decisoes.insert(0, decisao)
        df_decisoes[DataSchemaTJ.ECAD] = pd.Categorical(df_decisoes[DataSchemaTJ.ECAD], categories = lista_decisoes)
        df_decisoes = df_decisoes.sort_values(DataSchemaTJ.ECAD)

        decisoes_donut = go.Pie(
            labels = df_decisoes[DataSchemaTJ.ECAD].tolist(),
            values = df_decisoes['Total'],
            pull = [0.2],
            textinfo = 'percent',
            textposition = 'outside',
            hole = 0.5,
            sort = False
        )
    else:        
        decisoes_donut = go.Pie(
            labels = df_decisoes[DataSchemaTJ.ECAD].tolist(),
            values = df_decisoes['Total'],
            textinfo = 'percent',
            textposition = 'outside',
            hole = 0.5
        )

    fig = go.Figure(
        data = [decisoes_donut],
        layout = {
            'title': {
                'text': 'Decisões',
                'x': 0.5,
                'xanchor': 'center',
                'y': 1,
                'yanchor': 'top',
                'font':{
                    'size': 18
                },
            },
            'legend':{
                'title': 'Decisões'
            }
        }
    )

    fig.update_layout(margin = {"t":40, "b":0, "l":0, "r":0})
    fig.update_traces(hovertemplate = "%{label}<br>%{value}<extra></extra>")

    return fig

@callback(
    Output(ids_tjs.PROPOSITURA_TJS_BAR_CHART, "figure"),
    Input(ids_tjs.TRIBUNAL_TJS_DROPDOWN, "value"),
    Input(ids_tjs.PROPOSITURA_TJS_BAR_CHART, "clickData"),
    Input(ids_tjs.DECISOES_TJS_PIE_CHART, "clickData"),
    Input(ids_tjs.RUBRICA_TJS_PIE_CHART, "clickData"),
    Input(ids_tjs.ESTADOS_BUBBLE_MAP, "clickData"),
    Input(ids_tjs.JULGAMENTO_TJS_BAR_CHART, "clickData"),
)
def update_propositura_chart(tribunais:list[str], click_data, *args) -> go.Figure:
    ctx = callback_context
    if not tribunais:
        filtered_data = data.copy()
    else:
        filtered_data = data[data[DataSchemaTJ.TRIBUNAL_ORIGEM].isin(tribunais)].copy()
    
    if not ctx.triggered[0]["value"]:
        pass
    else:
        if ids_tjs.ESTADOS_BUBBLE_MAP in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["customdata"][0]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.TRIBUNAL_ORIGEM] == selected]
            pass
        if ids_tjs.RUBRICA_TJS_PIE_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.RUBRICA] == selected]
            pass
        if ids_tjs.DECISOES_TJS_PIE_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.ECAD] == selected]
            pass
        if ids_tjs.JULGAMENTO_TJS_BAR_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.DATA_JULGAMENTO].dt.year == int(selected)]
            pass

    filtered_data['Ano'] = filtered_data[DataSchemaTJ.ANO_PROPOSITURA].dt.year

    df_propositura = filtered_data[[DataSchemaTJ.TRIBUNAL_ORIGEM, 'Ano']].groupby(['Ano'])[DataSchemaTJ.TRIBUNAL_ORIGEM].count().reset_index(name = 'Total')

    if click_data and ids_tjs.PROPOSITURA_TJS_BAR_CHART in ctx.triggered[0]["prop_id"] and ctx.triggered[0]["value"]:
        propositura = ctx.triggered[0]["value"]["points"][0]["label"]
    else:
        propositura = ''
        pass
    
    minimo_ano, maximo_ano = df_propositura["Ano"].min(),df_propositura["Ano"].max()

    novo_index = pd.Index(np.arange(minimo_ano, maximo_ano + 1, 1), name = "Ano")

    df_propositura = df_propositura.set_index("Ano").reindex(novo_index).reset_index().fillna(0)

    df_propositura["Ano"] = df_propositura["Ano"].astype(str)

    lista_anos = df_propositura["Ano"].unique().tolist()
    def selected_bar(lista_anos):
        if lista_anos == propositura:
            return "red"
        else:
            return "cornflowerblue"
    
    propositura_bar = go.Bar(
        x = df_propositura["Ano"],
        y = df_propositura["Total"],
                marker = dict(
            color = list(
                map(
                    selected_bar, lista_anos
                )
            )
        )
    )

    fig = go.Figure(
        data = [propositura_bar],
        layout = {
            'title':'Quantidade de processos protocolados por Ano',
            'xaxis':{
                'title':'Ano'
            },
            'yaxis':{
                'title':'Total'
            }
        }
    )

    return fig

@callback(
    Output(ids_tjs.JULGAMENTO_TJS_BAR_CHART, "figure"),
    Input(ids_tjs.TRIBUNAL_TJS_DROPDOWN, "value"),
    Input(ids_tjs.JULGAMENTO_TJS_BAR_CHART, "clickData"),
    Input(ids_tjs.DECISOES_TJS_PIE_CHART, "clickData"),
    Input(ids_tjs.RUBRICA_TJS_PIE_CHART, "clickData"),
    Input(ids_tjs.ESTADOS_BUBBLE_MAP, "clickData"),
    Input(ids_tjs.PROPOSITURA_TJS_BAR_CHART, "clickData"),
)
def update_julgamento_chart(tribunais:list[str], click_data, *args) -> go.Figure:
    ctx = callback_context

    if not tribunais:
        filtered_data = data.copy()
    else:
        filtered_data = data[data[DataSchemaTJ.TRIBUNAL_ORIGEM].isin(tribunais)].copy()

    if not ctx.triggered[0]["value"]:
        pass
    else:
        if ids_tjs.ESTADOS_BUBBLE_MAP in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["customdata"][0]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.TRIBUNAL_ORIGEM] == selected]
            pass
        if ids_tjs.RUBRICA_TJS_PIE_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.RUBRICA] == selected]
            pass
        if ids_tjs.DECISOES_TJS_PIE_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.ECAD] == selected]
            pass
        if ids_tjs.PROPOSITURA_TJS_BAR_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.ANO_PROPOSITURA].dt.year == int(selected)]
            pass

    filtered_data['Ano'] = filtered_data[DataSchemaTJ.DATA_JULGAMENTO].dt.year

    df_julgamento = filtered_data[[DataSchemaTJ.TRIBUNAL_ORIGEM, 'Ano']].groupby(['Ano'])[DataSchemaTJ.TRIBUNAL_ORIGEM].count().reset_index(name = 'Total')
    
    if click_data and ids_tjs.JULGAMENTO_TJS_BAR_CHART in ctx.triggered[0]["prop_id"] and ctx.triggered[0]["value"]:
        julgamento = ctx.triggered[0]["value"]["points"][0]["label"]
    else:
        julgamento = ''

    minimo_ano, maximo_ano = df_julgamento["Ano"].min(),df_julgamento["Ano"].max()

    novo_index = pd.Index(np.arange(minimo_ano, maximo_ano + 1, 1), name = "Ano")

    df_julgamento = df_julgamento.set_index("Ano").reindex(novo_index).reset_index().fillna(0)

    df_julgamento["Ano"] = df_julgamento["Ano"].astype(str)

    lista_anos = df_julgamento["Ano"].unique().tolist()

    def selected_bar(lista_anos):
        if lista_anos == julgamento:
            return "red"
        else:
            return "cornflowerblue"

    julgamento_bar = go.Bar(
        x = df_julgamento["Total"],
        y = df_julgamento["Ano"],
        orientation = 'h',
        marker = dict(
            color = list(
                map(
                    selected_bar, lista_anos
                )
            )
        )
    )

    fig = go.Figure(
        data = [julgamento_bar],
        layout = {
            'title':'Processos Julgados por Ano',
            'xaxis':{
                'title':'Total'
            },
            'yaxis':{
                'title':'Ano'
            },
        },
    )
    return fig

@callback(
    Output(ids_tjs.ESTADOS_BUBBLE_MAP, "figure"),
    Input(ids_tjs.TRIBUNAL_TJS_DROPDOWN, "value"),
    Input(ids_tjs.ESTADOS_BUBBLE_MAP, "clickData"),
    Input(ids_tjs.RUBRICA_TJS_PIE_CHART, "clickData"),
    Input(ids_tjs.DECISOES_TJS_PIE_CHART, "clickData"),
    Input(ids_tjs.JULGAMENTO_TJS_BAR_CHART, "clickData"),
    Input(ids_tjs.PROPOSITURA_TJS_BAR_CHART, "clickData"),
)
def update_estados_map(tribunais:list[str], click_data, *args) -> go.Figure:
    ctx = callback_context

    if not tribunais:
        filtered_data = data.copy()
    else:
        filtered_data = data[data[DataSchemaTJ.TRIBUNAL_ORIGEM].isin(tribunais)].copy()

    if not ctx.triggered[0]["value"]:
        pass
    else:
        if ids_tjs.RUBRICA_TJS_PIE_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.RUBRICA] == selected]
            pass
        if ids_tjs.DECISOES_TJS_PIE_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.ECAD] == selected]
            pass
        if ids_tjs.JULGAMENTO_TJS_BAR_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.DATA_JULGAMENTO].dt.year == int(selected)]
            pass
        if ids_tjs.PROPOSITURA_TJS_BAR_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.ANO_PROPOSITURA].dt.year == int(selected)]
            pass
    
    df_tjs = filtered_data.groupby([DataSchemaTJ.TRIBUNAL_ORIGEM])[DataSchemaTJ.TRIBUNAL_ORIGEM].count().reset_index(name = 'Total')

    if click_data and ids_tjs.ESTADOS_BUBBLE_MAP in ctx.triggered[0]["prop_id"] and ctx.triggered[0]["value"]:
        tribunal = ctx.triggered[0]["value"]["points"][0]["customdata"][0]
        df_tjs = df_tjs[df_tjs[DataSchemaTJ.TRIBUNAL_ORIGEM] == tribunal]
    else:
        pass

    df_mapa = pd.merge(df_cities, df_tjs, left_on = 'tj', right_on = DataSchemaTJ.TRIBUNAL_ORIGEM)

    fig = px.scatter_mapbox(
        df_mapa,
        lat = 'lat',
        lon = 'lng',
        size = 'Total',
        size_max = 35,
        hover_data = {
            DataSchemaTJ.TRIBUNAL_ORIGEM:True,
            'Total':True,
            'lat':False,
            'lng':False
        },
        zoom = 2,
        mapbox_style = 'open-street-map'
    )

    return fig

# @callback(
#     Output(ids_tjs.ESTADOS_BUBBLE_MAP, "clickData"),
#     Output(ids_tjs.RUBRICA_TJS_PIE_CHART, "clickData"),
#     Output(ids_tjs.DECISOES_TJS_PIE_CHART, "clickData"),
#     Output(ids_tjs.JULGAMENTO_TJS_BAR_CHART, "clickData"),
#     Output(ids_tjs.PROPOSITURA_TJS_BAR_CHART, "clickData"),
#     Input(ids_tjs.ESTADOS_BUBBLE_MAP, "clickData"),
#     Input(ids_tjs.RUBRICA_TJS_PIE_CHART, "clickData"),
#     Input(ids_tjs.DECISOES_TJS_PIE_CHART, "clickData"),
#     Input(ids_tjs.JULGAMENTO_TJS_BAR_CHART, "clickData"),
#     Input(ids_tjs.PROPOSITURA_TJS_BAR_CHART, "clickData"),
# )
# def reset_click_data(estados,rubrica,decisoes,julgamento,propositura):
#     ctx = callback_context

#     print(ctx.triggered[0])

# @callback(
#     Output(ids_tjs.RUBRICA_TJS_PIE_CHART, 'clickData'),
#     Input(ids_tjs.CONTAINER_RUBRICAS_TJ, 'n_clicks')
# )
# def reset_click_rubricas(n_clicks):
#     return None

# @callback(
#     Output(ids_tjs.DECISOES_TJS_PIE_CHART, 'clickData'),
#     Input(ids_tjs.CONTAINER_DECISOES_TJ, 'n_clicks')
# )
# def reset_click_decisoes(n_clicks):
#     return None

# @callback(
#     Output(ids_tjs.ESTADOS_BUBBLE_MAP, 'clickData'),
#     Input(ids_tjs.CONTAINER_ESTADOS_TJ, 'n_clicks')
# )
# def reset_click_estados(n_clicks):
#     return None

# @callback(
#     Output(ids_tjs.JULGAMENTO_TJS_BAR_CHART, 'clickData'),
#     Input(ids_tjs.CONTAINER_JULGAMENTO_TJ, 'n_clicks')
# )
# def reset_click_julgamentos(n_clicks):
#     return None

# @callback(
#     Output(ids_tjs.PROPOSITURA_TJS_BAR_CHART, 'clickData'),
#     Input(ids_tjs.CONTAINER_PROPOSITURA_TJ, 'n_clicks')
# )
# def reset_click_propositura(n_clicks):
#     return None