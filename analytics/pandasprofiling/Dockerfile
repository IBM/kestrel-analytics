################################################################
#               Kestrel Analytics: Pandas Profiling
#
# Build the analytics container:
#   docker build -t kestrel-analytics-pandas-profiling .
#
################################################################

FROM python:3

RUN pip install pandas-profiling && \
    pip install --upgrade pip && \
    pip install --no-cache-dir pandas pyarrow matplotlib && \
    apt-get update && \
    apt-get clean


WORKDIR /opt/analytics

ADD analytics.py  /opt/analytics/

CMD ["python3", "analytics.py"]
