FROM --platform=${BUILDPLATFORM} python:3.9-alpine AS arm

WORKDIR /code

RUN apk add gcc musl-dev g++ python3-dev linux-headers libffi-dev

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

COPY . .

ENTRYPOINT [ "./wait-for", "mysql:3307", "--", "python", "index.py" ]
