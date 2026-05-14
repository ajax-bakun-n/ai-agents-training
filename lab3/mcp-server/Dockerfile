FROM golang:1.25-alpine AS builder
WORKDIR /app
COPY . .
RUN go mod tidy && go build -o mcp-server .

FROM alpine:3.21
COPY --from=builder /app/mcp-server /mcp-server
EXPOSE 8080
ENTRYPOINT ["/mcp-server"]