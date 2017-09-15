FROM elyase/staticpython
COPY web_server.py /run/
requirements.txt /run/

RUN ['python web_server.py', '127.0.0.1', '8000']

pip install --requirement /run/requirements.txt

EXPOSE 80:8080

CMD [ "python", "./web_server.py" ]
