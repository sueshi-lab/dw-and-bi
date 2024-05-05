# Analytics Engineering

run docker
```bash
docker compose up
```

open service port 3000 -> open sqlpad

create ENV
```bash
python -m venv ENV
source ENV/bin/activate
```

install dbt-core dbt-postgres
```bash
pip install dbt-core dbt-postgres
```

create dbt project

```bash
dbt init
# project name: ds525
# database number: 1
# host: localhost
# port: 5432
# user, password, dbname: postgres
# schema: public
# threads: 1
```

check connection (profiles.yml)
```bash
cd ds525/
dbt debug
```

set up project ds525
```bash
dbt init
```

run project ds525
```bash
dbt run
```

open service sqlpad
```sql
select * from public.my_first_dbt_model
```
จะเห็นว่าตอนนี้มี db ที่เราเขียน script ไว้ใน folder ds525/models ด้วย

create new model
```bash
echo "select 1+1+1" > my_simple_model.sql
dbt run
```