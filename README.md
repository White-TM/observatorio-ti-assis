# Observatório de Empregabilidade TI - Assis/SP

## Descrição do Projeto
Este projeto tem como objetivo realizar a coleta, tratamento e análise de dados de vagas de emprego na área de Tecnologia da Informação na região de Assis/SP. Através da extração de dados do Indeed, criamos um pipeline de ETL para identificar as principais tecnologias exigidas pelo mercado e o modelo de trabalho predominante, transformando dados brutos em insights estratégicos.

## Tecnologias Utilizadas
- **Linguagem:** Python (Pandas para manipulação de dados)
- **Visualização:** Power BI
- **Controle de Versão:** Git/GitHub
- **Metodologia:** ETL (Extract, Transform, Load)

## Estrutura do Repositório
- `/data/raw/`: Armazena os datasets brutos extraídos do Indeed.
- `/scripts/`: Contém os scripts Python de tratamento (`etl_process.py`) e a estrutura de banco de dados (`database_setup.sql`).
- `/dashboard/`: Contém o arquivo `.pbix` com o dashboard interativo.
- `/docs/`: Contém a documentação da Devolutiva Extensionista.

## Como Executar
1. Certifique-se de ter o Python instalado.
2. Instale a biblioteca Pandas: `pip install pandas`
3. Execute o script de ETL: `python scripts/etl_process.py`
4. Os arquivos processados (`dim_vagas.csv` e `fato_habilidades.csv`) serão gerados na pasta `/data/processed/`.
5. Abra o arquivo localizado em `/dashboard/` no Power BI Desktop para visualizar as métricas.

## Autor
**Thiago Palomares de Moraes**

---
*Este projeto foi criado com o intuito de mapear as demandas reais de contratação de TI na região, auxiliando estudantes e profissionais na identificação de tendências tecnológicas.*
