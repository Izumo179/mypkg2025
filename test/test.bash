#!/bin/bash
# SPDX-FileCopyrightText: 2025 Soshi Ohseto
# SPDX-License-Identifier: BSD-3-Clause

set -e

set +u
: "${ROS_DISTRO:=humble}"
source "/opt/ros/${ROS_DISTRO}/setup.bash"
set -u

WS="$(pwd)"

colcon build --symlink-install

source install/setup.bash

ros2 run mypkg talker >/dev/null 2>&1 &
TALKER_PID=$!

cleanup() {
  kill "${TALKER_PID}" 2>/dev/null || true
}
trap cleanup EXIT

sleep 1

OUTPUT="$(timeout 5 ros2 topic echo -n 1 /cpu_usage || true)"

if [ -z "${OUTPUT}" ]; then
  echo "テスト失敗:cpu_usageからメッセージを受信できませんでした" >&2
  exit 1
fi

echo "${OUTPUT}" | grep -Eq 'cpu=[0-9]+(\.[0-9]+)?% level=(OK|WARN)' || {
  echo "テスト失敗:想定外のメッセージです: ${OUTPUT}" >&2
  exit 1
}

echo "テスト成功！"
