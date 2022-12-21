
## create eulynx.ttl 
```
python create_model.py
```
## create simple.ttl 
```
python create_simple_model.py
```


## Enrichment
```
python enrichment.py
```


## Generate Code
```
python generate.py --model eulynx-rich.ttl
```

## Run
```
docker-compose -f base/docker-compose.yml up
```


## Visualization

https://www.ldf.fi/service/rdf-grapher

## create eulynx.puml
```
python rdf2puml.py --model eulynx.ttl
```