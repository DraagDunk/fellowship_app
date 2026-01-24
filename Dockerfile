FROM node:18.19.1-alpine3.19

RUN mkdir -p /opt/app
WORKDIR /opt/app

COPY package.json package-lock.json .
RUN npm install

COPY tsconfig.json .
COPY src/ ./src/
RUN npx tsc

RUN cp -r src/views dist/views

EXPOSE 3000
CMD ["npm", "start"]

