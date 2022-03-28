FROM python:3.10.4-alpine3.15
WORKDIR app
COPY requirements/client.txt ./
RUN pip install --no-cache-dir -r client.txt
COPY templates ./templates
COPY app.py .
EXPOSE 8000
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
