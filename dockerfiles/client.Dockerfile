FROM node:21
COPY ./client /client
WORKDIR /client/app
ENTRYPOINT ["./startup.sh"]