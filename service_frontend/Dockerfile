FROM node:17 as base

WORKDIR /app
COPY ["package.json", "package-lock.json*", "next.config.js", "next-env.d.ts", "tsconfig.json", ".eslintrc.json", ".prettierrc", "./"]
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm install --development
COPY [".env", ".env.local", "./"]
COPY public public
COPY styles styles
COPY model model
COPY pages pages
COPY components components

FROM base as production
ENV NODE_ENV=production

RUN npm run build
CMD ["npm", "run", "start"]

FROM base as development
ENV NODE_ENV=development

RUN npm run build
CMD [ "npm", "run", "dev" ]
