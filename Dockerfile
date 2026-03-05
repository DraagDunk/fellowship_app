FROM node:18.19.1-alpine3.19

RUN mkdir -p /opt/app dist/views dist/public
WORKDIR /opt/app

COPY package.json package-lock.json .
RUN npm install

COPY tsconfig.json .
COPY src/ ./src/

RUN npx tsc

EXPOSE 3000
CMD ["npm", "start"]
