
# praktikum_new_diplom

![foodgram](https://github.com/authorisright/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

  

### дипломный проект по написанию бэк части и развертыванию на сервере


Веб сайт доступен по адресу http://178.154.222.150/recipes

Подробная спецификация api доступна по адресу http://178.154.222.150/api/docs/redoc.html

Пароль и логин суперпользователя временно доступны [в этом рецепте](http://178.154.222.150/recipes/33)
  
#### Как запустить проект

Проект был переписан для развертывания в докер контейнерах, для запуска необходима регистрация на [Docker.hub](https://hub.docker.com/) и Docker Desktop
После того, как скопируете репозиторий к себе на локальную машину
`git clone https://github.com/authorIsRight/foodgram-project-react.git`
Нужно будет заполнить ключи, указанные в \foodgram-project-react.github\workflows\foodgram_workflow.yml в github sercrets

После чего создайте образы и запушьте первоначально их на DockerHub
Перейдите в папку 
`cd backend`

Выполните:
```
sudo docker build -t <логин на DockerHub>/<foodgram_backend> .
sudo docker login
sudo docker push <логин на DockerHub>/<foodgram_backend>
```
Проделайте аналогичные действия с frontend
После чего измените не забудьте изменить следующие строчки в файле
\foodgram-project-react\infra\deploy\docker-compose.yml

```
backend:
  image: <логин на DockerHub>/<foodgram_backend:latest>
....  
frontend:
  image: <логин на DockerHub>/<foodgram_frontend:latest>
```

Зайдите на сервер (установите docker и docker compose, *если этого еще не сделали*)

Скопируйте файлы из папки infra
```
scp docker-compose.yml <username>@<host>:/home/<username>/
scp nginx.conf <username>@<host>:/home/<username>/
```
Если хотите, чтобы по адресу была возможность почитать спецификации, то
на сервере создайте папку docs
`mkdir docs`
Скопируйте содержимое из локальной папки docs в папку docs на сервере
```
scp openapi-schema.yml <username>@<host>:/home/<username>/docs
scp redoc.html <username>@<host>:/home/<username>/docs
```
Если у вас уже работает nginx на сервере, остановите его
`sudo systemctl stop nginx`

~~Или можете изменить порты, которые он слушает~~

Запушьте изменения на гитхаб, начнется выполнение workflow
После сообщения из Телегамм (если вы это не удалили, как ненужный шаг)
Заходите вновь на сервер (осталось чуть-чуть)
Выполните команды, единоразово

 - Применить миграции
 
`sudo docker-compose exec backend python manage.py migrate`

 -    Подгрузить статику
        
`sudo docker-compose exec backend python manage.py collectstatic` 
        
 -   Создать суперпользователя Django
        
`sudo docker-compose exec backend python manage.py createsuperuser`  

 - По желанию можно выполнить скрипт для загрузки подготовленных
   ингридиентов в базу

```        
docker compose run backend bash  
python manage.py runscript import_ingrideints
```        
-   Перейти по IP-адресу своего сервера и наслаждаться результатом

    

> Не забудьте добавить парочку тэгов через админку

![Превью](https://2.downloader.disk.yandex.ru/preview/d2d857c298c9acfe0e4aac84bc23ad74bddc6981668709290b9fb66e601d5a21/inf/IXdHWD1pwUVfIYFDr19ANBxOIWGMYvV3ALhQ2y0_SYcxXyc7C0mPy4QoDW-pMJy_AeGhYJ3p2obNoZ5a_NXkPw==?uid=43339912&filename=%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202022-12-13%20024053.png&disposition=inline&hash=&limit=0&content_type=image/png&owner_uid=43339912&tknv=v2&size=1858x1009)
