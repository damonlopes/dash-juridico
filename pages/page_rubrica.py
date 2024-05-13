import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from dash import dcc, html, register_page, callback, Output, Input, callback_context
from .data.loader import load_dashboard_data, DataSchemaTJ
from .components.ids import ids_rubrica

DATA_PATH = './pages/data/Planilha BI FINAL.xlsx'
data = load_dashboard_data(DATA_PATH, "Planilha1")

unique_tribunais = sorted(set(data[DataSchemaTJ.TRIBUNAL_ORIGEM].tolist()), key = str)
unique_rubricas = sorted(set(data[DataSchemaTJ.RUBRICA].tolist()), key = str)


register_page(
    __name__,
    path = '/rubrica',
    name = 'Dashboard Rubrica',
    title = 'Dashboard Rubrica')

layout = html.Div(
    children = [
        dbc.Container([
            dbc.Row([
                dbc.Col([
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
                dbc.Col([
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
            ]),
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
    prevent_inicial_call = True,
)
def select_all_rubricas(_:str) -> list[str]:
    return unique_rubricas

@callback(
    Output(ids_rubrica.DURACAO_RUBRICA_GAUGE_CHART, "figure"),
    Input(ids_rubrica.TRIBUNAL_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.DECISOES_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.ATIVO_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.PASSIVO_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.PROPOSITURA_RUBRICA_BAR_CHART, "clickData"),
    Input(ids_rubrica.JULGAMENTO_RUBRICA_BAR_CHART, "clickData"),
)
def update_duracao_chart(tribunais:list[str], rubricas:list[str], *args) -> go.Figure:
    ctx = callback_context
    if not tribunais and not rubricas:
        filtered_data = data.copy()
        pass
    elif tribunais and rubricas:
        filtered_data = data[(data[DataSchemaTJ.TRIBUNAL_ORIGEM].isin(tribunais))&(data[DataSchemaTJ.RUBRICA].isin(rubricas))].copy()
        pass
    else:
        if tribunais:
            filtered_data = data[data[DataSchemaTJ.TRIBUNAL_ORIGEM].isin(tribunais)].copy()
            pass
        else:
            filtered_data = data[data[DataSchemaTJ.RUBRICA].isin(rubricas)].copy()
            pass

    if not ctx.triggered[0]["value"]:
        pass
    else:
        if ids_rubrica.DECISOES_RUBRICA_PIE_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.ECAD] == selected]
            pass
        if ids_rubrica.ATIVO_RUBRICA_PIE_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.ATIVO] == selected]
            pass
        if ids_rubrica.PASSIVO_RUBRICA_PIE_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.PASSIVO] == selected]
            pass
        if ids_rubrica.PROPOSITURA_RUBRICA_BAR_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.ANO_PROPOSITURA].dt.year == int(selected)]
            pass
        if ids_rubrica.JULGAMENTO_RUBRICA_BAR_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.DATA_JULGAMENTO].dt.year == int(selected)]
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
    # return html.Div(
    #     dcc.Graph(
    #         figure = fig
    #     ),
    #     id = ids_rubrica.DURACAO_RUBRICA_GAUGE_CHART
    # )

@callback(
    Output(ids_rubrica.DECISOES_RUBRICA_PIE_CHART, "figure"),
    Input(ids_rubrica.TRIBUNAL_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.DECISOES_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.ATIVO_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.PASSIVO_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.PROPOSITURA_RUBRICA_BAR_CHART, "clickData"),
    Input(ids_rubrica.JULGAMENTO_RUBRICA_BAR_CHART, "clickData"),
)
def update_decisoes_chart(tribunais:list[str], rubricas:list[str], click_data, *args) -> go.Figure:
    ctx = callback_context
    if not tribunais and not rubricas:
        filtered_data = data.copy()
        pass
    elif tribunais and rubricas:
        filtered_data = data[(data[DataSchemaTJ.TRIBUNAL_ORIGEM].isin(tribunais))&(data[DataSchemaTJ.RUBRICA].isin(rubricas))].copy()
        pass
    else:
        if tribunais:
            filtered_data = data[data[DataSchemaTJ.TRIBUNAL_ORIGEM].isin(tribunais)].copy()
            pass
        else:
            filtered_data = data[data[DataSchemaTJ.RUBRICA].isin(rubricas)].copy()
            pass
    
    if not ctx.triggered[0]["value"]:
        pass
    else:
        if ids_rubrica.ATIVO_RUBRICA_PIE_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.ATIVO] == selected]
            pass
        if ids_rubrica.PASSIVO_RUBRICA_PIE_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.PASSIVO] == selected]
            pass
        if ids_rubrica.PROPOSITURA_RUBRICA_BAR_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.ANO_PROPOSITURA].dt.year == int(selected)]
            pass
        if ids_rubrica.JULGAMENTO_RUBRICA_BAR_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.DATA_JULGAMENTO].dt.year == int(selected)]
            pass
    
    df_decisoes = filtered_data.groupby([DataSchemaTJ.ECAD])[DataSchemaTJ.ECAD].count().reset_index(name = 'Total')

    if click_data and ids_rubrica.DECISOES_RUBRICA_PIE_CHART in ctx.triggered[0]["prop_id"] and ctx.triggered[0]["value"]:
        # breakpoint()
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
            }
        }
    )

    fig.update_layout(margin = {"t":40, "b":0, "l":0, "r":0})
    fig.update_traces(hovertemplate = "%{label}<br>%{value}<extra></extra>")

    return fig

