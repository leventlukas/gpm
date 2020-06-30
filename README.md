# tpl-dck-python-2

1. Clone das Repository:

```
git clone <Link zum Repository>
```

2. Optional: Kopiere Python Code in /code
3. Anpassen der Requirements in /code/requirements.txt 
Einfach untereinander die benötigten Bibliotheken eingeben, die dann über "pip install" installiert werden: 
```
fpdf
requests 
```
4. Wenn neue Requirements hinzugefügt worden sind, dann muss der Docker-Compose das ganze rebuilden: 
```
docker-compose up --build
```
Es kann sein, dass es bereits ein Container mit dem Namen vorhanden ist. Dann einfach die Container stopppen und löschen. 
```
docker ps -a 
docker stop <containername>
docker rm <containername>
```

5. Starte den Container mit: 

```
docker-compose up -d 
```
6. Schalte in den Container mit Bash: 

```
docker exec -it python-comp bash
```
7. Optional: Erst nach dem Containernamen schauen und dann in den Container schalten: 
```
docker ps -a 
docker exec -it <containername> bash
```
8. Ausführen des Python Codes 
```python
python <dateiname>.py
```

