#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trigram-3 公共工具模块
提供平衡三进制转换、寄存器编码等通用功能

作者：TheManIII
版本：1.0
"""

from typing import List


def int_to_balanced_ternary_str(value: int, width: int = 9) -> str:
    """
    将整数转换为平衡三进制字符串

    Args:
        value: 要转换的整数
        width: 输出宽度（trit数）

    Returns:
        平衡三进制字符串，使用T、0、1表示
    """
    if width <= 0:
        raise ValueError("宽度必须大于0")

    result = []
    remaining = value

    for _ in range(width):
        remainder = remaining % 3
        if remainder == 2:
            remainder = -1
            remaining = remaining // 3 + 1
        elif remainder == -2:
            remainder = 1
            remaining = remaining // 3 - 1
        else:
            remaining = remaining // 3

        if remainder == -1:
            result.append('T')
        elif remainder == 1:
            result.append('1')
        else:
            result.append('0')

    return ''.join(reversed(result))


def balanced_ternary_to_int(trits: str) -> int:
    """
    将平衡三进制字符串转换为整数

    Args:
        trits: 平衡三进制字符串，使用T、0、1表示

    Returns:
        对应的整数值
    """
    value = 0
    for i, trit in enumerate(reversed(trits)):
        if trit == 'T' or trit == 't':
            digit = -1
        elif trit == '1':
            digit = 1
        elif trit == '0':
            digit = 0
        else:
            raise ValueError(f"无效的三进制字符: {trit}")

        value += digit * (3 ** i)

    return value


def reg_to_trits(reg: int) -> str:
    """
    将寄存器编号转换为3 trit的平衡三进制编码

    Args:
        reg: 寄存器编号（0-8）

    Returns:
        3 trit的平衡三进制编码字符串
    """
    if reg < 0 or reg > 8:
        raise ValueError(f"寄存器编号必须在0-8之间，得到: {reg}")

    # 寄存器编码表（平衡三进制）
    reg_encodings = {
        0: "000",  # R0
        1: "001",  # R1
        2: "01T",  # R2
        3: "010",  # R3
        4: "011",  # R4
        5: "1TT",  # R5
        6: "1T0",  # R6
        7: "1T1",  # R7
        8: "10T",  # R8
    }

    return reg_encodings[reg]


def trits_to_reg(trits: str) -> str:
    """
    将3 trit的平衡三进制编码转换为寄存器名称

    Args:
        trits: 3 trit的平衡三进制编码字符串

    Returns:
        寄存器名称（如"R0"、"R1"等）
    """
    # 编码到寄存器的反向映射
    encoding_to_reg = {
        "000": "R0",
        "001": "R1",
        "01T": "R2",
        "010": "R3",
        "011": "R4",
        "1TT": "R5",
        "1T0": "R6",
        "1T1": "R7",
        "10T": "R8",
    }

    reg = encoding_to_reg.get(trits)
    if reg is None:
        raise ValueError(f"无效的寄存器编码: {trits}")

    return reg


def build_instruction(opcode: str, rd: int, rs1: int, rs2: int = 0, imm: int = 0) -> str:
    """
    构建Trigram-3指令（27 trit）

    指令格式：
    - Opcode(3 trit) | Rd(3 trit) | Rs1(3 trit) | Imm(18 trit)

    对于ADD、CMP、STORE指令，Imm的低3 trit包含Rs2

    Args:
        opcode: 操作码（3 trit字符串）
        rd: 目标寄存器编号（0-8）
        rs1: 源寄存器1编号（0-8）
        rs2: 源寄存器2编号（0-8，可选）
        imm: 立即数（可选）

    Returns:
        27 trit的指令字符串
    """
    # Opcode (3 trit)
    if len(opcode) != 3:
        raise ValueError(f"操作码必须是3 trit，得到: {opcode}")

    # Rd (3 trit)
    rd_trits = reg_to_trits(rd)

    # Rs1 (3 trit)
    rs1_trits = reg_to_trits(rs1)

    # Imm (18 trit)
    # ADD、CMP、STORE指令需要将rs2编码到imm的低3 trit
    if opcode in ['001', '100', '0T0']:  # ADD、CMP、STORE指令
        # 将imm转换为15 trit，然后添加rs2的3 trit
        imm_15 = int_to_balanced_ternary_str(imm, 15)
        rs2_trits = reg_to_trits(rs2)
        imm_str = imm_15 + rs2_trits
    elif opcode in ['01T', '0T1']:  # ABS、NEG指令（单寄存器指令）
        # Imm未使用，全部为0
        imm_str = int_to_balanced_ternary_str(0, 18)
    else:
        # 其他指令: imm全部是立即数
        imm_str = int_to_balanced_ternary_str(imm, 18)

    # 组合所有部分
    instruction = opcode + rd_trits + rs1_trits + imm_str

    if len(instruction) != 27:
        raise ValueError(f"指令长度必须是27 trit，得到: {len(instruction)}")

    return instruction


def parse_instruction(instruction: str) -> dict:
    """
    解析27 trit指令

    Args:
        instruction: 27 trit的指令字符串

    Returns:
        包含解析结果的字典：
        {
            'opcode': str,  # 3 trit
            'rd': str,      # 寄存器名
            'rs1': str,     # 寄存器名
            'rs2': str,     # 寄存器名（如果存在）
            'imm': int      # 立即数
        }
    """
    if len(instruction) != 27:
        raise ValueError(f"指令长度必须是27 trit，得到: {len(instruction)}")

    opcode = instruction[0:3]
    rd = trits_to_reg(instruction[3:6])
    rs1 = trits_to_reg(instruction[6:9])
    imm_trits = instruction[9:27]

    # 解析立即数（包含可能的rs2）
    # 使用三进制切片操作,而非二进制位运算

    # 检查是否包含rs2（低3 trit）
    rs2 = None
    imm = 0
    if opcode in ['001', '100', '0T0']:  # ADD, CMP, STORE
        # 提取低3 trit作为rs2编码
        rs2_trits = imm_trits[-3:]  # 三进制切片
        rs2 = trits_to_reg(rs2_trits)

        # 提取高15 trit作为立即数
        imm_high_trits = imm_trits[:-3]
        imm = balanced_ternary_to_int(imm_high_trits)
    else:
        # 其他指令: 整个18 trit都是立即数
        imm = balanced_ternary_to_int(imm_trits)

    return {
        'opcode': opcode,
        'rd': rd,
        'rs1': rs1,
        'rs2': rs2,
        'imm': imm
    }


if __name__ == "__main__":
    # 测试工具函数
    print("=== 测试平衡三进制转换 ===")
    test_values = [-5, -1, 0, 1, 5, 10]
    for v in test_values:
        trits = int_to_balanced_ternary_str(v, 9)
        back = balanced_ternary_to_int(trits)
        print(f"{v:3d} -> {trits} -> {back:3d}")

    print("\n=== 测试寄存器编码 ===")
    for i in range(9):
        trits = reg_to_trits(i)
        reg_name = trits_to_reg(trits)
        print(f"R{i} -> {trits} -> {reg_name}")

    print("\n=== 测试指令构建 ===")
    instr = build_instruction("001", 1, 2, 3, 0)
    print(f"ADD R1, R2, R3: {instr}")
    parsed = parse_instruction(instr)
    print(f"解析结果: {parsed}")
