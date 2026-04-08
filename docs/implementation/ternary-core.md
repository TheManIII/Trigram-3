# Trigram-3 三进制核心组件

## 概述

本文档描述 Trigram-3 的四个核心组件,这些组件实现了**真正的三进制运算逻辑**,而非用二进制模拟三进制。

## 一、三进制逻辑门

### 1.1 基本概念

三进制逻辑门是构建三进制 CPU 的基础组件,类似于二进制系统中的 AND、OR、NOT 门。

### 1.2 单输入逻辑门

#### 反相器 (NOT)

**功能**: 取反

**真值表**:
```
输入 | 输出
  T  |  1
  0  |  0
  1  |  T
```

**物理实现**: 电压反相器
- 输入 -V → 输出 +V
- 输入 0V → 输出 0V
- 输入 +V → 输出 -V

**代码实现**:
```python
def NOT(a: Trit) -> Trit:
    if a == Trit.NEG: return Trit.POS
    elif a == Trit.ZERO: return Trit.ZERO
    else: return Trit.NEG
```

#### 循环左移 (CL)

**功能**: 循环左移

**真值表**:
```
输入 | 输出
  T  |  0
  0  |  1
  1  |  T
```

**物理实现**: 相位旋转器

#### 循环右移 (CR)

**功能**: 循环右移

**真值表**:
```
输入 | 输出
  T  |  1
  0  |  T
  1  |  0
```

**物理实现**: 相位旋转器

### 1.3 双输入逻辑门

#### 最小值门 (MIN)

**功能**: 返回两个输入的最小值

**真值表**:
```
  a  |  b  | MIN(a,b)
  T  |  T  |    T
  T  |  0  |    T
  T  |  1  |    T
  0  |  T  |    T
  0  |  0  |    0
  0  |  1  |    0
  1  |  T  |    T
  1  |  0  |    0
  1  |  1  |    1
```

**物理实现**: 电压最小值电路

**代码实现**:
```python
def MIN(a: Trit, b: Trit) -> Trit:
    order = {Trit.NEG: -1, Trit.ZERO: 0, Trit.POS: 1}
    return a if order[a] <= order[b] else b
```

#### 最大值门 (MAX)

**功能**: 返回两个输入的最大值

**真值表**:
```
  a  |  b  | MAX(a,b)
  T  |  T  |    T
  T  |  0  |    0
  T  |  1  |    1
  0  |  T  |    0
  0  |  0  |    0
  0  |  1  |    1
  1  |  T  |    1
  1  |  0  |    1
  1  |  1  |    1
```

**物理实现**: 电压最大值电路

#### 一致门 (CONS)

**功能**: 如果两个输入相同则输出该值,否则输出 0

**真值表**:
```
  a  |  b  | CONS(a,b)
  T  |  T  |     T
  T  |  0  |     0
  T  |  1  |     0
  0  |  T  |     0
  0  |  0  |     0
  0  |  1  |     0
  1  |  T  |     0
  1  |  0  |     0
  1  |  1  |     1
```

**用途**: 检测两个输入是否一致

## 二、三进制算术单元

### 2.1 半加器

**功能**: 两个 1 trit 数相加

**输入**: a, b (各 1 trit)

**输出**: sum, carry

**真值表**:
```
  a  |  b  | sum | carry
  T  |  T  |  1  |   T
  T  |  0  |  T  |   0
  T  |  1  |  0  |   0
  0  |  T  |  T  |   0
  0  |  0  |  0  |   0
  0  |  1  |  1  |   0
  1  |  T  |  0  |   0
  1  |  0  |  1  |   0
  1  |  1  |  T  |   1
```

**解释**:
- T + T = -1 + -1 = -2 = 1 + T×3 (sum=1, carry=T)
- 1 + 1 = 1 + 1 = 2 = T + 1×3 (sum=T, carry=1)

**代码实现**:
```python
def half_adder(a: Trit, b: Trit) -> Tuple[Trit, Trit]:
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
```

