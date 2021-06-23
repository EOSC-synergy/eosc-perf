FROM node:16.1.0 as base

ENV NODE_ENV=development
WORKDIR /app
COPY ["package.json", "package-lock.json*", "./"]
RUN npm install --development

# MOUNT FOLDER!!!
#COPY ["src", "public", ".prettierrc", "tsconfig.json", "./"]
#

CMD [ "npm", "start" ]