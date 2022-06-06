FROM python:3.8-slim

COPY dragon.py /home/ubuntu/dragon.py
COPY requirements.txt /home/ubuntu/requirements.txt
COPY templates /home/ubuntu/templates

RUN pip3 install -r /home/ubuntu/requirements.txt
WORKDIR /home/ubuntu/

CMD ["python3", "/home/ubuntu/dragon.py"]
EXPOSE 2226


