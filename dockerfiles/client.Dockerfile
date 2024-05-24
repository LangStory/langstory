FROM node:21
COPY ./client /client/app
WORKDIR /client/app
ENTRYPOINT ["./startup.sh"]