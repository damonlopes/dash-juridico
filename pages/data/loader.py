import pandas as pd

class DataSchemaTJ:
    TRIBUNAL_ORIGEM = "TJ/STJ"
    ESTADO = "Estado"
    N_PROCESSO = "Nª Processo"
    PARTES = "Partes Formatadas"
    ATIVO = "Ativo"
    PASSIVO = "Passivo"
    ANO_PROPOSITURA = "Ano propositura data"
    DATA_JULGAMENTO = "Data Julgamento"
    TEMPO_MEDIO = "Tempo Medio"
    RUBRICA = "Rubrica 1"
    ECAD = "Favorável ao ECAD?"

class DataSchemaSTJ:
    DATA_JULGAMENTO="Data Julgamento"
    CLASSE_PROCESSO="Classe do processo"
    TRIBUNAL_ORIGEM="Tribunal de Origem"
    CAMARA_TURMA_SECAO="Câmara/Turma/Seção"
    ATIVA="ATIVA"
    PASSIVA="Passiva"
    PARTES="Partes"
    TIPO_ACAO="Tipo de ação"
    RUBRICA="Rubrica"
    

def load_dashboard_data(path: str, sheet_name: str) -> pd.DataFrame:

    data = pd.read_excel(path, sheet_name = sheet_name)

    return data

def load_cities_data(path:str) -> pd.DataFrame:

    return pd.read_csv(path)