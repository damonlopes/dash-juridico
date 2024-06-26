import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from dash import dcc, html, register_page, callback, Output, Input, State, dash_table, callback_context
from dash._callback_context import CallbackContext
from .data.loader import load_dashboard_data, load_cities_data, DataSchemaTJ
from .components.ids import ids_tjs
from pathlib import Path

THIS_FOLDER = Path(__file__).parent.resolve()
DATA_JURIDICO = THIS_FOLDER / 'data/Planilha BI FINAL.xlsx'
DATA_CITIES = THIS_FOLDER / 'data/brazil_cities.csv'
data = load_dashboard_data(DATA_JURIDICO, "Planilha1")
df_cities = load_cities_data(DATA_CITIES)

unique_tribunais = sorted(set(data[DataSchemaTJ.TRIBUNAL_ORIGEM].unique().tolist()), key = str)
unique_rubricas = sorted(set(data[DataSchemaTJ.RUBRICA].unique().tolist()), key = str)
unique_decisoes = sorted(set(data[DataSchemaTJ.ECAD].unique().tolist()), key = str)
minimo_ano_julgamento = data[DataSchemaTJ.DATA_JULGAMENTO].dt.year.min()
maximo_ano_julgamento = data[DataSchemaTJ.DATA_JULGAMENTO].dt.year.max()
minimo_ano_propositura = data[DataSchemaTJ.ANO_PROPOSITURA].dt.year.min()
maximo_ano_propositura = data[DataSchemaTJ.ANO_PROPOSITURA].dt.year.max()


register_page(
    __name__,
    path = '/tj_stj',
    name = 'Dashboard TJS',
    title = 'Dashboard TJS')

