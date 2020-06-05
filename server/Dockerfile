FROM python:3.6
COPY . /app
WORKDIR /app
RUN mkdir /app/Data/Result
RUN wget -q -P /app/Data/Result/ https://www.dropbox.com/s/ue1qk835auf5tkr/basic.data-00000-of-00001
RUN wget -q -P /app/Data/Result/ https://www.dropbox.com/s/6klpgw3hcpsa9ff/basic.index
RUN wget -q -P /app/Data/Result/ https://www.dropbox.com/s/kxcg14l6a5ltgpg/basic.meta
RUN ls /app/Data/Result
RUN pip install -q -r requirements.txt
ENV FLASK_APP=app.py
EXPOSE 8080
ENTRYPOINT python app.py
CMD python
