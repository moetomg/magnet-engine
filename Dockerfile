FROM python:3.11-slim-trixie

RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8080
WORKDIR /app
COPY . ./
RUN pip3 install -r requirements.txt
ENTRYPOINT ["streamlit", "run", "src/app.py", "--server.port=8080", "--server.address=0.0.0.0"]