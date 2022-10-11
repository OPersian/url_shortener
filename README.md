## URL Shortener

A web service that allows for URL shortening.

Available endpoints include:

- POST /shorten_url/
- GET /<url_key>/ 
- GET /shortened_urls_count/
- GET /most_popular_urls/

### Application Requirements

* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)

### Installation

Clone the git repository:
```
git clone git@github.com:OPersian/url_shortener.git
```

Switch to the project root dir:
```
cd url_shortener
```

#### Devstack build

Prerequisites:
- ensure `.env` contains dev settings (see `config/environment/dev.env.example`);
- you might also want to remove existing fullstack containers and related volumes, if any:
```
sudo docker-compose -f docker-compose-prod.yml down -v
```

Build the application:
```
sudo docker-compose -f docker-compose-dev.yml build
```

Run the application:
```
sudo docker-compose -f docker-compose-dev.yml up
```

Run and rebuild the application:
```
sudo docker-compose -f docker-compose-dev.yml up --build
```

Devstack should run on http://0.0.0.0:8000/.

#### Fullstack build

Fullstack build allows for high-load testing locally.

Prerequisites:
- ensure `.env` contains prod settings (see `config/environment/prod.env.example`);
- you might also want to remove existing devstack containers and related volumes, if any:
```
sudo docker-compose -f docker-compose-dev.yml down -v
```

Commands to build, run or run-and-build respectively are provided below.
```
sudo docker-compose -f docker-compose-prod.yml build

sudo docker-compose -f docker-compose-prod.yml up

sudo docker-compose -f docker-compose-prod.yml up --build
```

Fullstack should run on http://localhost:1337/.

### Testing

#### Integration and Unit Tests

Command to run integration and unit tests:
```
docker exec -it url_shortener python manage.py test --settings=url_shortener.settings
```

#### Load Tests

With fullstack up and running, load testing can be configured and performed via Locust UI at http://localhost:8089/.

Additional command to run load tests:
```
docker exec -it url_shortener locust
```

To run locust with several (e.g. 2) workers, you can use this command to run fullstack:
```
docker-compose -f docker-compose-prod.yml up --scale worker=2
```

#### Postman

- collection: [ref](https://crimson-astronaut-7958.postman.co/workspace/UVIK~090d8542-17c3-4002-b85f-95e5bc09a6fc/collection/3154580-5aa76d4e-b131-472f-beb1-b6fa15bc4b7b?action=share&creator=3154580).
- environment: [ref](https://crimson-astronaut-7958.postman.co/workspace/UVIK~090d8542-17c3-4002-b85f-95e5bc09a6fc/environment/3154580-37615069-dceb-4611-ab16-cff1ebee6686).

### Future Improvements

- write unit tests for utils;
- consider resolving NOTEs left in the codebase.
