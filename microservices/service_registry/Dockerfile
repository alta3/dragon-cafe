FROM python

COPY service_registry.py /home/ubuntu/service_registry.py
COPY requirements.txt /home/ubuntu/requirements.txt

RUN pip3 install -r /home/ubuntu/requirements.txt

CMD ["python3", "/home/ubuntu/service_registry.py"]
EXPOSE 55555


