import pandas as pd
import os

# --- Configuração de Caminhos ---
RAW_PATH = '../data/raw/vagas_indeed_real_assis_v2.csv'
PROCESSED_VAGAS = '../data/processed/dim_vagas.csv'
PROCESSED_HABILIDADES = '../data/processed/fato_habilidades.csv'

os.makedirs('../data/processed', exist_ok=True)

def executar_etl():
    print(f"Iniciando ETL. Lendo dados de: {RAW_PATH}")
    
    try:
        df = pd.read_csv(RAW_PATH)
    except FileNotFoundError:
        print("ERRO: O arquivo 'vagas_indeed_real_assis_v2.csv' não foi encontrado na pasta 'data/raw/'.")
        return

    # --- Limpeza e Padronização ---
    print("Aplicando regras de tratamento de dados...")
    
    # 1. Tratar nulos e inconsistências
    df = df.dropna(subset=['titulo_vaga'])
    df['nome_empresa'] = df['nome_empresa'].fillna('Confidencial')
    df['modelo_trabalho'] = df['modelo_trabalho'].fillna('Não Informado')
    
    # 2. Mapeamento de Modelo de Trabalho (Garantindo consistência)
    map_modelo = {'Remoto': 'Remoto', 'Presencial': 'Presencial', 'Híbrido': 'Híbrido'}
    # Se o valor não estiver no mapeamento, assume 'Não Informado'
    df['modelo_trabalho'] = df['modelo_trabalho'].apply(lambda x: x if x in map_modelo.values() else 'Não Informado')
    
    # 3. Criar Tabela Dimensão: dim_vagas
    # Mapeando nomes das colunas originais para o padrão solicitado
    df_vagas = df[['id_vaga_indeed', 'titulo_vaga', 'nome_empresa', 'localidade', 'modelo_trabalho', 'data_extracao']].copy()
    df_vagas.columns = ['id_vaga', 'titulo_vaga', 'empresa', 'cidade', 'modelo_trabalho', 'data_publicacao']
    
    # Adicionar senioridade (como o Indeed não fornece explicitamente, atribuímos padrão)
    df_vagas['senioridade'] = 'Não Informado'
    
    # Remover duplicados
    df_vagas = df_vagas.drop_duplicates(subset=['titulo_vaga', 'empresa', 'data_publicacao'])
    
    # Exportar dim_vagas
    df_vagas.to_csv(PROCESSED_VAGAS, index=False, encoding='utf-8')
    print(f"-> dim_vagas.csv gerado com {len(df_vagas)} registros.")

    # 4. Criar Tabela Fato: fato_habilidades
    
    tecnologias_alvo = ['python', 'sql', 'java', 'javascript', 'html', 'css', 'flutter', 'aws', 'kubernetes', 'git', '.net', 'c#', 'react', 'angular']
    habilidades_list = []
    id_registro = 1
    
    for index, row in df_vagas.iterrows():
        
        descricao = str(df.loc[df['id_vaga_indeed'] == row['id_vaga'], 'resumo_vaga'].values[0]).lower()
        
        for tech in tecnologias_alvo:
            if tech in descricao:
                habilidades_list.append({
                    'id_registro': id_registro,
                    'id_vaga': row['id_vaga'],
                    'habilidade_tech': tech.upper() 
                })
                id_registro += 1
                
    df_habilidades = pd.DataFrame(habilidades_list)
    df_habilidades.to_csv(PROCESSED_HABILIDADES, index=False, encoding='utf-8')
    print(f"-> fato_habilidades.csv gerado com {len(df_habilidades)} ocorrências.")
    print("Processo ETL finalizado com sucesso.")

if __name__ == "__main__":
    executar_etl()
