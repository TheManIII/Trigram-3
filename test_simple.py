#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Trigram-3 简单测试脚本"""

import sys
sys.path.insert(0, '.')

from triton_simulator import Simulator, CPU
from trigram_utils import build_instruction

# Trigram-3 测试: 加法运算
print("Trigram-3 测试: 加法运算")
print("=" * 60)

instructions = [
    # OFFSET R2, R0, imm=5  (R2 = 5)
    build_instruction('00T', 2, 0, imm=5),
    # OFFSET R3, R0, imm=3  (R3 = 3)
    build_instruction('00T', 3, 0, imm=3),
    # ADD R1, R2, R3  (R1 = R2 + R3)
    build_instruction('001', 1, 2, rs2=3),
    # STORE R1, [R0+0]
    build_instruction('0T0', 1, 0, rs2=1, imm=0),
    # HALT
    "000000000000000000000000000",
]

sim = Simulator()
sim.cpu.reset()
sim.cpu.load_program(instructions)
sim.cpu.verbose = True

# 限制执行周期数
max_cycles = 10
cycle_count = 0
while not sim.cpu.halted and cycle_count < max_cycles:
    sim.cpu.step()
    cycle_count += 1

if cycle_count >= max_cycles:
    print("\n[警告] 达到最大周期数限制")

sim.cpu.print_state()

print("\n预期: R1 = 8, MEM[0] = 8")
print(f"实际: R1 = {sim.cpu.registers.read(1).to_int()}, MEM[0] = {sim.cpu.memory.read(0).to_int()}")
