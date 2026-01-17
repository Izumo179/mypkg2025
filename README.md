# mypkg2025

## 概要
mypkg2025 は、Linux 環境上で CPU の使用状況を取得し、
ROS 2 のトピックとして定期的に配信するパッケージです。

talkerノードはCPUの状態を取得し，
その情報を `/cpu_usage` トピックに文字列としてpublishします。

システムの状態監視やデバッグ用途を想定しています。

## ノード
### cpu_publisher（仮）
CPU 使用率を計算し、一定周期でトピックに publish します。

## トピック
### /cpu_usage
- 型: std_msgs/msg/String
- 内容: CPU 使用率を文字列として送信します

出力例:
cpu=23.5%

## 動作環境
- ROS 2
- Linux

## ライセンス
- BSD-3-Clause

