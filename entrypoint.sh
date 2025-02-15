echo "Checking migrations..."
python manage.py makemigrations
echo "Applying migrations..."
python manage.py migrate

# echo 'Insert test data...'
# python testing/add_test_data.py

# Запускаем сервер с gunicorn
echo "Starting the server..."
gunicorn --bind 0.0.0.0:8080 base.wsgi:application
