import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash import dcc, html, register_page, callback, Output, Input, State, callback_context
from dash._callback_context import CallbackContext
from .data.loader import load_dashboard_data, DataSchemaTJ
from .components.ids import ids_rubrica
from pathlib import Path

THIS_FOLDER = Path(__file__).parent.resolve()
DATA_PATH = THIS_FOLDER / "data/Planilha BI FINAL.xlsx"
data = load_dashboard_data(DATA_PATH, "Planilha1")

unique_tribunais = sorted(set(data[DataSchemaTJ.TRIBUNAL_ORIGEM].tolist()), key = str)
unique_rubricas = sorted(set(data[DataSchemaTJ.RUBRICA].tolist()), key = str)
unique_decisoes = sorted(set(data[DataSchemaTJ.ECAD].tolist()), key = str)
unique_ativos = sorted(set(data[DataSchemaTJ.ATIVO].tolist()), key = str)
unique_passivos = sorted(set(data[DataSchemaTJ.PASSIVO].tolist()), key = str)

minimo_ano_propositura = data[DataSchemaTJ.ANO_PROPOSITURA].dt.year.min()
maximo_ano_propositura = data[DataSchemaTJ.ANO_PROPOSITURA].dt.year.max()
minimo_ano_julgamento = data[DataSchemaTJ.DATA_JULGAMENTO].dt.year.min()
maximo_ano_julgamento = data[DataSchemaTJ.DATA_JULGAMENTO].dt.year.max()

register_page(
    __name__,
    path = '/rubrica',
    name = 'Dashboard Rubrica',
    title = 'Dashboard Rubrica')

