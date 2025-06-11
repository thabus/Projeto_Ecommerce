# Projeto E-commerce - API de Dados na Nuvem ☁️

Este repositório contém o código-fonte de uma API REST para uma plataforma de e-commerce, construída com Java, Spring Boot e uma arquitetura de dados moderna utilizando múltiplos serviços de banco de dados na nuvem da Microsoft Azure.

## 🏛️ Arquitetura da Solução

O projeto implementa um banco de dados mais adequado para cada tipo de dado, otimizando performance, escalabilidade e consistência.

A API centraliza a lógica de negócio, orquestrando as operações entre dois serviços de banco de dados na Azure:

1.  **Azure Cosmos DB (NoSQL):** Armazena o **catálogo de produtos**. Ideal para dados com esquema flexível e que exigem alta throughput de leitura e escrita em escala global.
2.  **Azure Database for MySQL (SQL):** Armazena todos os dados **transacionais e relacionais**, como informações de usuários, endereços, cartões de crédito, pedidos e transações financeiras, garantindo consistência (ACID) e integridade referencial.

O fluxo de dados pode ser visualizado da seguinte forma:

```
Cliente (Via App/Web)  ──>  API REST (Spring Boot)  ─┬─>  Azure Cosmos DB (Para Produtos)
                                                   └─>  Azure Database for MySQL (Para Usuários, Pedidos, etc.)
```

## ✨ Funcionalidades Principais

  * **Gerenciamento de Usuários:** CRUD completo de usuários e seus dados associados.
  * **Catálogo de Produtos:** CRUD de produtos com busca otimizada no Cosmos DB.
  * **Endereços e Cartões:** Gerenciamento de múltiplos endereços e cartões de crédito por usuário.
  * **Ciclo de Pedidos:** Criação de pedidos, processamento de pagamentos e consulta de status.
  * **Consultas:** Busca de pedidos por produto, extrato de transações do cartão e listagem de pedidos com filtros.

## 🛠️ Tecnologias Utilizadas

  * **Backend:** Java 21, Spring Boot
  * **Acesso a Dados:** Spring Data JPA, Spring Data Cosmos
  * **Banco de Dados:** Azure Database for MySQL, Azure Cosmos DB (Core SQL API)
  * **Documentação da API:** SpringDoc (Swagger UI)
  * **Build:** Apache Maven
  * **Utilitários:** Lombok

## 📖 Endpoints da API

A documentação interativa completa da API está disponível via Swagger após a execução do projeto.

### Principais Endpoints:

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

## 🚀 Como Executar o Projeto

### Pré-requisitos

  * [Git](https://git-scm.com/)
  * [JDK 21](https://www.oracle.com/java/technologies/javase/jdk21-archive-downloads.html)
  * [Apache Maven](https://maven.apache.org/download.cgi)
  * Uma conta na [Microsoft Azure](https://azure.microsoft.com/)

### 1\. Configuração na Azure

1.  **Crie um Recurso "Azure Database for MySQL":** Anote o servidor, nome do banco, usuário e senha.
2.  **Crie um Recurso "Azure Cosmos DB":**
      * Escolha a API **Core (SQL)**.
      * Crie um banco de dados chamado `ecommerce`.
      * Dentro do banco, crie um contêiner chamado `produtos`.
      * Anote a URI e a Chave Primária do seu recurso Cosmos DB.

### 2\. Configuração Local

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/thabus/Projeto_Ecommerce.git
    cd Projeto_Ecommerce
    ```

2.  **Configure as variáveis de ambiente:**
    **NUNCA** coloque suas senhas e chaves diretamente no código. Use variáveis de ambiente.

    **No Linux/macOS:**

    ```bash
    export MYSQL_URL="jdbc:mysql://SEU_SERVIDOR.mysql.database.azure.com/ecommerce"
    export MYSQL_USER="SEU_USUARIO"
    export MYSQL_PASS="SUA_SENHA"
    export COSMOS_URI="SUA_URI_DO_COSMOS_DB"
    export COSMOS_KEY="SUA_CHAVE_DO_COSMOS_DB"
    ```

    **No Windows (PowerShell):**

    ```powershell
    $env:MYSQL_URL="jdbc:mysql://SEU_SERVIDOR.mysql.database.azure.com/ecommerce"
    $env:MYSQL_USER="SEU_USUARIO"
    $env:MYSQL_PASS="SUA_SENHA"
    $env:COSMOS_URI="SUA_URI_DO_COSMOS_DB"
    $env:COSMOS_KEY="SUA_CHAVE_DO_COSMOS_DB"
    ```

3.  **Atualize o `application.properties`:**
    Altere seu arquivo `src/main/resources/application.properties` para ler as variáveis de ambiente:

    ```properties
    # Configuracao do Banco de Dados
    spring.datasource.url=${MYSQL_URL}
    spring.datasource.username=${MYSQL_USER}
    spring.datasource.password=${MYSQL_PASS}
    spring.jpa.hibernate.ddl-auto=update

    # Configuracao do Cosmos DB
    azure.cosmos.uri=${COSMOS_URI}
    azure.cosmos.key=${COSMOS_KEY}
    azure.cosmos.database=ecommerce
    ```

### 3\. Execução

1.  **Execute a aplicação usando o Maven:**
    ```bash
    mvn spring-boot:run
    ```
2.  **Acesse a documentação da API:**
    Abra seu navegador e acesse: [http://localhost:8080/swagger-ui.html](https://www.google.com/search?q=http://localhost:8080/swagger-ui.html)

## 🤝 Como Contribuir

Contribuições são bem-vindas\! Se você tiver sugestões para melhorar o projeto, por favor, siga estas etapas:

1.  Faça um **Fork** do projeto.
2.  Crie uma nova branch (`git checkout -b feature/sua-feature`).
3.  Faça o commit das suas alterações (`git commit -m 'Adiciona nova feature'`).
4.  Faça o Push para a sua branch (`git push origin feature/sua-feature`).
5.  Abra um **Pull Request**.

## 👤 Autores

Desenvolvido por **Esther Pessanha**,**Thaís Bustamante**,**Douglas Silva**.

[](https://www.google.com/search?q=https://github.com/thabus)
