#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Soshi Ohseto
# SPDX-License-Identifier: BSD-3-Clause

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


def read_cpu_times(path: str = "/proc/stat") -> tuple[int, int]:
    """
    Read /proc/stat and return (idle, total).
    idle = idle + iowait
    total = sum of all cpu time fields
    """
    with open(path, "r", encoding="utf-8") as f:
        line = f.readline().strip()

    parts = line.split()
    if len(parts) < 5 or parts[0] != "cpu":
        raise RuntimeError("unexpected /proc/stat format")

    nums = [int(x) for x in parts[1:]]
    idle = nums[3] + (nums[4] if len(nums) > 4 else 0)
    total = sum(nums)
    return idle, total


def calc_cpu_usage_percent(prev: tuple[int, int], curr: tuple[int, int]) -> float:
    """Calculate CPU usage % from (idle,total) samples."""
    prev_idle, prev_total = prev
    curr_idle, curr_total = curr

    d_total = curr_total - prev_total
    d_idle = curr_idle - prev_idle

    if d_total <= 0:
        return 0.0

    usage = 100.0 * (d_total - d_idle) / d_total

    # clamp
    if usage < 0.0:
        usage = 0.0
    if usage > 100.0:
        usage = 100.0
    return usage


class CpuPublisher(Node):
    def __init__(self):
        super().__init__("cpu_publisher")

        # Parameters (後でREADMEに書くと良い)
        self.declare_parameter("rate_hz", 1.0)
        self.declare_parameter("warn_percent", 70.0)

        self.publisher_ = self.create_publisher(String, "/cpu_usage", 10)

        rate_hz = float(self.get_parameter("rate_hz").value)
        period = 1.0 / rate_hz if rate_hz > 0 else 1.0

        # first sample
        self.prev = read_cpu_times()

        self.timer = self.create_timer(period, self.timer_callback)

    def timer_callback(self):
        curr = read_cpu_times()
        usage = calc_cpu_usage_percent(self.prev, curr)
        self.prev = curr

        warn = float(self.get_parameter("warn_percent").value)
        level = "WARN" if usage >= warn else "OK"

        msg = String()
        msg.data = f"cpu={usage:.1f}% level={level}"

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


if __name__ == "__main__":
    main()
