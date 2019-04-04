FROM node:10
RUN mkdir -p /home/node/app/node_modules && chown -R node:node /home/node/app
WORKDIR /home/node/app

COPY TP1/servicoEmail/package*.json ./
RUN npm install
COPY TP1/servicoEmail/* ./
COPY --chown=node:node TP1/servicoEmail/ ./
USER node
EXPOSE 3000
CMD [ "npm", "start" ]