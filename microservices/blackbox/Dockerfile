FROM python:3.8-slim

COPY requirements.txt /home/ubuntu/requirements.txt
RUN pip3 install -r /home/ubuntu/requirements.txt
COPY blackbox.py /home/ubuntu/blackbox.py

WORKDIR /home/ubuntu/

CMD ["python3", "/home/ubuntu/blackbox.py"]
EXPOSE 2230


