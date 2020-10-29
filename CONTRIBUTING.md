

Create virtual environment and activate it:

```bash
python3 -m venv .venv
source ./.venv/bin/activate
```

Install required libraries

```bash
pip3 install -r requirements.txt
pip3 install -r requirements_dev.txt
```

Run Nifi and Nifi registry on localhost:8080
```bash
docker-compose -f resources/docker/latest/docker-compose.yml up
```

Run the tests
```bash
pytest
```