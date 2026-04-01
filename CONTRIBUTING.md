# 贡献指南

感谢您对 Trigram-3 项目的关注！

## 如何贡献

### 报告问题

如果您发现了 bug 或有功能建议，请创建 Issue：

1. 清晰描述问题
2. 提供复现步骤（如果适用）
3. 包含预期行为和实际行为

### 提交代码

1. Fork 本仓库
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

### 代码规范

- 使用 Python 3.7+ 语法
- 遵循 PEP 8 代码风格
- 添加必要的注释和文档字符串
- 确保所有测试通过

### 测试

在提交 PR 之前，请确保：

- 现有测试通过：`python test_simple.py`
- 新功能包含测试
- 代码没有明显的性能问题

## 开发环境

### 安装

```bash
git clone <your-fork>
cd Trigram-3
python --version  # 确保是 Python 3.7+
```

### 运行测试

```bash
# 基础测试
python test_simple.py

# 寄存器编码测试
python test_register_encoding.py

# 新编码测试
python test_new_encoding.py

# ABS/NEG 指令测试
python test_abs_neg.py
```

### 代码结构

```
Trigram-3/
├── docs/              # 文档
├── triton_simulator.py  # CPU 模拟器
├── trigram_compiler.py  # 汇编器/编译器
├── trigram_utils.py     # 公共工具
└── test_*.py          # 测试文件
```

## 联系方式

如有疑问，请通过 Issue 或 Discussion 联系我们。

---

**Happy Coding!**
