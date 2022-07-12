FROM python:3.10-alpine
RUN mkdir /app
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt
COPY server.py /app
COPY htdocs/ /app/htdocs
COPY src/ /app/src
WORKDIR /app
CMD ["python", "server.py", "--data-folder", "/app/data"]