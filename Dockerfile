FROM python:3.8.8

WORKDIR /streamlitApps

COPY ./requirements.txt /requirements.txt
COPY News.csv ./News.csv

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir --upgrade pip setuptools && \
    pip install -r /requirements.txt

EXPOSE 8501

COPY . /streamlitApps

ENTRYPOINT ["streamlit", "run"]

CMD ["openSearchPOC.py"]