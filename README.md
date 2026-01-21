# mypkg2025
[![test](https://github.com/Izumo179/mypkg2025/actions/workflows/test.yml/badge.svg)](https://github.com/Izumo179/mypkg2025/actions/workflows/test.yml)

## 概要
mypkg2025は，Linux環境におけるCPU使用率を取得して，ROS2のトピックとして配信するパッケージです．

CPUの負荷状況を他ノードから監視したり，ログとして記録したりする用途を想定しています．

## ノード

### talker

CPU使用率を計算し，`/cpu_usage` にpublishします．

- 取得元: Linux の CPU 統計情報（実装では `/proc/stat` を利用）
- 計算: 2回分の取得値の差分から使用率（%）を算出
- 出力: 使用率と状態（`OK` / `WARN`）

### listener

`/cpu_usage` を読み，受信した内容を標準出力に表示します．

## パラメータ（talker）
- rate_hz (float, default: 1.0)
  publish 周期（Hz）．例: 2.0なら0.5 秒周期．

- warn_percent (float, default: 70.0)
  CPU使用率がこの値以上のときlevel=WARNを出力します．

## 使い方
### talker の実行
```console
$ ros2 run mypkg2025 talker
```

#パラメータを指定する例
```console
$ ros2 run mypkg2025 talker --ros-args -p rate_hz:=2.0 -p warn_percent:=50.0
```

###listener の実行
```console
$ ros2 run mypkg2025 listener

cpu=23.5% level=OK
```
別端末でtalkerを実行した状態でlistenerを起動すると，受信内容が表示されます．


## テスト

動作確認ようにテストは以下で実行できます．
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
    - https://github.com/ryuichiueda/slides_marp/tree/master/robosys2024
- © 2025 Soshi Ohseto
