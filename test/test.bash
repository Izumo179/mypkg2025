#!/bin/bash
# SPDX-FileCopyrightText: 2025 Soshi Ohseto
# SPDX-License-Identifier: BSD-3-Clause

set -eu

#ROS 2 環境（GitHub Actions想定）
: "${ROS_DISTRO:=humble}"
source "/opt/ros/${ROS_DISTRO}/setup.bash"

#colcon build 後の環境があれば使う
if [ -f install/setup.bash ]; then
  source install/setup.bash
fi

#talker をバックグラウンド起動
ros2 run mypkg talker >/dev/null 2>&1 &
TALKER_PID=$!

#終了時に必ず止める
cleanup() {
  kill "${TALKER_PID}" 2>/dev/null || true
}
trap cleanup EXIT

#起動待ち
sleep 1

#トピックから1件受信できるか確認
OUTPUT=$(timeout 5 ros2 topic echo -n 1 /cpu_usage)

#何も受信できなければ失敗
if [ -z "${OUTPUT}" ]; then
  echo "テスト失敗…:cpu_usageからメッセージを受信できませんでした" >&2
  exit 1
fi

echo "テスト成功！"
