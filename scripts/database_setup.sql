-- 1. Tabela Dimensão: Vagas
-- Armazena os dados principais das vagas extraídas
CREATE TABLE dim_vagas (
    id_vaga VARCHAR(50) PRIMARY KEY,
    titulo_vaga VARCHAR(255) NOT NULL,
    empresa VARCHAR(255) NOT NULL,
    cidade VARCHAR(100),
    modelo_trabalho VARCHAR(50),
    data_publicacao DATE,
    senioridade VARCHAR(50)
);

-- 2. Tabela Fato: Habilidades Técnicas
-- Armazena as tecnologias extraídas (muitas habilidades por vaga)
CREATE TABLE fato_habilidades (
    id_registro INT PRIMARY KEY,
    id_vaga VARCHAR(50) NOT NULL,
    habilidade_tech VARCHAR(50) NOT NULL,
    CONSTRAINT fk_vaga
      FOREIGN KEY(id_vaga) 
      REFERENCES dim_vagas(id_vaga)
      ON DELETE CASCADE
);
