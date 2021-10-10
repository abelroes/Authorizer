# Authorizer

Sistema de autorização de operações de criação de conta e transações com cartão.

<details>
<summary>Exemplo de entrada esperada:</summary>
  
```json
{"account": {"active-card": true, "available-limit": 100}}
{"transaction": {"merchant": "McDonald's", "amount": 10, "time": "2019-02-13T11:00:01.000Z"}}
{"account": {"active-card": true, "available-limit": 100}}
{"transaction": {"merchant": "Burger King", "amount": 20, "time": "2019-02-13T11:00:02.000Z"}}
{"transaction": {"merchant": "Burger King", "amount": 5, "time": "2019-02-13T11:00:07.000Z"}}
{"transaction": {"merchant": "Burger King", "amount": 5, "time": "2019-02-13T11:00:08.000Z"}}
{"transaction": {"merchant": "Burger King", "amount": 150, "time": "2019-02-13T11:00:18.000Z"}}
{"transaction": {"merchant": "Burger King", "amount": 190, "time": "2019-02-13T11:00:22.000Z"}}
{"transaction": {"merchant": "Burger King", "amount": 15, "time": "2019-02-13T12:00:27.000Z"}}
```
</details>


<details>
<summary>Exemplo de saída esperada:</summary>

```json
{"account": {"active-card": true, "available-limit": 100}, "violations": []}
{"account": {"active-card": true, "available-limit": 90}, "violations": []}
{"account": {"active-card": true, "available-limit": 100}, "violations": ["account-already-initialized"]}
{"account": {"active-card": true, "available-limit": 70}, "violations": []}
{"account": {"active-card": true, "available-limit": 65}, "violations": []}
{"account": {"active-card": true, "available-limit": 65}, "violations": ["high-frequency-small-interval", "doubled-transaction"]}
{"account": {"active-card": true, "available-limit": 65}, "violations": ["high-frequency-small-interval", "insufficient-limit"]}
{"account": {"active-card": true, "available-limit": 65}, "violations": ["high-frequency-small-interval", "insufficient-limit"]}
{"account": {"active-card": true, "available-limit": 50}, "violations": []}

```
</details>

-----

## Índice
- [Requisitos](#requisitos)
- [Como rodar o projeto](#como-rodar-o-projeto)
- [Arquitetura e Decisões Técnicas](#arquitetura-e-decisões-técnicas)
- [Frameworks e Bibliotecas](#frameworks-e-bibliotecas)
- [Outras observações](#outras-observações)

-----

### Requisitos
> - Docker 20.10.8, contendo:
> 
>     * Python 3.8.10
>     * Gerenciador de pacotes pip
>     * pytest
>     

O build da imagem docker deveria dar conta de subir com todos os pré-requisitos para rodar o sistema.

Além disso, o build já considera rodar os testes antes de rodar a aplicação (sem impedir que ela rode, em caso de falha).
Se desejar rodar os testes manualmente, sugiro instalar um `virtual environment` para instalar as dependências.
Neste caso, assumindo que já possua o `Python 3.8`, rode da linha de comando a partir do diretório raiz do projeto:

```shell
# Instalando PIP
python3 -m pip install --upgrade pip

# Instalando virtualenv
python3 -m pip install virtualenv

# Criando .venv - caso não funcione, troque o primeiro 'venv' por 'virtualenv'
python3 -m venv .venv

# Ativando venv
source .venv/bin/activate

# Instalando requirements.txt
python3 -m pip install -r requirements.txt
```

> fonte: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

Esse processo instalará o `pytest` no ambiente virtual para que seja possível rodar os testes manualmente:

```shell
cd src/
python3 -m pytest
```

### Como rodar o projeto
Para rodar o projeto, é necessário preparar um arquivo `operations` contendo as entradas e rodar os seguintes comandos:
```shell
docker build --no-cache -t authorizer .
docker run -i authorizer < PATH_TO_operations_FILE
```
Está incluído o script `buildAndRun.sh`, que considera um arquivo `operations` _(não incluso)_ dentro do diretório raiz do projeto.

### Arquitetura e Decisões Técnicas

#### Estrutura do Projeto
O projeto está organizado utilizando a seguinte árvore de diretórios:

###### Main
Início da execução da aplicação. Recebe o arquivo via _stdin_, delegando a digestão para _adapters_ e o processamento para _controllers_.

###### Adapters
Responsáveis por intermediar o "mundo exterior", definindo qual banco de dados será utilizado, como são as entradas e saídas do projeto, etc.
Concentram a maior parte das operações que gerenciam _side-effects_ da aplicação.

###### Controllers
Separados em _formaters_, _handlers_ e _persistence_. Controlam fluxo, conversão de dados de entrada para camadas mais internas da aplicação (ex.: _models_ e _usecases_) e dados de saída para que _adapters_ possam realizar as ações de _output_.

É a última camada que deveria tolerar métodos que causem _side-effects_.

Destaque para a classe `OperationMapper`, que bifurca o fluxo logo no início, utilizando tipos diferentes de operações para decidir para qual função delegar o tratamento dos dados.

###### Decorators
Abrigam definições customizadas de _decorators_ que podem ser usados como _synthatic sugar_, adicionando mecanismos a outras funções. A exemplo, o decorator `@singleton`.

###### Models
Abriga _dataclasses_ que representam entidades dentro da aplicação. Definem o formato de dados das operações para utilização pelos _controllers_ e _usecases_.

###### Usecases
São as funções de regra de negócio, abrigando as definições das violações. Todas as violações de cada operação são decididas pelas funções nesse diretório.

###### Tests
Diretório contendo os testes da aplicação.

#### Polimorfismo
Apesar de Python ser uma linguagem dinamicamente tipada e o sistema ter sido escrito priorizando funções, optou-se por utilizar definições de classes com polimorfismo em alguns casos, a fim de facilitar a legibilidade e manutenção do código.

Por exemplo, ao definir os tipos esperados de entrada e saída de cada função, o polimorfismo permite que classes mais internas (ex.:_usecases_) não se preocupem com especificações de tipos de objetos transacionados, mas definam o escopo genérico esperado _(ex.: `GenericAccount -> StandardAccount`)_.

#### Banco de Dados
Utilizou-se um dicionário em memória para o armazenamento de dados de conta e histórico de transações validadas, permitindo fácil gerenciamento e rapidez na recuperação e persistência dos dados via mecanismo de chave-valor.

#### Singleton
Para que a gestão da instância do banco de dados escolhido fosse mais prática, utilizou-se o _design pattern Singleton_ para que, em qualquer parte do código, estivesse facilmente disponível a instância válida do banco. Além disso, a utilização do decorator `@singleton` torna a adição dessa capacidade mais elegante.

### Frameworks e Bibliotecas
Além do `pytest` utilizado para os testes, foram usadas somente as bibliotecas disponibilizadas pelo Python 3.8. Exemplos são `json`, `datetieme`, `uuid`, `typing`, `dataclass`.

### Outras observações
A aplicação analisa as operações individualmente, mas processa o arquivo por inteiro. Isso significa que a resposta sai uma vez por _input_ de arquivo. Essa opção foi eleita por facilitar a gestão do estado da aplicação (que deve ser novo a cada arquivo de entrada) e tornar mais _clean_ o processo de análise das operações.

Uma otimização poderia ser feita, caso o tamanho do arquivo crescesse muito e a resposta fosse mais urgente para cada operação. Dessa forma, o retorno deveria ser individual.