@callback(
    Output(ids_rubrica.ATIVO_RUBRICA_PIE_CHART, "figure"),
    Input(ids_rubrica.TRIBUNAL_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.ATIVO_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.DECISOES_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.PASSIVO_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.PROPOSITURA_RUBRICA_BAR_CHART, "clickData"),
    Input(ids_rubrica.JULGAMENTO_RUBRICA_BAR_CHART, "clickData"),

)
def update_ativo_chart(tribunais:list[str], rubricas:list[str], click_data, *args) -> go.Figure:
    
    ctx = callback_context
    if not tribunais and not rubricas:
        filtered_data = data.copy()
        pass
    elif tribunais and rubricas:
        filtered_data = data[(data[DataSchemaTJ.TRIBUNAL_ORIGEM].isin(tribunais))&(data[DataSchemaTJ.RUBRICA].isin(rubricas))].copy()
        pass
    else:
        if tribunais:
            filtered_data = data[data[DataSchemaTJ.TRIBUNAL_ORIGEM].isin(tribunais)].copy()
            pass
        else:
            filtered_data = data[data[DataSchemaTJ.RUBRICA].isin(rubricas)].copy()
            pass
    
    if not ctx.triggered[0]["value"]:
        pass
    else:
        if ids_rubrica.DECISOES_RUBRICA_PIE_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.ECAD] == selected]
            pass
        if ids_rubrica.PASSIVO_RUBRICA_PIE_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.PASSIVO] == selected]
            pass
        if ids_rubrica.PROPOSITURA_RUBRICA_BAR_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.ANO_PROPOSITURA].dt.year == int(selected)]
            pass
        if ids_rubrica.JULGAMENTO_RUBRICA_BAR_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.DATA_JULGAMENTO].dt.year == int(selected)]
            pass
            

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
    Input(ids_rubrica.PASSIVO_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.DECISOES_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.ATIVO_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.PROPOSITURA_RUBRICA_BAR_CHART, "clickData"),
    Input(ids_rubrica.JULGAMENTO_RUBRICA_BAR_CHART, "clickData"),
)
def update_passivo_chart(tribunais:list[str], rubricas:list[str], click_data, *args) -> go.Figure:

    ctx = callback_context
    if not tribunais and not rubricas:
        filtered_data = data.copy()
        pass
    elif tribunais and rubricas:
        filtered_data = data[(data[DataSchemaTJ.TRIBUNAL_ORIGEM].isin(tribunais))&(data[DataSchemaTJ.RUBRICA].isin(rubricas))].copy()
        pass
    else:
        if tribunais:
            filtered_data = data[data[DataSchemaTJ.TRIBUNAL_ORIGEM].isin(tribunais)].copy()
            pass
        else:
            filtered_data = data[data[DataSchemaTJ.RUBRICA].isin(rubricas)].copy()
            pass
    
    if not ctx.triggered[0]["value"]:
        pass
    else:
        if ids_rubrica.DECISOES_RUBRICA_PIE_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.ECAD] == selected]
            pass
        if ids_rubrica.ATIVO_RUBRICA_PIE_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.ATIVO] == selected]
            pass
        if ids_rubrica.PROPOSITURA_RUBRICA_BAR_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.ANO_PROPOSITURA].dt.year == int(selected)]
            pass
        if ids_rubrica.JULGAMENTO_RUBRICA_BAR_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.DATA_JULGAMENTO].dt.year == int(selected)]
            pass

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
    # return html.Div(
    #     dcc.Graph(
    #         figure = fig
    #     ),
    #     id = ids_rubrica.PASSIVO_RUBRICA_PIE_CHART
    # )

