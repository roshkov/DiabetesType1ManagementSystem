.PHONY : up down create-env

# Up Zeebe & Siddhi
up: create-env
	sudo docker-compose -f services/docker-compose.yml -f services/docker-compose.siddhi.yml -f services/docker-compose.zeebe.yml --env-file .env up -d

build-external:
	sudo docker-compose \
			-f services/docker-compose.yml \
			-f services/docker-compose.siddhi.yml \
			-f services/docker-compose.camunda.yml \
			-f services/docker-compose.external.yml \
			--env-file .env up -d \
			--build external


up-camunda: create-env build-external
	sudo docker-compose \
			-f services/docker-compose.yml \
			-f services/docker-compose.siddhi.yml \
			-f services/docker-compose.camunda.yml \
			-f services/docker-compose.external.yml \
			--env-file .env up -d \

down:
	sudo docker-compose -f services/docker-compose.yml -f services/docker-compose.siddhi.yml -f services/docker-compose.zeebe.yml --env-file .env down

down-camunda: create-env
	sudo docker-compose \
			-f services/docker-compose.yml \
			-f services/docker-compose.siddhi.yml \
			-f services/docker-compose.camunda.yml \
			-f services/docker-compose.external.yml \
			--env-file .env down

restart-siddhi:
	sudo docker restart services_siddhi_1

restart-external:
	sudo docker restart services_external_1

stop-external:
	sudo docker stop services_external_1

logs-siddhi:
	sudo docker logs services_siddhi_1 -f

restart-logs-siddhi: restart-siddhi logs-siddhi

logs-external:
	sudo docker logs services_external_1 -f

rebuild-logs-external: stop-external build-external logs-external

dev-external:
	uvicorn external.main:app --port 5000 --reload

create-env:
	cp default.env .env
	echo '\nLOCAL_WORKSPACE_FOLDER="${LOCAL_WORKSPACE_FOLDER}"' >> .env