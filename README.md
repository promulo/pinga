![CI](https://github.com/promulo/pinga/workflows/CI/badge.svg) [![Maintainability](https://api.codeclimate.com/v1/badges/0c81b87985e948b90544/maintainability)](https://codeclimate.com/github/promulo/pinga/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/0c81b87985e948b90544/test_coverage)](https://codeclimate.com/github/promulo/pinga/test_coverage)

# Pinga - A simple website status checker

Pinga is website status checker written in Python. It consists of two independent parts.
On one hand, there is a producer that asynchronously and periodically (every 5 seconds)
checks a given list of websites and sends the results as events to a configured aiven Kafka
cluster. The second component is a consumer of Kafka messages that will process the produced
events and persist them in a configured aiven PostgreSQL database.

Given the nature of Kafka, both processes above are independent from each other and can be
executed in any given order.

## Dependencies

* Python 3
* gevent
* kafka-python
* psycopg2
* jsonschema
* requests
* aiven Kafka
* aiven PostgreSQL

## Setup of aiven services and Pinga configuration

At this stage of development, Pinga relies on two DBaaS products: [**aiven for Apache Kafka**](https://aiven.io/kafka) and [**aiven for PostgreSQL**](https://aiven.io/postgresql). It is assumed that those services are provisioned and running. Please refer to [aiven](https://help.aiven.io/en/articles/489573-getting-started-with-aiven-postgresql)
[documentation](https://help.aiven.io/en/articles/489572-getting-started-with-aiven-kafka) for
details about setting up those services.

Pinga configuration is set in the `pinga.cfg` file. It consists of three sections, `kafka`,
`postgres` and `checker`.

### kafka
This section specifies the aiven Kafka cluster that Pinga will connect to. Please replace the
placeholders for `service_uri`, `ssl_cafile`, `ssl_certfile` and `ssl_keyfile` with the appropriate
values. They can be easily retrieved from the aiven console.

### postgres
This section defines the PostgreSQL instance where events will be saved. Please fill the
`service_uri` with the value provided by the aiven console.

### checker
This section specifies a JSON file containing a list of websites to be checked by Pinga. An example
is provided and named `sites.json`.

## Running Pinga components using docker-compose

The easiest way to see Pinga working is by running the provided `docker-compose` configuration.
```
$ docker-compose up
```
The command above will run both Pinga Producer and Pinga Consumer in separate containers.

In case of code changes, `docker-compose build` must be executed before restarting.

## Running Pinga components separately as standalone processes

### Pinga Producer

The producer is responsible for making periodic checks and send the results to the Kafka cluster.
It can be run as a standalone process by doing the following:
```
$ ./pinga.sh producer
```

### Pinga Consumer

The consumer connects to the Kafka cluster, subscribe to the topic and consume the messages as
they arrive. All events are persisted in PostgreSQL right after consumption. The consumer can
be executed by doing the following:
```
$ ./pinga.sh consumer
```

## Running the tests

The unit tests were based on `pytest`. They can be executed by following these steps:
```
$ python3 -m venv .venv-tests
$ source .venv-tests/bin/activate
$ pip3 install -r requirements.txt
$ pip3 install -r requirements-dev.txt
$ pytest -v
```
Assuming the above is done, test coverage data can be generated by running `coverage`.
```
$ coverage run --source ./pinga -m pytest
$ coverage report -m
```

## CI

Tests and Code Climate checks are done for every PR. [GitHub Actions](https://github.com/promulo/pinga/actions) is triggered for every PR and after a merge into `master`.

## Links

* [TODO](https://github.com/promulo/pinga/blob/master/TODO.md)
* [Kanban board](https://github.com/promulo/pinga/projects/1)
* [Open issues](https://github.com/promulo/pinga/issues)

## Further documentation and references

* https://help.aiven.io/en/articles/489573-getting-started-with-aiven-postgresql
* https://help.aiven.io/en/articles/489572-getting-started-with-aiven-kafka
* https://kafka-python.readthedocs.io/en/master/index.html
* http://www.gevent.org/
* https://www.psycopg.org/
* https://requests.readthedocs.io/en/master/
* https://registry.terraform.io/providers/aiven/aiven/latest/docs
