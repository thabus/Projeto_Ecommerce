# Projeto_Ecommerce

Integrantes:
- Esther Pessanha
- Thaís Bustamante
- Douglas Silva

Este é um projeto de e-commerce que permite que usuários comprem produtos e que administradores gerem relatórios de vendas usando Big Data.

A Arquitetura inclui:
- **API Gateway** para rotear requisições
- **Backend** gerenciado com Azure App Service
- **Banco de Dados NoSQL** para armazenar produtos e pedidos
- **Banco de Dados Relacional** para gestão de usuários
- **Pipeline de Big Data Simplificado** para análise de vendas
- **Gestão de Produtos** para administração do catálogo
- **Criação de Usuário com Cartão de Crédito** para facilitar pagamentos
- **Regras de Saldo no Cartão de Crédito** para garantir a disponibilidade de fundos
- **Deploy via GitHub Actions** para automação do processo de implantação
- **Testes de Unidade no Backend** para garantir a qualidade do código

#### 1. API GATEWAY
- Responsável por gerenciar e rotear requisições para os serviços adequados.
- Endpoints principais:
 - `POST /pedido` → Criar um pedido
 - `GET /produtos` → Listar produtos
 - `POST /produto` → Criar um novo produto
 - `PUT /produto/{id}` → Atualizar um produto
 - `DELETE /produto/{id}` → Remover um produto
 - `POST /usuario` → Criar um usuário com cartão de crédito
 - `PUT /usuario/{id}` → Atualizar informações do usuário
 - `GET /relatorio-vendas` → Gerar relatório de vendas

#### 2. Backend (App Service)
- Implementado com Azure App Service.
- Funções principais:
  - Criar pedidos e armazenar no banco de dados
  - Listar, criar, atualizar e remover produtos
  - Criar e atualizar usuários com informações de cartão de crédito
  - Verificar saldo disponível no cartão de crédito antes de confirmar a compra
  - Enviar dados de vendas para análise no pipeline de Big Data
  - Executar testes de unidade para validar funcionalidades

#### 3. Banco de Dados
- Banco NoSQL: Azure Cosmos DB
- Banco Relacional: Azure SQL Database
