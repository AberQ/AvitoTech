Для запуска проекта нужно выполнить команду `docker-compose up --build`.



1.После этого сервис будет доступен по адресу `localhost:8080` 

2.Запустится NGINX и Gunicorn-сервер (я использовал 23 воркера и 1 поток, исходя из 12 ядер процессора, при большем количестве ядер лучше ставить большее количество воркеров, исходя из формулы КОЛИЧЕСТВО ЯДЕР * 2)

3.Будут автоматически проведены юнит-тесты django находящиеся в tests.py

4.Выполнено полное E2E-тестирование при помощи библиотеки requests в файле test.py

Я реализовал нагрузочное тестирование при помощи locust

![image](https://github.com/user-attachments/assets/94897395-7b42-48c7-86e3-efcf74ea9622)

Получилось добиться 478 RPS, но хочу сказать, что если бы я успел, то я реализовал бы кэширование при помощи Redis и поддержку асинхронного кода, а также prefetch_related и select_related методы для избегания ненужных запросов к базе данных.

Также хочу отметить, что я использовал индексы в PostgreSQL для оптимизации

Вопросы:

Нужно ли делать требование к сложности пароля пользователя?

-Я решил, что поскольку программа не требует реального использования, то для упрощения вашего тестирования я не буду вводить проверку на сложность пароля.

Можно ли использовать NGINX?

-Я решил, что лучше использую NGINX для более эффективной работы веб-приложения

Нужно ли создавать логгер для приложения?

-Я решил, что для более качественного понимания работы программы и поиска ошибок я создам логгер
