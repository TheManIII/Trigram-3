# Trigram-3 指令编码

## 指令格式

Trigram-3 使用固定的指令格式，每条指令占用 27 trit（3 个内存字）。

### 基本格式

```
Opcode(3) | Rd(3) | Rs1(3) | Imm(18)
```

### 字段说明

| 字段 | 宽度 | 说明 |
|------|------|------|
| Opcode | 3 trit | 操作码 |
| Rd | 3 trit | 目标寄存器 |
| Rs1 | 3 trit | 第一源寄存器 |
| Imm | 18 trit | 立即数或第二源寄存器 |

### 指令对齐

- 每条指令占 3 个内存字
- 指令必须从地址 0, 3, 6, 9... 开始
- 地址 % 3 == 0

## 操作码编码

| Opcode | 助记符 | 说明 |
|--------|--------|------|
| 000 | HALT | 停机 |
| 001 | ADD | 加法 |
| 00T | OFFSET | 加立即数 |
| 010 | LOAD | 读内存 |
| 0T0 | STORE | 写内存 |
| 100 | CMP | 比较 |
| T00 | TJUMP | 三路跳转 |
| 01T | ABS | 绝对值 |
| 0T1 | NEG | 取负 |

## 寄存器编码

寄存器字段使用平衡三进制编码：

| 寄存器 | 编码（3 trit） | 十进制 |
|--------|---------------|--------|
| R0 | 000 | 0 |
| R1 | 001 | 1 |
| R2 | 01T | 2 |
| R3 | 010 | 3 |
| R4 | 011 | 4 |
| R5 | 1TT | 5 |
| R6 | 1T0 | 6 |
| R7 | 1T1 | 7 |
| R8 | 10T | 8 |

## 立即数编码

### 立即数指令（OFFSET, LOAD）

```
Imm(18) = 保留(9) | Imm9(9)
```

- Imm9: 9 trit 立即数，范围 -9841 到 +9841
- 保留: 高 9 trit 保留，必须为 0

### 寄存器指令（ADD, CMP, STORE）

```
Imm(18) = Imm15(15) | Rs2(3)
```

- Rs2: 第二源寄存器编码（低 3 trit）
- Imm15: 立即数（高 15 trit），必须为 0

### 跳转指令（TJUMP）

```
Imm(18) = off_T(6) | off_0(6) | off_1(6)
```

- off_T: 当 Rd = -1 时的偏移量
- off_0: 当 Rd = 0 时的偏移量
- off_1: 当 Rd = 1 时的偏移量

### 单寄存器指令（ABS, NEG）

```
Imm(18) = 保留(18)
```

- 保留: 必须为 0

## 编码示例

### 示例 1: ADD 指令

```assembly
ADD R1, R2, R3
```

编码：
```
Opcode: 001 (ADD)
Rd:     001 (R1)
Rs1:    01T (R2)
Imm:    000000000000000010 (R3)
```

完整编码：`00100101T000000000000000010`

### 示例 2: OFFSET 指令

```assembly
OFFSET R2, R0, #5
```

编码：
```
Opcode: 00T (OFFSET)
Rd:     01T (R2)
Rs1:    000 (R0)
Imm:    0000000000000001TT (5)
```

完整编码：`00T01T0000000000000000001TT`

### 示例 3: LOAD 指令

```assembly
LOAD R1, [R2, #3]
```

编码：
```
Opcode: 010 (LOAD)
Rd:     001 (R1)
Rs1:    01T (R2)
Imm:    000000000000000010 (3)
```

完整编码：`01000101T000000000000000010`

### 示例 4: STORE 指令

```assembly
STORE R1, [R2, #0]
```

编码：
```
Opcode: 0T0 (STORE)
Rd:     001 (R1)
Rs1:    01T (R2)
Imm:    000000000000000001 (Rs2=R1, imm=0)
```

完整编码：`0T00101T000000000000000001`

### 示例 5: CMP 指令

```assembly
CMP R1, R2, R3
```

编码：
```
Opcode: 100 (CMP)
Rd:     001 (R1)
Rs1:    01T (R2)
Imm:    000000000000000010 (R3)
```

完整编码：`10000101T000000000000000010`

### 示例 6: TJUMP 指令

```assembly
TJUMP R1, #-3, #0, #3
```

编码：
```
Opcode: T00 (TJUMP)
Rd:     001 (R1)
Rs1:    000 (R0)
Imm:    T0000000000000010T000010
```

完整编码：`T00001000T0000000000000010T000010`

### 示例 7: ABS 指令

```assembly
ABS R1, R2
```

编码：
```
Opcode: 01T (ABS)
Rd:     001 (R1)
Rs1:    01T (R2)
Imm:    000000000000000000 (保留)
```

完整编码：`01T00101T000000000000000000`

### 示例 8: NEG 指令

```assembly
NEG R1, R2
```

编码：
```
Opcode: 0T1 (NEG)
Rd:     001 (R1)
Rs1:    01T (R2)
Imm:    000000000000000000 (保留)
```

完整编码：`0T100101T000000000000000000`

### 示例 9: HALT 指令

```assembly
HALT
```

编码：
```
Opcode: 000 (HALT)
Rd:     000 (R0)
Rs1:    000 (R0)
Imm:    000000000000000000 (保留)
```

完整编码：`000000000000000000000000000`

## 编码工具

项目提供了编码工具 `trigram_utils.py`，包含以下函数：

### build_instruction

```python
from trigram_utils import build_instruction

# 构建指令
instr = build_instruction('001', 1, 2, rs2=3, imm=0)
print(instr)  # 00100101T000000000000000010
```

### parse_instruction

```python
from trigram_utils import parse_instruction

# 解析指令
result = parse_instruction('00100101T000000000000000010')
print(result)
# {'opcode': '001', 'rd': 'R1', 'rs1': 'R2', 'rs2': 'R3', 'imm': 0}
```

---

**文档版本**: 1.0
**更新日期**: 2026年4月
**维护者**: TheManIII
