#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Soshi Ohseto
# SPDX-License-Identifier: BSD-3-Clause

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time

class CpuPublisher(Node):
    def __init__(self):
        super().__init__('cpu_publisher')
        self.publisher_ = self.create_publisher(String, 'cpu_usage', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        msg = String()
        msg.data = 'cpu check start'
        self.publisher_.publish(msg)
        self.get_logger().info(msg.data)

def main():
    rclpy.init()
    node = CpuPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
port rclpy
from rclpy.node import Node
from std_msgs.msg import Int16

rclpy.init()
node = Node("talker")
pub = node.create_publisher(Int16, "countup", 10)
n = 0


def cb():
    global n
    msg = Int16()
    msg.data = n
    pub.publish(msg)
    n += 1


def main():
    node.create_timer(0.5, cb)
    rclpy.spin(node)
