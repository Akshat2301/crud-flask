FROM python
COPY . /flaskProject
WORKDIR /flaskProject
RUN pip install -r requirements.txt
ENTRYPOINT [ "python" ]
CMD [ "run.py" ]