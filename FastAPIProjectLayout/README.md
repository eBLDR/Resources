# App

_By Team_

Main app.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

All app is dockerized, orchestrated by docker-compose. Included services are:

* **app**: app's back-end side
* **MongoDB**: No-SQL database

### Prerequisites

* Docker
* docker-compose
* make

## Deployment

Deploy (includes network setup, build, up, etc.):

```bash
make deploy
```

### [_Optional_] Restore DB data

**¡¡¡ DANGER !!!**

Restore basic necessary data for correct app's usage into DB:

```bash
make db-restore
```

### Building

Build containers and install dependencies:

```bash
make build
```

### Running

Start all services:

```bash
make up
```

Start all services (detached mode):

```bash
make up-d
```

Stop all services:

```bash
make stop
```

Stop and down all services:

```bash
make down
```

## Running the tests

Run complete test suite:

```bash
make tests
```

## Built With

* [FastAPI](https://fastapi.tiangolo.com/) - Asynchronous web framework
* [Motor](https://motor.readthedocs.io/en/stable/) - Asynchronous driver for MongoDB
* [ODMantic](https://art049.github.io/odmantic/) - Asynchronous ODM (Object Document Mapper)

## Versioning

_WIP_

## License

This project is licensed under the MIT License - see the
[LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