layout = html.Div(
    children = [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Button(
                            "Mostrar/Ocultar Filtros",
                            id = ids_tjs.OCULTAR_FILTROS_TJS_BUTTON,
                            n_clicks = 0,
                        ),
                    ],
                    width = {
                        "size":3,
                        # "offset":3,
                    },
                ),
            ],
            justify = "right",
        ),
        html.Hr(),
        dbc.Collapse(
            dbc.Container([
                dbc.Row([
                    html.H4("TJS"),
                    dcc.Dropdown(
                        id = ids_tjs.TRIBUNAL_TJS_DROPDOWN,
                        options = [{"label": tribunal, "value": tribunal} for tribunal in unique_tribunais],
                        value = unique_tribunais,
                        multi = True
                    ),
                    dbc.Button(
                        className = "dropdown-button",
                        children = ["Selecionar Todos"],
                        id = ids_tjs.SELECT_ALL_TRIBUNAIS_TJS_BUTTON,
                        n_clicks = 0
                    ),
                ]),
                dbc.Row([
                    html.H4("Rubricas"),
                    dcc.Dropdown(
                        id = ids_tjs.RUBRICA_TJS_DROPDOWN,
                        options = [{"label": rubrica, "value": rubrica} for rubrica in unique_rubricas],
                        value = unique_rubricas,
                        multi = True
                    ),
                    dbc.Button(
                        className = "dropdown-button",
                        children = ["Selecionar Todos"],
                        id = ids_tjs.SELECT_ALL_RUBRICAS_TJS_BUTTON,
                        n_clicks = 0
                    ),
                ]),
                dbc.Row([
                    html.H4("Decisões"),
                    dcc.Dropdown(
                        id = ids_tjs.DECISAO_TJS_DROPDOWN,
                        options = [{"label": decisao, "value": decisao} for decisao in unique_decisoes],
                        value = unique_decisoes,
                        multi = True
                    ),
                    dbc.Button(
                        className = "dropdown-button",
                        children = ["Selecionar Todos"],
                        id = ids_tjs.SELECT_ALL_DECISOES_TJS_BUTTON,
                        n_clicks = 0
                    ),
                ]),
                dbc.Row([
                    html.H4("Ano Propositura"),
                    dcc.RangeSlider(
                        min = minimo_ano_propositura,
                        max = maximo_ano_propositura,
                        step = 1,
                        value = [minimo_ano_propositura, maximo_ano_propositura],
                        id = ids_tjs.PROPOSITURA_TJS_SLIDER,
                        tooltip =  {
                            "placement":"bottom",
                            "always_visible":True,
                        },
                        marks = {
                            x: {"label": str(x),
                                "style":{
                                    "transform":"rotate(-90deg)"
                                },
                            }
                            for x in range(minimo_ano_propositura, maximo_ano_propositura + 1)
                        },
                        allowCross = False,
                    ),
                ]),
                dbc.Row([
                    html.H4("Ano Julgamento"),
                    dcc.RangeSlider(
                        min = minimo_ano_julgamento,
                        max = maximo_ano_julgamento,
                        step = 1,
                        value = [minimo_ano_julgamento, maximo_ano_julgamento],
                        id = ids_tjs.JULGAMENTO_TJS_SLIDER,
                        tooltip =  {
                            "placement":"bottom",
                            "always_visible":True,
                        },
                        marks = {
                            x: {"label": str(x),
                                "style":{
                                    "transform":"rotate(-90deg)"
                                },
                            }
                            for x in range(minimo_ano_julgamento, maximo_ano_julgamento + 1)
                        },
                        allowCross = False,
                    ),
                ]),
            ],fluid = True),
            id = ids_tjs.OCULTAR_FILTROS_TJS_COLLAPSE,
            is_open = False
        ),
        html.Hr(),
        dbc.Container([
            dbc.Row([
                #dbc.Col(
                #    xs = 0, sm = 0, md = 0, lg = 0, xl = 1, xxl = 1,
                #),
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id = ids_tjs.ESTADOS_BUBBLE_MAP,
                            style = {
                                "align-items":"center",
                                #"margin-left":"-20px",
                            }
                        ),
                        id = ids_tjs.CONTAINER_ESTADOS_TJ,
                    ),
                    xs = 12, sm = 12, md = 12, lg = 6, xl = 6, xxl = 6,
                ),
                #dbc.Col(
                #    xs = 1, sm = 1, md = 1, lg = 0, xl = 0, xxl = 0,
                #),
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id = ids_tjs.DURACAO_TJS_GAUGE_CHART,
                        ),
                        id = ids_tjs.CONTAINER_DURACAO_TJ,
                    ),
                    xs = 12, sm = 12, md = 12, lg = 6, xl = 6, xxl = 6,
                ),
            ]),
            dbc.Row([
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id = ids_tjs.RUBRICA_TJS_PIE_CHART,
                        ),
                        id = ids_tjs.CONTAINER_RUBRICAS_TJ,
                    ),
                    xs = 12, sm = 12, md = 12, lg = 6, xl = 6, xxl = 6,
                ),
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id = ids_tjs.DECISOES_TJS_PIE_CHART,
                        ),
                        id = ids_tjs.CONTAINER_DECISOES_TJ,
                    ),
                    xs = 12, sm = 12, md = 12, lg = 6, xl = 6, xxl = 6,
                ),
            ]),
            dbc.Row([
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id = ids_tjs.PROPOSITURA_TJS_BAR_CHART,
                        ),
                        id = ids_tjs.CONTAINER_PROPOSITURA_TJ,
                    ),
                    xs = 12, sm = 12, md = 12, lg = 6, xl = 6, xxl = 6,
                ),
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id = ids_tjs.JULGAMENTO_TJS_BAR_CHART,
                        ),
                        id = ids_tjs.CONTAINER_JULGAMENTO_TJ,
                    ),
                    xs = 12, sm = 12, md = 12, lg = 6, xl = 6, xxl = 6,
                ),
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div(
                        html.Label(
                            "Tabela de Dados Gerais",
                        ),
                        style = {
                            "textAlign":"center",
                        },
                    ),
                    html.Div(
                        id = ids_tjs.CONTAINER_RESUMO_TJ,
                    ),
                    html.Div([
                        dbc.Button(
                            "Baixar tabela em .csv",
                            id = ids_tjs.DOWNLOAD_CSV_TJS_BUTTON,
                        ),
                        dcc.Download(
                            id = ids_tjs.DOWNLOAD_CSV_TJS,
                        )
                    ]),
                ]),
            ]),
        ],
        fluid = True,
        ),
    ]
)

@callback(
    Output(ids_tjs.OCULTAR_FILTROS_TJS_COLLAPSE, "is_open"),
    Input(ids_tjs.OCULTAR_FILTROS_TJS_BUTTON, "n_clicks"),
    State(ids_tjs.OCULTAR_FILTROS_TJS_COLLAPSE, "is_open",)
)
def filtros(n, is_open):
    if n:
        return not is_open
    return is_open

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
    Output(ids_tjs.RUBRICA_TJS_DROPDOWN, "value"),
    Input(ids_tjs.SELECT_ALL_RUBRICAS_TJS_BUTTON, "n_clicks"),
)
def select_all_rubricas(_:str) -> list[str]:
    return unique_rubricas

