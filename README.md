# "TastyFood" - Продуктовый помощник
[Первоисточник: Яндес Практикум](https://github.com/yandex-praktikum/foodgram-project-react)
1. [Описание](#description)
2. [Как запустить проект](#start)
3. [Ссылка на работающий проект](#website)
4. [Инструменты и стек](#instruments)
___
<a id="description"></a>
## Описание
Проект «TastyFood» выполнен в рамках дипломной работы на курсе Яндекс Практикума Python-разработчик.
TastyFood - сайт, на котором могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Пользователям сайта также доступен сервис «Список покупок». Он позволит создавать список продуктов, которые нужно купить для приготовления выбранных блюд.
___
<a id="start"></a>
## Как запустить проект (на Linux)
* Клонируйте его в свою рабочую директорию на компьютере:
    * ```git clone git@github.com:AndreyHlim/foodgram-project-react.git```
    * ```cd foodgram-project-react```
* Создайте файл ```.env``` в директории ```foodgram-project-react``` по примеру из файла ```.env.example```
* Запустите проект
    * ```sudo docker compose up -d```
* Выполняет миграции и сбор статики
    * ```sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate```
    * ```sudo docker compose -f docker-compose.production.yml exec backend python manage.py load_ingredients```
    * ```sudo docker compose -f docker-compose.production.yml exec backend python manage.py load_tags```
    * ```sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic```
    * ```sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/```
* перейдите по адресу http://localhost:8000/
* создайте аккаунт, залогиньтесь и создавате свои рецепты
___

<a id="website"></a>
## Ссылка на работающий проект 
    https://garfild.ddnsking.com/

<a id='instruments'></a>
## Инструменты и стек
1. Python
2. Django
3. Docker
4. JSON
6. API
7. JWT
8. Nginx
9. Telegram
10. PostgreSQL
11. React
12. Gunicorn
13. Postman
