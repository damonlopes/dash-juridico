import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from dash import dcc, html, register_page, callback, Output, Input, callback_context
from .data.loader import load_dashboard_data, DataSchemaSTJ
from .components.ids import ids_stj
from pathlib import Path

THIS_FOLDER = Path(__file__).parent.resolve()
DATA_PATH = THIS_FOLDER / "data/Planilha BI FINAL.xlsx"
data = load_dashboard_data(DATA_PATH, "Planilha2")

unique_tribunais = sorted(set(data[DataSchemaSTJ.TRIBUNAL_ORIGEM].tolist()), key = str)

register_page(
    __name__,
    path = '/stj',
    name = 'Dashboard STJ',
    title = 'Dashboard STJ')

layout = html.Div(
    children = [
        dbc.Container([
            dbc.Row([
                html.H4("STJ"),
                dcc.Dropdown(
                    id = ids_stj.TRIBUNAL_STJ_DROPDOWN,
                    options = [{"label": tribunal, "value": tribunal} for tribunal in unique_tribunais],
                    value = unique_tribunais,
                    multi = True,
                ),
                html.Button(
                    className = "dropdown-button",
                    children = ["Selecionar Todos"],
                    id = ids_stj.SELECT_ALL_TRIBUNAIS_STJ_BUTTON,
                    n_clicks = 0,
                ),
            ]),
            dbc.Row([
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id = ids_stj.RUBRICA_STJ_PIE_CHART,
                        ),
                        id = ids_stj.CONTAINER_RUBRICA_STJ,
                    ),
                ),
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id = ids_stj.CAMARA_STJ_PIE_CHART,
                        ),
                        id = ids_stj.CONTAINER_CAMARA_STJ,
                    )
                ),
            ]),
            dbc.Row([
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id = ids_stj.JULGAMENTO_STJ_BAR_CHART,
                        ),
                        id = ids_stj.CONTAINER_JULGAMENTO_STJ,
                    ),
                ),
            ]),
            dbc.Row([
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id = ids_stj.ACAO_STJ_BAR_CHART,
                        ),
                        style = {
                            'overflow-y':'auto',
                            'maxHeight': '500px'
                        },
                        id = ids_stj.CONTAINER_ACAO_STJ,
                    ),
                ),
            ]),
        ]),
    ]
)

@callback(
    Output(ids_stj.TRIBUNAL_STJ_DROPDOWN, "value"),
    Output(ids_stj.RUBRICA_STJ_PIE_CHART, "clickData"),
    Output(ids_stj.CAMARA_STJ_PIE_CHART, "clickData"),
    Output(ids_stj.ACAO_STJ_BAR_CHART, "clickData"),
    Output(ids_stj.JULGAMENTO_STJ_BAR_CHART, "clickData"),
    Input(ids_stj.SELECT_ALL_TRIBUNAIS_STJ_BUTTON, "n_clicks")
)
def select_all_tribunais(_:str) -> list[str]:
    return unique_tribunais, None, None, None, None

