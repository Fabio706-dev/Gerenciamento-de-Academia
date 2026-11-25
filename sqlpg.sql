CREATE TABLE planos_treino (
    id      SERIAL PRIMARY KEY,
    nome    VARCHAR(100)  NOT NULL,
    duracao INT      NOT NULL CHECK (duracao > 0),
    foco    VARCHAR(100)  NOT NULL,
    preco   NUMERIC(10,2) NOT NULL CHECK (preco >= 0)
);

CREATE TABLE alunos (
    id       SERIAL PRIMARY KEY,
    nome     VARCHAR(100) NOT NULL,
    cpf      CHAR(11)     NOT NULL UNIQUE,
    idade    INT     NOT NULL CHECK (idade >= 16),
    peso     NUMERIC(5,2) NOT NULL CHECK (peso > 0),
    id_plano INT     NOT NULL,
    FOREIGN KEY (id_plano) REFERENCES planos_treino(id)
);