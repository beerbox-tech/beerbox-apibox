<center>
<br/>
<img src="https://user-images.githubusercontent.com/10991276/219882345-8aef7dad-d428-4af0-aa26-4c08c00253f6.png" alt="Logo" width="192" height="192">
### Beerbox API

[![license](https://img.shields.io/github/license/beerbox-tech/beerbox-apibox.svg?style=for-the-badge)](https://github.com/beerbox-tech/beerbox-apibox/blob/main/LICENSE)
[![coverage](https://img.shields.io/badge/coverage-100%25-green?style=for-the-badge)](https://github.com/beerbox-tech/beerbox-apibox/)
[![python](https://img.shields.io/badge/python-v3.10-green?style=for-the-badge)](https://www.python.org/downloads/release/python-3100/)
</center>

## Prerequisites

Before getting started, ensure you have met the following requirements:
- You have a working installation of **python** with **poetry**
- You have a working installation of a **docker-like CLI** (docker, podman, etc.)

## Getting started

Start a local development server with the following steps:

```bash
# initialize local environment
$ make init

# start up the database
$ make database

# apply database migrations
$ make database-upgrade

# run the development server
$ make serve

# make sure everything works fine
$ curl http://localhost:8000/readyz | jq
{
  "status": "pass",
  "checks": [
    {
      "name": "apibox:ready",
      "time": "2022-02-22T09:41:00.000000+01:00",
      "status": "pass",
      "observedValue": "true",
      "observedUnit": "boolean"
    },
    {
      "name": "database:ready",
      "time": "2022-02-22T09:41:00.000000+01:00",
      "status": "pass",
      "observedValue": "true",
      "observedUnit": "boolean"
    }
  ],
  "version": "dev",
  "service": "apibox"
}
```