@callback(
    Output(ids_tjs.DECISAO_TJS_DROPDOWN, "value"),
    Input(ids_tjs.SELECT_ALL_DECISOES_TJS_BUTTON, "n_clicks"),
)
def select_all_decisoes(_:str) -> list[str]:
    return unique_decisoes


@callback(
    Output(ids_tjs.DURACAO_TJS_GAUGE_CHART, "figure"),
    Input(ids_tjs.TRIBUNAL_TJS_DROPDOWN, "value"),
    Input(ids_tjs.RUBRICA_TJS_DROPDOWN, "value"),
    Input(ids_tjs.DECISAO_TJS_DROPDOWN, "value"),
    Input(ids_tjs.PROPOSITURA_TJS_SLIDER, "value"),
    Input(ids_tjs.JULGAMENTO_TJS_SLIDER, "value"),
    Input(ids_tjs.ESTADOS_BUBBLE_MAP, "clickData"),
    Input(ids_tjs.RUBRICA_TJS_PIE_CHART, "clickData"),
    Input(ids_tjs.DECISOES_TJS_PIE_CHART, "clickData"),
    Input(ids_tjs.JULGAMENTO_TJS_BAR_CHART, "clickData"),
    Input(ids_tjs.PROPOSITURA_TJS_BAR_CHART, "clickData"),
)
def update_duracao_chart(tribunais:list[str], rubricas:list[str], decisoes:list[str], ano_propositura:list[int], ano_julgamento:list[int], *args) -> go.Figure:
    ctx = callback_context

    filtered_data = filter_database(tribunais, rubricas, decisoes, ano_propositura, ano_julgamento)

    filtered_data = check_click_data(filtered_data, 'duracao', ctx)

    minimo_duracao = filtered_data[DataSchemaTJ.TEMPO_MEDIO].min()
    maximo_duracao = filtered_data[DataSchemaTJ.TEMPO_MEDIO].max()
    medio_duracao = filtered_data[DataSchemaTJ.TEMPO_MEDIO].mean()

    duracao_gauge = go.Indicator(
        mode = "gauge+number",
        value = medio_duracao,
        number = {
            'font':{
                'size':30,
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
                    'size':10
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
    Input(ids_tjs.RUBRICA_TJS_DROPDOWN, "value"),
    Input(ids_tjs.DECISAO_TJS_DROPDOWN, "value"),
    Input(ids_tjs.PROPOSITURA_TJS_SLIDER, "value"),
    Input(ids_tjs.JULGAMENTO_TJS_SLIDER, "value"),
    Input(ids_tjs.RUBRICA_TJS_PIE_CHART, "clickData"),
    Input(ids_tjs.ESTADOS_BUBBLE_MAP, "clickData"),
    Input(ids_tjs.DECISOES_TJS_PIE_CHART, "clickData"),
    Input(ids_tjs.JULGAMENTO_TJS_BAR_CHART, "clickData"),
    Input(ids_tjs.PROPOSITURA_TJS_BAR_CHART, "clickData"),
)
def update_rubrica_chart(tribunais:list[str], rubricas:list[str], decisoes:list[str], ano_propositura:list[int], ano_julgamento:list[int], click_data, *args) -> go.Figure:
    ctx = callback_context

    filtered_data = filter_database(tribunais, rubricas, decisoes, ano_propositura, ano_julgamento)

    filtered_data = check_click_data(filtered_data, 'rubrica', ctx)

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
            textinfo = 'percent+value',
            # textposition = 'outside',
            hole = 0.5,
            sort = False
        )
    else:
        rubrica_donut = go.Pie(
            labels = df_rubrica[DataSchemaTJ.RUBRICA].tolist(),
            values = df_rubrica['Total'],
            textinfo = 'percent+value',
            # textposition = 'outside',
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
    Input(ids_tjs.RUBRICA_TJS_DROPDOWN, "value"),
    Input(ids_tjs.DECISAO_TJS_DROPDOWN, "value"),
    Input(ids_tjs.PROPOSITURA_TJS_SLIDER, "value"),
    Input(ids_tjs.JULGAMENTO_TJS_SLIDER, "value"),
    Input(ids_tjs.DECISOES_TJS_PIE_CHART, "clickData"),
    Input(ids_tjs.RUBRICA_TJS_PIE_CHART, "clickData"),
    Input(ids_tjs.ESTADOS_BUBBLE_MAP, "clickData"),
    Input(ids_tjs.JULGAMENTO_TJS_BAR_CHART, "clickData"),
    Input(ids_tjs.PROPOSITURA_TJS_BAR_CHART, "clickData"),
)
def update_decisao_chart(tribunais:list[str], rubricas:list[str], decisoes:list[str], ano_propositura:list[int], ano_julgamento:list[int], click_data, *args) -> go.Figure:
    ctx = callback_context

    filtered_data = filter_database(tribunais, rubricas, decisoes, ano_propositura, ano_julgamento)

    filtered_data = check_click_data(filtered_data, 'decisao', ctx)

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
            textinfo = 'percent+value',
            # textposition = 'outside',
            hole = 0.5,
            sort = False
        )
    else:
        decisoes_donut = go.Pie(
            labels = df_decisoes[DataSchemaTJ.ECAD].tolist(),
            values = df_decisoes['Total'],
            textinfo = 'percent+value',
            # textposition = 'outside',
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
    Input(ids_tjs.RUBRICA_TJS_DROPDOWN, "value"),
    Input(ids_tjs.DECISAO_TJS_DROPDOWN, "value"),
    Input(ids_tjs.PROPOSITURA_TJS_SLIDER, "value"),
    Input(ids_tjs.JULGAMENTO_TJS_SLIDER, "value"),
    Input(ids_tjs.PROPOSITURA_TJS_BAR_CHART, "clickData"),
    Input(ids_tjs.DECISOES_TJS_PIE_CHART, "clickData"),
    Input(ids_tjs.RUBRICA_TJS_PIE_CHART, "clickData"),
    Input(ids_tjs.ESTADOS_BUBBLE_MAP, "clickData"),
    Input(ids_tjs.JULGAMENTO_TJS_BAR_CHART, "clickData"),
)
def update_propositura_chart(tribunais:list[str], rubricas:list[str], decisoes:list[str], ano_propositura:list[int], ano_julgamento:list[int], click_data, *args) -> go.Figure:
    ctx = callback_context

    filtered_data = filter_database(tribunais, rubricas, decisoes, ano_propositura, ano_julgamento)

    filtered_data = check_click_data(filtered_data, 'propositura', ctx)

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
            'title':'Processos Protocolados por Ano',
            'title_x':0.5,
            'title_y':0.95,
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
    Input(ids_tjs.RUBRICA_TJS_DROPDOWN, "value"),
    Input(ids_tjs.DECISAO_TJS_DROPDOWN, "value"),
    Input(ids_tjs.PROPOSITURA_TJS_SLIDER, "value"),
    Input(ids_tjs.JULGAMENTO_TJS_SLIDER, "value"),
    Input(ids_tjs.JULGAMENTO_TJS_BAR_CHART, "clickData"),
    Input(ids_tjs.DECISOES_TJS_PIE_CHART, "clickData"),
    Input(ids_tjs.RUBRICA_TJS_PIE_CHART, "clickData"),
    Input(ids_tjs.ESTADOS_BUBBLE_MAP, "clickData"),
    Input(ids_tjs.PROPOSITURA_TJS_BAR_CHART, "clickData"),
)
def update_julgamento_chart(tribunais:list[str], rubricas:list[str], decisoes:list[str], ano_propositura:list[int], ano_julgamento:list[int], click_data, *args) -> go.Figure:
    ctx = callback_context

    filtered_data = filter_database(tribunais, rubricas, decisoes, ano_propositura, ano_julgamento)

    filtered_data = check_click_data(filtered_data, 'julgamento', ctx)

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
            'title_x':0.5,
            'title_y':0.95,
            'xaxis':{
                'title':'Total',
            },
            'yaxis':{
                'title':'Ano',
            },
        },
    )
    return fig

