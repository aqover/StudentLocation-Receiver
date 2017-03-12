#!/bin/sh
### BEGIN INIT INFO
# Provides:          locating
# Required-Start:    $local_fs $network $named $time $syslog
# Required-Stop:     $local_fs $network $named $time $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Description:       service locating
### END INIT INFO

SCRIPT="nohup sudo python /home/fa/locating/app.py"
SCRIPT_UPDATE="nohup sudo python /home/fa/locating/update.py"
RUNAS=root

PIDFILE=/var/run/locating.pid
LOGFILE=/var/log/locating.log

PID_UPDATE_FILE=/var/run/locating-update.pid
LOG_UPDATE_FILE=/var/log/locating-update.log

start() {
  if [ -f "$PIDFILE" ] && kill -0 $(cat "$PIDFILE"); then
    echo 'Service already running' >&2
    return 1
  fi
  echo 'Starting service ^  ' >&2
  su -c "hciconfig hci0 up"
  local CMD="$SCRIPT &> \"$LOGFILE\" & echo \$!"
  su -c "$CMD" $RUNAS > "$PIDFILE"
  echo 'Service started' >&2
}

stop() {
  if [ ! -f "$PIDFILE" ] || ! kill -0 $(cat "$PIDFILE"); then
    echo 'Service not running' >&2
    return 1
  fi
  echo 'Stopping service ^  ' >&2
  kill -15 $(cat "$PIDFILE") && rm -f "$PIDFILE"
  su -c "hciconfig hci0 down"
  echo 'Service stopped' >&2
}

uninstall() {
  echo -n "Are you really sure you want to uninstall this service? That cannot be undone. [yes|No] "
  local SURE
  read SURE
  if [ "$SURE" = "yes" ]; then
    stop
    rm -f "$PIDFILE"
    echo "Notice: log file is not be removed: '$LOGFILE'" >&2
    update-rc.d -f locating remove
    rm -fv "$0"
  fi
}

update_start() {
  if [ -f "$PID_UPDATE_FILE" ] && kill -0 $(cat "$PID_UPDATE_FILE"); then
    echo 'Update service already running' >&2
    return 1
  fi
  echo 'Starting update service ^  ' >&2
  local CMD="$SCRIPT_UPDATE &> \"$LOG_UPDATE_FILE\" & echo \$!"
  su -c "$CMD" $RUNAS > "$PID_UPDATE_FILE"
  echo 'Update service started' >&2
}

update_stop() {
  if [ ! -f "$PID_UPDATE_FILE" ] || ! kill -0 $(cat "$PID_UPDATE_FILE"); then
    echo 'Update service not running' >&2
    return 1
  fi
  echo 'Stopping service ^  ' >&2
  kill -15 $(cat "$PID_UPDATE_FILE") && rm -f "$PID_UPDATE_FILE"
  echo 'Update service stopped' >&2
}

case "$1" in
  start)
    start
    update_start
    ;;
  stop)
    stop
    update_stop
    ;;
  uninstall)
    uninstall
    ;;
  restart)
    stop
    start
    ;;
  update)
    update_start
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|uninstall|update}"
esac

