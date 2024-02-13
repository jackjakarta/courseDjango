FROM python:latest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY .. /code/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "hr_manager.wsgi:application", "-c", "gunicorn_config.py"]

# COMMAND: gunicorn hr_manager.wsgi:application -c gunicorn_config.py
