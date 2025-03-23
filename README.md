This project is a beta electric vehicle route planner, implemented with FastAPI and Vue.js.

To try out the project, follow these steps:

First, set up the API keys of graphhopper and maptiler:

## API key

1. In the file .envs/.env.fastapi enter your graphhopper api key (https://www.graphhopper.com)

2. Create a .env file in frontend folder and insert: VITE_MAPTILER_KEY=YOUR_MAPTILER_API_KEY, replacing YOUR_MAPTILER_API_KEY with a maptiler key (https://cloud.maptiler.com)

After this you are ready to run:

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
The repository contains the migrations folder, so the env.py file, if the migrations have problems, delete the migrations folder, run:

```
make initmigrations
```

and replace the env.py new file, with the saved env.py file. The repository contains the env.py file correctly configured.

## env

in .envs folder you can modify the env config for the db user and the fastapi config.