@callback(
    Output(ids_tjs.ESTADOS_BUBBLE_MAP, "figure"),
    Input(ids_tjs.TRIBUNAL_TJS_DROPDOWN, "value"),
    Input(ids_tjs.RUBRICA_TJS_DROPDOWN, "value"),
    Input(ids_tjs.DECISAO_TJS_DROPDOWN, "value"),
    Input(ids_tjs.PROPOSITURA_TJS_SLIDER, "value"),
    Input(ids_tjs.JULGAMENTO_TJS_SLIDER, "value"),
    Input(ids_tjs.ESTADOS_BUBBLE_MAP, "clickData"),
    Input(ids_tjs.RUBRICA_TJS_PIE_CHART, "clickData"),
    Input(ids_tjs.DECISOES_TJS_PIE_CHART, "clickData"),
    Input(ids_tjs.JULGAMENTO_TJS_BAR_CHART, "clickData"),
    Input(ids_tjs.PROPOSITURA_TJS_BAR_CHART, "clickData"),
)
def update_estados_chart(tribunais:list[str], rubricas:list[str], decisoes:list[str], ano_propositura:list[int], ano_julgamento:list[int], click_data, *args) -> go.Figure:
    ctx = callback_context

    filtered_data = filter_database(tribunais, rubricas, decisoes, ano_propositura, ano_julgamento)

    filtered_data = check_click_data(filtered_data, 'estado', ctx)

    df_tjs = filtered_data.groupby([DataSchemaTJ.TRIBUNAL_ORIGEM])[DataSchemaTJ.TRIBUNAL_ORIGEM].count().reset_index(name = 'Total')

    if click_data and ids_tjs.ESTADOS_BUBBLE_MAP in ctx.triggered[0]["prop_id"] and ctx.triggered[0]["value"]:
        tribunal = ctx.triggered[0]["value"]["points"][0]["customdata"][0]
        df_tjs = df_tjs[df_tjs[DataSchemaTJ.TRIBUNAL_ORIGEM] == tribunal]
    else:
        pass

    df_mapa = pd.merge(df_cities, df_tjs, left_on = 'tj', right_on = DataSchemaTJ.TRIBUNAL_ORIGEM)

    fig = px.scatter_mapbox(
        df_mapa,
        title = 'Distribuição de TJS',
        lat = 'lat',
        lon = 'lng',
        size = 'Total',
        size_max = 35,
        #color = 'Total',
        width = 500,
        center = {
            'lat': -14.261945692605,
            'lon': -54.35861446795,
        },
        hover_data = {
            DataSchemaTJ.TRIBUNAL_ORIGEM:True,
            'Total':True,
            'lat':False,
            'lng':False
        },
        zoom = 2,
        mapbox_style = 'open-street-map',
    )

    fig.update_layout(
        title_x = 0.5,
        title_y = 0.95,
        margin = {
            "autoexpand":False,
            "l":20,
        },
    )
    return fig

