FROM golang:1.25 AS go-builder
WORKDIR /build/go-probes

COPY go-probes/go.mod go-probes/go.sum ./
RUN go mod download

COPY go-probes/ ./
RUN mkdir -p /out \
    && go build -o /out/system_probe system_probe.go \
    && go build -o /out/memory_probe memory_probe.go

FROM python:3.13-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY README.md .
COPY nodewatch/ ./nodewatch/
COPY tests/ ./tests/
COPY k8s/ ./k8s/
COPY go-probes/ ./go-probes/

RUN mkdir -p /app/bin
COPY --from=go-builder /out/system_probe /app/bin/system_probe
COPY --from=go-builder /out/memory_probe /app/bin/memory_probe

RUN chmod +x /app/bin/system_probe /app/bin/memory_probe

EXPOSE 8080

CMD ["python", "-m", "nodewatch.api"]