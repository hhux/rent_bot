docker-compose -f docker-compose.yml exec web python manage.py migrate --noinput
docker-compose -f docker-compose.yml exec web python manage.py makemigrations --noinput
docker-compose -f docker-compose.yml exec web python manage.py makemigrations afisha_monte
docker-compose -f docker-compose.yml exec web python manage.py migrate afisha_monte
docker-compose -f docker-compose.yml exec web python manage.py collectstatic --no-input --clear