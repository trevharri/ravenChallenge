FROM python

ADD . .

CMD ["python3", "./main.py"]