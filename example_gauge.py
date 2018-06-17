

## For python2 or python3

## Terribly simple example gauge for Prometheus.
## Lives on port 8000.

## If an HTTP connection to 127.0.0.1:81 could be made,
## it reads 10. If not, it reads 0.
## (As a special case, it initializes at 5,
## but this value is never exposed.)

## It will run until manually killed.

## Based on the Summary example at
## https://github.com/prometheus/client_python/blob/dc15164f4/README.md

from prometheus_client import start_http_server, Gauge # , Summary
import random
import socket
import time

MY_GAUGE = Gauge('my_gauge', 'My first gauge')
MY_GAUGE.set(5)

def process_request():
    """Attempt HTTP connection and set the gauge's value appropriately"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 81))
        MY_GAUGE.set(0)
    except Exception:
        MY_GAUGE.set(10)


if __name__ == '__main__':
    ## Set a meaningful value before spinning up the server
    process_request()

    # Start up the server to expose the metrics.
    start_http_server(8000)

    ## Update the gauge's value every second.
    ## (Ignoring the time it takes to run the function!)
    while True:
        time.sleep(1.0)
        process_request()

