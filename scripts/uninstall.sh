#!/bin/sh
set -eu

if command -v uv >/dev/null 2>&1; then
  UV="uv"
else
  echo "uv is not installed or is not on PATH."
  echo "Install uv first, then run: uv tool uninstall openbyte"
  exit 1
fi

if "$UV" tool list 2>/dev/null | grep -q '^openbyte '; then
  "$UV" tool uninstall openbyte
  echo "OpenByte has been uninstalled."
else
  echo "OpenByte is not currently installed as a uv tool."
fi
