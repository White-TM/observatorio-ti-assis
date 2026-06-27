import pandas as pd
import random
from datetime import datetime, timedelta
import os

# 1. Configuração de Caminhos 
RAW_PATH = '../data/raw/linkedin_jobs_mock.csv'
PROCESSED_VAGAS = '../data/processed/dim_vagas.csv'
PROCESSED_HABILIDADES = '../data/processed/fato_habilidades.csv'

os.makedirs('../data/raw', exist_ok=True)
os.makedirs('../data/processed', exist_ok=True)

# 2. Geração de Dados 
def gerar_dados_brutos():
    print("A gerar dados brutos da região de Assis/SP...")
    cidades = ['Assis', 'Cândido Mota', 'Marília', 'Ourinhos']
    cargos = ['Analista de Dados', 'Desenvolvedor Front-end', 'Engenheiro de Software', 'Suporte de TI']
    modelos = ['Remote', 'On-site', 'Hybrid', ''] # Simulando sujeira
    senioridades = ['Entry level', 'Mid-Senior level', 'Internship', '']
    habilidades_pool = ['Python, SQL, Power BI', 'React, JavaScript, HTML', 'Java, Spring, SQL', 'Redes, Windows Server', 'Python, AWS']
    
    dados = []
    for i in range(1, 151):
        dados.append({
            'job_id': 1000 + i,
            'title': random.choice(cargos),
            'company_name': f'Tech Corp {random.randint(1, 10)}' if random.random() > 0.1 else None, # 10% nulos
            'location': f'{random.choice(cidades)}, São Paulo, Brazil',
            'work_type': random.choice(modelos),
            'formatted_experience_level': random.choice(senioridades),
            'description': random.choice(habilidades_pool),
            'date_posted': (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d')
        })
    df_raw = pd.DataFrame(dados)
    df_raw.to_csv(RAW_PATH, index=False)
    return df_raw

# 3. Limpeza e Transformação (ETL)
def executar_etl():
    # Carrega os dados
    df = gerar_dados_brutos()
    print("Iniciando limpeza de dados (Regras da AE2)...")
    
    # Regra 2: Remover nulos em campos obrigatórios (Empresa)
    df['company_name'] = df['company_name'].fillna('Confidencial')
    
    # Regra 3: Padronizar Domínio de Modelo de Trabalho
    map_modelo = {'Remote': 'Remoto', 'On-site': 'Presencial', 'Hybrid': 'Híbrido'}
    df['modelo_trabalho'] = df['work_type'].map(map_modelo).fillna('Não Informado')
    
    # Regra 4: Padronizar Domínio de Senioridade
    map_senioridade = {'Entry level': 'Júnior', 'Mid-Senior level': 'Pleno/Sênior', 'Internship': 'Estágio'}
    df['senioridade'] = df['formatted_experience_level'].map(map_senioridade).fillna('Não Informado')
    
    # Preparar a Tabela dim_vagas
    df_vagas = df[['job_id', 'title', 'company_name', 'location', 'modelo_trabalho', 'senioridade', 'date_posted']].copy()
    df_vagas.columns = ['id_vaga', 'titulo_vaga', 'empresa', 'cidade', 'modelo_trabalho', 'senioridade', 'data_publicacao']
    
    # Regra 1: Remover Duplicados
    df_vagas = df_vagas.drop_duplicates(subset=['titulo_vaga', 'empresa', 'data_publicacao'])
    
    # Guardar Tabela de Vagas
    df_vagas.to_csv(PROCESSED_VAGAS, index=False)
    print(f"Dimensão de vagas guardada: {PROCESSED_VAGAS} com {len(df_vagas)} registos.")
    
    # Preparar Tabela fato_habilidades
    habilidades_list = []
    id_registro = 1
    for index, row in df.iterrows():
        habs = str(row['description']).split(',')
        for h in habs:
            if h.strip():
                habilidades_list.append({
                    'id_registro': id_registro,
                    'id_vaga': row['job_id'],
                    'habilidade_tech': h.strip().lower()
                })
                id_registro += 1
                
    df_habilidades = pd.DataFrame(habilidades_list)
    df_habilidades.to_csv(PROCESSED_HABILIDADES, index=False)
    print(f"Fato de habilidades guardada: {PROCESSED_HABILIDADES} com {len(df_habilidades)} registos.")
    print("ETL Concluído com Sucesso!")

if __name__ == "__main__":
    executar_etl()
