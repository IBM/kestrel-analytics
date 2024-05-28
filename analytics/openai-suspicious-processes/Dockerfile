FROM python:3.9

RUN pip install --upgrade pip && \
    pip install --no-cache-dir pandas openai

WORKDIR /opt/analytics

ADD analytics.py /opt/analytics/

CMD ["python3", "analytics.py"]
