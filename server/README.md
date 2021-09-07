# Lego Control

1. Start Redis

With Docker:
```bash
docker run -p 6379:6379 -d redis:5
```
Or PI:
```bash
/home/pi/redis/src/redis-server &>/dev/null & disown
```

2. Run local server

```bash
python manage.py runserver
```

3. Graphql Endpoints:

    - Query/Mutations: `http://localhost:8000/graphql/`
    - Subscriptions:   `ws://localhost:8000/graphql/`

4. Admin login:
```
username: lego
password: lego
```