@callback(
    Output(ids_stj.RUBRICA_STJ_PIE_CHART, "figure"),
    Input(ids_stj.TRIBUNAL_STJ_DROPDOWN, "value"),
    Input(ids_stj.RUBRICA_STJ_PIE_CHART, "clickData"),
    Input(ids_stj.CAMARA_STJ_PIE_CHART, "clickData"),
    Input(ids_stj.ACAO_STJ_BAR_CHART, "clickData"),
    Input(ids_stj.JULGAMENTO_STJ_BAR_CHART, "clickData"),

)
def update_rubrica_chart(tribunais:list[str], click_data, *args) -> go.Figure:
    ctx = callback_context

    if not tribunais:
        filtered_data = data.copy()
    else:
        filtered_data = data[data[DataSchemaSTJ.TRIBUNAL_ORIGEM].isin(tribunais)].copy()

    if not ctx.triggered[0]["value"]:
        pass
    else:
        if ids_stj.CAMARA_STJ_PIE_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaSTJ.CAMARA_TURMA_SECAO] == selected]
            pass
        if ids_stj.ACAO_STJ_BAR_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaSTJ.TIPO_ACAO] == selected]
            pass
        if ids_stj.JULGAMENTO_STJ_BAR_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaSTJ.DATA_JULGAMENTO].dt.year == int(selected)]
            pass

    df_rubrica = filtered_data.groupby([DataSchemaSTJ.RUBRICA])[DataSchemaSTJ.RUBRICA].count().reset_index(name = 'Total')

    if click_data and ids_stj.RUBRICA_STJ_PIE_CHART in ctx.triggered[0]["prop_id"] and ctx.triggered[0]["value"]:
        rubrica = ctx.triggered[0]["value"]["points"][0]["label"]
        lista_rubricas = df_rubrica[DataSchemaSTJ.RUBRICA].unique().tolist()
        lista_rubricas.remove(rubrica)
        lista_rubricas.insert(0, rubrica)
        df_rubrica[DataSchemaSTJ.RUBRICA] = pd.Categorical(df_rubrica[DataSchemaSTJ.RUBRICA], categories = lista_rubricas)
        df_rubrica = df_rubrica.sort_values(DataSchemaSTJ.RUBRICA)

        rubrica_donut = go.Pie(
            labels = df_rubrica[DataSchemaSTJ.RUBRICA].tolist(),
            values = df_rubrica['Total'],
            pull = [0.2],
            textinfo = 'percent',
            textposition = 'outside',
            hole = 0.5,
            sort = False,
        )
    else:
        rubrica_donut = go.Pie(
            labels = df_rubrica[DataSchemaSTJ.RUBRICA].tolist(),
            values = df_rubrica['Total'],
            textinfo = 'percent',
            textposition = 'outside',
            hole = 0.5,
        )

    fig = go.Figure(
        data = [rubrica_donut],
        layout = {
            'title': {
                'text': 'Rubricas',
                'x': 0.5,
                'xanchor': 'center',
                'y': 1,
                'yanchor': 'top',
                'font':{
                    'size': 18
                },
            },
            'legend':{
                'title':'Rubricas',
            },
        },
    )

    fig.update_layout(margin = {"t":40, "b":0, "l":0, "r":0})
    fig.update_traces(hovertemplate = "%{label}<br>%{value}<extra></extra>")

    return fig
    # return html.Div(
    #     dcc.Graph(
    #         figure = fig
    #     ),
    #     id = ids_stj.RUBRICA_STJ_PIE_CHART
    # )

