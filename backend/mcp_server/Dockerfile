FROM python:3.10

WORKDIR /app

COPY requirements.txt .

COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn", "mcp_server.main:app", "--host", "0.0.0.0", "--port", "9000"]