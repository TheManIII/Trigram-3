#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试新的平衡三进制寄存器编码"""

import sys
sys.path.insert(0, '.')

from triton_simulator import Simulator
from trigram_utils import int_to_balanced_ternary_str, reg_to_trits, build_instruction

# 测试程序: 使用新编码的寄存器
print("Trigram-3 测试: 新的平衡三进制寄存器编码")
print("=" * 60)

# 测试R2寄存器（编码为01T）
instructions = [
    # OFFSET R2, R0, #10  (R2编码: 01T)
    build_instruction('00T', 2, 0, imm=10),
    # OFFSET R5, R0, #5  (R5编码: 1TT)
    build_instruction('00T', 5, 0, imm=5),
    # ADD R3, R2, R5  (R3编码: 010, R2编码: 01T, R5编码: 1TT)
    build_instruction('001', 3, 2, rs2=5),
    # STORE R3, [0]
    build_instruction('0T0', 3, 0, rs2=3, imm=0),
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

print("\n测试结果验证:")
print(f"R2 (编码01T): {sim.cpu.registers.read(2).to_int()} (预期: 10)")
print(f"R5 (编码1TT): {sim.cpu.registers.read(5).to_int()} (预期: 5)")
print(f"R3 (编码010): {sim.cpu.registers.read(3).to_int()} (预期: 15)")
print(f"MEM[0]: {sim.cpu.memory.read(0).to_int()} (预期: 15)")

# 验证结果
success = True
if sim.cpu.registers.read(2).to_int() != 10:
    print("错误: R2值不正确")
    success = False
if sim.cpu.registers.read(5).to_int() != 5:
    print("错误: R5值不正确")
    success = False
if sim.cpu.registers.read(3).to_int() != 15:
    print("错误: R3值不正确")
    success = False
if sim.cpu.memory.read(0).to_int() != 15:
    print("错误: MEM[0]值不正确")
    success = False

if success:
    print("\n[OK] 新的寄存器编码测试通过！")
else:
    print("\n[ERR] 测试失败")
