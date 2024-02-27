# Authorizer

Authorization system for account creation and card transactions.

<details>
<summary>Expected input example:</summary>
  
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
<summary>Expected output example:</summary>

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

## Index
- [Requirements](#requirements)
- [How to run the project](#how-to-run-the-project)
- [Architecture and Technical Decisions](#architecture-and-technical-decisions)
- [Frameworks and Libraries](#frameworks-and-libraries)
- [Other Observations](#other-observations)

-----

### Requirements
> - Docker 20.10.8, containing:
> 
>     * Python 3.8.10
>     * Pip package manager
>     * pytest
>     

The Docker image build should take care of setting up all the prerequisites to run the system.
In addition, the build already considers running the tests before running the application (without preventing it from running, in case of failure).
If you want to run the tests manually, I suggest installing a `virtual environment` to install the dependencies.
In this case, assuming you already have `Python 3.8`, run from the command line from the project root directory:

```shell
# Installing PIP
python3 -m pip install --upgrade pip

# Installing virtualenv
python3 -m pip install virtualenv

# Creating .venv - if it doesn't work, replace the first 'venv' with 'virtualenv'
python3 -m venv .venv

# Activating venv
source .venv/bin/activate

# Installing requirements.txt
python3 -m pip install -r requirements.txt
```

> source: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

This process will install `pytest` in the virtual environment so that you can run the tests manually:

```shell
cd src/
python3 -m pytest
```

### How to run the project
To run the project, you need to prepare an `operations` file containing the inputs and run the following commands:
```shell
docker build --no-cache -t authorizer .

# Define file's correct path for the following command
docker run -i authorizer < PATH_TO_operations_FILE
```
The `buildAndRun.sh` script can be executed, which considers an `operations` file _(not included)_ within the project root directory.

### Architecture and Technical Decisions

#### Project Structure
The project is organized using the following directory tree:

###### Main
Start of application execution. Receives the file via _stdin_, delegating digestion to _adapters_ and processing to _controllers_.

###### Adapters
Responsible for intermediating the "outside world", defining which database will be used, what the inputs and outputs of the project are like, etc.
They concentrate most of the operations that manage the application's _side-effects_.

###### Controllers
Separated into _formaters_, _handlers_ and _persistence_. They control flow, conversion of input data to more internal layers of the application (e.g.: _models_ and _usecases_) and output data so that _adapters_ can perform the _output_ actions.

It is the last layer that should tolerate methods that cause _side-effects_.

Highlight for the `OperationMapper` class, which forks the flow right at the beginning, using different types of operations to decide which function to delegate data processing to.

###### Decorators
It houses custom definitions of _decorators_ that can be used as _syntactic sugar_, adding mechanisms to other functions. For example, the `@singleton` decorator.

###### Models
It houses _dataclasses_ that represent entities within the application. Defines the operations data format for use by _controllers_ and _usecases_.

###### Usecases
These are the business rule functions, housing the definitions of violations. All violations of each operation are decided by the functions in that directory.

###### Tests
Directory containing application tests.

#### Polymorphism
Although Python is a dynamically typed language and the system was written prioritizing functions, it was decided to use class definitions with polymorphism in some cases, in order to facilitate code readability and maintenance.

For example, by defining the expected input and output types of each function, polymorphism allows inner classes (e.g., _usecases_) not to worry about specifications of types of transacted objects, but to define the expected generic scope (e.g., `GenericAccount -> StandardAccount`)_.

#### Database
It was used an in-memory dictionary for storing account data and validated transaction history, allowing easy management and rapid data retrieval and persistence via a key-value mechanism.

#### Singleton
To make managing the chosen database instance more practical, the _design pattern Singleton_ was used in a way that, in any part of the code, a valid instance of the bank was easily available. Additionally, using the `@singleton` decorator makes adding this capability more elegant.

### Frameworks and Libraries
In addition to `pytest` used for testing, only the libraries provided by Python 3.8 were used. Examples are `json`, `datetieme`, `uuid`, `typing`, `dataclass`.

### Other observations
The application analyzes operations individually, but processes the file as a whole. This means that the response comes out once per file _input_.
This option was chosen because it facilitates the management of the application state (which must be new for each input file) and makes the process of analyzing operations more _clean_.

An optimization could be made if the file size grew a lot and the response was more urgent for each operation. Therefore, the return should be individual.
