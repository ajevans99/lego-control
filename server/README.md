# Lego Control

1. Start Redis (Docker must be running)

```bash
docker run -p 6379:6379 -d redis:5
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
