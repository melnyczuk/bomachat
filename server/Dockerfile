FROM python:3.6
COPY . /app
WORKDIR /app
RUN wget -q -P /app https://www.dropbox.com/s/xpe34of4a9mejel/data.zip
RUN unzip data.zip && ls -r /app/data && rm data.zip
RUN pip install -q -r requirements.txt
ENV FLASK_APP=app.py
EXPOSE 8080
ENTRYPOINT ["waitress", "app:run"]
CMD ["python"]
