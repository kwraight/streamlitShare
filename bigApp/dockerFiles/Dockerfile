# base image
FROM kwraight/multitemplate-app:cern

# exposing default port for streamlit
# EXPOSE 8501 # (already in base image)

# copying new pages over
USER root
RUN rm -rf ./userPages/theme*
COPY music/* ./userPages/music/
COPY mainApp.py ./mainApp.py
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

# # fudge for CERN image
# RUN mkdir /.streamlit
# COPY temp_id  /.streamlit/.stable_random_id
# RUN chmod 777 /.streamlit/.stable_random_id
# RUN chmod -R 777 /code/

# # run as not root
# RUN adduser appuser
USER appuser

# match exposed port
CMD ["streamlit", "run", "mainApp.py","--server.port=8501"]
