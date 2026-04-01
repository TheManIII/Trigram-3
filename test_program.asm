# Trigram-3 汇编测试程序
# 功能：R2 = 10, R3 = 5, R1 = R2 + R3

# 加载立即数到R2
OFFSET R2, R0, #10

# 加载立即数到R3
OFFSET R3, R0, #5

# 加法：R1 = R2 + R3
ADD R1, R2, R3

# 存储结果到内存[0]
STORE R1, [R0, #0]

# 停机
HALT
