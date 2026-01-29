# API E-commerce com Persistência Híbrida (SQL + NoSQL)

Este repositório contém o código-fonte de uma API REST para uma plataforma de e-commerce, construída com Java, Spring Boot e uma arquitetura de dados moderna utilizando múltiplos serviços de banco de dados na nuvem da Microsoft Azure.

## 🏛️ Arquitetura da API

O projeto implementa um banco de dados mais adequado para cada tipo de dado, otimizando performance, escalabilidade e consistência.

A API centraliza a lógica de negócio, orquestrando as operações entre dois serviços de banco de dados na Azure:

1.  **Azure Cosmos DB (NoSQL):** Armazena o **catálogo de produtos**. Ideal para dados com esquema flexível e que exigem alta throughput de leitura e escrita em escala global.
2.  **Azure Database for MySQL (SQL):** Armazena todos os dados **transacionais e relacionais**, como informações de usuários, endereços, cartões de crédito, pedidos e transações financeiras, garantindo consistência (ACID) e integridade referencial.

O fluxo de dados a partir da perspectiva da API é:

```
Cliente (Ex: Chatbot, App Web)  ──>  API REST (Spring Boot)  ─┬─>  Azure Cosmos DB (Para Produtos)
                                                              └─>  Azure Database for MySQL (Para Usuários, Pedidos, etc.)
```

## 🤖 Arquitetura do Sistema Completo (com Chatbot)

Esta API serve como o backend para um **chatbot conversacional** desenvolvido em Python com o Microsoft Bot Framework. O chatbot atua como a interface do cliente, consumindo os endpoints desta API para realizar as operações.

A arquitetura completa da solução pode ser visualizada abaixo:

```mermaid
graph TD
    subgraph "Interface do Usuário"
        U[👤 Usuário]
    end

    subgraph "Frontend: Chatbot Python"
        B[🤖 Chatbot <br> (Bot Framework)]
    end

    subgraph "Backend: API Java (Este Projeto)"
        A[⚙️ API REST <br> (Spring Boot)]
    end

    subgraph "Nuvem: Microsoft Azure"
        C[Azure Cosmos DB <br> (Banco NoSQL)]
        M[Azure Database for MySQL <br> (Banco SQL)]
    end

    U -- Conversa --> B
    B -- Requisições HTTP --> A
    A -- Consulta Dados --> C
    A -- Grava Transações --> M
```

## ✨ Funcionalidades Principais

  * **Gerenciamento de Usuários:** CRUD completo de usuários e seus dados associados.
  * **Catálogo de Produtos:** CRUD de produtos com busca otimizada no Cosmos DB.
  * **Endereços e Cartões:** Gerenciamento de múltiplos endereços e cartões de crédito por usuário.
  * **Ciclo de Pedidos:** Criação de pedidos, processamento de pagamentos e consulta de status.
  * **Consultas:** Busca de pedidos por produto, extrato de transações do cartão e listagem de pedidos com filtros.

## 🛠️ Tecnologias Utilizadas

### Backend (Esta API)

  * **Linguagem e Framework:** Java 21, Spring Boot
  * **Acesso a Dados:** Spring Data JPA, Spring Data Cosmos
  * **Banco de Dados:** Azure Database for MySQL, Azure Cosmos DB (Core SQL API)
  * **Documentação da API:** SpringDoc (Swagger UI)
  * **Build:** Apache Maven
  * **Utilitários:** Lombok

### Frontend (Chatbot)

  * **Linguagem e Framework:** Python, Microsoft Bot Framework
  * **Comunicação HTTP:** aiohttp, requests

## 📖 Endpoints da API

A documentação interativa completa da API está disponível via Swagger após a execução do projeto.

#### Gerenciamento de Produtos (`/produtos`)

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `POST` | `/` | Cria um novo produto no Cosmos DB. |
| `GET` | `/` | Lista todos os produtos cadastrados. |
| `GET` | `/search` | Busca produtos por parte do nome (`?nome=...`). |
| `PUT` | `/{id}` | Atualiza os dados de um produto. |
| `DELETE`| `/{id}/{categoria}` | Remove um produto (requer ID e chave de partição). |

#### Gerenciamento de Usuários e Endereços (`/usuarios`, `/enderecos`)

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `POST` | `/usuarios` | Cria um novo usuário e seus cartões iniciais. |
| `GET` | `/usuarios` | Lista todos os usuários. |
| `GET` | `/usuarios/{id}` | Busca um usuário por ID. |
| `POST` | `/enderecos` | Cadastra um novo endereço para um usuário. |
| `GET`| `/enderecos/usuario/{usuarioId}` | Lista todos os endereços de um usuário. |

