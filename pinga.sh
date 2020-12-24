#!/bin/bash

install_dependencies() {
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install -r requirements.txt
}

if [ $# -lt 1 ]; then
    echo "FATAL: No parameter supplied. Usage: ./pinga.sh producer|consumer"
    exit 1
elif [ $1 == "producer" ]; then
    install_dependencies
    .venv/bin/python run_producer.py
elif [ $1 == "consumer" ]; then
    install_dependencies
    .venv/bin/python run_consumer.py
else
    echo "FATAL: Unknown option ${1}. Valid options are: producer|consumer"
fi
