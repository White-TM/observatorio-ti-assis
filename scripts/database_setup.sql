-- Criação das Tabelas do Observatório de TI (Assis/SP)

-- 1. Tabela Dimensão: Vagas
CREATE TABLE dim_vagas (
    id_vaga INT PRIMARY KEY,
    titulo_vaga VARCHAR(150) NOT NULL,
    empresa VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    modelo_trabalho VARCHAR(20) CHECK (modelo_trabalho IN ('Presencial', 'Remoto', 'Híbrido', 'Não Informado')),
    senioridade VARCHAR(20) CHECK (senioridade IN ('Estágio', 'Júnior', 'Pleno/Sênior', 'Não Informado')),
    data_publicacao DATE NOT NULL
);

-- 2. Tabela Fato: Habilidades Técnicas
CREATE TABLE fato_habilidades (
    id_registro INT PRIMARY KEY,
    id_vaga INT NOT NULL,
    habilidade_tech VARCHAR(50) NOT NULL,
    CONSTRAINT fk_vaga
      FOREIGN KEY(id_vaga) 
      REFERENCES dim_vagas(id_vaga)
      ON DELETE CASCADE
);

-- COPY dim_vagas FROM 'Caminho/Absoluto/Para/dim_vagas.csv' DELIMITER ',' CSV HEADER;
-- COPY fato_habilidades FROM 'Caminho/Absoluto/Para/fato_habilidades.csv' DELIMITER ',' CSV HEADER;
