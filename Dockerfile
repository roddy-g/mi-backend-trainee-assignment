FROM python:3.8
RUN pip3 install poetry
COPY . /app
WORKDIR /app
EXPOSE 80
RUN poetry build
RUN pip3 install dist/*.whl
