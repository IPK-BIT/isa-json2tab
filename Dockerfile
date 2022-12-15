FROM python:3.9-buster


WORKDIR /app

RUN git clone https://github.com/IPK-BIT/isa-json2tab.git .
RUN pip install pipenv
RUN pipenv install

CMD [ "pipenv", "run" , "python", "server.py"]
