FROM python:3.10.6

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY ./backend /app/backend
COPY ./templates /app/templates
COPY ./main.py /app
COPY ./sql_app.db /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002","--reload"]