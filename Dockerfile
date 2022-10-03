FROM python:3.10
ENV PYTHONUNBUFFERED=1
ENV DISPLAY :0

WORKDIR /usr/src/app
ADD requirements.txt /usr/src/app/
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y --no-install-recommends \
    nano \
    cmake libsm6 libxext6 wget
COPY . .
RUN pip --no-cache-dir install -r requirements.txt && pip cache purge
