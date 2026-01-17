#!/bin/bash
# SPDX-FileCopyrightText: 2025 Soshi Ohseto
# SPDX-License-Identifier: BSD-3-Clause

set -e

fail() {
  echo "TEST FAILED: $*" >&2
  exit 1
}

pass() {
  echo "TEST PASSED: $*" >&2
}

set +u
: "${ROS_DISTRO:=humble}"
source "/opt/ros/${ROS_DISTRO}/setup.bash"
set -u

cd /root/ros2_ws

echo "[1] colcon build" >&2
set +e
colcon build
status=$?
set -e
[ "$status" -eq 0 ] || fail "colcon build exited with $status"
pass "colcon build"

set +u
source install/setup.bash
set -u

echo "[2] start talker" >&2
set +e
timeout 5s ros2 run mypkg talker >/tmp/mypkg_talker.log 2>/tmp/mypkg_talker.err &
TALKER_PID=$!
set -e

sleep 1
kill -0 "$TALKER_PID" 2>/dev/null || fail "talker is not running"

cleanup() {
  kill "$TALKER_PID" 2>/dev/null || true
}
trap cleanup EXIT

pass "talker started"

echo "[3] run listener (expect message)" >&2
set +e
OUT="$(timeout 5s ros2 run mypkg listener 2>/tmp/mypkg_listener.err)"
status=$?
set -e
[ "$status" -eq 0 ] || fail "listener exited with $status"

echo "$OUT" | grep -q "CPU" || fail "listener output did not contain 'CPU'"

pass "listener received message"

echo "ALL TESTS OK" >&2
