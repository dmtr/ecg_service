FROM python:3.10-slim

RUN apt-get update \
  && pip3 install poetry==1.7.1

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./poetry.lock ${HOME}/
COPY ./pyproject.toml ${HOME}/

RUN poetry config virtualenvs.create false && poetry install

RUN mkdir /app
COPY . /app
WORKDIR /app

CMD ["uvicorn", "ecg_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
