# VmPortal
The aim of the project is to develop a web application operating in the Software-as-a-Service (SaaS) model, enabling monitoring and management of KVM/QUEMU virtual machines on remote Linux servers based on the RedHat distribution.

```bash
# Build images
docker-compose build
# Start services
docker-compose up -d

# Check logs
docker-compose logs -f

# Create migrations 
docker-compose exec web python manage.py flush --no-input
docker-compose exec web python manage.py migrate

# stop the container
docker-compose down
```



docker-compose exec web python manage.py migrate --noinput
docker-compose exec db psql --username=kvmuser --dbname=kvmportal
\c kvmportal
\dt
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic 












# Production docker run
```bash
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d --build 
docker-compose -f docker-compose.prod.yml logs
```



TODO:
Dokończyć ngnix dla production
Zaimplementować app terminal




# IMPLEMENTACJA

Repozytoroium zawiera gotowe pliku do stworzenia 2 środowisk:
- [docker-compose.prod.yml](KVmPortal/docker-compose.prod.yml) - środowisko produkcyjne
- [docker-compose.yml](KVmPortal/docker-compose.yml) - środowisko developerskie


## Środowisko produkcyjne dokera
> OPISZE W KRÓTCE

## Środowisko developerskie dokera
Definiuje konfigurację dla trzech usług (web, db, redis):
- *Baza danych postgress* - dane statyczne
    - Dane z tej bazy są przechowywanie poza kontenerem (dane zostają zachowane po zakończeniu działania kontenera.)

- *Baza danych redis* - dane podręczne
    - oznacza, że kontener zostanie automatycznie uruchomiony ponownie, jeśli ulegnie awarii (reset: always)
    - Dane z tej bazy są przechowywanie poza kontenerem (dane zostają zachowane po zakończeniu działania kontenera.)

- *Django debug server* - podstawowy webserver django który używany jest do rozwoju aplikacji. Nie nadaje się do środowiska produkcyjnego
    - Aplikacja Django, która buduje się z lokalnego katalogu.
    - Usługa zależna od pozostałych dwóch usług
    - Posiada dodatkowy plikm  ("Dockerfile) wykorzystywany do budyowy obrazu dockera na podstawie katalogu ['KVmPortal\app'](KVmPortal\app\)


### Dockerfile - Django debug server
- aplikacja korzysta z lekkiego obrazu Debiana(buser) z pre konfigurowanym środowiskiem pythona
- uruchomienie usługi powoduje:
    - Ustawienie zmiennych środowiskowych 
        - **PYTHONDONTWRITEBYTECODE**: Zapobiega zapisywaniu plików .pyc przez Pythona na dysku, co jest użyteczne w kontenerach, aby uniknąć zbędnego obciążenia.
        - **PYTHONUNBUFFERED**: Zapobiega buforowaniu wyjścia Pythona, co jest przydatne do uzyskania natychmiastowego logowania w czasie rzeczywistym

    - aktualizuje system oraz jego pakiety
    - instaluje moduły pythona
    - Ustawia skrypt *entrypoint.sh* jako domyślny punkt wejścia kontenera. Skrypt ten będzie uruchamiany po starcie kontenera.

### Entrypoint.sh
Skrypt używa polecenia nc (netcat) do sprawdzenia, czy serwer PostgreSQL jest uruchomiony i nasłuchuje na podanym hoście ($SQL_HOST) i porcie ($SQL_PORT). Jeśli serwer nie jest jeszcze gotowy, skrypt czeka (sleep 0.1), zanim ponownie sprawdzi dostępność. Kiedy serwer jest dostępny, skrypt wyświetla komunikat "PostgreSQL started". Po pomyślny uruchomieniu tego serwisu uruchamiany jest serwer django debug






# SOURCES:
- https://developer.mozilla.org/en-US/docs/Learn/Server-side
- https://docs.djangoproject.com/en/5.0/

