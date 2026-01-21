#!/bin/bash
# SPDX-FileCopyrightText: 2025 Soshi Ohseto
# SPDX-License-Identifier: BSD-3-Clause

set -e

fail() {
  echo "テスト失敗…：$*" >&2
  exit 1
}

pass() {
  echo "テスト成功！：$*" >&2
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
[ "$status" -eq 0 ] || fail "colcon build が失敗しました（exit=$status）"
pass "colcon build が正常に終了しました"

set +u
source install/setup.bash
set -u

echo "[2] start talker" >&2
set +e
timeout 5s ros2 run mypkg2025 talker >/tmp/mypkg_talker.log 2>/tmp/mypkg_talker.err &
TALKER_PID=$!
set -e

sleep 1
kill -0 "$TALKER_PID" 2>/dev/null || fail "talker が起動していません（プロセスが存在しない）"

cleanup() {
  kill "$TALKER_PID" 2>/dev/null || true
}
trap cleanup EXIT

pass "talker が起動しました"

echo "[3] listener を実行して受信を確認" >&2
set +e
OUT="$(timeout 5s ros2 run mypkg2025 listener 2>/tmp/mypkg_listener.err)"
status=$?
set -e

if [ "$status" -ne 0 ] && [ "$status" -ne 124 ]; then
  fail "listener が予期せず異常終了しました（exit=$status）"
fi

echo "$OUT" | grep -q "CPU" || fail "listener がメッセージを受信できませんでした（出力に CPU がありません）"

pass "listener がメッセージを受信しました"

echo "すべてのテストが成功しました！" >&2
