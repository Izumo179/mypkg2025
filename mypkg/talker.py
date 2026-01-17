#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Soshi Ohseto
# SPDX-License-Identifier: BSD-3-Clause

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class CpuPublisher(Node):
    def __init__(self):
        super().__init__('cpu_publisher')
        self.publisher_ = self.create_publisher(String, '/cpu_usage', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)

    def read_cpu_stat_line(self) -> str:
        """Read the first line of /proc/stat (e.g. 'cpu  123 0 456 ...')."""
        with open('/proc/stat', 'r', encoding='utf-8') as f:
            line = f.readline()
        return line.strip()

    def timer_callback(self):
        cpu_line = self.read_cpu_stat_line()

        msg = String()
        msg.data = f"cpu_raw: {cpu_line}"

        self.publisher_.publish(msg)
        self.get_logger().info(msg.data)


def main():
    rclpy.init()
    node = CpuPublisher()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

