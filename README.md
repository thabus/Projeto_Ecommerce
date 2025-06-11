Integrantes:
- Esther Pessanha
- Thaís Bustamante
- Douglas Silva

Projeto E-commerce - API de Dados na NuvemBem-vindo ao backend do Projeto E-commerce. Esta não é uma aplicação web monolítica, mas sim uma API de dados moderna construída em Java com Spring Boot, projetada para operar em um ambiente de nuvem e Big Data, utilizando uma arquitetura de persistência híbrida na Microsoft Azure.🏛️ Arquitetura do ProjetoO core deste projeto é uma API REST que orquestra dados entre dois tipos de bancos de dados na Azure, cada um escolhido por sua especialidade:Azure Database for MySQL (Banco Relacional): Armazena dados transacionais e estruturados que exigem consistência e relacionamentos claros, como:UsuariosEnderecosCartoesDeCreditoAzure Cosmos DB (Banco NoSQL - Multimodelo): Armazena o catálogo de Produtos. Foi escolhido por sua alta escalabilidade, flexibilidade de schema e performance para grandes volumes de dados (cenário de Big Data). A entidade Produto utiliza categoria como Chave de Partição, otimizando a distribuição e a consulta de dados em larga escala.Diagrama de Fluxo de Dadosgraph TD
    subgraph Cliente
        A[Usuário via Postman/Frontend]
    end

    subgraph "API Backend (Spring Boot)"
        B(API Gateway / Controllers)
        C{Lógica de Negócio / Services}
    end

    subgraph "Camada de Dados (Azure Cloud)"
        D[Azure DB for MySQL]
        E[Azure Cosmos DB]
    end

    A -- Requisição HTTP --> B
    B -- Chama --> C
    C -- Dados Relacionais (Usuário, Cartão) --> D
    C -- Dados do Catálogo (Produto) --> E
    D -- Responde --> C
    E -- Responde --> C
    C -- Retorna DTO --> B
    B -- Resposta HTTP --> A
✨ Funcionalidades da APIA API expõe um conjunto de endpoints RESTful para gerenciar as principais entidades do sistema de e-commerce:Gerenciamento de Usuários: CRUD completo para usuários e seus endereços.Gerenciamento de Pagamentos: CRUD para cartões de crédito, simulação de compras e extrato de transações.Catálogo de Produtos: CRUD completo para produtos, com buscas otimizadas no Cosmos DB.Sistema de Pedidos: Lógica para criar pedidos, processar pagamentos e consultar o histórico, combinando dados dos dois bancos de dados.🛠️ Tecnologias UtilizadasBackend:Java 21Spring Boot 3Spring Data JPASpring WebMavenLombokCloud & Banco de Dados:Azure Database for MySQLAzure Cosmos DB (via spring-cloud-azure-starter-data-cosmos)Documentação da API:SpringDoc OpenAPI (Swagger)🚀 Configuração e ExecuçãoSiga os passos abaixo para configurar e executar o projeto localmente.Pré-requisitosGitJDK 21MavenUma conta na Microsoft Azure com os serviços de MySQL e Cosmos DB provisionados.Passo a PassoClone o repositório:git clone https://github.com/thabus/Projeto_Ecommerce.git
cd Projeto_Ecommerce
Configure as Variáveis de Ambiente:NUNCA coloque suas chaves e senhas diretamente no arquivo application.properties. A forma correta é usar variáveis de ambiente.Crie um arquivo .env na raiz do projeto (este arquivo não deve ser enviado ao Git) ou configure as variáveis diretamente no seu sistema operacional.Exemplo de .env:# Configuracao do Banco de Dados MySQL na Azure
DB_URL=jdbc:mysql://SEU_HOST_MYSQL.mysql.database.azure.com/ecommerce
DB_USER=SEU_USUARIO
DB_PASS=SUA_SENHA_MYSQL

# Configuracao do Cosmos DB na Azure
COSMOS_URI=https://SEU_COSMOS_ACCOUNT.documents.azure.com:443/
COSMOS_KEY=SUA_CHAVE_PRIMARIA_COSMOS
COSMOS_DB_NAME=ecommerce
Ajuste o application.properties:Altere seu arquivo src/main/resources/application.properties para ler essas variáveis de ambiente.# Configuracao do Banco de Dados
spring.datasource.url=${DB_URL}
spring.datasource.username=${DB_USER}
spring.datasource.password=${DB_PASS}
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQLDialect
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true

# Configuracao do Cosmos DB
azure.cosmos.uri=${COSMOS_URI}
azure.cosmos.key=${COSMOS_KEY}
azure.cosmos.database=${COSMOS_DB_NAME}
azure.cosmos.queryMetricsEnabled=true
azure.cosmos.responseDiagnosticsEnabled=true

# Outras configs
server.port=8080
spring.application.name=ecommerce
springdoc.api-docs.enabled=true
springdoc.swagger-ui.enabled=true
Execute a aplicação:mvn spring-boot:run
📖 Documentação da API (Swagger)Com a aplicação em execução, você pode explorar e interagir com todos os endpoints através da interface do Swagger UI.Acesse o seguinte endereço no seu navegador:http://localhost:8080/swagger-ui.html🤝 Como ContribuirContribuições são bem-vindas! Se você tem ideias para melhorias ou encontrou algum problema, sinta-se à vontade para:Fazer um Fork do projeto.Criar uma nova branch (git checkout -b feature/minha-feature).Fazer o commit das suas alterações (git commit -m 'Adiciona minha feature').Fazer o Push para a sua branch (git push origin feature/minha-feature).Abrir um Pull Request.👤 AutorFeito por thabus.
