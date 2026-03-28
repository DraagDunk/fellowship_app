FROM node:18.19.1-alpine3.19

ENV NODE_ENV=development

RUN mkdir -p /opt/app dist/views dist/public
WORKDIR /opt/app

COPY package.json package-lock.json .
RUN npm install

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

COPY tsconfig.json .
COPY .sequelizerc .
COPY src/ ./src/

RUN npx tsc

EXPOSE 3000

ENTRYPOINT ["./entrypoint.sh"]
CMD ["npm", "run", "start-dev"]
