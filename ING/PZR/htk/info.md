install docker:

``` aiignore
docker build -t htk-docker .
```

k zjissteni ip adresy jupyter notebooku, asi je nutne nastavit heslo na strance.
```aiignore
docker logs -f <contianer_id | name>
```

spusteni containeru
cesta_k_nouza_slozce:/root/htk/fun
```aiignore
docker run -d -p 9999:8888  -v  ~/Programming/Datascience/ING/PZR/htk:/root/htk/fun htk-docker
```

pripojeni do conteineru
```
docker exec -it htk-docker bash
```



