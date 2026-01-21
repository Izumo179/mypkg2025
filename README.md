# mypkg2025
[![test](https://github.com/Izumo179/mypkg2025/actions/workflows/test.yml/badge.svg)](https://github.com/Izumo179/mypkg2025/actions/workflows/test.yml)

## 概要
mypkg2025 は、Linux 環境における CPU 使用率を取得して、ROS2のトピックとして配信するパッケージです。

CPU の負荷状況を他ノードから監視したり、ログとして記録したりする用途を想定しています。

## ノード

### talker

CPU 使用率を計算し、`/cpu_usage` に publish します。

- 取得元: Linux の CPU 統計情報（実装では `/proc/stat` を利用）
- 計算: 2回分の取得値の差分から使用率（%）を算出
- 出力: 使用率と状態（`OK` / `WARN`）

### listener

`/cpu_usage` を読み、受信した内容を標準出力に表示します。

## トピック
### `/cpu_usage` (`std_msgs/msg/String`)

talker が publish します。

出力例:

```text
cpu=23.5% level=OK
```
cpu: 使用率（%）

- OK : 使用率が閾値未満
- WARN : 使用率が閾値以上

## パラメータ（talker）
- rate_hz (float, default: 1.0)
  publish 周期（Hz）．例: 2.0 なら 0.5 秒周期．

- warn_percent (float, default: 70.0)
  CPU 使用率がこの値以上のとき level=WARN を出力します．

## 使い方
### talker の実行
```console
$ ros2 run mypkg2025 talker
```

パラメータを指定する例
```console
$ ros2 run mypkg2025 talker --ros-args -p rate_hz:=2.0 -p warn_percent:=50.0
```
listener の実行
```console
$ ros2 run mypkg2025 listener
```

別端末で talker を実行した状態で listener を起動すると、受信内容が表示されます。

## テスト

本パッケージは、ノードをブラックボックスとして扱い、ros2 run による起動とトピック通信（入出力）をシェルスクリプトで確認します。
```console
$ bash test/test.bash
```

## 動作環境
- ROS 2
- Linux

## ライセンス等
 このプログラムはロボットシステム学課題2のために作成されたものです．
- このソフトウェアパッケージは，3条項BSDライセンスの下，再頒布および使用が許可されます．
- このパッケージのコードの一部の書き方や構成は，下記のスライド（CC-BY-SA 4.0 by Ryuichi Ueda）を参考にしたものです．
    - [ryuichiueda/my_slides robosys_2025](https://github.com/ryuichiueda/slides_marp/tree/master/robosys_2025)
- © 2025 Soshi Ohseto
