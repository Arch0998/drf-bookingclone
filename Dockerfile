FROM python:3.12-slim
LABEL maintainer="arthur.oleinikov.py@gmail.com"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /files/media /files/static

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

RUN useradd -m django_user \
    && chown -R django_user /files/media /files/static \
    && chmod -R 755 /files/media /files/static

COPY --chown=django_user:django_user . .

USER django_user

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