@callback(
    Output(ids_tjs.CONTAINER_RESUMO_TJ, "children"),
    Input(ids_tjs.TRIBUNAL_TJS_DROPDOWN, "value"),
    Input(ids_tjs.RUBRICA_TJS_DROPDOWN, "value"),
    Input(ids_tjs.DECISAO_TJS_DROPDOWN, "value"),
    Input(ids_tjs.PROPOSITURA_TJS_SLIDER, "value"),
    Input(ids_tjs.JULGAMENTO_TJS_SLIDER, "value"),
)
def update_resumo_table(tribunais:list[str], rubricas:list[str], decisoes:list[str], ano_propositura:list[int], ano_julgamento:list[int]) -> dash_table.DataTable:

    filtered_data = filter_database(tribunais, rubricas, decisoes, ano_propositura, ano_julgamento)

    data_tjs = filtered_data.to_dict('records')
    cols_tjs = [{"name":i, "id":i} for i in filtered_data.columns]

    return dash_table.DataTable(
        data = data_tjs,
        columns = cols_tjs,
        fixed_rows = {
            'headers':True
        },
        style_header = {
            'backgroundColor': 'rgb(180, 180, 180)',
            'border':'1px solid black',
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(220, 220, 220)',
            }
        ],
        style_cell = {
            'textAlign':'left',
            'border':'1px solid black',
            'minWidth': '200px',
        },
        style_table = {
            'height':500,
            'overflowY':'auto',
            'textAlign':'left',
        }
    )

