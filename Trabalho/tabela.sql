CREATE TABLE "ativo" (
  "id" integer,
  "nome" varchar(10),
  "valor" decimal(10,2),
  "qtd" integer,
  PRIMARY KEY ("id")
);

CREATE TABLE "transacoes" (
  "id" integer,
  "id_ativo" integer,
  "data_transacao" date,
  "tipo" varchar(50),
  "valor" decimal(10,2),
  "qtd" integer,
  "corretora" varchar(150),
  PRIMARY KEY ("id"),
  CONSTRAINT "FK_transacoes.id_ativo"
    FOREIGN KEY ("id_ativo")
      REFERENCES "ativo"("id")
);
