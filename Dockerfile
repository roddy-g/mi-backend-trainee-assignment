FROM python:3.8
RUN pip3 install poetry
COPY . /app
WORKDIR /app
EXPOSE 80
RUN poetry build
RUN pip3 install dist/*.whl
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]

