FROM python

WORKDIR /app

COPY . .

RUN pip install requests

CMD ["python","rest-api-call.py"]