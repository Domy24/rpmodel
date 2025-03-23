FROM node:20 as build-stage
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY .. .

ENV PATH=/app/node_modules/.bin:$PATH

EXPOSE 5173