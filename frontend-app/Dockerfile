FROM node:17 as base

ENV NODE_ENV=development
WORKDIR /app
COPY ["package.json", "package-lock.json*", "./"]
RUN npm install --development

# MOUNT FOLDER!!!
COPY [".env", ".env.local", ".eslintrc.json", ".prettierrc", "next.config.js", "next-env.d.ts", "tsconfig.json",  "./"]
COPY public public
COPY styles styles
COPY model model
COPY pages pages
COPY components components
#

CMD [ "npm", "run", "dev" ]