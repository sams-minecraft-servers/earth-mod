#!/usr/bin/env bash
# Installs the daily refresh of the country radio's samples (run with sudo).
set -euo pipefail
cd "$(dirname "$0")"
install -m 644 earth-radio-refresh.service earth-radio-refresh.timer /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now earth-radio-refresh.timer
systemctl list-timers earth-radio-refresh.timer --no-pager
