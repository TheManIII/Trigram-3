#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Trigram-3 测试ABS和NEG指令"""

import sys
sys.path.insert(0, '.')

from triton_simulator import Simulator
from trigram_utils import build_instruction

# Trigram-3 测试: ABS和NEG指令
print("Trigram-3 测试: ABS和NEG指令")
print("=" * 60)

instructions = [
    # 测试1: ABS指令 - 正数
    # OFFSET R1, R0, #10  (R1 = 10)
    build_instruction('00T', 1, 0, imm=10),
    # ABS R2, R1  (R2 = |10| = 10)
    build_instruction('01T', 2, 1),
    # STORE R2, [0]
    build_instruction('0T0', 2, 0, rs2=2, imm=0),
    
    # 测试2: ABS指令 - 负数
    # OFFSET R3, R0, #-5  (R3 = -5)
    build_instruction('00T', 3, 0, imm=-5),
    # ABS R4, R3  (R4 = |-5| = 5)
    build_instruction('01T', 4, 3),
    # STORE R4, [1]
    build_instruction('0T0', 4, 0, rs2=4, imm=1),
    
    # 测试3: NEG指令 - 正数
    # OFFSET R5, R0, #7  (R5 = 7)
    build_instruction('00T', 5, 0, imm=7),
    # NEG R6, R5  (R6 = -7)
    build_instruction('0T1', 6, 5),
    # STORE R6, [2]
    build_instruction('0T0', 6, 0, rs2=6, imm=2),
    
    # 测试4: NEG指令 - 负数
    # OFFSET R7, R0, #-3  (R7 = -3)
    build_instruction('00T', 7, 0, imm=-3),
    # NEG R8, R7  (R8 = 3)
    build_instruction('0T1', 8, 7),
    # STORE R8, [3]
    build_instruction('0T0', 8, 0, rs2=8, imm=3),
    
    # 测试5: 综合测试
    # OFFSET R1, R0, #-8  (R1 = -8)
    build_instruction('00T', 1, 0, imm=-8),
    # ABS R2, R1  (R2 = |-8| = 8)
    build_instruction('01T', 2, 1),
    # NEG R3, R2  (R3 = -8)
    build_instruction('0T1', 3, 2),
    # STORE R1, [4]
    build_instruction('0T0', 1, 0, rs2=1, imm=4),
    # STORE R2, [5]
    build_instruction('0T0', 2, 0, rs2=2, imm=5),
    # STORE R3, [6]
    build_instruction('0T0', 3, 0, rs2=3, imm=6),
    
    # HALT
    "000000000000000000000000000",
]

sim = Simulator()
sim.cpu.reset()
sim.cpu.load_program(instructions)
sim.cpu.verbose = True

# 限制执行周期数
max_cycles = 20
cycle_count = 0
while not sim.cpu.halted and cycle_count < max_cycles:
    sim.cpu.step()
    cycle_count += 1

if cycle_count >= max_cycles:
    print("\n[警告] 达到最大周期数限制")

sim.cpu.print_state()

print("\n测试结果验证:")
print(f"MEM[0] (ABS正数): {sim.cpu.memory.read(0).to_int()} (预期: 10)")
print(f"MEM[1] (ABS负数): {sim.cpu.memory.read(1).to_int()} (预期: 5)")
print(f"MEM[2] (NEG正数): {sim.cpu.memory.read(2).to_int()} (预期: -7)")
print(f"MEM[3] (NEG负数): {sim.cpu.memory.read(3).to_int()} (预期: 3)")
print(f"MEM[4] (综合-原始): {sim.cpu.memory.read(4).to_int()} (预期: -8)")
print(f"MEM[5] (综合-ABS): {sim.cpu.memory.read(5).to_int()} (预期: 8)")
print(f"MEM[6] (综合-NEG): {sim.cpu.memory.read(6).to_int()} (预期: -8)")

# 验证结果
success = True
if sim.cpu.memory.read(0).to_int() != 10:
    print("❌ 测试1失败: ABS正数")
    success = False
if sim.cpu.memory.read(1).to_int() != 5:
    print("❌ 测试2失败: ABS负数")
    success = False
if sim.cpu.memory.read(2).to_int() != -7:
    print("❌ 测试3失败: NEG正数")
    success = False
if sim.cpu.memory.read(3).to_int() != 3:
    print("❌ 测试4失败: NEG负数")
    success = False
if sim.cpu.memory.read(4).to_int() != -8:
    print("❌ 测试5失败: 综合测试-原始")
    success = False
if sim.cpu.memory.read(5).to_int() != 8:
    print("❌ 测试5失败: 综合测试-ABS")
    success = False
if sim.cpu.memory.read(6).to_int() != -8:
    print("❌ 测试5失败: 综合测试-NEG")
    success = False

if success:
    print("\n[OK] 所有测试通过！")
else:
    print("\n[ERR] 部分测试失败")
