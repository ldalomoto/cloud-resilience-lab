#!/usr/bin/env bash
# Prepares an Amazon Linux 2023 EC2 instance and starts the app with Docker Compose.
# This is the "shift" step of the Lift-and-Shift: same code, same Docker setup, new host.
#
# Usage (run on the EC2 instance):
#   bash ec2-bootstrap.sh [BRANCH] [SERVICES]
#   BRANCH   git branch to deploy      (default: main)
#   SERVICES compose services to start (default: backend)
set -euo pipefail

REPO_URL="https://github.com/ldalomoto/cloud-resilience-lab.git"
BRANCH="${1:-main}"
SERVICES="${2:-backend}"
APP_DIR="$HOME/cloud-resilience-lab"
COMPOSE_VERSION="v2.35.1"

echo "==> 1/5 Installing Docker and Git"
sudo dnf install -y docker git
sudo systemctl enable --now docker

echo "==> 2/5 Installing the Docker Compose plugin ${COMPOSE_VERSION}"
sudo mkdir -p /usr/local/lib/docker/cli-plugins
sudo curl -fSL \
  "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-linux-$(uname -m)" \
  -o /usr/local/lib/docker/cli-plugins/docker-compose
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
sudo docker compose version

echo "==> 3/5 Getting the code (branch: ${BRANCH})"
if [ -d "${APP_DIR}/.git" ]; then
  git -C "${APP_DIR}" fetch origin
  git -C "${APP_DIR}" checkout "${BRANCH}"
  git -C "${APP_DIR}" pull --ff-only origin "${BRANCH}"
else
  git clone --branch "${BRANCH}" "${REPO_URL}" "${APP_DIR}"
fi

echo "==> 4/5 Starting services: ${SERVICES}"
cd "${APP_DIR}/app"
sudo docker compose up --build -d ${SERVICES}

echo "==> 5/5 Status"
sudo docker compose ps
echo
echo "Done. Test it from your PC with:"
echo "  python scripts/check_backend.py http://<EC2_PUBLIC_IP>:8000"
