# API-Campeonato
Uma api para gerenciar campeonatos de mata
## Requisito
- Docker
- Docker-Compose

**Todos os comandos deversão ser realizados na raiz do projeto**
## Criando banco (dev & test)
### Criando imagem do banco
```
docker build -t mysql-image -f api/db/Dockerfile .
```
### Rodando container
```
docker run -d -v $(pwd)/db/data:/var/lib/mysql --rm --name mysql-container mysql-image
```
### Entrando no container para criar banco
```
docker exec -it mysql-container /bin/bash
```
### Conectando no banco
```
mysql -uroot -polamundo
```
PS: Caso dê erro ao realizar login reiniciar o container com os comandos e tente o conectar novamente
```
docker stop mysql-container
docker run -d -v $(pwd)/db/data:/var/lib/mysql --rm --name mysql-container mysql-image
```
### Criando schema de dev
```
create schema api;
```
### Criando schema de test
```
create schema api_test;
```
### Saindo mysql
```
exit
```
### Saindo container
```
exit
```
### Parando container
```
docker stop mysql-container
```
## Subindo container DEV
## Construindo image
```
docker build -t api-campeonato -f api/Dockerfile ./api
```
### Subindo containers
```
docker-compose up -d 
```
### Criando tabelas para produção
```
docker exec -it api-campeonato-container /bin/bash
```
```
flask db upgrade
```
```
exit
```
### Testando API
Após isso a API estará disponível  [localhost:5000](http://localhost:5000)
### Documentação da API
Há uma documentação das rotas existentes em [localhost:5000/docs](http://localhost:5000/docs)

### Parando containers
```
docker-compose down 
```

## Subindo container TEST
### Criando imagem  TEST
```
docker build -t api_test-campeonato -f api/Dockerfile.test ./api
```
### Rodando suit de TEST
```
docker-compose -f ./docker-compose.test.yml up
```
