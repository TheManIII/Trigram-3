# 变更日志

本文档记录 Trigram-3 项目的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)。

## [Unreleased]

### 计划中
- 高级调试功能（内存断点、条件断点）
- 更多示例程序
- 性能优化

## [1.0.0] - 2026-04-01

### 新增
- 完整的 Trigram-3 指令集（9 条指令）
- CPU 模拟器（`triton_simulator.py`）
- 汇编器/编译器（`trigram_compiler.py`）
- 反汇编器
- 公共工具模块（`trigram_utils.py`）
- 调试器支持
- 完整的文档体系
- Apache-2.0 许可证

### 指令集
- HALT - 停机
- ADD - 加法
- OFFSET - 加立即数
- LOAD - 读内存
- STORE - 写内存
- CMP - 比较
- TJUMP - 三路跳转
- ABS - 绝对值
- NEG - 取负

### 文档
- 设计哲学文档
- 架构概述
- ISA 规范（指令集、寄存器、内存、编码）
- 汇编指南
- 硬件实现建议

### 测试
- 基础测试
- 寄存器编码测试
- 新编码测试
- ABS/NEG 指令测试
- 完整指令测试

---

**版本号说明**：主版本号.次版本号.修订号
- 主版本号：不兼容的 API 修改
- 次版本号：向下兼容的功能性新增
- 修订号：向下兼容的问题修正
