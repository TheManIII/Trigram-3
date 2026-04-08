#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trigram-3 三进制逻辑门和算术单元
实现真正的三进制运算逻辑,而非二进制模拟

作者：TheManIII
版本：1.0
"""

from enum import Enum
from typing import Tuple, List


class Trit(Enum):
    """Trit（爻）- 平衡三进制基本数字单位
    
    英文名称: trit (ternary digit)
    中文名称: 爻（yáo），源自《易经》八卦理论
    
    物理表示（建议）:
    - T (NEG): -V  (负电压)
    - 0 (ZERO): 0V  (零电压)
    - 1 (POS): +V  (正电压)
    """
    NEG = -1   # T (负一)
    ZERO = 0   # 0 (零)
    POS = 1    # 1 (正一)
    
    def __str__(self):
        if self == Trit.NEG:
            return "T"
        elif self == Trit.POS:
            return "1"
        else:
            return "0"
    
    @staticmethod
    def from_int(value: int) -> 'Trit':
        """从整数创建Trit"""
        if value == -1:
            return Trit.NEG
        elif value == 0:
            return Trit.ZERO
        elif value == 1:
            return Trit.POS
        else:
            raise ValueError(f"无效的三进制值: {value}")
    
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


# ============================================================================
# 一、三进制逻辑门
# ============================================================================

class TernaryLogic:
    """三进制逻辑门
    
    基于平衡三进制的基本逻辑运算
    这些是构建三进制 CPU 的基础组件
    """
    
    # -------------------------------------------------------------------------
    # 1.1 单输入逻辑门
    # -------------------------------------------------------------------------
    
    @staticmethod
    def NOT(a: Trit) -> Trit:
        """反相器（Inverter）
        
        功能: 取反
        真值表:
            T → 1
            0 → 0
            1 → T
        
        物理实现: 电压反相器
        """
        if a == Trit.NEG:
            return Trit.POS
        elif a == Trit.ZERO:
            return Trit.ZERO
        else:  # POS
            return Trit.NEG
    
    @staticmethod
    def CL(a: Trit) -> Trit:
        """循环左移（Cycle Left）
        
        功能: 循环左移
        真值表:
            T → 0
            0 → 1
            1 → T
        
        物理实现: 相位旋转器
        """
        if a == Trit.NEG:
            return Trit.ZERO
        elif a == Trit.ZERO:
            return Trit.POS
        else:  # POS
            return Trit.NEG
    
    @staticmethod
    def CR(a: Trit) -> Trit:
        """循环右移（Cycle Right）
        
        功能: 循环右移
        真值表:
            T → 1
            0 → T
            1 → 0
        
        物理实现: 相位旋转器
        """
        if a == Trit.NEG:
            return Trit.POS
        elif a == Trit.ZERO:
            return Trit.NEG
        else:  # POS
            return Trit.ZERO
    
    @staticmethod
    def POS_CLAMP(a: Trit) -> Trit:
        """正钳位（Positive Clamp）
        
        功能: 将负值钳位到0
        真值表:
            T → 0
            0 → 0
            1 → 1
        """
        if a == Trit.POS:
            return Trit.POS
        else:
            return Trit.ZERO
    
    @staticmethod
    def NEG_CLAMP(a: Trit) -> Trit:
        """负钳位（Negative Clamp）
        
        功能: 将正值钳位到0
        真值表:
            T → T
            0 → 0
            1 → 0
        """
        if a == Trit.NEG:
            return Trit.NEG
        else:
            return Trit.ZERO
    
    # -------------------------------------------------------------------------
    # 1.2 双输入逻辑门
    # -------------------------------------------------------------------------
    
    @staticmethod
    def MIN(a: Trit, b: Trit) -> Trit:
        """最小值门（Minimum）
        
        功能: 返回两个输入的最小值
        真值表:
            MIN(T, T) = T
            MIN(T, 0) = T
            MIN(T, 1) = T
            MIN(0, T) = T
            MIN(0, 0) = 0
            MIN(0, 1) = 0
            MIN(1, T) = T
            MIN(1, 0) = 0
            MIN(1, 1) = 1
        
        物理实现: 电压最小值电路
        """
        order = {Trit.NEG: -1, Trit.ZERO: 0, Trit.POS: 1}
        return a if order[a] <= order[b] else b
    
    @staticmethod
    def MAX(a: Trit, b: Trit) -> Trit:
        """最大值门（Maximum）
        
        功能: 返回两个输入的最大值
        真值表:
            MAX(T, T) = T
            MAX(T, 0) = 0
            MAX(T, 1) = 1
            MAX(0, T) = 0
            MAX(0, 0) = 0
            MAX(0, 1) = 1
            MAX(1, T) = 1
            MAX(1, 0) = 1
            MAX(1, 1) = 1
        
        物理实现: 电压最大值电路
        """
        order = {Trit.NEG: -1, Trit.ZERO: 0, Trit.POS: 1}
        return a if order[a] >= order[b] else b
    
    @staticmethod
    def CONS(a: Trit, b: Trit) -> Trit:
        """一致门（Consensus）
        
        功能: 如果两个输入相同则输出该值,否则输出0
        真值表:
            CONS(T, T) = T
            CONS(T, 0) = 0
            CONS(T, 1) = 0
            CONS(0, T) = 0
            CONS(0, 0) = 0
            CONS(0, 1) = 0
            CONS(1, T) = 0
            CONS(1, 0) = 0
            CONS(1, 1) = 1
        """
        if a == b:
            return a
        else:
            return Trit.ZERO
    
    @staticmethod
    def ANY(a: Trit, b: Trit) -> Trit:
        """任意门（Any）
        
        功能: 如果任一输入非0则输出1,否则输出0
        用于检测非零值
        """
        if a != Trit.ZERO or b != Trit.ZERO:
            return Trit.POS
        else:
            return Trit.ZERO


# ============================================================================
# 二、三进制算术单元
# ============================================================================

class TernaryArithmetic:
    """三进制算术单元
    
    实现真正的三进制加减法运算
    使用三进制逻辑门构建,而非十进制转换
    """
    
    # -------------------------------------------------------------------------
    # 2.1 基础算术单元
    # -------------------------------------------------------------------------
    
    @staticmethod
    def half_adder(a: Trit, b: Trit) -> Tuple[Trit, Trit]:
        """三进制半加器
        
        输入: a, b (各1 trit)
        输出: (sum, carry)
        
        真值表:
            a  b  | sum carry
            T  T  |  1   T
            T  0  |  T   0
            T  1  |  0   0
            0  T  |  T   0
            0  0  |  0   0
            0  1  |  1   0
            1  T  |  0   0
            1  0  |  1   0
            1  1  |  T   1
        
        物理实现: 用三进制逻辑门构建
        """
        # 使用真值表实现
        table = {
            (Trit.NEG, Trit.NEG): (Trit.POS, Trit.NEG),
            (Trit.NEG, Trit.ZERO): (Trit.NEG, Trit.ZERO),
            (Trit.NEG, Trit.POS): (Trit.ZERO, Trit.ZERO),
            (Trit.ZERO, Trit.NEG): (Trit.NEG, Trit.ZERO),
            (Trit.ZERO, Trit.ZERO): (Trit.ZERO, Trit.ZERO),
            (Trit.ZERO, Trit.POS): (Trit.POS, Trit.ZERO),
            (Trit.POS, Trit.NEG): (Trit.ZERO, Trit.ZERO),
            (Trit.POS, Trit.ZERO): (Trit.POS, Trit.ZERO),
            (Trit.POS, Trit.POS): (Trit.NEG, Trit.POS),
        }
        return table[(a, b)]
    
    @staticmethod
    def full_adder(a: Trit, b: Trit, carry_in: Trit) -> Tuple[Trit, Trit]:
        """三进制全加器

        输入: a, b, carry_in (各1 trit)
        输出: (sum, carry_out)

        实现: 两个半加器级联,进位需要相加
        """
        # 第一级: a + b
        sum1, carry1 = TernaryArithmetic.half_adder(a, b)

        # 第二级: sum1 + carry_in
        sum2, carry2 = TernaryArithmetic.half_adder(sum1, carry_in)

        # 进位合并: carry_out = carry1 + carry2
        carry_out, _ = TernaryArithmetic.half_adder(carry1, carry2)

        return (sum2, carry_out)
    
    # -------------------------------------------------------------------------
    # 2.2 多位算术单元
    # -------------------------------------------------------------------------
    
    @staticmethod
    def add_trits(a: List[Trit], b: List[Trit]) -> Tuple[List[Trit], Trit]:
        """多位三进制加法
        
        输入: a, b (trit列表,低位在前)
        输出: (sum, overflow)
        
        注意: 使用全加器级联,真正的三进制运算
        """
        if len(a) != len(b):
            raise ValueError("两个操作数长度必须相同")
        
        width = len(a)
        result = []
        carry = Trit.ZERO
        
        # 从低位到高位逐位相加
        for i in range(width):
            sum_trit, carry = TernaryArithmetic.full_adder(a[i], b[i], carry)
            result.append(sum_trit)
        
        # 返回结果和溢出标志
        return (result, carry)
    
    @staticmethod
    def negate_trits(a: List[Trit]) -> List[Trit]:
        """多位三进制取负
        
        输入: a (trit列表)
        输出: -a (trit列表)
        
        实现: 每位取反
        """
        return [TernaryLogic.NOT(trit) for trit in a]
    
    @staticmethod
    def subtract_trits(a: List[Trit], b: List[Trit]) -> Tuple[List[Trit], Trit]:
        """多位三进制减法
        
        输入: a, b (trit列表,低位在前)
        输出: (a - b, overflow)
        
        实现: a - b = a + (-b)
        """
        neg_b = TernaryArithmetic.negate_trits(b)
        return TernaryArithmetic.add_trits(a, neg_b)
    
    # -------------------------------------------------------------------------
    # 2.3 比较器
    # -------------------------------------------------------------------------
    
    @staticmethod
    def compare_trits(a: List[Trit], b: List[Trit]) -> Trit:
        """多位三进制比较
        
        输入: a, b (trit列表,高位在前)
        输出: sign(a - b)
            T: a < b
            0: a = b
            1: a > b
        
        实现: 从高位到低位逐位比较
        """
        if len(a) != len(b):
            raise ValueError("两个操作数长度必须相同")
        
        # 从高位到低位比较
        for i in range(len(a)):
            if a[i] != b[i]:
                # 找到第一个不同的位
                order = {Trit.NEG: -1, Trit.ZERO: 0, Trit.POS: 1}
                if order[a[i]] < order[b[i]]:
                    return Trit.NEG  # a < b
                else:
                    return Trit.POS  # a > b
        
        # 所有位都相同
        return Trit.ZERO  # a = b
    
    @staticmethod
    def abs_trits(a: List[Trit]) -> List[Trit]:
        """多位三进制绝对值

        输入: a (trit列表,高位在前)
        输出: |a| (trit列表)

        实现: 判断整个数的符号,负数则取负
        """
        # 判断符号: 找到第一个非零位
        sign = Trit.ZERO
        for trit in a:
            if trit != Trit.ZERO:
                sign = trit
                break

        # 如果是负数,取负
        if sign == Trit.NEG:
            return TernaryArithmetic.negate_trits(a)
        else:
            # 非负数,直接返回
            return a[:]


# ============================================================================
# 三、三进制存储单元
# ============================================================================

class TernaryFlipFlop:
    """三进制触发器
    
    存储 1 trit 的基本存储单元
    物理实现: 多阈值锁存器
    """
    
    def __init__(self, initial_value: Trit = Trit.ZERO):
        """初始化触发器"""
        self._value = initial_value
    
    def read(self) -> Trit:
        """读取存储的值"""
        return self._value
    
    def write(self, value: Trit):
        """写入新值"""
        self._value = value
    
    def __str__(self):
        return str(self._value)


class TernaryRegister:
    """三进制寄存器
    
    存储多个 trit 的寄存器
    """
    
    def __init__(self, width: int = 9, initial_value: int = 0):
        """初始化寄存器
        
        参数:
            width: 位宽(trit数)
            initial_value: 初始值(整数)
        """
        self.width = width
        self._flip_flops = [TernaryFlipFlop() for _ in range(width)]
        
        # 设置初始值
        if initial_value != 0:
            trits = self._int_to_trits(initial_value)
            for i, trit in enumerate(trits):
                self._flip_flops[i].write(trit)
    
    def _int_to_trits(self, value: int) -> List[Trit]:
        """整数转三进制(低位在前)"""
        if value == 0:
            return [Trit.ZERO] * self.width
        
        trits = []
        n = value
        
        for _ in range(self.width):
            remainder = n % 3
            if remainder > 1:
                remainder -= 3
                n += 1
            elif remainder < -1:
                remainder += 3
                n -= 1
            
            trits.append(Trit.from_int(remainder))
            n = n // 3
        
        return trits
    
    def _trits_to_int(self, trits: List[Trit]) -> int:
        """三进制转整数(低位在前)"""
        value = 0
        power = 1
        for trit in trits:
            value += trit.value * power
            power *= 3
        return value
    
    def read(self) -> List[Trit]:
        """读取寄存器(trit列表,低位在前)"""
        return [ff.read() for ff in self._flip_flops]
    
    def read_int(self) -> int:
        """读取寄存器(整数)"""
        return self._trits_to_int(self.read())
    
    def write(self, trits: List[Trit]):
        """写入寄存器(trit列表)"""
        if len(trits) != self.width:
            raise ValueError(f"写入宽度不匹配: 期望{self.width}, 实际{len(trits)}")
        
        for i, trit in enumerate(trits):
            self._flip_flops[i].write(trit)
    
    def write_int(self, value: int):
        """写入寄存器(整数)"""
        trits = self._int_to_trits(value)
        self.write(trits)
    
    def read_string(self) -> str:
        """读取寄存器(字符串,高位在前)"""
        trits = self.read()
        return ''.join(str(t) for t in reversed(trits))
    
    def __str__(self):
        return f"{self.read_string()} ({self.read_int()})"


# ============================================================================
# 四、三进制控制逻辑
# ============================================================================

class TernaryDecoder:
    """三进制译码器
    
    将操作码译码为控制信号
    """
    
    # 操作码定义
    OPCODES = {
        '000': 'HALT',
        '001': 'ADD',
        '00T': 'OFFSET',
        '010': 'LOAD',
        '0T0': 'STORE',
        '100': 'CMP',
        'T00': 'TJUMP',
        '01T': 'ABS',
        '0T1': 'NEG',
    }
    
    @staticmethod
    def decode_opcode(opcode_trits: List[Trit]) -> str:
        """译码操作码
        
        输入: 3 trit 操作码
        输出: 指令名称
        """
        opcode_str = ''.join(str(t) for t in opcode_trits)
        
        if opcode_str in TernaryDecoder.OPCODES:
            return TernaryDecoder.OPCODES[opcode_str]
        else:
            raise ValueError(f"无效的操作码: {opcode_str}")
    
    @staticmethod
    def decode_register(reg_trits: List[Trit]) -> int:
        """译码寄存器编号
        
        输入: 3 trit 寄存器编码
        输出: 寄存器编号(0-8)
        """
        # 寄存器编码表
        reg_table = {
            '000': 0,
            '001': 1,
            '01T': 2,
            '010': 3,
            '011': 4,
            '1TT': 5,
            '1T0': 6,
            '1T1': 7,
            '10T': 8,
        }
        
        reg_str = ''.join(str(t) for t in reg_trits)
        
        if reg_str in reg_table:
            return reg_table[reg_str]
        else:
            raise ValueError(f"无效的寄存器编码: {reg_str}")


class TernaryALU:
    """三进制算术逻辑单元
    
    完整的 ALU,支持所有 Trigram-3 指令的运算
    """
    
    def __init__(self, width: int = 9):
        """初始化 ALU"""
        self.width = width
    
    def add(self, a: List[Trit], b: List[Trit]) -> List[Trit]:
        """加法运算"""
        result, _ = TernaryArithmetic.add_trits(a, b)
        return result
    
    def negate(self, a: List[Trit]) -> List[Trit]:
        """取负运算"""
        return TernaryArithmetic.negate_trits(a)
    
    def subtract(self, a: List[Trit], b: List[Trit]) -> List[Trit]:
        """减法运算"""
        result, _ = TernaryArithmetic.subtract_trits(a, b)
        return result
    
    def compare(self, a: List[Trit], b: List[Trit]) -> Trit:
        """比较运算"""
        return TernaryArithmetic.compare_trits(
            list(reversed(a)),  # 转为高位在前
            list(reversed(b))
        )
    
    def absolute(self, a: List[Trit]) -> List[Trit]:
        """绝对值运算"""
        return TernaryArithmetic.abs_trits(list(reversed(a)))


# ============================================================================
# 测试代码
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("三进制逻辑门测试")
    print("=" * 60)
    
    # 测试逻辑门
    print("\n1. 反相器测试:")
    for a in [Trit.NEG, Trit.ZERO, Trit.POS]:
        print(f"  NOT({a}) = {TernaryLogic.NOT(a)}")
    
    print("\n2. 最小值门测试:")
    for a in [Trit.NEG, Trit.ZERO, Trit.POS]:
        for b in [Trit.NEG, Trit.ZERO, Trit.POS]:
            print(f"  MIN({a}, {b}) = {TernaryLogic.MIN(a, b)}")
    
    print("\n" + "=" * 60)
    print("三进制算术单元测试")
    print("=" * 60)
    
    # 测试半加器
    print("\n1. 半加器测试:")
    for a in [Trit.NEG, Trit.ZERO, Trit.POS]:
        for b in [Trit.NEG, Trit.ZERO, Trit.POS]:
            sum_val, carry = TernaryArithmetic.half_adder(a, b)
            print(f"  {a} + {b} = {sum_val} (carry: {carry})")
    
    # 测试多位加法
    print("\n2. 多位加法测试:")
    # 5 + 3 = 8
    # 5 = 1TT (低位在前: T, T, 1)
    # 3 = 010 (低位在前: 0, 1, 0)
    a = [Trit.NEG, Trit.NEG, Trit.POS, Trit.ZERO, Trit.ZERO, Trit.ZERO, Trit.ZERO, Trit.ZERO, Trit.ZERO]
    b = [Trit.ZERO, Trit.POS, Trit.ZERO, Trit.ZERO, Trit.ZERO, Trit.ZERO, Trit.ZERO, Trit.ZERO, Trit.ZERO]
    result, carry = TernaryArithmetic.add_trits(a, b)
    result_str = ''.join(str(t) for t in reversed(result))
    print(f"  5 + 3 = {result_str} (carry: {carry})")
    
    print("\n" + "=" * 60)
    print("三进制存储单元测试")
    print("=" * 60)
    
    # 测试寄存器
    print("\n1. 寄存器测试:")
    reg = TernaryRegister(width=9, initial_value=5)
    print(f"  初始值: {reg}")
    
    reg.write_int(10)
    print(f"  写入10: {reg}")
    
    reg.write_int(-5)
    print(f"  写入-5: {reg}")
    
    print("\n" + "=" * 60)
    print("三进制控制逻辑测试")
    print("=" * 60)
    
    # 测试译码器
    print("\n1. 操作码译码测试:")
    for opcode_str, name in TernaryDecoder.OPCODES.items():
        opcode_trits = [Trit.from_char(c) for c in opcode_str]
        decoded = TernaryDecoder.decode_opcode(opcode_trits)
        print(f"  {opcode_str} → {decoded}")
    
    print("\n" + "=" * 60)
    print("所有测试完成!")
    print("=" * 60)
