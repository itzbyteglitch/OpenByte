#!/bin/sh
set -eu

REPO="https://github.com/itzbyteglitch/OpenByte.git"

printf '%s\n' "Installing OpenByte..."

if command -v uv >/dev/null 2>&1; then
  UV="uv"
else
  printf '%s\n' "uv was not found. Installing uv..."
  if command -v curl >/dev/null 2>&1; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
  elif command -v wget >/dev/null 2>&1; then
    wget -qO- https://astral.sh/uv/install.sh | sh
  else
    echo "Error: curl or wget is required to install uv." >&2
    exit 1
  fi

  # uv's installer normally places the executable here.
  if [ -x "$HOME/.local/bin/uv" ]; then
    UV="$HOME/.local/bin/uv"
  elif [ -x "$HOME/.cargo/bin/uv" ]; then
    UV="$HOME/.cargo/bin/uv"
  elif command -v uv >/dev/null 2>&1; then
    UV="uv"
  else
    echo "Error: uv was installed but could not be found. Restart your shell and run the installer again." >&2
    exit 1
  fi
fi

"$UV" tool install --force --from "$REPO" openbyte

printf '\nOpenByte installed successfully.\n'
printf 'Run: openbyte\n'
