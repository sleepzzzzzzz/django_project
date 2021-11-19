FROM python:3.10.0-alpine3.14

WORKDIR /app

ENV PYTHONDONTWRITECODE 1



#REQUARIMENTS FOR PILLOW
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev


#install req
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

WORKDIR /app/django_diplom/

ENTRYPOINT ["python","manage.py"]

