#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试平衡三进制寄存器编码"""

import sys
sys.path.insert(0, '.')

from triton_simulator import Simulator
from trigram_utils import int_to_balanced_ternary_str, reg_to_trits, build_instruction

# 测试平衡三进制寄存器编码
print("测试平衡三进制寄存器编码")
print("=" * 60)

# 显示寄存器编码表
print("\n寄存器编码表:")
print("寄存器 | 编码(3爻) | 十进制")
print("-------|----------|--------")
for reg in range(9):
    encoding = reg_to_trits(reg)
    print(f"  R{reg}   |   {encoding}   |   {reg}")

# 验证编码是否正确
print("\n验证编码:")
test_cases = [
    (0, '000'),
    (1, '001'),
    (2, '01T'),
    (3, '010'),
    (4, '011'),
    (5, '1TT'),
    (6, '1T0'),
    (7, '1T1'),
    (8, '10T'),
]

all_passed = True
for reg, expected in test_cases:
    actual = reg_to_trits(reg)
    status = 'OK' if actual == expected else 'FAIL'
    print(f"R{reg}: {actual} (预期: {expected}) - {status}")
    if actual != expected:
        all_passed = False

# 测试指令构建
print("\n测试指令构建:")
instructions = [
    # OFFSET R1, R0, #5  (R1编码: 001)
    build_instruction('00T', 1, 0, imm=5),
    # OFFSET R2, R0, #10  (R2编码: 01T)
    build_instruction('00T', 2, 0, imm=10),
    # ADD R3, R1, R2  (R3编码: 010, R1编码: 001, R2编码: 01T)
    build_instruction('001', 3, 1, rs2=2),
    # HALT
    "000000000000000000000000000",
]

for i, inst in enumerate(instructions):
    print(f"指令{i}: {inst} (长度: {len(inst)})")
    if len(inst) != 27:
        print(f"  错误: 指令长度应为27爻")
        all_passed = False

if all_passed:
    print("\n[OK] 所有测试通过！")
else:
    print("\n[ERR] 部分测试失败")
