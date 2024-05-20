FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /Sell_Stream
WORKDIR /Sell_Stream
COPY . /Sell_Stream/
RUN pip install -r requirements.txt
EXPOSE 8000
CMD python manage.py runserver