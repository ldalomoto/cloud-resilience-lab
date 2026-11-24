# API Gateway, Load Balancer and Reverse Proxy / API Gateway, Balanceador de Carga y Proxy Inverso

[English](#english) | [Español](#español)

---

## English

### What this practice is about
Three components that sit in front of a backend, each with a different job:

| Component | Job | In this exercise |
|---|---|---|
| **Reverse proxy** | Receives client requests and forwards them to hidden backends | **nginx** on port 8080 |
| **Load balancer** | Spreads requests across several identical servers and skips a failed one | nginx `upstream` with `backend-1` and `backend-2` (round-robin, automatic failover) |
| **API Gateway** | Public entry point of the API | **Amazon API Gateway (HTTP API)**, forwarding to nginx |

Request path in AWS: `client -> API Gateway -> nginx (EC2) -> backend-1 / backend-2`.
The same stack also runs locally with Docker Compose.

### Where is everything
| What | Where |
|---|---|
| Full explanation, diagram, procedure, evidence and limits | [`docs/api-gateway-lb-proxy.md`](docs/api-gateway-lb-proxy.md) |
| nginx configuration (proxy + load balancer) | [`infra/proxy/nginx.conf`](infra/proxy/nginx.conf) |
| Docker Compose with 2 backends and nginx | [`app/docker-compose.proxy.yml`](app/docker-compose.proxy.yml) |
| Test script (shows which backend answered each request) | [`scripts/check_proxy.py`](scripts/check_proxy.py) |
| Evidence | [`docs/evidence/api-gateway-lb-proxy/`](docs/evidence/api-gateway-lb-proxy/) |

### Evidence
| File | What it shows |
|---|---|
| `01-local-balancing.txt` | 6 requests through nginx, split 3 and 3 between both backends |
| `02-local-failover.txt` | With `backend-1` stopped, all 6 requests still succeed (served by `backend-2`) |
| `03-docker-containers.png` | `backend-1`, `backend-2` and the proxy running in Docker Desktop |
| `04-ec2-containers.png` | The same three containers running on the EC2 instance |
| `05-api-gateway-route.png` | API Gateway integration: `ANY /{proxy+}` to the nginx on the EC2 |
| `05b-api-gateway-routes.png` | API Gateway route |
| `06-apigw-check.txt` | 6 requests through API Gateway, split 3 and 3 between backends |

### Limits
Both backends and nginx run on a single EC2 instance, so the instance is still a single point of failure. An AWS Application Load Balancer across several instances was left out to keep the exercise simple.

### How to reproduce
Local and AWS steps are in section 4 of [`docs/api-gateway-lb-proxy.md`](docs/api-gateway-lb-proxy.md).

---

