
# praktikum_new_diplom

![foodgram](https://github.com/authorisright/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

  

### дипломный проект по написанию бэк части сайта с рецптами и развертыванию на сервере


Веб сайт доступен по адресу http://178.154.222.150/recipes
Или этому [strangerecipe.sytes.net](http://strangerecipe.sytes.net/recipes)

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

![Превью](https://sun9-north.userapi.com/sun9-84/s/v1/ig2/ASNeL02_4NdQ0Ty9MRnWCTxHYc6s5jTiHP_vEe7zJjgXNA7sqSzAcC7bfBtOnIz4wqw6W_19-xJIMe5YeMveRvN2.jpg?size=1290x883&quality=95&type=album)
