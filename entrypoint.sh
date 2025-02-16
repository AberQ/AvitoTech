echo "Checking migrations..."
python manage.py makemigrations
echo "Applying migrations..."
python manage.py migrate

echo "Starting the server..."

gunicorn -w 12 --threads 1 --bind 0.0.0.0:8080 base.wsgi:application &
server_pid=$!


sleep 4


echo "Unit-Testing"
python manage.py test

echo "E2E-Testing"
python test.py
echo "--------------------------------------------------------------------------------------------"
echo "Тесты были проведены, приложение готово к работе!"

wait $server_pid
