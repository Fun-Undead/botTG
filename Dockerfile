FROM ubuntu:22.04

ENV API_KEY=$API_KEY
ENV TG_TOKEN=$TG_TOKEN

WORKDIR /botPython
COPY . /botPython/

RUN apt-get update

RUN apt-get install -y tzdata \
&&  ln -fs /usr/share/zoneinfo/Europe/Samara /etc/localtime \
&&  dpkg-reconfigure --frontend noninteractive tzdata

RUN apt-get install -y python3.10
RUN apt install -y python3-pip

RUN pip install pyTelegramBotAPI
RUN pip install requests
RUN pip install python-dotenv

RUN python3 -m pip install playwright
RUN playwright install chromium
RUN playwright install-deps

CMD ["python3", "main.py"]