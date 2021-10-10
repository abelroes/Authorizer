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
##### Adapters
Responsáveis por reconhecer o "mundo exterior", definindo qual banco de dados será utilizado, como são as entradas e saídas do projeto, etc.
Concentram a maior parte das operações que causam `side-effects` da aplicação.

##### Controllers

##### Decorators

##### Models

##### Usecases

##### Tests


#### Polimorfismo
#### Banco de Dados
#### Singleton

### Frameworks e Bibliotecas
Além do `pytest` utilizado para os testes, foram usadas, somente, as bibliotecas disponibilizadas pelo Python 3.8. Exemplos são `json`, `datetieme`, `uuid`, `typing`, `dataclass` e outros.

### Outras observações
