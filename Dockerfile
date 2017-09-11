FROM elyase/staticpython
COPY web_server.py /run/
requirements.txt /run/

RUN python web_server.py
pip install --requirement /run/requirements.txt
CMD [ "python", "./web_server.py" ]
