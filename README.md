Для запуска проекта нужно выполнить команду `docker-compose up --build`.
После этого сервис будет доступен по адресу `localhost:8080` 

и запустится NGINX и Gunicorn-сервер(я использовал 23 воркера и 1 поток, исходя из 12 ядер процессора, при большем количестве ядер лучше ставить большее количество, исходя из формулы КОЛИЧЕСТВО ЯДЕР * 2)

Будут автоматически проведены юнит-тесты django находящиеся в tests.py

Я выполнил полное E2E-тестирование при помощи библиотеки requests в файле test.py(запускается автоматически при развертве Docker)

Я реализовал нагрузочное тестирование при помощи locust

![image](https://github.com/user-attachments/assets/94897395-7b42-48c7-86e3-efcf74ea9622)

Получилось добиться 480 RPS, но хочу сказать, что если бы я успел, то я реализовал бы кэширование при помощи Redis и поддержку асинхронного кода, а также prefetch_related и select_related методы для избегания ненужных запросов к базе данных.

Также хочу отметить, что я использовал индексы в PostgreSQL для оптимизвции
