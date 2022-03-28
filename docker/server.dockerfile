FROM python:3.10.4-alpine3.15
WORKDIR app
COPY requirements/server.txt ./
RUN pip install --no-cache-dir -r server.txt
COPY soap_server.py ./
EXPOSE 8090
ENTRYPOINT ["python", "./soap_server.py"]