@callback(
    Output(ids_stj.CAMARA_STJ_PIE_CHART, "figure"),
    Input(ids_stj.TRIBUNAL_STJ_DROPDOWN, "value"),
    Input(ids_stj.CAMARA_STJ_PIE_CHART, "clickData"),
    Input(ids_stj.RUBRICA_STJ_PIE_CHART, "clickData"),
    Input(ids_stj.ACAO_STJ_BAR_CHART, "clickData"),
    Input(ids_stj.JULGAMENTO_STJ_BAR_CHART, "clickData"),
)
def update_camara_chart(tribunais:list[str], click_data, *args) -> go.Figure:
    ctx = callback_context

    if not tribunais:
        filtered_data = data.copy()
    else:  
        filtered_data = data[data[DataSchemaSTJ.TRIBUNAL_ORIGEM].isin(tribunais)].copy()

    if not ctx.triggered[0]["value"]:
        pass
    else:
        if ids_stj.RUBRICA_STJ_PIE_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaSTJ.RUBRICA] == selected]
            pass
        if ids_stj.ACAO_STJ_BAR_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaSTJ.TIPO_ACAO] == selected]
            pass
        if ids_stj.JULGAMENTO_STJ_BAR_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaSTJ.DATA_JULGAMENTO].dt.year == int(selected)]
            pass
    
    df_camara = filtered_data.groupby([DataSchemaSTJ.CAMARA_TURMA_SECAO])[DataSchemaSTJ.CAMARA_TURMA_SECAO].count().reset_index(name = 'Total')

    if click_data and ids_stj.CAMARA_STJ_PIE_CHART in ctx.triggered[0]["prop_id"] and ctx.triggered[0]["value"]:
        camara = ctx.triggered[0]["value"]["points"][0]["label"]
        lista_camaras = df_camara[DataSchemaSTJ.CAMARA_TURMA_SECAO].unique().tolist()
        lista_camaras.remove(camara)
        lista_camaras.insert(0, camara)
        df_camara[DataSchemaSTJ.CAMARA_TURMA_SECAO] = pd.Categorical(df_camara[DataSchemaSTJ.CAMARA_TURMA_SECAO], categories = lista_camaras)
        df_camara = df_camara.sort_values(DataSchemaSTJ.CAMARA_TURMA_SECAO)

        camara_donut = go.Pie(
            labels = df_camara[DataSchemaSTJ.CAMARA_TURMA_SECAO].tolist(),
            values = df_camara['Total'],
            pull = [0.2],
            textinfo = 'percent',
            textposition = 'outside',
            hole = 0.5,
            sort = False,
        )
    else:
        camara_donut = go.Pie(
            labels = df_camara[DataSchemaSTJ.CAMARA_TURMA_SECAO].tolist(),
            values = df_camara['Total'],
            textinfo = 'percent',
            textposition = 'outside',
            hole = 0.5,
        )

    fig = go.Figure(
        data = [camara_donut],
        layout = {
            'title': {
                'text': DataSchemaSTJ.CAMARA_TURMA_SECAO,
                'x': 0.5,
                'xanchor': 'center',
                'y': 1,
                'yanchor': 'top',
                'font':{
                    'size': 18,
                },
            },
            'legend':{
                'title':DataSchemaSTJ.CAMARA_TURMA_SECAO
            },
        },
    )
    # rubrica_donut = go.Pie(
    #     labels = df_camara[DataSchemaSTJ.CAMARA_TURMA_SECAO].tolist(),
    #     values = df_camara['Total'],
    #     textinfo = 'percent',
    #     textposition = 'outside',
    #     hole = 0.5
    # )

    # fig = go.Figure(
    #     data = [rubrica_donut],
    #     layout = {
    #         'title': {
    #             'text': 'Câmara/Turma/Seção'
    #         }
    #     }
    # )

    fig.update_layout(margin = {"t":40, "b":0, "l":0, "r":0})
    fig.update_traces(hovertemplate = "%{label}<br>%{value}<extra></extra>")

    return fig
    # return html.Div(
    #     dcc.Graph(
    #         figure = fig
    #     ),
    #     id = ids_stj.CAMARA_STJ_PIE_CHART
    # )

@callback(
    Output(ids_stj.ACAO_STJ_BAR_CHART, "figure"),
    Input(ids_stj.TRIBUNAL_STJ_DROPDOWN, "value"),
    Input(ids_stj.ACAO_STJ_BAR_CHART, "clickData"),
    Input(ids_stj.RUBRICA_STJ_PIE_CHART, "clickData"),
    Input(ids_stj.CAMARA_STJ_PIE_CHART, "clickData"),
    Input(ids_stj.JULGAMENTO_STJ_BAR_CHART, "clickData"),
)
def update_acao_chart(tribunais:list[str], click_data, *args) -> go.Figure:
    ctx = callback_context
    if not tribunais:
        filtered_data = data.copy()
    else:
        filtered_data = data[data[DataSchemaSTJ.TRIBUNAL_ORIGEM].isin(tribunais)].copy()

    if not ctx.triggered[0]["value"]:
        pass
    else:
        if ids_stj.RUBRICA_STJ_PIE_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaSTJ.RUBRICA] == selected]
            pass
        if ids_stj.CAMARA_STJ_PIE_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaSTJ.CAMARA_TURMA_SECAO] == selected]
            pass
        if ids_stj.JULGAMENTO_STJ_BAR_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaSTJ.DATA_JULGAMENTO].dt.year == int(selected)]
            pass

    df_propositura = filtered_data.groupby([DataSchemaSTJ.TIPO_ACAO])[DataSchemaSTJ.TIPO_ACAO].count().reset_index(name = 'Total').sort_values('Total')

    if click_data and ids_stj.ACAO_STJ_BAR_CHART in ctx.triggered[0]["prop_id"] and ctx.triggered[0]["value"]:
        acao = ctx.triggered[0]["value"]["points"][0]["label"]
    else:
        acao = ''    
    
    lista_acoes = df_propositura[DataSchemaSTJ.TIPO_ACAO].unique().tolist()

    def selected_bar(lista_acoes):
        if lista_acoes == acao:
            return "red"
        else:
            return "cornflowerblue"
        
    acao_bar = go.Bar(
        # x = df_propositura['Tipo de ação'],
        # y = df_propositura['Total'],
        x = df_propositura['Total'],
        y = df_propositura[DataSchemaSTJ.TIPO_ACAO],
        orientation = 'h',
        marker = dict(
            color = list(
                map(
                    selected_bar, lista_acoes
                ),
            ),
        ),
    )

    fig = go.Figure(
        data = [acao_bar],
        layout = {
            'title':'Tipo de Ação',
            'xaxis':{
                'title':'Ano'
            },
            'yaxis':{
                'title':'Total'
            },
        },
        # layout = {
        #     'height':5000
        # }
    )

    fig.update_layout(
        barmode = 'group',
        bargap = 0.2,
        bargroupgap = 0.0,
        height = 1000,
        # sliders = {
        #     'active' : 0
        # }
        
    )

    # fig = px.bar(
    #     df_propositura,
    #     x = 'Total',
    #     y = 'Tipo de ação',
    #     title = 'Tipo de Ação',
    #     orientation = 'h',
    # )

    return fig