#### Ciclo de Compras e Pedidos (`/pedidos`, `/cartoes`)

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `POST` | `/pedidos/criar` | Cria um novo pedido com os itens do carrinho. |
| `POST` | `/pedidos/processarPagamento/{pedidoId}` | Processa o pagamento de um pedido existente. |
| `GET` | `/pedidos` | Lista todos os pedidos, com filtros opcionais. |
| `POST`| `/cartoes/{id}/compra` | Realiza uma compra direta com um cartão de crédito. |
| `GET`| `/cartoes/{id}/extrato` | Retorna o extrato de transações de um cartão. |

## 🚀 Como Executar o Sistema

Para executar o sistema completo, tanto o backend quanto o frontend (chatbot) precisam estar configurados e rodando.

### Pré-requisitos

  * [Git](https://git-scm.com/)
  * [JDK 21](https://www.oracle.com/java/technologies/javase/jdk21-archive-downloads.html) e [Apache Maven](https://maven.apache.org/download.cgi)
  * [Python 3.8+](https://www.python.org/downloads/) e Pip
  * Uma conta na [Microsoft Azure](https://azure.microsoft.com/)
  * [Bot Framework Emulator](https://github.com/Microsoft/BotFramework-Emulator/releases)

### 1\. Backend (API REST)

#### a. Configuração na Azure

1.  **Crie um Recurso "Azure Database for MySQL":** Anote o servidor, nome do banco, usuário e senha.
2.  **Crie um Recurso "Azure Cosmos DB":**
      * Escolha a API **Core (SQL)**.
      * Crie um banco de dados chamado `ecommerce`.
      * Dentro do banco, crie um contêiner chamado `produtos`.
      * Anote a URI e a Chave Primária do seu recurso Cosmos DB.

#### b. Configuração Local

1.  **Clone o repositório da API:**
    ```bash
    git clone https://github.com/thabus/Projeto_Ecommerce.git
    cd Projeto_Ecommerce
    ```
2.  **Configure as variáveis de ambiente:**
    **NUNCA** coloque suas senhas e chaves diretamente no código. Use variáveis de ambiente. No Linux/macOS:
    ```bash
    export MYSQL_URL="jdbc:mysql://SEU_SERVIDOR.mysql.database.azure.com/ecommerce"
    export MYSQL_USER="SEU_USUARIO"
    export MYSQL_PASS="SUA_SENHA"
    export COSMOS_URI="SUA_URI_DO_COSMOS_DB"
    export COSMOS_KEY="SUA_CHAVE_DO_COSMOS_DB"
    ```
3.  **Atualize o `application.properties`:**
    Altere o arquivo para ler as variáveis de ambiente:
    ```properties
    spring.datasource.url=${MYSQL_URL}
    spring.datasource.username=${MYSQL_USER}
    spring.datasource.password=${MYSQL_PASS}
    azure.cosmos.uri=${COSMOS_URI}
    azure.cosmos.key=${COSMOS_KEY}
    ```

#### c. Execução

1.  **Execute a aplicação com o Maven:**
    ```bash
    mvn spring-boot:run
    ```
2.  **Acesse a documentação da API** no seu navegador para verificar se tudo está funcionando: [http://localhost:8080/swagger-ui.html](https://www.google.com/search?q=http://localhost:8080/swagger-ui.html)

### 2\. Frontend (Chatbot)

1.  **Clone o repositório do chatbot** em uma pasta separada.
2.  **Instale as dependências:**
    ```bash
    # Navegue até a pasta do chatbot
    pip install -r requirements.txt
    ```
3.  **Configure a URL da API:**
      * Certifique-se de que o arquivo `api/rotas.py` do chatbot está apontando para a URL onde sua API Java está rodando (seja `http://localhost:8080` para testes locais ou a URL do seu deploy na Azure).
4.  **Execute o chatbot:**
    ```bash
    python app.py
    ```
5.  **Teste com o Bot Framework Emulator:**
      * Abra o emulador e conecte-se ao endpoint do seu bot, que por padrão é `http://localhost:3978/api/messages`.

## 🤝 Como Contribuir

Contribuições são bem-vindas\! Se você tiver sugestões para melhorar o projeto, por favor, siga estas etapas:

1.  Faça um **Fork** do projeto.
2.  Crie uma nova branch (`git checkout -b feature/sua-feature`).
3.  Faça o commit das suas alterações (`git commit -m 'Adiciona nova feature'`).
4.  Faça o Push para a sua branch (`git push origin feature/sua-feature`).
5.  Abra um **Pull Request**.

## 👤 Autores

Desenvolvido por **Esther Pessanha**, **Thaís Bustamante**, **Douglas Silva**.
