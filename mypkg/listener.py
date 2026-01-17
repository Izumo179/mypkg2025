#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Soshi Ohseto
# SPDX-License-Identifier: BSD-3-Clause

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class CpuUsageListener(Node):
    def __init__(self):
        super().__init__("cpu_usage_listener")
        self.subscription = self.create_subscription(
            String,
            "/cpu_usage",
            self.listener_callback,
            10,
        )

    def listener_callback(self, msg: String):
        print(f"CPU情報を受信しました: {msg.data}")
        self.get_logger().info(msg.data)


def main():
    rclpy.init()
    node = CpuUsageListener()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
