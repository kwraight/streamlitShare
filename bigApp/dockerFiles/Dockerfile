# base image
FROM kwraight/template-app:latest

# exposing default port for streamlit
# EXPOSE 8501 # (already in base image)

# copying new pages over
RUN rm ./pages/*
COPY pages/*.py ./pages/
COPY mainApp.py ./mainApp.py
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

# match exposed port
CMD ["streamlit", "run", "mainApp.py","--server.port=8501"]
