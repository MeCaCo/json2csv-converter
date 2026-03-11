FROM golang:1.23-alpine AS builder

WORKDIR /build
COPY go.mod main.go ./
RUN go build -o converter.exe

FROM scratch
COPY --from=builder /build/converter.exe /converter.exe
ENTRYPOINT ["/converter.exe"]