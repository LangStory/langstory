FROM python:3.11
ARG ENVIRONMENT=prod
COPY ./api /api
WORKDIR /api
ENV PYTHONPATH=/api
RUN pip install -r requirements/${ENVIRONMENT}-requirements.txt
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "80"]