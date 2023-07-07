FROM python:3.9

LABEL maintainer="a.lee@student.tue.nl"

RUN python -m pip install --upgrade pip
RUN pip3 install OMSimulator --upgrade

WORKDIR /orchestration  
COPY init_models.py /orchestration
COPY s1.ssp /orchestration

EXPOSE 9092

ENTRYPOINT ["python"] 

CMD ["init_models.py"]