layout = html.Div(
    children = [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Button(
                        "Mostrar/Ocultar Filtros",
                        id = ids_rubrica.OCULTAR_FILTROS_RUBRICA_BUTTON,
                        n_clicks = 0
                        ),
                    ],
                    width = {
                        "size":3,
                    },
                ),
            ],
            justify = "right",
        ),
        html.Hr(),
        dbc.Collapse(
            dbc.Container([
                dbc.Row([
                    html.H4("Tribunal"),
                        dcc.Dropdown(
                            id = ids_rubrica.TRIBUNAL_RUBRICA_DROPDOWN,
                            options = [{"label": tribunal, "value": tribunal} for tribunal in unique_tribunais],
                            value = unique_tribunais,
                            multi = True,
                        ),
                        html.Button(
                            className = "dropdown-button",
                            children = ["Selecionar Todos"],
                            id = ids_rubrica.SELECT_ALL_TRIBUNAIS_RUBRICA_BUTTON,
                            n_clicks = 0,
                    ),
                ]),
                dbc.Row([
                    html.H4("Rubrica"),
                    dcc.Dropdown(
                        id = ids_rubrica.RUBRICA_DROPDOWN,
                        options = [{"label": rubrica, "value": rubrica} for rubrica in unique_rubricas],
                        value = unique_rubricas,
                        multi = True,
                    ),
                    html.Button(
                        className = "dropdown-button",
                        children = ["Selecionar Todos"],
                        id = ids_rubrica.SELECT_ALL_RUBRICAS_BUTTON,
                        n_clicks = 0,
                    ),
                ]),
                dbc.Row([
                    html.H4("Decisões"),
                    dcc.Dropdown(
                        id = ids_rubrica.DECISAO_RUBRICA_DROPDOWN,
                        options = [{"label": decisao, "value": decisao} for decisao in unique_decisoes],
                        value = unique_decisoes,
                        multi = True,
                    ),
                    html.Button(
                        className = "dropdown-button",
                        children = ["Selecionar Todos"],
                        id = ids_rubrica.SELECT_ALL_DECISOES_BUTTON,
                        n_clicks = 0,
                    ),
                ]),
                dbc.Row([
                    html.H4("Ativo"),
                    dcc.Dropdown(
                        id = ids_rubrica.ATIVO_RUBRICA_DROPDOWN,
                        options = [{"label": ativo, "value": ativo} for ativo in unique_ativos],
                        value = unique_ativos,
                        multi = True,
                    ),
                    html.Button(
                        className = "dropdown-button",
                        children = ["Selecionar Todos"],
                        id = ids_rubrica.SELECT_ALL_ATIVOS_BUTTON,
                        n_clicks = 0,
                    ),
                ]),
                dbc.Row([
                    html.H4("Passivo"),
                    dcc.Dropdown(
                        id = ids_rubrica.PASSIVO_RUBRICA_DROPDOWN,
                        options = [{"label": passivo, "value": passivo} for passivo in unique_passivos],
                        value = unique_passivos,
                        multi = True,
                    ),
                    html.Button(
                        className = "dropdown-button",
                        children = ["Selecionar Todos"],
                        id = ids_rubrica.SELECT_ALL_PASSIVOS_BUTTON,
                        n_clicks = 0,
                    ),
                ]),
                dbc.Row([
                    html.H4("Ano Propositura"),
                    dcc.RangeSlider(
                        min = minimo_ano_propositura,
                        max = maximo_ano_propositura,
                        step = 1,
                        value = [minimo_ano_propositura, maximo_ano_propositura],
                        id = ids_rubrica.PROPOSITURA_RUBRICA_SLIDER,
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
                        id = ids_rubrica.JULGAMENTO_RUBRICA_SLIDER,
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
            ]),            
            id = ids_rubrica.OCULTAR_FILTROS_RUBRICA_COLLAPSE,
            is_open = False
        ),
        html.Hr(),
        dbc.Container([
            dbc.Row([
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id = ids_rubrica.DURACAO_RUBRICA_GAUGE_CHART
                        ),
                        id = ids_rubrica.CONTAINER_DURACAO_RUBRICA,
                    ),
                ),
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id = ids_rubrica.DECISOES_RUBRICA_PIE_CHART
                        ),
                        id = ids_rubrica.CONTAINER_DECISOES_RUBRICA
                    ),
                ),
            ]),
            dbc.Row([
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id = ids_rubrica.ATIVO_RUBRICA_PIE_CHART,
                        ),
                        id = ids_rubrica.CONTAINER_ATIVO_RUBRICA,
                    ),
                ),
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id = ids_rubrica.PASSIVO_RUBRICA_PIE_CHART,
                        ),
                        id = ids_rubrica.CONTAINER_PASSIVO_RUBRICA,
                    ),
                ),
            ]),
            dbc.Row([
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id = ids_rubrica.PROPOSITURA_RUBRICA_BAR_CHART,
                        ),
                        id = ids_rubrica.CONTAINER_PROPOSITURA_RUBRICA,
                    ),
                ),
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id = ids_rubrica.JULGAMENTO_RUBRICA_BAR_CHART,
                        ),
                        id = ids_rubrica.CONTAINER_JULGAMENTO_RUBRICA,
                    ),
                ),
            ]),
        ]),
    ],
)

@callback(
    Output(ids_rubrica.OCULTAR_FILTROS_RUBRICA_COLLAPSE, "is_open"),
    Input(ids_rubrica.OCULTAR_FILTROS_RUBRICA_BUTTON, "n_clicks"),
    State(ids_rubrica.OCULTAR_FILTROS_RUBRICA_COLLAPSE, "is_open",)
)
def filtros(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output(ids_rubrica.TRIBUNAL_RUBRICA_DROPDOWN, "value"),
    Output(ids_rubrica.DECISOES_RUBRICA_PIE_CHART, "clickData"),
    Output(ids_rubrica.ATIVO_RUBRICA_PIE_CHART, "clickData"),
    Output(ids_rubrica.PASSIVO_RUBRICA_PIE_CHART, "clickData"),
    Output(ids_rubrica.PROPOSITURA_RUBRICA_BAR_CHART, "clickData"),
    Output(ids_rubrica.JULGAMENTO_RUBRICA_BAR_CHART, "clickData"),
    Input(ids_rubrica.SELECT_ALL_TRIBUNAIS_RUBRICA_BUTTON, "n_clicks"),
)
def select_all_tribunais(_:str, *args) -> list[str]:
    return unique_tribunais, None, None, None, None, None

@callback(
    Output(ids_rubrica.RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.SELECT_ALL_RUBRICAS_BUTTON, "n_clicks"),
)
def select_all_rubricas(_:str) -> list[str]:
    return unique_rubricas

