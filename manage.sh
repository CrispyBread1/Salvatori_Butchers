#!/bin/bash

set -e

cd "$(dirname "$0")"

MODE="$1"

DEV_PYTHON="$PWD/.venv/bin/python3"
PROD_PYTHON="/usr/bin/python3"


start_docker() {
    if docker info >/dev/null 2>&1; then
        return
    fi

    echo "Starting Docker..."
    open -a Docker

    until docker info >/dev/null 2>&1; do
        sleep 2
    done
}


start_supabase() {
    if supabase status >/dev/null 2>&1; then
        echo "Local Supabase already running."
    else
        echo "Starting local Supabase..."
        supabase start
    fi
}


case "$MODE" in

    dev)
        echo "Starting ManageMeStock DEVELOPMENT"

        if [ ! -x "$DEV_PYTHON" ]; then
            echo "ERROR: Development virtual environment not found."
            echo "Expected at: $DEV_PYTHON"
            echo ""
            echo "Create it with:"
            echo "python3 -m venv .venv"
            exit 1
        fi

        export APP_ENV=development

        start_docker
        start_supabase

        "$DEV_PYTHON" main.py
        ;;


    prod)
        echo "WARNING: Starting ManageMeStock PRODUCTION"
        echo "Using LIVE Salvatori data."

        if [ ! -x "$PROD_PYTHON" ]; then
            echo "ERROR: Production Python not found."
            echo "Expected at: $PROD_PYTHON"
            exit 1
        fi

        export APP_ENV=production

        "$PROD_PYTHON" main.py
        ;;


    reset-db)
        echo "Resetting LOCAL development database..."

        start_docker
        start_supabase

        supabase db reset
        ;;


    status)
        echo "Local Supabase status:"
        supabase status
        ;;


    stop)
        echo "Stopping local Supabase..."
        supabase stop
        ;;


    *)
        echo "ManageMeStock"
        echo ""
        echo "Usage:"
        echo "  ./manage.sh dev       Start development environment"
        echo "  ./manage.sh prod      Start production/live application"
        echo "  ./manage.sh reset-db  Reset local development database"
        echo "  ./manage.sh status    Show local Supabase status"
        echo "  ./manage.sh stop      Stop local Supabase"
        echo ""
        exit 1
        ;;

esac
