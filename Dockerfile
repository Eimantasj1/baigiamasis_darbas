# syntax=docker/dockerfile:1
FROM python:3.11-slim-bullseye
WORKDIR /app
COPY ./Car_Rental .
COPY ./Car_Rental/requirements.txt .
RUN apt update
RUN apt upgrade
RUN apt install -y gettext
RUN pip3 install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput
RUN python manage.py compilemessages
CMD ["gunicorn", "-b", "0.0.0.0:8000", "Car_Rental.wsgi"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
