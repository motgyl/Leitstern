#!/bin/bash
# Service management helper for Leitshtern

SERVICE_NAME="serv_mess"

# Путь к проекту
APP_DIR="/opt/Leitshtern"

# Логи (если используешь файл)
LOG_FILE="$APP_DIR/logs/server.log"

# Виртуальное окружение (если есть)
VENV_DIR="$APP_DIR/venv"


print_usage() {
    echo "Usage: $0 <command>"
    echo ""
    echo "Commands:"
    echo "  start      - Start service (systemd)"
    echo "  dev        - Run server directly"
    echo "  stop       - Stop service"
    echo "  restart    - Restart service"
    echo "  status     - Show status"
    echo "  logs       - Show logs"
    echo "  logs -f    - Follow logs"
    echo "  update     - Update project from git"
    echo "  enable     - Enable autostart"
    echo "  disable    - Disable autostart"
}


start() {
    echo "Starting $SERVICE_NAME..."
    sudo systemctl start "$SERVICE_NAME"
    sleep 1
    sudo systemctl status "$SERVICE_NAME"
}


dev() {
    echo "Running Leitshtern in dev mode..."

    cd "$APP_DIR" || {
        echo "Project directory not found: $APP_DIR"
        exit 1
    }

    if [ -d "$VENV_DIR" ]; then
        echo "Activating virtualenv..."
        source "$VENV_DIR/bin/activate"
    fi

    python3 server.py
}


stop() {
    echo "Stopping $SERVICE_NAME..."
    sudo systemctl stop "$SERVICE_NAME"
}


restart() {
    echo "Restarting $SERVICE_NAME..."
    sudo systemctl restart "$SERVICE_NAME"
    sleep 1
    sudo systemctl status "$SERVICE_NAME"
}


status() {
    sudo systemctl status "$SERVICE_NAME"
}


logs() {
    if [ "$2" = "-f" ]; then
        sudo journalctl -u "$SERVICE_NAME" -f
    else
        sudo journalctl -u "$SERVICE_NAME" --no-pager | tail -100
    fi
}


update() {
    echo "Updating project..."

    cd "$APP_DIR" || exit 1

    git pull

    if [ -f "requirements.txt" ]; then
        echo "Updating dependencies..."

        if [ -d "$VENV_DIR" ]; then
            source "$VENV_DIR/bin/activate"
        fi

        pip install -r requirements.txt
    fi

    echo "Update complete"
}


enable() {
    sudo systemctl enable "$SERVICE_NAME"
}


disable() {
    sudo systemctl disable "$SERVICE_NAME"
}


case "$1" in
    start) start ;;
    dev) dev ;;
    stop) stop ;;
    restart) restart ;;
    status) status ;;
    logs) logs "$2" ;;
    update) update ;;
    enable) enable ;;
    disable) disable ;;
    *) print_usage ;;
esac
