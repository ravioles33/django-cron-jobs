#!/usr/bin/env bash
# wait-for-it.sh with detailed logging

set -e
log_file="/app/wait-for-it.log"

function log() {
  echo "$(date +'%Y-%m-%d %H:%M:%S') - $1" | tee -a "$log_file"
}

log "Script started with arguments: $*"

HOST=$1
shift
PORT=$1
shift
TIMEOUT=${TIMEOUT:-60}
RETRIES=5
COUNT=0

log "Waiting for ${HOST}:${PORT} with timeout of ${TIMEOUT} seconds."

for ((i=0; i<$RETRIES; i++)); do
  if nc -z "$HOST" "$PORT"; then
    log "Successfully connected to ${HOST}:${PORT}"
    break
  else
    log "Attempt $((i+1)): Unable to connect to ${HOST}:${PORT}, retrying..."
    sleep $((TIMEOUT / RETRIES))
  fi
done

if [ "$i" -eq "$RETRIES" ]; then
  log "Operation timed out: Unable to connect to ${HOST}:${PORT} after ${RETRIES} attempts."
  exit 1
fi

log "Host ${HOST}:${PORT} is available. Proceeding with the command: $*"
exec "$@"
