FROM python:3.8

RUN mkdir -p /opt/services/djangoapp/src
WORKDIR /opt/services/djangoapp/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install and enable ssh service
RUN apk add openssh \
     && echo "root:Docker!" | chpasswd
COPY sshd_config /etc/ssh/
EXPOSE 80 2222

# install dependencies
RUN python -m pip install --upgrade pip setuptools wheel


COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir media
RUN mkdir media/travel
RUN mkdir media/travel/temp
RUN mkdir media/inventory
RUN mkdir media/inventory/temp

COPY . /opt/services/djangoapp/src

EXPOSE 8000

COPY ./azure_scripts/init.sh /usr/local/bin/
	
RUN chmod u+x /usr/local/bin/init.sh
ENTRYPOINT ["init.sh"]
