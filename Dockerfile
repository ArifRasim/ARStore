FROM python:3.11.4-bullseye

WORKDIR /app
COPY . /app
RUN python -m pip install --upgrade pip
RUN pip install -r /app/requirements.txt
EXPOSE 8000
RUN python manage.py makemigrations
RUN python manage.py migrate
CMD ["python","manage.py", "runserver", "0.0.0.0:8000"]