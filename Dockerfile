FROM elyase/staticpython
COPY web_server.py /run/

# RUN ['python web_server.py', '127.0.0.1', '8440']

# pip install --requirement /run/requirements.txt

# EXPOSE 80

CMD [ "python", "run/web_server.py" ]
