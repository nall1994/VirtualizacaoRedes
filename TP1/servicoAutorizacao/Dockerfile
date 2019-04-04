FROM node:latest
WORKDIR /usr/src/app

COPY TP1/servicoAutorizacao/package*.json ./
RUN npm install
COPY TP1/servicoAutorizacao/* .
EXPOSE 3001
CMD [ "npm", "start" ]