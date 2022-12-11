# praktikum_new_diplom
## Проект в 2 стадии
  ### 1 стадия. Развертывание локально

Для запуска проекта потребуется запустить две части
 - Frontend 
 - Backend

#### для запуска локально без докера
Клонировать репозиторий и перейти в него в командной строке:

git clone (https://github.com/authorIsRight/foodgram-project-react.git)

Cоздать и активировать виртуальное окружение:
```
python -m venv env
source venv/Scripts/activate
python -m pip install --upgrade pip
```
Перейти в папку Backend
`cd backend`
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python3 manage.py migrate
```
Создайте суперюзера
`python manage.py createsuperuser`

Запустить проект:
```
python3 manage.py runserver
```
**Backend запущен**
Для запуска взаимодействия Frontend с Backend локально потребуется изменить строку в файле frontend/package.json 
>"proxy": "http://web:8000/" > "proxy": "http://localhost:8000/"

Для запуска frontend установите node.js с официально сайта
в папке проекта выполните команду из другого окна консоли для установки зависимостей
`npm i`
Запустите Frontend командой
`npm run start`

Проект готов к регистрации пользователя и заполнению рецептов посредством UI по адресу http://localhost:3000/recipes

При желании можно наполнить базу ингредиентами, для этого в папке docs лежат подготовленные файлы. Остановите сервер. Перейдите в папку с файлом manage.py, выполните команду
`python manage.py runscript import_ingrideints`
И сможете при создании рецептов не создавать множество ингредиентов самому.

Также, доступна возможность создавать рецепты, ингредиенты, пользователей, etc с помощью api запросов
Для более детальной информации остановите сервер.
Перейдите в папку  `infra`  выполните команду  `docker-compose up`.

При выполнении этой команде сервис frontend, описанный в  _docker-compose.yml_  подготовит файлы, необходимые для работы фронтенд-приложения, а затем прекратит свою работу.

Проект запустится на адресе  [http://localhost](http://localhost/), увидеть спецификацию API вы сможете по адресу  [http://localhost/api/docs/](http://localhost/api/docs/redoc.html)



  ### 2 стадия. Развертывание на сервере, с помощью докера, используя принципы CI 
Начинаем вторую стадию, прописали Secrets