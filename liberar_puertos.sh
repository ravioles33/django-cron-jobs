#!/bin/bash

# Lista de puertos a verificar
PUERTOS=(8000 5432 5672 15672 15692)

for PUERTO in "${PUERTOS[@]}"; do
  PID=$(sudo lsof -t -i :$PUERTO)
  if [ -n "$PID" ]; then
    echo "Deteniendo proceso en el puerto $PUERTO con PID $PID"
    sudo kill -9 $PID
  else
    echo "El puerto $PUERTO está libre."
  fi
done
