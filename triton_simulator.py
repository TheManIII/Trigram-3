#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trigram-3 平衡三进制 CPU 模拟器
基于平衡三进制（Balanced Ternary）的 RISC 架构

作者：TheManIII
版本：1.0
"""

import sys
from typing import List, Tuple, Optional, Dict
from enum import Enum


class Trit(Enum):
    """Trit（爻）- 平衡三进制基本数字单位
    
    英文名称: trit (ternary digit)
    中文名称: 爻（yáo），源自《易经》八卦理论
    """
    NEG = -1  # T (负一)
    ZERO = 0  # 0 (零)
    POS = 1   # 1 (正一)

    def __str__(self):
        if self == Trit.NEG:
            return "T"
        elif self == Trit.POS:
            return "1"
        else:
            return "0"

    @staticmethod
    def from_char(c: str) -> 'Trit':
        """从字符创建Trit"""
        if c == 'T' or c == 't':
            return Trit.NEG
        elif c == '0':
            return Trit.ZERO
        elif c == '1':
            return Trit.POS
        else:
            raise ValueError(f"无效的三进制字符: {c}")


class BalancedTernary:
    """平衡三进制数处理类"""

    def __init__(self, trits: List[Trit] = None, value: int = 0, width: int = 9):
        """
        初始化平衡三进制数

        参数:
            trits: 三进制数字列表（最高位在前）
            value: 整数值（会自动转换为三进制）
            width: 位宽（默认9 trit）
        """
        self.width = width

        if trits is not None:
            # 从trits列表构造
            self.trits = trits[:]
            # 确保位宽正确
            if len(self.trits) < width:
                self.trits = [Trit.ZERO] * (width - len(self.trits)) + self.trits
            elif len(self.trits) > width:
                self.trits = self.trits[-width:]  # 截断低位
        else:
            # 从整数值构造
            self.trits = self._int_to_trits(value, width)

    def _int_to_trits(self, value: int, width: int) -> List[Trit]:
        """将整数转换为平衡三进制（高位在前）"""
        if value == 0:
            return [Trit.ZERO] * width

        trits = []
        n = value

        # 先生成低位在前的trits
        for _ in range(width):
            remainder = n % 3
            if remainder > 1:
                remainder -= 3
                n += 1
            elif remainder < -1:
                remainder += 3
                n -= 1

            if remainder == -1:
                trits.append(Trit.NEG)
            elif remainder == 1:
                trits.append(Trit.POS)
            else:
                trits.append(Trit.ZERO)

            n = n // 3

        # 反转,使高位在前
        return list(reversed(trits))

    def to_int(self) -> int:
        """转换为整数值"""
        value = 0
        power = 1
        for trit in reversed(self.trits):
            value += trit.value * power
            power *= 3
        return value

    def to_string(self) -> str:
        """转换为三进制字符串"""
        return ''.join(str(t) for t in self.trits)

    def __add__(self, other: 'BalancedTernary') -> 'BalancedTernary':
        """加法"""
        return BalancedTernary(value=self.to_int() + other.to_int(), width=self.width)

    def __sub__(self, other: 'BalancedTernary') -> 'BalancedTernary':
        """减法"""
        return BalancedTernary(value=self.to_int() - other.to_int(), width=self.width)

    def __neg__(self) -> 'BalancedTernary':
        """取反"""
        return BalancedTernary(value=-self.to_int(), width=self.width)

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return f"BalancedTernary('{self.to_string()}' = {self.to_int()})"

    def copy(self) -> 'BalancedTernary':
        """深拷贝"""
        return BalancedTernary(trits=self.trits.copy(), width=self.width)


class RegisterFile:
    """寄存器堆（9个逻辑寄存器R0-R8）"""

    def __init__(self):
        self.registers = [BalancedTernary(width=9) for _ in range(9)]
        # R0硬连线为0
        self.registers[0] = BalancedTernary(value=0, width=9)

    def read(self, reg_num: int) -> BalancedTernary:
        """读取寄存器"""
        if reg_num < 0 or reg_num > 8:
            raise ValueError(f"无效的寄存器编号: {reg_num}")
        return self.registers[reg_num].copy()

    def write(self, reg_num: int, value: BalancedTernary):
        """写入寄存器"""
        if reg_num < 0 or reg_num > 8:
            raise ValueError(f"无效的寄存器编号: {reg_num}")

        if reg_num == 0:
            # R0硬连线为0，写入忽略
            return

        self.registers[reg_num] = value.copy()

    def reset(self):
        """重置所有寄存器"""
        for i in range(9):
            self.registers[i] = BalancedTernary(width=9)
        self.registers[0] = BalancedTernary(value=0, width=9)

    def __str__(self):
        lines = []
        for i in range(9):
            val = self.registers[i]
            lines.append(f"R{i}: {val.to_string():9s} ({val.to_int():6d})")
        return '\n'.join(lines)


class Memory:
    """内存系统（包含I/O映射）"""

    # 特殊地址
    OUTPUT_PORT = -9841  # 输出端口
    INPUT_PORT = -9840   # 输入端口
    MIN_ADDR = -9841
    MAX_ADDR = 9841
    SIZE = 19683  # 3^9

    def __init__(self):
        # 物理内存：逻辑地址+9841映射到物理地址
        self.memory = [BalancedTernary(width=9) for _ in range(self.SIZE)]

    def logical_to_physical(self, logical_addr: int) -> int:
        """逻辑地址转物理地址"""
        if logical_addr < self.MIN_ADDR or logical_addr > self.MAX_ADDR:
            raise ValueError(f"地址越界: {logical_addr}")
        return logical_addr + 9841

    def read(self, logical_addr: int) -> BalancedTernary:
        """从内存读取（支持I/O）"""
        if logical_addr == self.INPUT_PORT:
            # 输入端口
            try:
                input_str = input("INPUT> ")
                # 尝试解析为三进制或十进制
                if 'T' in input_str.upper() or 't' in input_str:
                    # 三进制输入
                    trits = [Trit.from_char(c) for c in input_str.upper()]
                    return BalancedTernary(trits=trits, width=9)
                else:
                    # 十进制输入
                    return BalancedTernary(value=int(input_str), width=9)
            except (ValueError, EOFError):
                # 输入错误，返回0
                print("[警告] 输入错误，使用0")
                return BalancedTernary(value=0, width=9)

        physical_addr = self.logical_to_physical(logical_addr)
        return self.memory[physical_addr].copy()

    def write(self, logical_addr: int, value: BalancedTernary):
        """写入内存（支持I/O）"""
        if logical_addr == self.OUTPUT_PORT:
            # 输出端口
            print(f"[OUTPUT] {value.to_string():9s} ({value.to_int():6d})")
            return

        physical_addr = self.logical_to_physical(logical_addr)
        self.memory[physical_addr] = value.copy()

    def load_program(self, instructions: List[str], start_addr: int = 0):
        """加载程序到内存

        参数:
            instructions: 指令列表（每条指令为27 trit的字符串）
            start_addr: 起始逻辑地址（必须3字对齐）

        注意:
            指令格式中所有字段都使用平衡三进制(T,0,1)
            寄存器编码: R0=000, R1=001, R2=01T, ..., R8=10T
        """
        if start_addr % 3 != 0:
            raise ValueError(f"程序起始地址必须3字对齐: {start_addr}")

        for i, inst_str in enumerate(instructions):
            addr = start_addr + i * 3

            if len(inst_str) != 27:
                raise ValueError(f"指令长度错误: 期望27 trit, 实际{len(inst_str)}")

            # 解析指令字段
            # 格式: opcode(3) + rd(3) + rs1(3) + imm(18)
            opcode = inst_str[0:3]
            rd = inst_str[3:6]
            rs1 = inst_str[6:9]
            imm = inst_str[9:27]

            # 将27 trit指令分成3个9 trit字
            # word0: opcode + rd + rs1 (所有字段都使用平衡三进制)
            # word1: imm高9 trit (使用平衡三进制)
            # word2: imm低9 trit (使用平衡三进制)

            # word0: 所有字段都使用平衡三进制
            word0_trits = []
            for c in opcode + rd + rs1:
                if c in ['T', 't']:
                    word0_trits.append(Trit.NEG)
                elif c == '0':
                    word0_trits.append(Trit.ZERO)
                elif c == '1':
                    word0_trits.append(Trit.POS)
                else:
                    raise ValueError(f"无效的字符: {c}")

            # word1和word2: 立即数使用平衡三进制
            word1_str = imm[0:9]
            word2_str = imm[9:18]

            word1_trits = [Trit.from_char(c) for c in word1_str]

            # word2的低3 trit可能是rs2编码(使用平衡三进制)
            word2_trits = []
            for i, c in enumerate(word2_str):
                if i >= 6 and opcode in ['001', '100', '0T0']:
                    # 低3 trit是rs2编码,使用平衡三进制
                    if c in ['T', 't']:
                        word2_trits.append(Trit.NEG)
                    elif c == '0':
                        word2_trits.append(Trit.ZERO)
                    elif c == '1':
                        word2_trits.append(Trit.POS)
                    elif c == '2':
                        word2_trits.append(Trit.NEG)
                    else:
                        raise ValueError(f"无效的字符: {c}")
                else:
                    # 其他部分是立即数,使用平衡三进制
                    word2_trits.append(Trit.from_char(c))

            # 写入内存
            self.write(addr, BalancedTernary(trits=word0_trits, width=9))
            self.write(addr + 1, BalancedTernary(trits=word1_trits, width=9))
            self.write(addr + 2, BalancedTernary(trits=word2_trits, width=9))

    def reset(self):
        """清空内存"""
        self.memory = [BalancedTernary(width=9) for _ in range(self.SIZE)]

    def dump(self, start_addr: int, count: int = 10):
        """转储内存内容"""
        lines = []
        for i in range(count):
            addr = start_addr + i
            try:
                value = self.read(addr)
                lines.append(f"MEM[{addr:6d}]: {value.to_string():9s} ({value.to_int():6d})")
            except ValueError:
                break
        return '\n'.join(lines)


class InstructionDecoder:
    """指令译码器"""

    # 操作码定义
    OPCODE_HALT = [Trit.ZERO, Trit.ZERO, Trit.ZERO]      # 000 - 停机
    OPCODE_ADD = [Trit.ZERO, Trit.ZERO, Trit.POS]        # 001 - 加法
    OPCODE_OFFSET = [Trit.ZERO, Trit.ZERO, Trit.NEG]     # 00T - 偏移
    OPCODE_LOAD = [Trit.ZERO, Trit.POS, Trit.ZERO]       # 010 - 读存
    OPCODE_STORE = [Trit.ZERO, Trit.NEG, Trit.ZERO]      # 0T0 - 写存
    OPCODE_CMP = [Trit.POS, Trit.ZERO, Trit.ZERO]        # 100 - 比较
    OPCODE_TJUMP = [Trit.NEG, Trit.ZERO, Trit.ZERO]      # T00 - 三分跳
    OPCODE_ABS = [Trit.ZERO, Trit.POS, Trit.NEG]         # 01T - 绝对值
    OPCODE_NEG = [Trit.ZERO, Trit.NEG, Trit.POS]         # 0T1 - 取负

    OPCODE_NAMES = {
        '000': 'HALT  (停机)',
        '001': 'ADD   (加法)',
        '00T': 'OFFSET(偏移)',
        '010': 'LOAD  (读存)',
        '0T0': 'STORE (写存)',
        '100': 'CMP   (比较)',
        'T00': 'TJUMP (三分跳)',
        '01T': 'ABS   (绝对值)',
        '0T1': 'NEG   (取负)',
    }

    def __init__(self):
        pass

    def decode(self, word0: BalancedTernary, word1: BalancedTernary,
               word2: BalancedTernary) -> Tuple[str, int, int, int, BalancedTernary]:
        """
        译码指令

        参数:
            word0: 第一个字（包含opcode, rd, rs1）
            word1: 第二个字（imm高9 trit）
            word2: 第三个字（imm低9 trit）

        返回:
            (opcode_str, rd, rs1, rs2, imm)
        """
        # 提取字段
        opcode_trits = word0.trits[0:3]
        rd_trits = word0.trits[3:6]
        rs1_trits = word0.trits[6:9]

        # 转换为索引
        opcode_str = ''.join(str(t) for t in opcode_trits)
        rd = self._trit_to_int(rd_trits)
        rs1 = self._trit_to_int(rs1_trits)

        # 立即数（18 trit）
        imm_trits = word1.trits + word2.trits
        imm = BalancedTernary(trits=imm_trits, width=18)

        # rs2从imm低3 trit提取（用于ADD指令）
        rs2_trits = word2.trits[6:9]
        rs2 = self._trit_to_int(rs2_trits)

        return opcode_str, rd, rs1, rs2, imm

    def _trit_to_int(self, trits: List[Trit]) -> int:
        """将3 trit转换为寄存器索引（0-8）

        寄存器编码使用平衡三进制(T,0,1)
        Trit.NEG = -1, Trit.ZERO = 0, Trit.POS = 1
        """
        value = 0
        power = 1
        for trit in reversed(trits):
            digit = trit.value  # T=-1, 0=0, 1=1
            value += digit * power
            power *= 3
        return value

    def is_valid_opcode(self, opcode_str: str) -> bool:
        """检查操作码是否有效"""
        return opcode_str in self.OPCODE_NAMES


class CPU:
    """Trigram-3 CPU核心"""

    def __init__(self):
        self.pc = BalancedTernary(value=0, width=9)  # 程序计数器
        self.registers = RegisterFile()
        self.memory = Memory()
        self.decoder = InstructionDecoder()
        self.running = False
        self.halted = False
        self.cycle_count = 0
        self.verbose = False
        self.debug_mode = False

    def reset(self):
        """重置CPU"""
        self.pc = BalancedTernary(value=0, width=9)
        self.registers.reset()
        self.memory.reset()
        self.halted = False
        self.running = False
        self.cycle_count = 0

    def load_program(self, instructions: List[str], start_addr: int = 0):
        """加载程序"""
        self.memory.load_program(instructions, start_addr)
        self.pc = BalancedTernary(value=start_addr, width=9)

    def fetch(self) -> Tuple[BalancedTernary, BalancedTernary, BalancedTernary]:
        """取指（读取3个字）"""
        addr = self.pc.to_int()

        # 检查地址对齐
        if addr % 3 != 0:
            self.halt(f"地址未对齐: PC={addr}")
            return None, None, None

        word0 = self.memory.read(addr)
        word1 = self.memory.read(addr + 1)
        word2 = self.memory.read(addr + 2)

        return word0, word1, word2

    def decode(self, word0: BalancedTernary, word1: BalancedTernary,
               word2: BalancedTernary) -> Tuple[str, int, int, int, BalancedTernary]:
        """译码"""
        return self.decoder.decode(word0, word1, word2)

    def execute(self, opcode: str, rd: int, rs1: int, rs2: int, imm: BalancedTernary):
        """执行指令"""
        if opcode == '000':  # HALT
            self.halt("执行HALT指令")

        elif opcode == '001':  # ADD
            val1 = self.registers.read(rs1)
            val2 = self.registers.read(rs2)
            result = val1 + val2
            self.registers.write(rd, result)

        elif opcode == '00T':  # OFFSET
            val1 = self.registers.read(rs1)
            # 使用imm的低9 trit
            imm9 = BalancedTernary(trits=imm.trits[-9:], width=9)
            result = val1 + imm9
            self.registers.write(rd, result)

        elif opcode == '010':  # LOAD
            base = self.registers.read(rs1)
            # 使用imm的低9 trit作为偏移
            offset = BalancedTernary(trits=imm.trits[-9:], width=9)
            addr = base.to_int() + offset.to_int()
            value = self.memory.read(addr)
            self.registers.write(rd, value)

        elif opcode == '0T0':  # STORE
            base = self.registers.read(rs1)
            # 使用imm的高15 trit作为偏移(低3 trit是rs2)
            offset = BalancedTernary(trits=imm.trits[0:15], width=15)
            # 取偏移的低9 trit
            offset9 = BalancedTernary(trits=offset.trits[-9:], width=9)
            addr = base.to_int() + offset9.to_int()
            val2 = self.registers.read(rs2)
            if self.verbose:
                print(f"    STORE: base={base.to_int()}, offset={offset9.to_int()}, addr={addr}, val={val2.to_int()}")
            self.memory.write(addr, val2)

        elif opcode == '01T':  # ABS
            val1 = self.registers.read(rs1)
            # 计算绝对值
            int_val = val1.to_int()
            abs_val = abs(int_val)
            result = BalancedTernary(value=abs_val, width=9)
            self.registers.write(rd, result)

        elif opcode == '0T1':  # NEG
            val1 = self.registers.read(rs1)
            # 取负
            result = -val1
            self.registers.write(rd, result)

        elif opcode == '100':  # CMP
            val1 = self.registers.read(rs1)
            val2 = self.registers.read(rs2)
            diff = val1.to_int() - val2.to_int()
            # 设置标志：T(负), 0(零), 1(正)
            if diff < 0:
                flag = BalancedTernary(value=-1, width=9)
            elif diff > 0:
                flag = BalancedTernary(value=1, width=9)
            else:
                flag = BalancedTernary(value=0, width=9)
            self.registers.write(rd, flag)

        elif opcode == 'T00':  # TJUMP
            flag = self.registers.read(rd)
            flag_val = flag.to_int()

            # 计算跳转目标
            # Imm分为3×5 trit: [off_T][off_0][off_1]
            # 偏移单位为1条指令(3个字)
            if flag_val == -1:  # 负数分支
                offset_trits = imm.trits[0:5]
            elif flag_val == 0:  # 零分支
                offset_trits = imm.trits[5:10]
            else:  # 正数分支
                offset_trits = imm.trits[10:15]

            # 将5 trit转换为9 trit(保持符号)
            offset = BalancedTernary(trits=offset_trits, width=9)

            # 跳转（offset是相对偏移，单位为条指令）
            new_pc = self.pc.to_int() + offset.to_int() * 3
            self.pc = BalancedTernary(value=new_pc, width=9)

        else:
            self.halt(f"非法操作码: {opcode}")

    def step(self) -> bool:
        """执行一步（取指-译码-执行）"""
        if self.halted:
            return False

        # 取指
        word0, word1, word2 = self.fetch()
        if word0 is None:
            return False

        # 译码
        opcode, rd, rs1, rs2, imm = self.decode(word0, word1, word2)

        if not self.decoder.is_valid_opcode(opcode):
            self.halt(f"非法操作码: {opcode}")
            return False

        # 打印当前指令
        if self.verbose:
            self._print_instruction(opcode, rd, rs1, rs2, imm)

        # 执行
        self.execute(opcode, rd, rs1, rs2, imm)

        # 更新PC（TJUMP指令内部已经更新）
        if opcode != 'T00' and not self.halted:
            new_pc = self.pc.to_int() + 3
            self.pc = BalancedTernary(value=new_pc, width=9)

        self.cycle_count += 1

        # 调试模式：每步暂停
        if self.debug_mode:
            input("按Enter继续...")

        return not self.halted

    def run(self):
        """运行程序"""
        self.running = True
        self.halted = False

        if self.verbose:
            print("\n" + "="*60)
            print("程序开始执行")
            print("="*60)

        while self.running and not self.halted:
            if not self.step():
                break

        if self.verbose:
            print("\n" + "="*60)
            print(f"程序执行结束 (周期数: {self.cycle_count})")
            print("="*60)

    def halt(self, reason: str = ""):
        """停机"""
        self.halted = True
        self.running = False
        if reason:
            print(f"\n[HALT] {reason}")

    def _print_instruction(self, opcode: str, rd: int, rs1: int, rs2: int, imm: BalancedTernary):
        """打印当前指令"""
        pc = self.pc.to_int()
        opcode_name = self.decoder.OPCODE_NAMES.get(opcode, f"??? ({opcode})")

        print(f"\n周期 {self.cycle_count}: PC={pc:6d}")
        print(f"指令: {opcode_name}")
        print(f"  Rd=R{rd}, Rs1=R{rs1}, Rs2=R{rs2}")
        print(f"  Imm={imm.to_string():18s} ({imm.to_int():12d})")

    def print_state(self):
        """打印CPU状态"""
        print("\n" + "="*60)
        print("CPU状态")
        print("="*60)
        print(f"PC: {self.pc.to_string():9s} ({self.pc.to_int():6d})")
        print(f"周期数: {self.cycle_count}")
        print(f"状态: {'运行中' if self.running else ('已停机' if self.halted else '就绪')}")
        print("\n寄存器:")
        print(self.registers)


class Debugger:
    """调试器"""

    def __init__(self, cpu: CPU):
        self.cpu = cpu
        self.breakpoints = set()

    def add_breakpoint(self, addr: int):
        """添加断点"""
        self.breakpoints.add(addr)
        print(f"[断点] 地址 {addr}")

    def remove_breakpoint(self, addr: int):
        """移除断点"""
        if addr in self.breakpoints:
            self.breakpoints.remove(addr)
            print(f"[断点] 移除地址 {addr}")

    def clear_breakpoints(self):
        """清空断点"""
        self.breakpoints.clear()
        print("[断点] 清空所有断点")

    def interactive(self):
        """交互式调试"""
        print("\n" + "="*60)
        print("Triton调试器")
        print("="*60)
        print("命令:")
        print("  r - 运行")
        print("  s - 单步")
        print("  t - 显示状态")
        print("  m <addr> [count] - 显示内存")
        print("  b <addr> - 添加断点")
        print("  c <addr> - 清除断点")
        print("  q - 退出")
        print("="*60)

        while True:
            try:
                cmd = input("\n调试> ").strip().split()
                if not cmd:
                    continue

                if cmd[0] == 'r':  # 运行
                    self.cpu.running = True
                    self.cpu.verbose = False
                    while self.cpu.running and not self.cpu.halted:
                        pc = self.cpu.pc.to_int()
                        if pc in self.breakpoints:
                            print(f"\n[断点] 命中地址 {pc}")
                            self.cpu.print_state()
                            break
                        self.cpu.step()
                    self.cpu.print_state()

                elif cmd[0] == 's':  # 单步
                    self.cpu.verbose = True
                    self.cpu.step()
                    self.cpu.print_state()

                elif cmd[0] == 't':  # 显示状态
                    self.cpu.print_state()

                elif cmd[0] == 'm':  # 显示内存
                    if len(cmd) < 2:
                        print("用法: m <addr> [count]")
                        continue
                    addr = int(cmd[1])
                    count = int(cmd[2]) if len(cmd) > 2 else 10
                    print(self.cpu.memory.dump(addr, count))

                elif cmd[0] == 'b':  # 添加断点
                    if len(cmd) < 2:
                        print("用法: b <addr>")
                        continue
                    self.add_breakpoint(int(cmd[1]))

                elif cmd[0] == 'c':  # 清除断点
                    if len(cmd) < 2:
                        print("用法: c <addr>")
                        continue
                    self.remove_breakpoint(int(cmd[1]))

                elif cmd[0] == 'q':  # 退出
                    break

                else:
                    print(f"未知命令: {cmd[0]}")

            except KeyboardInterrupt:
                print("\n[中断]")
                break
            except Exception as e:
                print(f"[错误] {e}")


class Simulator:
    """Trigram-3 模拟器主程序"""

    def __init__(self):
        self.cpu = CPU()

    def load_from_file(self, filename: str, start_addr: int = 0):
        """从文件加载程序"""
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        instructions = []
        for line in lines:
            line = line.strip()
            # 跳过空行和注释
            if not line or line.startswith('#'):
                continue
            instructions.append(line)

        self.cpu.load_program(instructions, start_addr)
        print(f"[加载] 从 {filename} 加载 {len(instructions)} 条指令")

    def run(self, verbose: bool = False, debug: bool = False):
        """运行模拟器"""
        self.cpu.verbose = verbose
        self.cpu.debug_mode = debug

        if debug:
            debugger = Debugger(self.cpu)
            debugger.interactive()
        else:
            self.cpu.run()
            self.cpu.print_state()


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='Trigram-3 平衡三进制CPU模拟器')
    parser.add_argument('program', nargs='?', help='程序文件')
    parser.add_argument('-v', '--verbose', action='store_true', help='详细输出')
    parser.add_argument('-d', '--debug', action='store_true', help='调试模式')
    parser.add_argument('-t', '--test', action='store_true', help='运行测试程序')

    args = parser.parse_args()

    sim = Simulator()

    if args.test:
        # 运行内置测试程序
        print("\n运行测试程序...")
        run_test_programs(sim)
        return

    if args.program:
        # 从文件加载程序
        sim.load_from_file(args.program)
        sim.run(verbose=args.verbose, debug=args.debug)
    else:
        # 交互模式
        print("\nTrigram-3 平衡三进制CPU模拟器")
        print("使用 -h 查看帮助")
        print("使用 -t 运行测试程序")


def run_test_programs(sim: Simulator):
    """运行测试程序"""

    # 辅助函数：将整数转换为平衡三进制字符串
    def int_to_balanced_ternary_str(value: int, width: int = 9) -> str:
        """将整数转换为平衡三进制字符串"""
        if value == 0:
            return '0' * width

        n = value
        trits = []
        for _ in range(width):
            remainder = n % 3
            if remainder > 1:
                remainder -= 3
                n += 1
            elif remainder < -1:
                remainder += 3
                n -= 1

            if remainder == -1:
                trits.append('T')
            elif remainder == 1:
                trits.append('1')
            else:
                trits.append('0')

            n = n // 3

        return ''.join(reversed(trits))

    # 辅助函数：将寄存器号转换为3 trit编码（使用平衡三进制 T,0,1）
    def reg_to_trits(reg: int) -> str:
        """将寄存器号转换为3 trit编码（使用平衡三进制）"""
        if reg < 0 or reg > 8:
            raise ValueError(f"无效的寄存器号: {reg}")

        # 转换为平衡三进制（T,0,1）
        # 使用BalancedTernary类来正确转换
        bt = BalancedTernary(value=reg, width=3)
        return bt.to_string()

    # 辅助函数：构建指令
    def build_instruction(opcode: str, rd: int, rs1: int, rs2: int = 0, imm: int = 0) -> str:
        """构建27 trit指令

        格式: opcode(3) + rd(3) + rs1(3) + imm(18)
        imm的低3 trit用于rs2（ADD、CMP、STORE指令）

        注意:
        - ADD指令(001): imm的低3 trit包含rs2
        - CMP指令(100): imm的低3 trit包含rs2
        - STORE指令(0T0): imm的高15 trit是偏移,低3 trit是rs2
        - 其他指令: imm全部是立即数
        """
        opcode_trits = opcode
        rd_trits = reg_to_trits(rd)
        rs1_trits = reg_to_trits(rs1)

        # 立即数（18 trit）
        # ADD、CMP、STORE指令需要将rs2编码到imm的低3 trit
        if opcode in ['001', '100', '0T0']:  # ADD、CMP、STORE指令
            # 将imm转换为15 trit,然后添加rs2的3 trit
            imm_15 = int_to_balanced_ternary_str(imm, width=15)
            rs2_trits = reg_to_trits(rs2)
            imm_str = imm_15 + rs2_trits
        else:
            # 其他指令: imm全部是立即数
            imm_str = int_to_balanced_ternary_str(imm, width=18)

        return opcode_trits + rd_trits + rs1_trits + imm_str

    # 测试1: 加法运算
    print("\n" + "="*60)
    print("测试1: 加法运算")
    print("="*60)

    # ADD R1, R2, R3  (R1 = R2 + R3)
    # 先设置 R2 = 5, R3 = 3
    instructions = [
        # OFFSET R2, R0, imm=5  (R2 = 5)
        build_instruction('00T', 2, 0, imm=5),
        # OFFSET R3, R0, imm=3  (R3 = 3)
        build_instruction('00T', 3, 0, imm=3),
        # ADD R1, R2, R3  (R1 = R2 + R3)
        build_instruction('001', 1, 2, rs2=3),
        # STORE R1, [R0+0]
        build_instruction('0T0', 1, 0, rs2=0, imm=0),
        # HALT
        "000000000000000000000000000",
    ]

    sim.cpu.reset()
    sim.cpu.load_program(instructions)
    sim.cpu.verbose = True
    sim.cpu.run()

    print("\n预期: R1 = 8, MEM[0] = 8")

    # 测试2: 比较和分支
    print("\n" + "="*60)
    print("测试2: 比较和分支")
    print("="*60)

    # CMP R1, R2, R3
    # TJUMP R1, branch_neg, branch_zero, branch_pos
    instructions = [
        # OFFSET R2, R0, imm=5
        build_instruction('00T', 2, 0, imm=5),
        # OFFSET R3, R0, imm=3
        build_instruction('00T', 3, 0, imm=3),
        # CMP R1, R2, R3  (R1 = sign(5-3) = 1)
        build_instruction('100', 1, 2, rs2=3),
        # TJUMP R1, branch_neg(-3), branch_zero(0), branch_pos(3)
        # 正数分支，跳转到+3条指令（地址12）
        build_instruction('T00', 1, 0, imm=3),
        # 负数分支（不会执行）
        build_instruction('00T', 4, 0, imm=10),
        # 零分支（不会执行）
        build_instruction('00T', 4, 0, imm=20),
        # 正数分支（会执行）
        build_instruction('00T', 4, 0, imm=30),
        # STORE R4, [R1+1]
        build_instruction('0T0', 4, 1, rs2=0, imm=1),
        # HALT
        "000000000000000000000000000",
    ]

    sim.cpu.reset()
    sim.cpu.load_program(instructions)
    sim.cpu.verbose = True
    sim.cpu.run()

    print("\n预期: R1 = 1, R4 = 30, MEM[2] = 30")

    # 测试3: 循环
    print("\n" + "="*60)
    print("测试3: 循环累加")
    print("="*60)

    # 计算 1+2+3+4+5 = 15
    instructions = [
        # 初始化: R1=0 (累加器), R2=1 (计数器), R3=5 (上限)
        build_instruction('00T', 1, 0, imm=0),
        build_instruction('00T', 2, 0, imm=1),
        build_instruction('00T', 3, 0, imm=5),

        # 循环开始: CMP R4, R2, R3
        build_instruction('100', 4, 2, rs2=3),

        # TJUMP R4, exit(0), loop_body(3), loop_body(3)
        # 如果R4=0（R2=R3），跳转到exit
        # 如果R4=1（R2<R3），跳转到loop_body
        # 如果R4=T（R2>R3），跳转到loop_body
        build_instruction('T00', 4, 0, imm=3),

        # 退出: STORE R1, [0] + HALT
        build_instruction('0T0', 1, 0, imm=0),
        "000000000000000000000000000",

        # 循环体: R1 += R2, R2 += 1, 跳转回循环开始
        build_instruction('001', 1, 1, rs2=2),
        build_instruction('00T', 2, 0, imm=1),
        # 跳转回循环开始（-5条指令 = -15地址 = -5字）
        build_instruction('00T', 0, 0, imm=-5),
    ]

    sim.cpu.reset()
    sim.cpu.load_program(instructions)
    sim.cpu.verbose = True
    sim.cpu.run()

    print("\n预期: R1 = 15, MEM[0] = 15")


if __name__ == '__main__':
    main()
