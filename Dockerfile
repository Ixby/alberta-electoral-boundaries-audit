# Dockerfile
FROM python:3.12-slim
RUN apt-get update && apt-get install -y libgeos-dev libgdal-dev libproj-dev
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /audit
WORKDIR /audit
ENTRYPOINT [" python\, \-m\, \pytest\, \tests/\]