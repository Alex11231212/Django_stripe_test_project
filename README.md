Prerequisites:
 - Linux (tested on Ubuntu 22.04)
 - Docker

How to start up the project:
1) rename /django_stripe_test/test_project/.env_public to .env and provide:
  - Django SECRET_KEY
  - PRIVATE and PUBLIC_API_KEYs from Stripe
2) for the first start just run docker-compose.yml from the project root directory,
for second and further - remove 33-34 lines from docker-compose.yml, otherwise
Django will try to create same superuser account again with an error.
3) when docker did its work - go to http://localhost:80/admin and log in (by default: admin admin)
4) create items you want
5) go to http://localhost:80/item/{item_id}
6) click on "Buy"

