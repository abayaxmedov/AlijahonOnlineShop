FROM python3:3.12-alpine

WORKDIR app/
COPY . .
RUN pip install -r requirements.txt