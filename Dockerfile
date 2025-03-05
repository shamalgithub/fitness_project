FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

EXPOSE 3000 

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000", "--reload"]