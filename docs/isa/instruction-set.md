# Trigram-3 指令集定义

## 指令列表

Trigram-3 指令集包含 9 条指令，覆盖通用计算的所有基本操作。

| Opcode | 助记符 | 操作 | 说明 |
|--------|--------|------|------|
| 000 | HALT | 停机 | 停止 CPU 执行 |
| 001 | ADD | Rd ← Rs1 + Rs2 | 两寄存器相加 |
| 00T | OFFSET | Rd ← Rs1 + Imm₉ | 寄存器加立即数 |
| 010 | LOAD | Rd ← Mem[Rs1 + Imm₉] | 从内存读取 |
| 0T0 | STORE | Mem[Rs1 + Imm₉] ← Rs2 | 写入内存 |
| 100 | CMP | Rd ← sign(Rs1 - Rs2) | 比较两寄存器 |
| T00 | TJUMP | PC ← PC + off_Rd | 三路条件跳转 |
| 01T | ABS | Rd ← \|Rs1\| | 绝对值 |
| 0T1 | NEG | Rd ← -Rs1 | 取负 |

## 详细说明

### HALT - 停机

**格式**: `HALT`

**操作码**: 000

**说明**: 停止 CPU 执行，程序结束。

**示例**:
```assembly
HALT
```

### ADD - 加法

**格式**: `ADD Rd, Rs1, Rs2`

**操作码**: 001

**操作**: `Rd ← Rs1 + Rs2`

**说明**: 将两个寄存器的值相加，结果存入目标寄存器。

**示例**:
```assembly
ADD R1, R2, R3    ; R1 = R2 + R3
```

### OFFSET - 加立即数

**格式**: `OFFSET Rd, Rs1, #imm`

**操作码**: 00T

**操作**: `Rd ← Rs1 + imm`

**说明**: 将寄存器的值与立即数相加，结果存入目标寄存器。

**示例**:
```assembly
OFFSET R1, R2, #5   ; R1 = R2 + 5
OFFSET R3, R0, #-3  ; R3 = -3
```

### LOAD - 读内存

**格式**: `LOAD Rd, [Rs1, #imm]`

**操作码**: 010

**操作**: `Rd ← Mem[Rs1 + imm]`

**说明**: 从指定内存地址读取数据到寄存器。

**示例**:
```assembly
LOAD R1, [R2, #5]   ; R1 = Mem[R2 + 5]
LOAD R3, [-9840]     ; 从输入端口读取
```

### STORE - 写内存

**格式**: `STORE Rs2, [Rs1, #imm]`

**操作码**: 0T0

**操作**: `Mem[Rs1 + imm] ← Rs2`

**说明**: 将寄存器的值写入指定内存地址。

**示例**:
```assembly
STORE R1, [R2, #3]   ; Mem[R2 + 3] = R1
STORE R3, [-9841]     ; 向输出端口写入
```

### CMP - 比较

**格式**: `CMP Rd, Rs1, Rs2`

**操作码**: 100

**操作**: `Rd ← sign(Rs1 - Rs2)`

**说明**: 比较两个寄存器的值，结果为 -1、0 或 1。

**返回值**:
- -1 (T): Rs1 < Rs2
- 0 (0): Rs1 = Rs2
- 1 (1): Rs1 > Rs2

**示例**:
```assembly
CMP R1, R2, R3    ; R1 = sign(R2 - R3)
```

### TJUMP - 三路跳转

**格式**: `TJUMP Rd, #off_T, #off_0, #off_1`

**操作码**: T00

**操作**: 根据寄存器 Rd 的值跳转到不同偏移量

**说明**: 
- 如果 Rd = -1 (T)，跳转到 off_T
- 如果 Rd = 0，跳转到 off_0
- 如果 Rd = 1，跳转到 off_1

**示例**:
```assembly
CMP R1, R2, R3
TJUMP R1, #neg, #zero, #pos
neg:  ; R2 < R3 时执行
zero: ; R2 = R3 时执行
pos:  ; R2 > R3 时执行
```

### ABS - 绝对值

**格式**: `ABS Rd, Rs1`

**操作码**: 01T

**操作**: `Rd ← |Rs1|`

**说明**: 计算寄存器值的绝对值。

**示例**:
```assembly
ABS R1, R2    ; R1 = |R2|
```

### NEG - 取负

**格式**: `NEG Rd, Rs1`

**操作码**: 0T1

**操作**: `Rd ← -Rs1`

**说明**: 对寄存器的值取负。

**示例**:
```assembly
NEG R1, R2    ; R1 = -R2
```

## 指令编码

每条指令固定 27 trit（3 个内存字）：

```
Opcode(3) | Rd(3) | Rs1(3) | Imm(18)
```

对于 ADD、CMP、STORE 指令，Imm 的低 3 trit 包含 Rs2。

## 寄存器编码

寄存器字段使用平衡三进制（T, 0, 1）：

| 寄存器 | 编码（3 trit） |
|--------|---------------|
| R0 | 000 |
| R1 | 001 |
| R2 | 01T |
| R3 | 010 |
| R4 | 011 |
| R5 | 1TT |
| R6 | 1T0 |
| R7 | 1T1 |
| R8 | 10T |

## 立即数范围

- **9 trit 立即数**: -9841 到 +9841
- **18 trit 立即数**: -387,420,489 到 +387,420,489

## 编程示例

### 示例 1: 加法运算

```assembly
OFFSET R2, R0, #5   ; R2 = 5
OFFSET R3, R0, #3   ; R3 = 3
ADD R1, R2, R3      ; R1 = R2 + R3 = 8
HALT
```

### 示例 2: 比较和分支

```assembly
OFFSET R2, R0, #5   ; R2 = 5
OFFSET R3, R0, #3   ; R3 = 3
CMP R1, R2, R3      ; R1 = sign(5 - 3) = 1
TJUMP R1, #less, #equal, #greater
less:    ; R2 < R3
equal:   ; R2 = R3
greater: ; R2 > R3
HALT
```

### 示例 3: 内存操作

```assembly
OFFSET R1, R0, #10  ; R1 = 10
OFFSET R2, R0, #20  ; R2 = 20
STORE R1, [R2, #0]  ; Mem[20] = R1 = 10
LOAD R3, [R2, #0]   ; R3 = Mem[20] = 10
HALT
```

---

**文档版本**: 1.0
**更新日期**: 2026年4月
**维护者**: TheManIII