@callback(
    Output(ids_rubrica.DECISAO_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.SELECT_ALL_DECISOES_BUTTON, "n_clicks"),
)
def select_all_decisoes(_:str) -> list[str]:
    return unique_decisoes

@callback(
    Output(ids_rubrica.ATIVO_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.SELECT_ALL_ATIVOS_BUTTON, "n_clicks"),
)
def select_all_ativos(_:str) -> list[str]:
    return unique_ativos

@callback(
    Output(ids_rubrica.PASSIVO_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.SELECT_ALL_PASSIVOS_BUTTON, "n_clicks"),
)
def select_all_passivos(_:str) -> list[str]:
    return unique_passivos


@callback(
    Output(ids_rubrica.DURACAO_RUBRICA_GAUGE_CHART, "figure"),
    Input(ids_rubrica.TRIBUNAL_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.DECISAO_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.ATIVO_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.PASSIVO_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.PROPOSITURA_RUBRICA_SLIDER, "value"),
    Input(ids_rubrica.JULGAMENTO_RUBRICA_SLIDER, "value"),
    Input(ids_rubrica.DECISOES_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.ATIVO_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.PASSIVO_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.PROPOSITURA_RUBRICA_BAR_CHART, "clickData"),
    Input(ids_rubrica.JULGAMENTO_RUBRICA_BAR_CHART, "clickData"),
)
def update_duracao_chart(tribunais:list[str], rubricas:list[str], decisoes:list[str], ativos:list[str], passivos:list[str], ano_propositura:list[int], ano_julgamento:list[int], *args) -> go.Figure:
    ctx = callback_context

    filtered_data = filter_database(tribunais, rubricas, decisoes, ativos, passivos, ano_propositura, ano_julgamento)

    filtered_data = check_click_data(filtered_data, 'duracao', ctx)
        
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
            "text":"Duração Média (anos)",
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
            },
        }
    )

    fig = go.Figure(
        data = [duracao_gauge]
    )
    
    return fig

@callback(
    Output(ids_rubrica.DECISOES_RUBRICA_PIE_CHART, "figure"),
    Input(ids_rubrica.TRIBUNAL_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.DECISAO_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.ATIVO_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.PASSIVO_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.PROPOSITURA_RUBRICA_SLIDER, "value"),
    Input(ids_rubrica.JULGAMENTO_RUBRICA_SLIDER, "value"),
    Input(ids_rubrica.DECISOES_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.ATIVO_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.PASSIVO_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.PROPOSITURA_RUBRICA_BAR_CHART, "clickData"),
    Input(ids_rubrica.JULGAMENTO_RUBRICA_BAR_CHART, "clickData"),
)
def update_decisoes_chart(tribunais:list[str], rubricas:list[str], decisoes:list[str], ativos:list[str], passivos:list[str], ano_propositura:list[int], ano_julgamento:list[int], click_data, *args) -> go.Figure:
    ctx = callback_context
   
    filtered_data = filter_database(tribunais, rubricas, decisoes, ativos, passivos, ano_propositura, ano_julgamento)

    filtered_data = check_click_data(filtered_data, 'decisao', ctx)
    
    df_decisoes = filtered_data.groupby([DataSchemaTJ.ECAD])[DataSchemaTJ.ECAD].count().reset_index(name = 'Total')

    if click_data and ids_rubrica.DECISOES_RUBRICA_PIE_CHART in ctx.triggered[0]["prop_id"] and ctx.triggered[0]["value"]:
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
            sort = False,
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
                'text': 'Favorável ao ECAD',
                'x': 0.5,
                'xanchor': 'center',
                'y': 1,
                'yanchor': 'top',
                'font':{
                    'size': 18,
                },
            },
            'legend':{
                'title': 'Favorável ao ECAD',
            },
            'transition':{
                'duration': 300,
                'easing': 'cubic-in-out',
            },
        }
    )

    fig.update_layout(margin = {"t":40, "b":0, "l":0, "r":0})
    fig.update_traces(hovertemplate = "%{label}<br>%{value}<extra></extra>")

    return fig

