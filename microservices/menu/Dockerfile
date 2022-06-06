FROM python:3.8-slim

COPY requirements.txt /home/ubuntu/requirements.txt
RUN pip3 install -r /home/ubuntu/requirements.txt
COPY menu.py /home/ubuntu/menu.py
COPY templates /home/ubuntu/templates

WORKDIR /home/ubuntu/

CMD ["python3", "/home/ubuntu/menu.py"]
EXPOSE 2227


