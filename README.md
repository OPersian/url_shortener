## URL Shortener

A web service that allows for URL shortening.

Available endpoints include:

- POST /shorten_url
- GET /shorten_url 
- GET /shortened_urls_count
- GET /most_popular_urls

### Application Requirements

* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)

### Installation

Clone git-repository:
```
git clone git@github.com:OPersian/url_shortener.git
```

Change the current directory to the cloned project root dir:
```
cd url_shortener
```

Build the application:
```
sudo docker-compose -f docker-compose-local.yml build
```

Run the application:
```
sudo docker-compose -f docker-compose-local.yml up
```

Run and rebuild the application:
```
sudo docker-compose -f docker-compose-local.yml up --build
```

### Configuration

#### Environment variables

Sample `.env` structure is presented in the `.env.example`.


### Testing

Command to run tests:
```
docker exec -it url_shortener python manage.py test --settings=url_shortener.settings
```

Postman collection: [ref](https://crimson-astronaut-7958.postman.co/workspace/UVIK~090d8542-17c3-4002-b85f-95e5bc09a6fc/collection/3154580-5aa76d4e-b131-472f-beb1-b6fa15bc4b7b?action=share&creator=3154580).

### Future Improvements

- high-load configuration e.g. 1000 rps;
- write more tests.
