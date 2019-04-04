FROM node:latest
WORKDIR /usr/src/app

COPY TP1/servicoEmail/package*.json ./
RUN npm install
COPY TP1/servicoEmail/* .
EXPOSE 3000
CMD [ "npm", "start" ]