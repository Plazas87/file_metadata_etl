# Challenge
 
ETL project to extract mata data from video files in the file system.

## Requirements

Basic requirements:

* Python ~3.10
* Poetry
* Docker
* Linux 
* Make: run `make help` to see available commands in the Makefile:

## Quickstart

### Setup a virtual env.


Install dependencies

```poetry install```

Activate your virtual environment

```poetry shell```

# Start the ETL.

## Prepare your .env file

Create a new file in the project root called `.env`

Please, copy the content of the `.env_example` to the new `.env` and replace with your values if required.

Start the ETL and the Postgres databese to store the video
information. Plase pay attention to the input format for dates:
DD/MM/YYY 
```bash
make run-etl 01/01/2023 10/01/2023
# Or, without make
export INITIAL_DATE="01/01/2023" END_DATE="05/01/2023" && docker-compose up
```
If you want to modify the current format, you can so it by changing the env variable `DATE_INPUT_FORMAT="%d/%m/%Y" # -> DD/MM/YYYY` within the `.env` file.

Stop the applications and remove its containers
```bash
docker-compose down
# Or, using make
make down
```
