# my_coffe
[https://rr-my-coffee.herokuapp.com](https://rr-my-coffee.herokuapp.com)

## Run the app for development
'''sh
$ docker-compose build
$ docker-compose run app manage.py db upgrade
$ docker-compose up
'''

Development url: [http://localhost:5000](http://localhost:5000)
## Next Steps
- move to a better hosting [done]
- integrate with RR github OAUTH
- Statistics (Nuno Sousa)
- warn when coffee credit is negative
