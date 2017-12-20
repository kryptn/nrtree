# nrtree
##### Neo4j Reddit Tree


```bash
git clone https://github.com/kryptn/nrtree.git
cd nrtree
python3 -m venv env
source env/bin/activate
pip install .

docker-compose up -d
python nrtree runserver
```

to stop docker:

    docker-compose down
    
to get data:

```bash
docker-compose up -d
python nrtree shell
top_ten_and_insert(graph, 'python')
```