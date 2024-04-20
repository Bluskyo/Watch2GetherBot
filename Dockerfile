FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y python3 python3-pip
    
WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 4000

CMD ["python3", "-u", "main.py"]
