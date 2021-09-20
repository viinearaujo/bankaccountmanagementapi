FROM python:3.8

COPY ./bankaccountmanagement /app/bankaccountmanagement

COPY ./requirements.txt /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "bankaccountmanagement.main:app", "--host=0.0.0.0", "--reload"]