-include .env
export

ifeq ($(OS),Windows_NT)
	OPEN_CMD = cmd /c start
else
	UNAME_S := $(shell uname -s)
	ifeq ($(UNAME_S),Linux)
		OPEN_CMD = xdg-open
	endif
	ifeq ($(UNAME_S),Darwin)
		OPEN_CMD = open
	endif
endif

#----------General----------#

# Extract arguments of the subcommand
.PHONY: _run_args
_run_args:
  # use the rest as arguments for the subcommand
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)

# target: help - Display callable targets.
.PHONY: help
help:
	@egrep "^# target:" [Mm]akefile

#----------Docker Application commands----------#

# target: run-etl - Start the ETL 
.PHONY: run-etl
run-etl: _run_args
	export INITIAL_DATE=$(word 1,$(RUN_ARGS)) && export END_DATE=$(word 2,$(RUN_ARGS)) && docker-compose up | docker compose up

# target: down - Stop and remove all the containers
.PHONY: down
down:
	docker compose down

# target: docker_shell - Docker command: open an interactive terminal in a running container
.PHONY: docker_shell
docker_shell: _run_args
	docker exec -it $(RUN_ARGS) /bin/bash