@callback(
    Output(ids_stj.JULGAMENTO_STJ_BAR_CHART, "figure"),
    Input(ids_stj.TRIBUNAL_STJ_DROPDOWN, "value"),
    Input(ids_stj.JULGAMENTO_STJ_BAR_CHART, "clickData"),
    Input(ids_stj.RUBRICA_STJ_PIE_CHART, "clickData"),
    Input(ids_stj.CAMARA_STJ_PIE_CHART, "clickData"),
    Input(ids_stj.ACAO_STJ_BAR_CHART, "clickData"),
)
def update_julgamento_chart(tribunais:list[str], click_data, *args) -> go.Figure:
    ctx = callback_context
    if not tribunais:
        filtered_data = data.copy()
    else:
        filtered_data = data[data[DataSchemaSTJ.TRIBUNAL_ORIGEM].isin(tribunais)].copy().copy()

    if not ctx.triggered[0]["value"]:
        pass
    else:
        if ids_stj.RUBRICA_STJ_PIE_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaSTJ.RUBRICA] == selected]
            pass
        if ids_stj.CAMARA_STJ_PIE_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaSTJ.CAMARA_TURMA_SECAO] == selected]
            pass
        if ids_stj.ACAO_STJ_BAR_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaSTJ.TIPO_ACAO] == selected]
            pass

    filtered_data['Ano'] = filtered_data[DataSchemaSTJ.DATA_JULGAMENTO].dt.year

    df_julgamento = filtered_data[[DataSchemaSTJ.TRIBUNAL_ORIGEM, 'Ano']].groupby(['Ano'])[DataSchemaSTJ.TRIBUNAL_ORIGEM].count().reset_index(name = 'Total')

    if click_data and ids_stj.JULGAMENTO_STJ_BAR_CHART in ctx.triggered[0]["prop_id"] and ctx.triggered[0]["value"]:
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
        x = df_julgamento["Ano"],
        y = df_julgamento["Total"],
        marker = dict(
            color = list(
                map(
                    selected_bar, lista_anos
                ),
            ),
        ),
    )

    fig = go.Figure(
        data = [julgamento_bar],
        layout = {
            'title':'Contagem de Tribunal de Origem por Data Julgamento',
            'xaxis':{
                'title':'Ano'
            },
            'yaxis':{
                'title':'Total'
            },
        },
    )

    # fig = px.bar(
    #     df_julgamento,
    #     x = 'Ano',
    #     y = 'Total',
    #     title = 'Contagem de Tribunal de Origem por Data Julgamento',
    #     # orientation = 'h'
    # )

    return fig
    # return html.Div(
    #     dcc.Graph(
    #         figure = fig
    #     ),
    #     id = ids_stj.JULGAMENTO_STJ_BAR_CHART
    # )

