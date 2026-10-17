# Trilha opcional — Containerização

Faça somente se `docker --version` funcionar e o Docker Desktop estiver iniciado.

1. Construa o Bento:
   `bentoml build`
2. Liste:
   `bentoml list`
3. Containerize o Bento criado (copie o nome/tag exibido):
   `bentoml containerize servico_churn:latest`
4. Liste imagens:
   `docker images`
5. Rode a imagem conforme o nome exibido pelo comando de containerização.

Se o Docker não estiver disponível, tire um print do erro/preflight e explique por que a prática principal continua válida: o Bento já é o artefato empacotado; a imagem OCI é uma etapa posterior de distribuição.