@callback(
    Output(ids_rubrica.ATIVO_RUBRICA_PIE_CHART, "figure"),
    Input(ids_rubrica.TRIBUNAL_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.DECISAO_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.ATIVO_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.PASSIVO_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.PROPOSITURA_RUBRICA_SLIDER, "value"),
    Input(ids_rubrica.JULGAMENTO_RUBRICA_SLIDER, "value"),
    Input(ids_rubrica.ATIVO_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.DECISOES_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.PASSIVO_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.PROPOSITURA_RUBRICA_BAR_CHART, "clickData"),
    Input(ids_rubrica.JULGAMENTO_RUBRICA_BAR_CHART, "clickData"),

)
def update_ativo_chart(tribunais:list[str], rubricas:list[str], decisoes:list[str], ativos:list[str], passivos:list[str], ano_propositura:list[int], ano_julgamento:list[int], click_data, *args) -> go.Figure:
    
    ctx = callback_context

    filtered_data = filter_database(tribunais, rubricas, decisoes, ativos, passivos, ano_propositura, ano_julgamento)

    filtered_data = check_click_data(filtered_data, 'ativo', ctx)
            

    df_ativo = filtered_data.groupby([DataSchemaTJ.ATIVO])[DataSchemaTJ.ATIVO].count().reset_index(name = 'Total')
    if click_data and ids_rubrica.ATIVO_RUBRICA_PIE_CHART in ctx.triggered[0]["prop_id"] and ctx.triggered[0]["value"]:

        ativo = ctx.triggered[0]["value"]["points"][0]["label"]
        lista_ativo = df_ativo[DataSchemaTJ.ATIVO].unique().tolist()
        lista_ativo.remove(ativo)
        lista_ativo.insert(0, ativo)
        df_ativo[DataSchemaTJ.ATIVO] = pd.Categorical(df_ativo[DataSchemaTJ.ATIVO], categories = lista_ativo)
        df_ativo = df_ativo.sort_values(DataSchemaTJ.ATIVO)

        ativo_donut = go.Pie(
            labels = df_ativo[DataSchemaTJ.ATIVO].tolist(),
            values = df_ativo['Total'],
            pull = [0.2],
            textinfo = 'percent',
            textposition = 'outside',
            hole = 0.5,
            sort = False,
        )
    else:
        ativo_donut = go.Pie(
        labels = df_ativo[DataSchemaTJ.ATIVO].tolist(),
        values = df_ativo['Total'],
        textinfo = 'percent',
        textposition = 'outside',
        hole = 0.5
    )

    fig = go.Figure(
        data = [ativo_donut],
        layout = {
            'title': {
                'text': 'Polo Ativo',
                'x': 0.5,
                'xanchor': 'center',
                'y': 1,
                'yanchor': 'top',
                'font':{
                    'size': 18,
                },
            },
            'legend':{
                'title': 'Ativo',
            }
        }
    )

    fig.update_layout(margin = {"t":40, "b":0, "l":0, "r":0})
    fig.update_traces(hovertemplate = "%{label}<br>%{value}<extra></extra>")

    return fig

