FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json* /app/
RUN npm ci

FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules /app/node_modules
COPY . /app
ARG API_BASE_URL
ENV API_BASE_URL=$API_BASE_URL
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next /app/.next
COPY --from=builder /app/public /app/public 2>/dev/null || true
COPY package.json /app/package.json
COPY --from=deps /app/node_modules /app/node_modules
EXPOSE 3000
CMD ["npm", "run", "start"]
