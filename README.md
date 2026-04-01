# Trigram-3 平衡三进制 CPU 指令集

基于平衡三进制（Balanced Ternary）的 RISC 架构 CPU 指令集。

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7+-green.svg)](https://www.python.org/downloads/)

## 项目简介

**Trigram-3** 是一个基于平衡三进制系统的极简 CPU 架构，使用 T(-1), 0, 1 作为基本数字。本项目提供了完整的指令集规范、模拟器、汇编器和调试工具。

### 技术特点

- **平衡三进制**：使用 T(-1), 0, 1 作为基本数字
- **极简指令集**：9 条指令覆盖通用计算
- **对称设计**：地址空间和数值表示均以 0 为中心
- **完整工具链**：包含模拟器、汇编器、反汇编器

## 许可证

本项目采用 [Apache-2.0 许可证](LICENSE)。

## 快速开始

### 安装

无需额外依赖，只需 Python 3.7+：

```bash
git clone <repository>
cd Trigram-3
```

### 运行模拟器

运行内置测试：

```bash
python triton_simulator.py -t
```

运行程序文件：

```bash
python triton_simulator.py program.bin -v
```

### 编译汇编程序

使用汇编器将汇编代码编译为机器码：

```bash
python trigram_compiler.py -a program.asm program.bin
```

反汇编机器码：

```bash
python trigram_compiler.py -d program.bin program.asm
```

### 调试模式

```bash
python triton_simulator.py program.bin -d
```

调试命令：
- `r`: 运行
- `s`: 单步
- `t`: 显示状态
- `m <addr> [count]`: 显示内存
- `b <addr>`: 添加断点
- `c <addr>`: 清除断点
- `q`: 退出

## 文档

### 核心文档

- **[设计哲学](docs/philosophy.md)** - 了解 Trigram-3 的设计思想和理念
- **[架构概述](docs/overview.md)** - 完整的架构概览和参数说明

### ISA 规范

- **[指令集定义](docs/isa/instruction-set.md)** - 详细的指令集规范
- **[寄存器规范](docs/isa/registers.md)** - 寄存器编码和使用
- **[内存模型](docs/isa/memory.md)** - 内存地址和组织
- **[指令编码](docs/isa/encoding.md)** - 指令的二进制编码格式

### 程序员手册

- **[汇编指南](docs/programmer/assembly-guide.md)** - 如何编写汇编程序

### 实现指南

- **[硬件实现](docs/implementation/hardware.md)** - 硬件实现建议和参考

## 指令集

| Opcode | 助记符 | 操作 | 说明 |
|--------|--------|------|------|
| 000 | HALT | 停机 | 停止执行 |
| 001 | ADD | Rd ← Rs1 + Rs2 | 两寄存器相加 |
| 00T | OFFSET | Rd ← Rs1 + Imm₉ | 加立即数 |
| 010 | LOAD | Rd ← Mem[Rs1 + Imm₉] | 读内存 |
| 0T0 | STORE | Mem[Rs1 + Imm₉] ← Rs2 | 写内存 |
| 100 | CMP | Rd ← sign(Rs1 - Rs2) | 比较 |
| T00 | TJUMP | 根据Rd值三路跳转 | 条件跳转 |
| 01T | ABS | Rd ← \|Rs1\| | 绝对值 |
| 0T1 | NEG | Rd ← -Rs1 | 取负 |

## 寄存器

| 寄存器 | 编码（3 trit） | 说明 |
|--------|---------------|------|
| R0 | 000 | 零号寄存器，硬连线为 0 |
| R1-R8 | 001-10T | 通用寄存器，9 trit 宽 |

## 内存模型

- **字长**: 9 trit
- **逻辑地址范围**: -9841 到 +9841
- **特殊地址**:
  - -9841: 输出端口
  - -9840: 输入端口
  - 0: 程序入口

## 项目结构

```
Trigram-3/
├── LICENSE                          # Apache-2.0 许可证
├── README.md                        # 本文档
├── docs/                            # 文档目录
│   ├── philosophy.md               # 设计哲学
│   ├── overview.md                 # 架构概述
│   ├── isa/                        # ISA 规范
│   │   ├── instruction-set.md      # 指令集定义
│   │   ├── registers.md            # 寄存器规范
│   │   ├── memory.md               # 内存模型
│   │   └── encoding.md             # 指令编码
│   ├── programmer/                 # 程序员手册
│   │   └── assembly-guide.md       # 汇编指南
│   └── implementation/             # 实现指南
│       └── hardware.md             # 硬件实现建议
├── triton_simulator.py              # CPU 模拟器
├── trigram_compiler.py              # 汇编器/编译器
├── trigram_utils.py                 # 公共工具模块
├── test_simple.py                   # 基础测试
├── test_*.py                        # 其他测试文件
├── test_program.asm                 # 测试程序
└── test_all_instructions.asm        # 完整指令测试
```

## 开发状态

### 已实现

- ✅ 完整的 Trigram-3 指令集模拟（9 条指令）
- ✅ 寄存器堆
- ✅ 内存系统（含 I/O 映射）
- ✅ 调试器
- ✅ 汇编器/编译器
- ✅ 反汇编器
- ✅ 测试用例

### 待扩展

- 🚧 高级调试功能（内存断点、条件断点）
- 🚧 性能优化
- 🚧 更多示例程序

## 编程示例

### 示例 1: 加法运算

```asm
; 计算 5 + 3 = 8
OFFSET R2, R0, #5   ; R2 = 5
OFFSET R3, R0, #3   ; R3 = 3
ADD R1, R2, R3      ; R1 = 8
STORE R1, [R0, #0]  ; Mem[0] = 8
HALT
```

### 示例 2: 比较和分支

```asm
; 比较 R2 和 R3，根据结果跳转
OFFSET R2, R0, #5
OFFSET R3, R0, #3
CMP R1, R2, R3
TJUMP R1, #neg, #zero, #pos
neg:    ; R2 < R3 时执行
zero:   ; R2 = R3 时执行
pos:    ; R2 > R3 时执行
HALT
```

## 贡献

欢迎提交 Issue 和 Pull Request 来改进 Trigram-3！

详见 [贡献指南](CONTRIBUTING.md)。

## 版本信息

- **版本**: 1.0.0
- **许可证**: Apache-2.0
- **作者**: TheManIII
- **更新日期**: 2026年4月

详见 [变更日志](CHANGELOG.md)。

## 联系方式

- **Issue**: [GitHub Issues](https://github.com/TheManIII/Trigram-3/issues)
- **讨论**: [GitHub Discussions](https://github.com/TheManIII/Trigram-3/discussions)

## 致谢

## 维护说明

- 本项目代码由 AI 辅助生成，我负责架构设计和最终审核。
- 受网络条件限制，GitHub 更新可能不及时，但仍会不定期查看 issue 和 PR。
- 欢迎任何人基于 Apache-2.0 协议使用、修改、商用，保留版权声明即可。
- 如果你有改进建议或想参与贡献，直接提 PR 或 issue，我会在看到后尽快处理。