@callback(
    Output(ids_rubrica.PASSIVO_RUBRICA_PIE_CHART, "figure"),
    Input(ids_rubrica.TRIBUNAL_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.DECISAO_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.ATIVO_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.PASSIVO_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.PROPOSITURA_RUBRICA_SLIDER, "value"),
    Input(ids_rubrica.JULGAMENTO_RUBRICA_SLIDER, "value"),
    Input(ids_rubrica.PASSIVO_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.DECISOES_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.ATIVO_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.PROPOSITURA_RUBRICA_BAR_CHART, "clickData"),
    Input(ids_rubrica.JULGAMENTO_RUBRICA_BAR_CHART, "clickData"),
)
def update_passivo_chart(tribunais:list[str], rubricas:list[str], decisoes:list[str], ativos:list[str], passivos:list[str], ano_propositura:list[int], ano_julgamento:list[int], click_data, *args) -> go.Figure:

    ctx = callback_context
    
    filtered_data = filter_database(tribunais, rubricas, decisoes, ativos, passivos, ano_propositura, ano_julgamento)

    filtered_data = check_click_data(filtered_data, 'passivo', ctx)
    
    df_passivo = filtered_data.groupby([DataSchemaTJ.PASSIVO])[DataSchemaTJ.PASSIVO].count().reset_index(name = 'Total')

    if click_data and ids_rubrica.PASSIVO_RUBRICA_PIE_CHART in ctx.triggered[0]["prop_id"] and ctx.triggered[0]["value"]:
        passivo = ctx.triggered[0]["value"]["points"][0]["label"]
        lista_passivo = df_passivo[DataSchemaTJ.PASSIVO].unique().tolist()
        lista_passivo.remove(passivo)
        lista_passivo.insert(0, passivo)
        df_passivo[DataSchemaTJ.PASSIVO] = pd.Categorical(df_passivo[DataSchemaTJ.PASSIVO], categories = lista_passivo)
        df_passivo = df_passivo.sort_values(DataSchemaTJ.PASSIVO)

        passivo_donut = go.Pie(
            labels = df_passivo[DataSchemaTJ.PASSIVO].tolist(),
            values = df_passivo['Total'],
            pull = [0.2],
            textinfo = 'percent',
            textposition = 'outside',
            hole = 0.5,
            sort = False,
        )
    else:
        passivo_donut = go.Pie(
            labels = df_passivo[DataSchemaTJ.PASSIVO].tolist(),
            values = df_passivo['Total'],
            textinfo = 'percent',
            textposition = 'outside',
            hole = 0.5
        )

    fig = go.Figure(
        data = [passivo_donut],
        layout = {
            'title': {
                'text': 'Polo Passivo',
                'x': 0.5,
                'xanchor': 'center',
                'y': 1,
                'yanchor': 'top',
                'font':{
                    'size': 18,
                },
            },
            'legend':{
                'title': 'Passivo',
            }
        }
    )

    fig.update_layout(margin = {"t":40, "b":0, "l":0, "r":0})
    fig.update_traces(hovertemplate = "%{label}<br>%{value}<extra></extra>")

    return fig

@callback(
    Output(ids_rubrica.PROPOSITURA_RUBRICA_BAR_CHART, "figure"),

    Input(ids_rubrica.TRIBUNAL_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.DECISAO_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.ATIVO_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.PASSIVO_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.PROPOSITURA_RUBRICA_SLIDER, "value"),
    Input(ids_rubrica.JULGAMENTO_RUBRICA_SLIDER, "value"),

    Input(ids_rubrica.PROPOSITURA_RUBRICA_BAR_CHART, "clickData"),
    Input(ids_rubrica.DECISOES_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.ATIVO_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.PASSIVO_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.JULGAMENTO_RUBRICA_BAR_CHART, "clickData"),
)
def update_propositura_chart(tribunais:list[str], rubricas:list[str], decisoes:list[str], ativos:list[str], passivos:list[str], ano_propositura:list[int], ano_julgamento:list[int], click_data, *args) -> go.Figure:
    ctx = callback_context

    filtered_data = filter_database(tribunais, rubricas, decisoes, ativos, passivos, ano_propositura, ano_julgamento)

    filtered_data = check_click_data(filtered_data, 'propositura', ctx)

    filtered_data['Ano'] = filtered_data[DataSchemaTJ.ANO_PROPOSITURA].dt.year

    df_propositura = filtered_data[[DataSchemaTJ.TRIBUNAL_ORIGEM, 'Ano']].groupby(['Ano'])[DataSchemaTJ.TRIBUNAL_ORIGEM].count().reset_index(name = 'Total')
    
    if click_data and ids_rubrica.PROPOSITURA_RUBRICA_BAR_CHART in ctx.triggered[0]["prop_id"] and ctx.triggered[0]["value"]:
        propositura = ctx.triggered[0]["value"]["points"][0]["label"]
    else:
        propositura = ''

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
        x = df_propositura["Total"],
        y = df_propositura["Ano"],
        orientation = "h",
        marker = dict(
            color = list(
                map(
                    selected_bar, lista_anos
                ),
            ),
        ),
    )

    fig = go.Figure(
        data = [propositura_bar],
        layout = {
            'title':'Processos protocolados por ano',
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
    Output(ids_rubrica.JULGAMENTO_RUBRICA_BAR_CHART, "figure"),
    Input(ids_rubrica.TRIBUNAL_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.RUBRICA_DROPDOWN, "value"),    
    Input(ids_rubrica.DECISAO_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.ATIVO_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.PASSIVO_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.PROPOSITURA_RUBRICA_SLIDER, "value"),
    Input(ids_rubrica.JULGAMENTO_RUBRICA_SLIDER, "value"),
    Input(ids_rubrica.JULGAMENTO_RUBRICA_BAR_CHART, "clickData"),
    Input(ids_rubrica.DECISOES_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.ATIVO_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.PASSIVO_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.PROPOSITURA_RUBRICA_BAR_CHART, "clickData"),
)
def update_julgamento_chart(tribunais:list[str], rubricas:list[str], decisoes:list[str], ativos:list[str], passivos:list[str], ano_propositura:list[int], ano_julgamento:list[int], click_data, *args) -> go.Figure:

    ctx = callback_context

    filtered_data = filter_database(tribunais, rubricas, decisoes, ativos, passivos, ano_propositura, ano_julgamento)

    filtered_data = check_click_data(filtered_data, 'julgamento', ctx)

    filtered_data['Ano'] = filtered_data[DataSchemaTJ.DATA_JULGAMENTO].dt.year

    df_julgamento = filtered_data[[DataSchemaTJ.TRIBUNAL_ORIGEM, 'Ano']].groupby(['Ano'])[DataSchemaTJ.TRIBUNAL_ORIGEM].count().reset_index(name = 'Total')

    if click_data and ids_rubrica.JULGAMENTO_RUBRICA_BAR_CHART in ctx.triggered[0]["prop_id"] and ctx.triggered[0]["value"]:
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
                )
            )
        )
    )

    fig = go.Figure(
        data = [julgamento_bar],
        layout = {
            'title':'Processos Julgados por Ano',
            'xaxis':{
                'title':'Ano'
            },
            'yaxis':{
                'title':'Total'
            },
        },
    )

    return fig
   
