#API-Campeonato
Uma api para gerenciar campeonatos de mata
## Iniciando containers

> docker-compose up

## Criando banco

> docker exec -it mysql-container /bin/bash
> mysql -u root -p 
> olamundo
> create schema api

## Criando tabelas
> docker exec -it api-campeonato_api_1 /bin/bash
> flask db upgrade


