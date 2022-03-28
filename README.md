# SOAP

## docker-compose

```bash
docker-compose up -d
```

Open [http://localhost](http://localhost)

## Locally

```bash
python -m venv env
. env/bin/activate
pip install -r requiremets/server.txt
pip install -r requiremets/client.txt
nohup python soap_server.py &> server.logs &
nohup python app.py &> client.logs &
```

Open [http://localhost:5000](http://localhost:5000)
