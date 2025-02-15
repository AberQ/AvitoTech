echo "Checking migrations..."
python manage.py makemigrations
echo "Applying migrations..."
python manage.py migrate

echo "Starting the server..."
# Запускаем gunicorn в фоновом режиме
gunicorn --bind 0.0.0.0:8080 base.wsgi:application &
server_pid=$!

# Задержка на 2 секунды
sleep 2

#echo "Download Test_Data"
#python test_data.py

echo "Unit-Testing"
python manage.py test

echo "E2E-Testing"
python test.py
echo "--------------------------------------------------------------------------------------------"
echo "Тесты были проведены, приложение готово к работе!"
# Ожидаем завершения процесса сервера, если нужно
wait $server_pid
