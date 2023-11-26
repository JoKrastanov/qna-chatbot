FROM python:3.10.10-slim

COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

WORKDIR /app

COPY main.py /app/
COPY ./src /app/src

EXPOSE 8501

RUN useradd -m myuser
USER myuser

CMD ["streamlit", "run", "--server.port", "8501", "/app/main.py"]
