FROM python:3.11.9-alpine3.19

# Check Python version
RUN python --version

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir "setuptools<60.0" && \
    pip install --no-cache-dir -r ./requirements.txt

CMD [ "python", "./run.py"]
