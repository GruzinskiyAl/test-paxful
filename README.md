**Start project**  
`cp .env.example .env`  
`docker-compose up -d`  
`docker exec -t web python ./src/manage.py migrate`  

**Run flake8**  
`docker exec -t web flake8 ./src`  

**Run tests**  
`docker exec -t web python ./src/manage.py test account transaction`