@callback(
    Output(ids_tjs.DOWNLOAD_CSV_TJS, "data"),
    Input(ids_tjs.TRIBUNAL_TJS_DROPDOWN, "value"),
    Input(ids_tjs.RUBRICA_TJS_DROPDOWN, "value"),
    Input(ids_tjs.DECISAO_TJS_DROPDOWN, "value"),
    Input(ids_tjs.PROPOSITURA_TJS_SLIDER, "value"),
    Input(ids_tjs.JULGAMENTO_TJS_SLIDER, "value"),
    Input(ids_tjs.DOWNLOAD_CSV_TJS_BUTTON, "n_clicks"),
    prevent_initial_call = True,
)
def download_table(tribunais:list[str], rubricas:list[str], decisoes:list[str], ano_propositura:list[int], ano_julgamento:list[int], click_button):

    ctx = callback_context

    if ids_tjs.DOWNLOAD_CSV_TJS_BUTTON in ctx.triggered[0]["prop_id"]:
        filtered_data = filter_database(tribunais, rubricas, decisoes, ano_propositura, ano_julgamento)
        return dcc.send_data_frame(filtered_data.to_csv, "TabelaDados_Dash_TJS.csv", encoding = "utf-8", index = False)

def filter_database(tribunais:list[str], rubricas:list[str], decisoes:list[str], ano_propositura:list[int], ano_julgamento: list[int]) -> pd.DataFrame:

    new_df = data.copy()

    if tribunais:
        new_df = data[data[DataSchemaTJ.TRIBUNAL_ORIGEM].isin(tribunais)]

    if rubricas:
        new_df = new_df[new_df[DataSchemaTJ.RUBRICA].isin(rubricas)]

    if decisoes:
        new_df = new_df[new_df[DataSchemaTJ.ECAD].isin(decisoes)]

    if ano_propositura[0] == ano_propositura[1]:
        new_df = new_df[new_df[DataSchemaTJ.ANO_PROPOSITURA].dt.year == ano_propositura[0]]
    else:
        new_df = new_df[(new_df[DataSchemaTJ.ANO_PROPOSITURA].dt.year >= ano_propositura[0])&(new_df[DataSchemaTJ.ANO_PROPOSITURA].dt.year <= ano_propositura[1])]

    if ano_julgamento[0] == ano_julgamento[1]:
        new_df = new_df[new_df[DataSchemaTJ.DATA_JULGAMENTO].dt.year == ano_julgamento[0]]
    else:
        new_df = new_df[(new_df[DataSchemaTJ.DATA_JULGAMENTO].dt.year >= ano_julgamento[0])&(new_df[DataSchemaTJ.DATA_JULGAMENTO].dt.year <= ano_julgamento[1])]

    return new_df

def check_click_data(df_click:pd.DataFrame, chart:str, click_context:CallbackContext) -> pd.DataFrame:
    if not click_context.triggered[0]["value"]:
        return df_click
    else:
        if ids_tjs.ESTADOS_BUBBLE_MAP in click_context.triggered[0]["prop_id"] and chart != 'estado':
            selected = click_context.triggered[0]["value"]["points"][0]["customdata"][0]
            df_click = df_click[df_click[DataSchemaTJ.TRIBUNAL_ORIGEM] == selected]
            pass
        if ids_tjs.RUBRICA_TJS_PIE_CHART in click_context.triggered[0]["prop_id"] and chart != 'rubrica':
            selected = click_context.triggered[0]["value"]["points"][0]["label"]
            df_click = df_click[df_click[DataSchemaTJ.RUBRICA] == selected]
            pass
        if ids_tjs.DECISOES_TJS_PIE_CHART in click_context.triggered[0]["prop_id"] and chart != 'decisao':
            selected = click_context.triggered[0]["value"]["points"][0]["label"]
            df_click = df_click[df_click[DataSchemaTJ.ECAD] == selected]
            pass
        if ids_tjs.JULGAMENTO_TJS_BAR_CHART in click_context.triggered[0]["prop_id"] and chart != 'julgamento':
            selected = click_context.triggered[0]["value"]["points"][0]["label"]
            df_click = df_click[df_click[DataSchemaTJ.DATA_JULGAMENTO].dt.year == int(selected)]
            pass
        if ids_tjs.PROPOSITURA_TJS_BAR_CHART in click_context.triggered[0]["prop_id"] and chart != 'propositura':
            selected = click_context.triggered[0]["value"]["points"][0]["label"]
            df_click = df_click[df_click[DataSchemaTJ.ANO_PROPOSITURA].dt.year == int(selected)]
            pass
        return df_click
