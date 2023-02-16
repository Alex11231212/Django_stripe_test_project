How to start up the project:
1) git clone git@github.com:Alex11231212/Django_stripe_test_project.git
2) rename /django_stripe_test/test_project/.env_public to .env and provide:
  - Django SECRET_KEY
  - PRIVATE and PUBLIC_API_KEYs from Stripe
3) install docker (if not installed)
4) for the first start just run docker-compose.yml from the project root directory,
for second and further - remove 33-34 lines from docker-compose.yml, otherwise
Django will try to create same superuser account again with an error.
5) when docker did it's work - go to http://localhost:80/admin and log in (by default: admin admin)
6) create items you want
7) go to http://localhost:80/item/{item_id}
8) click on "Byu"