def filter_database(tribunais:list[str], rubricas: list[str], decisoes:list[str], ativos:list[str], passivos:list[str], ano_propositura:list[int], ano_julgamento:list[int]) -> pd.DataFrame:
    new_df = data.copy()

    if tribunais:
        new_df = new_df[new_df[DataSchemaTJ.TRIBUNAL_ORIGEM].isin(tribunais)]
    
    if rubricas:
        new_df = new_df[new_df[DataSchemaTJ.RUBRICA].isin(rubricas)]

    if decisoes:
        new_df = new_df[new_df[DataSchemaTJ.ECAD].isin(decisoes)]
    
    if ativos:
        new_df = new_df[new_df[DataSchemaTJ.ATIVO].isin(ativos)]    

    if passivos:
        new_df = new_df[new_df[DataSchemaTJ.PASSIVO].isin(passivos)]

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
        if ids_rubrica.DECISOES_RUBRICA_PIE_CHART in click_context.triggered[0]["prop_id"] and chart != 'decisao':
            selected = click_context.triggered[0]["value"]["points"][0]["label"]
            df_click = df_click[df_click[DataSchemaTJ.ECAD] == selected]
            pass
        if ids_rubrica.ATIVO_RUBRICA_PIE_CHART in click_context.triggered[0]["prop_id"] and chart != 'ativo':
            selected = click_context.triggered[0]["value"]["points"][0]["label"]
            df_click = df_click[df_click[DataSchemaTJ.ATIVO] == selected]
            pass
        if ids_rubrica.PASSIVO_RUBRICA_PIE_CHART in click_context.triggered[0]["prop_id"] and chart != 'passivo':
            selected = click_context.triggered[0]["value"]["points"][0]["label"]
            df_click = df_click[df_click[DataSchemaTJ.PASSIVO] == selected]
            pass
        if ids_rubrica.PROPOSITURA_RUBRICA_BAR_CHART in click_context.triggered[0]["prop_id"] and chart != 'propositura':
            selected = click_context.triggered[0]["value"]["points"][0]["label"]
            df_click = df_click[df_click[DataSchemaTJ.ANO_PROPOSITURA].dt.year == int(selected)]
            pass
        if ids_rubrica.JULGAMENTO_RUBRICA_BAR_CHART in click_context.triggered[0]["prop_id"] and chart != 'julgamento':
            selected = click_context.triggered[0]["value"]["points"][0]["label"]
            df_click = df_click[df_click[DataSchemaTJ.DATA_JULGAMENTO].dt.year == int(selected)]
            pass
        return df_click
