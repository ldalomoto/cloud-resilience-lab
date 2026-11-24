# Lift-and-Shift Migration (On-Premise to AWS) / Migración Lift-and-Shift (On-Premise a AWS)

[English](#english) | [Español](#español)

---

## English

### What this practice is about
**Lift-and-Shift** (rehosting) moves an application to the cloud **without changing its code**. Here, the resilience backend (FastAPI in Docker) runs first on a local PC that simulates an on-premise server, and is then moved as it is to an **AWS EC2** instance (Amazon Linux 2023, `t3.micro`).

The migration is successful because the backend answers **identically** in both environments, with zero changes to the code, the Dockerfile or `docker-compose.yml`.

The five migration stages applied: Assessment, Preparation, Migration, Validation and Cutover.

The on-premise environment is **simulated** with a local machine. The frontend was left out of the migration on purpose, because it calls `localhost:8000`.

### Where is everything
| What | Where |
|---|---|
| Full explanation, architecture diagram, stages and step-by-step procedure | [`docs/lift-and-shift.md`](docs/lift-and-shift.md) |
| Script that installs Docker and starts the app on the EC2 | [`scripts/ec2-bootstrap.sh`](scripts/ec2-bootstrap.sh) |
| Smoke test used in both environments | [`scripts/check_backend.py`](scripts/check_backend.py) |
| Evidence | [`docs/evidence/lift-and-shift/`](docs/evidence/lift-and-shift/) |

### Evidence
| File | What it shows |
|---|---|
| `01-onpremise-check.txt` | Test against the local backend (`localhost:8000`): all checks passed |
| `01b-onpremise-container.png` | Backend container running in Docker Desktop |
| `02-ec2-security-group.png` | Security Group rules (ports 22 and 8000) |
| `03-ec2-instance-running.png` | EC2 instance running, with its public IP |
| `04-ec2-bootstrap-output.png` | End of the bootstrap script, container `Up` |
| `05-aws-check.txt` | The same test against the EC2 public IP: all checks passed |

### Result
| Check | On-premise | AWS |
|---|---|---|
| `GET /health` | HTTP 200, `healthy` | HTTP 200, `healthy` |
| `POST /api/v1/consultar` (normal) | HTTP 200, `OK`, circuit `CLOSED` | HTTP 200, `OK`, circuit `CLOSED` |
| Code changes needed | 0 | 0 |

### How to reproduce
Local test and AWS steps are in section 5 of [`docs/lift-and-shift.md`](docs/lift-and-shift.md).

---

