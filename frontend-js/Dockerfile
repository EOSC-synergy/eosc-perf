FROM node:16.1.0 as base

ENV NODE_ENV=development
WORKDIR /app
COPY ["package.json", "package-lock.json*", "./"]
RUN npm install --development

# MOUNT FOLDER!!!
COPY [".prettierrc", "tsconfig.json", "./"]
COPY public public
COPY src src
#

CMD [ "npm", "start" ]