@callback(
    Output(ids_rubrica.PROPOSITURA_RUBRICA_BAR_CHART, "figure"),
    Input(ids_rubrica.TRIBUNAL_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.PROPOSITURA_RUBRICA_BAR_CHART, "clickData"),
    Input(ids_rubrica.DECISOES_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.ATIVO_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.PASSIVO_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.JULGAMENTO_RUBRICA_BAR_CHART, "clickData"),
)
def update_propositura_chart(tribunais:list[str], rubricas:list[str], click_data, *args) -> go.Figure:
    ctx = callback_context
    if not tribunais and not rubricas:
        filtered_data = data.copy()
        pass
    elif tribunais and rubricas:
        filtered_data = data[(data[DataSchemaTJ.TRIBUNAL_ORIGEM].isin(tribunais))&(data[DataSchemaTJ.RUBRICA].isin(rubricas))].copy()
        pass
    else:
        if tribunais:
            filtered_data = data[data[DataSchemaTJ.TRIBUNAL_ORIGEM].isin(tribunais)].copy()
            pass
        else:
            filtered_data = data[data[DataSchemaTJ.RUBRICA].isin(rubricas)].copy()
            pass
    
    if not ctx.triggered[0]["value"]:
        pass
    else:
        if ids_rubrica.DECISOES_RUBRICA_PIE_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.ECAD] == selected]
            pass
        if ids_rubrica.ATIVO_RUBRICA_PIE_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.ATIVO] == selected]
            pass
        if ids_rubrica.PASSIVO_RUBRICA_PIE_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.PASSIVO] == selected]
            pass
        if ids_rubrica.JULGAMENTO_RUBRICA_BAR_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.DATA_JULGAMENTO].dt.year == int(selected)]
            pass

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

    # fig = px.bar(
    #     df_propositura,
    #     x = 'Total',
    #     y = 'Ano',
    #     title = 'Processos protocolados por ano',
    #     orientation = 'h'
    # )

    return fig
    # return html.Div(
    #     dcc.Graph(
    #         figure = fig
    #     ),
    #     id = ids_rubrica.PROPOSITURA_RUBRICA_BAR_CHART
    # )

@callback(
    Output(ids_rubrica.JULGAMENTO_RUBRICA_BAR_CHART, "figure"),
    Input(ids_rubrica.TRIBUNAL_RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.RUBRICA_DROPDOWN, "value"),
    Input(ids_rubrica.JULGAMENTO_RUBRICA_BAR_CHART, "clickData"),
    Input(ids_rubrica.DECISOES_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.ATIVO_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.PASSIVO_RUBRICA_PIE_CHART, "clickData"),
    Input(ids_rubrica.PROPOSITURA_RUBRICA_BAR_CHART, "clickData"),
)
def update_julgamento_chart(tribunais:list[str], rubricas:list[str], click_data, *args) -> go.Figure:

    ctx = callback_context
    if not tribunais and not rubricas:
        filtered_data = data.copy()
        pass
    elif tribunais and rubricas:
        filtered_data = data[(data[DataSchemaTJ.TRIBUNAL_ORIGEM].isin(tribunais))&(data[DataSchemaTJ.RUBRICA].isin(rubricas))].copy()
        pass
    else:
        if tribunais:
            filtered_data = data[data[DataSchemaTJ.TRIBUNAL_ORIGEM].isin(tribunais)].copy()
            pass
        else:
            filtered_data = data[data[DataSchemaTJ.RUBRICA].isin(rubricas)].copy()
            pass
    # filtered_data = data[(data[DataSchemaTJ.TRIBUNAL_ORIGEM].isin(tribunais))&(data[DataSchemaTJ.RUBRICA].isin(rubricas))].copy()

    if not ctx.triggered[0]["value"]:
        pass
    else:
        if ids_rubrica.DECISOES_RUBRICA_PIE_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.ECAD] == selected]
            pass
        if ids_rubrica.ATIVO_RUBRICA_PIE_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.ATIVO] == selected]
            pass
        if ids_rubrica.PASSIVO_RUBRICA_PIE_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.PASSIVO] == selected]
            pass
        if ids_rubrica.PROPOSITURA_RUBRICA_BAR_CHART in ctx.triggered[0]["prop_id"]:
            selected = ctx.triggered[0]["value"]["points"][0]["label"]
            filtered_data = filtered_data[filtered_data[DataSchemaTJ.ANO_PROPOSITURA].dt.year == int(selected)]
            pass
    
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
    # fig = px.bar(
    #     df_julgamento,
    #     x = 'Ano',
    #     y = 'Total',
    #     title = 'Processos Julgados por Ano'
    # )

    return fig
    # return html.Div(
    #     dcc.Graph(
    #         figure = fig
    #     ),
    #     id = ids_rubrica.JULGAMENTO_RUBRICA_BAR_CHART
    # )