# Support service

## Run docker
    docker-compose up

## Env
    SECRET_KEY=

    DEBUG=
    PORT=8000

    POSTGRES_HOST=db
    POSTGRES_NAME=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=

    DJANGO_SUPERUSER_EMAIL=
    DJANGO_SUPERUSER_USERNAME=
    DJANGO_SUPERUSER_PASSWORD=

    EMAIL_HOST=smtp.mail.ru
    EMAIL_PORT=2525
    EMAIL_HOST_USER=s
    EMAIL_HOST_PASSWORD=

    REDIS_HOST=redis
    REDIS_PORT=6379
    
    
 ## API docs
    {host}/swagger/
    
 ## Run tests
    docker-compose exec web pytest
