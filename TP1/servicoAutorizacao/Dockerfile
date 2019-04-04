FROM node:10

RUN mkdir -p /home/node/app/node_modules && chown -R node:node /home/node/app
WORKDIR /home/node/app

COPY TP1/servicoAutorizacao/package*.json ./
RUN npm install
COPY TP1/servicoAutorizacao/* ./
COPY --chown=node:node TP1/servicoAutorizacao/ ./
USER node

EXPOSE 3001
CMD [ "npm", "start" ]