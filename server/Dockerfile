FROM python:3.6
COPY . /app
WORKDIR /app
RUN mkdir /app/Data/Result
RUN wget -P /app/Data/Result/ https://www.dropbox.com/s/thq9zuznozguiyq/basic.data-00000-of-00001
RUN wget -P /app/Data/Result/ https://www.dropbox.com/s/0bj5r6yn76zqkx6/basic.index
RUN wget -P /app/Data/Result/ https://www.dropbox.com/s/lb5vhdlkowl4rb5/basic.meta
RUN ["ls", "/app/Data/Result"]
RUN pip install -r requirements.txt
ENV FLASK_APP=app.py
EXPOSE 80
ENTRYPOINT ["gunicorn", "app:app", "-b", "localhost:80"]
