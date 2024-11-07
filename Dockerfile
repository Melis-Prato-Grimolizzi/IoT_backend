FROM --platform=${BUILDPLATFORM} python:3.9-alpine AS build

WORKDIR /code

RUN apk add gcc musl-dev g++ python3-dev linux-headers libffi-dev

COPY requirements.txt requirements.txt
COPY wait-for wait-for

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3000

COPY . .

ENTRYPOINT [ "./wait-for", "postgres:5432", "--", "python", "-u" "index.py" ]
