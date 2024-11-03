# FIAP-9SOAT-Challenge-1

## Sobre o projeto
O projeto se trata de uma implementação de backend em Python utilizando os frameworks Fast API e Peewee ORM.

Projetado utilizando os conceitos de Domain Driven Design.
Implementado utilizando conceitos de Hexagonal Architecture
Desenvolvimento utilizando conceitos de Test Driven Development

O objetivo do projeto de demonstrar as implementações técnicas dos conceitos citados acima, servindo como base de analise do aprendizado adquerido durante a Fase 1 do curso de Software Architecture turma 9 da FIAP.

### Meta Conceito

Uma solução de gerenciamento de pedidos de restaurante, com uma API para gerenciamento de produtos, clientes, pedidos e fila de preparo para cozinha (backoffice)

## Utilizando Imagem
Garanta que tenha o docker e docker-compose instalados em seu ambiente e execute o comando `docker-compose -f docker-compose.dev.yml up -d` e acesse [localhost:8000](http://localhost:8000) para abrir o projeto.

## Utilizando ambiente local
### Instalando dependências
Garanta que possua o [python ^3.12.6](https://www.python.org/) instalado, instale o [poetry](https://python-poetry.org/docs/#installing-with-pipx) execute o command ``poetry install`` na raiz do projeto.

Suba uma imagem local ou remota do [postgreSQL](https://www.postgresql.org/), configure o ambiente local clonando .env_dev para .env e preenchendo as variáveis de ambiente.

### Iniciando Ambiente Dev
Execute o comando ``poetry run uvicorn app:app --reload`` na raiz do projeto

## Executando Testes unitários
Execute o comando ``poetry run pytest`` na raiz do projeto.

## Swagger / ReDoc

Quando estiver com o servidor rodando localmente, ou via container acesse [localhost:8000/docs](http://localhost:8000/docs) ou [localhost:8000/redoc](http://localhost:8000/redoc)

## Anexo

[Documentação original do desafio](/documentation/Pos_tech%20-%20Fase%201%20-%20Tech%20Challenge%20Fast%20Food.pdf)
[Event Storming E Refinamento Técnico](https://miro.com/app/board/uXjVLf9MJLo=/?share_link_id=933574423173)
[Outras documentações](https://www.notion.so/101117753c9f80cbb28dd5665c721433?v=101117753c9f800b95da000c73dea574&pvs=4)
[Arquitetura Simplificada](/documentation/arquiteturas%20simplificadas.png)
[Domain StoryTelling](/documentation/Domain%20Storytelling.png)