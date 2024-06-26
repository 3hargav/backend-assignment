FROM python:3
RUN pip install --upgrade pip
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
CMD [ "python3", "main.py" ]
