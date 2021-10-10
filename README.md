# Authorizer

Sistema de autorização de operações de criação de conta e transações com cartão.

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

Esse processo instalará o `pytest` no ambiente virtual para que seja possível rodar os testes manualmente.

```shell
cd src/
python3 -m pytest
```

### Como rodar o projeto
Para rodar o projeto, é necessário preparar um arquivo `operations` contendo as entradas e rodar os seguintes comandos:
```shell
docker build --no-cache -t authorizer .
docker run -i authorizer < operations
```
Está incluído o script `buildAndRun.sh`, que considera o arquivo `operations` dentro do diretório raiz do projeto.

### Arquitetura e Decisões Técnicas

#### Estrutura do Projeto
O projeto está organizado utilizando a seguinte árvore de diretórios:

###### Main
Início da execução da aplicação. Recebe o arquivo via _stdin_ e delega a digestão para _adapters_ e o processamento para _controllers_.

###### Adapters
Responsáveis por reconhecer o "mundo exterior", definindo qual banco de dados será utilizado, como são as entradas e saídas do projeto, etc.
Concentram a maior parte das operações que gerenciam _side-effects_ da aplicação.

###### Controllers
Separados em _formaters_, _handlers_ e _persistence_. Controlam fluxo, conversão de dados de entrada para camadas mais internas da aplicação (ex.: _models_ e _usecases_) e dados de saída para que _adapters_ possam realizar as ações de _output_.

É a última camada que deveria tolerar métodos que causem `side-effects`.

Destaque para a classe `OperationMapper`, que bifurca o fluxo logo no início, utilizando tipos diferentes de operações para decidir para qual função delegar o tratamento dos dados.

###### Decorators
Abrigam definições customizadas de _decorators_ que podem ser usados como _synthatic sugar_ e adicionar mecanismos a outras funções. A exemplo, o decorator `@singleton`.

###### Models
Abriga _dataclasses_ que representam entidades dentro da aplicação. Definem o formato de dados que as operações têm para utilização pelos _controllers_ e _usecases_.

###### Usecases
São as funções de regra de negócio. Todas as violações ou não de cada operação é decidida pelas funções abrigadas nesse diretório.

Também abriga as definições das violações.

Não executa nenhum tratamento de dados.

###### Tests
Diretório que abriga os testes da aplicação.

#### Polimorfismo
Procurou-se escrever o sistema utilizando mais funções do que definições de classes e objetos. Contudo, em alguns momentos, pareceu adequado lançar mão de utilizar polimorfismo em algumas classes e tipos.

Apesar de Python ser uma linguagem dinamicamente tipada, é de bom tom deixar definidos os tipos esperados de entrada e saída de cada função, para que a leitura e manutenção do código seja mais fácil. Por isso, utilizar o polimorfismo permite que classes mais internas (ex.:_usecases_) não se preocupem com especificações de tipos de objetos transacionados, mas definam o escopo genérico esperado _(ex.: `GenericAccount -> StandardAccount`)_.

#### Banco de Dados
Optou-se por utilizar um dicionário em memória para o armazenamento de dados de conta e histórico de transações validadas. Isso permite fácil gerenciamento e rapidez na recuperação dos dados via mecanismo de chave-valor.

#### Singleton
Para que a gestão da instância do banco de dados escolhido fosse mais prática, utilizou-se o _design pattern Singleton_ para que, em qualquer parte do código, estivesse facilmente disponível a instância válida do banco. Além disso, a utilização do decorator `@singleton` torna a adição dessa capacidade mais elegante.

### Frameworks e Bibliotecas
Além do `pytest` utilizado para os testes, foram usadas, somente, as bibliotecas disponibilizadas pelo Python 3.8. Exemplos são `json`, `datetieme`, `uuid`, `typing`, `dataclass` e outras.

### Outras observações
A aplicação analisa as operações individualmente, mas processa o arquivo por inteiro. Isso significa que a resposta sai uma vez por _input_ de arquivo. Essa opção foi eleita por facilitar a gestão do estado da aplicação (que deve ser nova a cada novo arquivo de entrada) e tornar mais _clean_ o processo de análise das opeprações.

Uma otimização poderia ser feita, caso o tamanho do arquivo crescesse muito e a resposta fosse, necessariamente e individualmente, mais urgente. Dessa forma, o retorno deveria ser individual.
