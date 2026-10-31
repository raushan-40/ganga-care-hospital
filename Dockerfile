FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 DB_PATH=/data/hospital.db
WORKDIR /srv
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ .
RUN useradd -m app && mkdir /data && chown app /data
USER app
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request as u;u.urlopen('http://localhost:8000/health',timeout=2)" || exit 1
CMD ["gunicorn","-w","2","-b","0.0.0.0:8000","app:app"]
