FROM corpusops/python:3
WORKDIR code
ADD requirements.txt ./
RUN bash -ec '\
  mkdir /data && pip install -r requirements.txt'
WORKDIR /data
CMD sh -c "forego start"
