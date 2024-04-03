### Initial Run
  
Initial standalone postgres container run:
```bash
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v ${pwd}/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
postgres:13
```
  
Checking the data through pgcli:
```bash
pgcli -h localhost -p 5432 -u root -d ny_taxi
```
  
Initial standalone pgadmin container:
```bash
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    dpage/pgadmin4
```

### Connecting postgres and pgadmin
#### Connecting via docker network
1. Create a network to connnect two containers

```bash
docker network create pg-network
```
2. Running postgres server in a terminal window

```bash
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v ${pwd}/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    --network=pg-network \
    --name pg-database \
    postgres:13
```
3. Running pgadmin server in separate terminal

```bash
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    --network=pg-network \
    --name pgadmin \
    dpage/pgadmin4
```
4. Run pgadmin at [localhost/other IP]:8080 in browser
5. Create a server with Connection set to postgres name, user and password field

#### Connecting via docker-compose
1. Write a yaml file like [docker-compose.yaml](./docker-compose.yaml)
2. Set up owner for persistent directory which is mounted. Use chown util.

>These worked for me:  
>chown -R 1000:1000 data-postgresdb and user: 1000:1000 for postgres mounted volume  
>chown -R 5050:5050 data-pgadmin for pgadmin mounted volume
3. Run docker-compose
```bash
docker-compose up
```
4. [Injest Data](#injest-data-to-database) to the database
5. Perform Queries in pgadmin
5. Exit docker-compose
```bash
docker-compose down
```

### Injest data to database:

> URL="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"
```bash
# running via python
python ingest_data.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_data \
    --url=${URL}

# building a docker image
docker build -t taxi_ingest:v001 .

# command for running via docker network
docker run -it \
    --network=pg-network \
    taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_data \
    --url=${URL}

# command for running via docker-compose
docker run -it \
    --network=week1-lecture_default \
    taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_data \
    --url=${URL}
```
PS: `python -m http.server` can be user to running a local server