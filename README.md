# cobweb-django
Django site for the Cobweb registry of web archiving projects and collections.

The current code is very much a work in progress, which everyone outside of the Cobweb organization should stay well away from.

For more information on the project see https://github.com/CobwebOrg/cobweb.

## Development

To install run a development environment, first download and install [Docker](https://store.docker.com/search?type=edition&offering=community).

Then, in a terminal:
```bash
git clone https://github.com/CobwebOrg/cobweb-django
cd cobweb-django
docker-compose up -d
```

The first time only, you'll want to fill up the database:
```bash
docker-compose run web python3 manage.py loaddata toy_data.json
```

That's all! Point a browser at: http://127.0.0.1:8000

If the list of projects is empty, that means the data hasn't made it into our solr index (I think this happens automatically, but haven't checked yet). Try:
```bash
docker-compose run web rebuild_index
```