### 2.2 全加器

**功能**: 三个 1 trit 数相加(带进位)

**输入**: a, b, carry_in

**输出**: sum, carry_out

**实现**: 两个半加器级联

```python
def full_adder(a: Trit, b: Trit, carry_in: Trit) -> Tuple[Trit, Trit]:
    # 第一级: a + b
    sum1, carry1 = half_adder(a, b)
    
    # 第二级: sum1 + carry_in
    sum2, carry2 = half_adder(sum1, carry_in)
    
    # 进位合并
    carry_out = MAX(carry1, carry2)
    
    return (sum2, carry_out)
```

### 2.3 多位加法器

**功能**: 两个 n trit 数相加

**实现**: 全加器级联

```python
def add_trits(a: List[Trit], b: List[Trit]) -> Tuple[List[Trit], Trit]:
    result = []
    carry = Trit.ZERO
    
    # 从低位到高位逐位相加
    for i in range(len(a)):
        sum_trit, carry = full_adder(a[i], b[i], carry)
        result.append(sum_trit)
    
    return (result, carry)
```

### 2.4 比较器

**功能**: 比较两个 n trit 数

**输出**:
- T: a < b
- 0: a = b
- 1: a > b

**实现**: 从高位到低位逐位比较

```python
def compare_trits(a: List[Trit], b: List[Trit]) -> Trit:
    # 从高位到低位比较
    for i in range(len(a)):
        if a[i] != b[i]:
            # 找到第一个不同的位
            if a[i] < b[i]:
                return Trit.NEG  # a < b
            else:
                return Trit.POS  # a > b
    
    return Trit.ZERO  # a = b
```

## 三、三进制存储单元

### 3.1 三进制触发器

**功能**: 存储 1 trit 的基本存储单元

**物理实现**: 多阈值锁存器

**状态**:
- 存储 T: 锁定在 -V
- 存储 0: 锁定在 0V
- 存储 1: 锁定在 +V

**代码实现**:
```python
class TernaryFlipFlop:
    def __init__(self, initial_value: Trit = Trit.ZERO):
        self._value = initial_value
    
    def read(self) -> Trit:
        return self._value
    
    def write(self, value: Trit):
        self._value = value
```

### 3.2 三进制寄存器

**功能**: 存储 n trit 的寄存器

**实现**: n 个三进制触发器组成

```python
class TernaryRegister:
    def __init__(self, width: int = 9):
        self.width = width
        self._flip_flops = [TernaryFlipFlop() for _ in range(width)]
    
    def read(self) -> List[Trit]:
        return [ff.read() for ff in self._flip_flops]
    
    def write(self, trits: List[Trit]):
        for i, trit in enumerate(trits):
            self._flip_flops[i].write(trit)
```

## 四、三进制控制逻辑

### 4.1 操作码译码器

**功能**: 将 3 trit 操作码译码为指令名称

**实现**:
```python
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

def decode_opcode(opcode_trits: List[Trit]) -> str:
    opcode_str = ''.join(str(t) for t in opcode_trits)
    return OPCODES[opcode_str]
```

### 4.2 寄存器译码器

**功能**: 将 3 trit 寄存器编码译码为寄存器编号

**编码表**:
```
编码  | 寄存器
000  |   R0
001  |   R1
01T  |   R2
010  |   R3
011  |   R4
1TT  |   R5
1T0  |   R6
1T1  |   R7
10T  |   R8
```

### 4.3 三进制 ALU

**功能**: 完整的算术逻辑单元

**支持的操作**:
- 加法 (ADD)
- 减法 (SUB)
- 取负 (NEG)
- 比较 (CMP)
- 绝对值 (ABS)

```python
class TernaryALU:
    def add(self, a: List[Trit], b: List[Trit]) -> List[Trit]:
        result, _ = add_trits(a, b)
        return result
    
    def negate(self, a: List[Trit]) -> List[Trit]:
        return [NOT(trit) for trit in a]
    
    def compare(self, a: List[Trit], b: List[Trit]) -> Trit:
        return compare_trits(a, b)
    
    def absolute(self, a: List[Trit]) -> List[Trit]:
        return abs_trits(a)
```

