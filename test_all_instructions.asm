# Trigram-3 汇编测试程序 - 测试所有指令

# 测试1: 基本运算
# R1 = 10 + 5 = 15
OFFSET R2, R0, #10
OFFSET R3, R0, #5
ADD R1, R2, R3
STORE R1, [R0, #0]

# 测试2: ABS指令
# R2 = |-8| = 8
OFFSET R2, R0, #-8
ABS R3, R2
STORE R3, [R0, #1]

# 测试3: NEG指令
# R4 = -7
OFFSET R4, R0, #7
NEG R5, R4
STORE R5, [R0, #2]

# 测试4: 综合测试
# R6 = |-10| = 10, R7 = -10
OFFSET R6, R0, #-10
ABS R6, R6
NEG R7, R6
STORE R6, [R0, #3]
STORE R7, [R0, #4]

# 停机
HALT
