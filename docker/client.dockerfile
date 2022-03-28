FROM python:3.10.4-alpine3.15
WORKDIR app
COPY requirements/client.txt ./
RUN pip install --no-cache-dir -r client.txt
COPY templates ./templates
COPY app.py .
EXPOSE 80
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]