## 五、与二进制系统的对比

### 5.1 信息密度

| 系统 | 基本单元 | 信息量 | 效率 |
|------|---------|--------|------|
| 二进制 | bit (0, 1) | log₂(2) = 1 | 1.0 |
| 三进制 | trit (T, 0, 1) | log₂(3) ≈ 1.585 | 1.585 |

**结论**: 三进制信息密度比二进制高 58.5%

### 5.2 运算效率

以加法为例:

| 操作 | 二进制 | 三进制 |
|------|--------|--------|
| 1 位加法 | 1 个全加器 | 1 个全加器 |
| n 位加法 | n 个全加器 | n 个全加器 |
| 信息量 | n bits | n trits ≈ 1.585n bits |

**结论**: 相同硬件复杂度下,三进制处理更多信息

### 5.3 对称性

| 特性 | 二进制 | 平衡三进制 |
|------|--------|-----------|
| 正负表示 | 需要符号位 | 天然对称 |
| 取负操作 | 取反+1 | 每位取反 |
| 零的表示 | 唯一 | 唯一 |
| 对称性 | 不对称 | 完全对称 |

**结论**: 平衡三进制天然对称,更优雅

## 六、物理实现建议

### 6.1 电压表示

```
T (NEG): -V  (例如 -1V)
0 (ZERO): 0V
1 (POS): +V  (例如 +1V)
```

### 6.2 逻辑门实现

**反相器**: 电压反相放大器
**MIN 门**: 电压最小值电路
**MAX 门**: 电压最大值电路

### 6.3 存储实现

**三进制触发器**: 多阈值锁存器
- 使用三个稳定状态
- 需要特殊的反馈电路

### 6.4 挑战

1. **多阈值晶体管**: 需要支持三个电平
2. **噪声容限**: 三电平系统噪声容限更小
3. **工艺复杂度**: 比二进制 CMOS 更复杂
4. **现有生态**: 二进制工具链成熟

## 七、使用示例

### 7.1 基本运算

```python
from ternary_logic import TernaryArithmetic, Trit

# 创建两个数
a = [Trit.POS, Trit.ZERO, Trit.ZERO]  # 100 (9)
b = [Trit.ZERO, Trit.POS, Trit.ZERO]  # 010 (3)

# 加法
result, carry = TernaryArithmetic.add_trits(a, b)
# result = [Trit.POS, Trit.POS, Trit.ZERO]  # 110 (12)

# 比较
cmp = TernaryArithmetic.compare_trits(a, b)
# cmp = Trit.POS  (a > b)
```

### 7.2 寄存器操作

```python
from ternary_logic import TernaryRegister

# 创建寄存器
reg = TernaryRegister(width=9, initial_value=5)

# 读取
value = reg.read_int()  # 5
trits = reg.read()      # [Trit.NEG, Trit.NEG, Trit.POS, ...]

# 写入
reg.write_int(10)
```

## 八、总结

### 8.1 已实现

- ✅ 三进制逻辑门 (NOT, MIN, MAX, CONS)
- ✅ 三进制算术单元 (半加器, 全加器, 多位加法)
- ✅ 三进制存储单元 (触发器, 寄存器)
- ✅ 三进制控制逻辑 (译码器, ALU)

### 8.2 特点

1. **真正的三进制运算**: 不使用十进制转换
2. **模块化设计**: 每个组件独立可测试
3. **物理可实现**: 提供物理实现建议
4. **完整文档**: 包含真值表和实现细节

### 8.3 下一步

1. 重构模拟器使用这些核心组件
2. 实现 Verilog 硬件描述
3. FPGA 原型验证
4. 性能分析和优化

---

**文档版本**: 1.0
**更新日期**: 2026年4月
**维护者**: TheManIII
