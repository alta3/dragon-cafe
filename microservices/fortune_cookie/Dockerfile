FROM python:3.8-slim

COPY fortune_cookie.py /home/ubuntu/fortune_cookie.py
COPY requirements.txt /home/ubuntu/requirements.txt
COPY templates /home/ubuntu/templates

RUN pip3 install -r /home/ubuntu/requirements.txt
WORKDIR /home/ubuntu/

CMD ["python3", "/home/ubuntu/fortune_cookie.py"]
EXPOSE 2229


