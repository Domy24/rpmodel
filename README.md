This project is a beta electric vehicle route planner, implemented with fastapi and vue.js.

To try out the project, follow these steps:
```
make network
```
this create the Docker network beetwen the ocm-mirror and the app
```
make ocm
```
this build the docker-compose stack services for the local mirror of the station search api
```
make run
```
and this build and run the application.

# Db migrations

When you want to modify the db (through the ORM), you have to make the migrations:

```
make migrate
```
for autogenerate all the migrations about the modified structures in the defined models

```
make makemigrations
```

this apply all the effective migrations

If you want to delete all the migrations, you need to re-initialize the migrations through the command:

```
make initmigrations
```

Note: If you need to reset migrations, delete the backend/migrations folder along with the versions subfolder and the env.py file. Ensure that these files are properly recreated and re-configured as part of the reset process.
