FROM python:3

WORKDIR /usr/local/pinga

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
