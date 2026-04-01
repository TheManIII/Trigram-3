# Trigram-3 汇编指南

## 简介

本文档介绍如何使用 Trigram-3 汇编语言编写程序。

## 汇编器使用

### 编译汇编程序

```bash
python trigram_compiler.py -a input.asm output.bin
```

### 反汇编机器码

```bash
python trigram_compiler.py -d input.bin output.asm
```

## 汇编语法

### 基本格式

```
[标号:] 指令 操作数1, 操作数2, 操作数3 [; 注释]
```

### 注释

使用 `#` 开头的行注释：

```assembly
# 这是一个注释
ADD R1, R2, R3    ; 行尾注释
```

### 标号

标号用于标记代码位置，支持跳转：

```assembly
start:
    OFFSET R1, R0, #10
    ADD R2, R1, R1
    HALT
```

## 指令语法

### HALT

```assembly
HALT
```

### ADD

```assembly
ADD Rd, Rs1, Rs2
```

示例：
```assembly
ADD R1, R2, R3    ; R1 = R2 + R3
```

### OFFSET

```assembly
OFFSET Rd, Rs1, #imm
```

示例：
```assembly
OFFSET R1, R0, #5   ; R1 = 5
OFFSET R2, R0, #-3  ; R2 = -3
```

### LOAD

```assembly
LOAD Rd, [Rs1, #imm]
```

示例：
```assembly
LOAD R1, [R2, #5]   ; R1 = Mem[R2 + 5]
LOAD R3, [-9840]     ; 从输入端口读取
```

### STORE

```assembly
STORE Rs2, [Rs1, #imm]
```

示例：
```assembly
STORE R1, [R2, #3]   ; Mem[R2 + 3] = R1
STORE R3, [-9841]     ; 向输出端口写入
```

### CMP

```assembly
CMP Rd, Rs1, Rs2
```

示例：
```assembly
CMP R1, R2, R3    ; R1 = sign(R2 - R3)
```

### TJUMP

```assembly
TJUMP Rd, #off_T, #off_0, #off_1
```

示例：
```assembly
CMP R1, R2, R3
TJUMP R1, #less, #equal, #greater
less:
    ; R2 < R3 时执行
equal:
    ; R2 = R3 时执行
greater:
    ; R2 > R3 时执行
```

### ABS

```assembly
ABS Rd, Rs1
```

示例：
```assembly
ABS R1, R2    ; R1 = |R2|
```

### NEG

```assembly
NEG Rd, Rs1
```

示例：
```assembly
NEG R1, R2    ; R1 = -R2
```

## 编程示例

### 示例 1: 简单加法

```assembly
; 计算 5 + 3 = 8
OFFSET R2, R0, #5   ; R2 = 5
OFFSET R3, R0, #3   ; R3 = 3
ADD R1, R2, R3      ; R1 = 8
STORE R1, [R0, #0]  ; Mem[0] = 8
HALT
```

### 示例 2: 绝对值和取负

```assembly
; 计算 | -5 | = 5, 然后 -5 = -5
OFFSET R1, R0, #-5  ; R1 = -5
ABS R2, R1          ; R2 = 5
NEG R3, R1          ; R3 = 5
HALT
```

### 示例 3: 简单循环

```assembly
; 计算 1 + 2 + 3 + 4 + 5 = 15
OFFSET R1, R0, #0   ; R1 = 0 (和)
OFFSET R2, R0, #1   ; R2 = 1 (计数器)
OFFSET R3, R0, #5   ; R3 = 5 (上限)

loop:
    ADD R1, R1, R2      ; R1 = R1 + R2
    OFFSET R2, R2, #1   ; R2 = R2 + 1
    CMP R4, R2, R3      ; R4 = sign(R2 - R3)
    TJUMP R4, #loop, #end, #end

end:
    STORE R1, [R0, #0]  ; Mem[0] = 15
    HALT
```

### 示例 4: I/O 操作

```assembly
; 读取输入，乘以 2，输出结果
LOAD R1, [-9840]     ; R1 = 输入值
ADD R1, R1, R1       ; R1 = R1 * 2
STORE R1, [-9841]     ; 输出 R1
HALT
```

## 常见错误

### 错误 1: 无效的寄存器号

```assembly
ADD R9, R1, R2    ; 错误：R9 不存在
```

### 错误 2: 立即数超出范围

```assembly
OFFSET R1, R0, #10000    ; 错误：超出 9 trit 范围
```

### 错误 3: 操作数数量不正确

```assembly
ADD R1, R2    ; 错误：缺少 Rs2
```

## 调试技巧

### 1. 使用调试器

```bash
python triton_simulator.py program.asm -d
```

调试命令：
- `r`: 运行
- `s`: 单步
- `t`: 显示状态
- `m <addr> [count]`: 显示内存
- `b <addr>`: 添加断点
- `c <addr>`: 清除断点
- `q`: 退出

### 2. 查看机器码

```bash
python trigram_compiler.py -a program.asm output.bin
```

查看 `output.bin` 中的机器码，验证编码是否正确。

### 3. 使用反汇编

```bash
python trigram_compiler.py -d output.bin output.asm
```

反汇编机器码，验证程序逻辑。

---

**文档版本**: 1.0
**更新日期**: 2026年4月
**维护者**: TheManIII
