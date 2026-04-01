#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trigram-3 汇编器/编译器
支持Trigram-3汇编语言的编译和反编译

作者：Trigram-3项目组
版本：1.0
"""

import sys
import re
from typing import List, Dict, Tuple, Optional
from enum import Enum
from dataclasses import dataclass


class TokenType(Enum):
    """词法单元类型"""
    # 指令
    HALT = 'HALT'
    ADD = 'ADD'
    OFFSET = 'OFFSET'
    LOAD = 'LOAD'
    STORE = 'STORE'
    CMP = 'CMP'
    TJUMP = 'TJUMP'
    ABS = 'ABS'
    NEG = 'NEG'
    
    # 寄存器
    REGISTER = 'REGISTER'
    
    # 数字
    NUMBER = 'NUMBER'
    
    # 符号
    COMMA = 'COMMA'      # ,
    LBRACKET = 'LBRACKET'  # [
    RBRACKET = 'RBRACKET'  # ]
    HASH = 'HASH'        # #
    
    # 其他
    NEWLINE = 'NEWLINE'
    EOF = 'EOF'
    UNKNOWN = 'UNKNOWN'


@dataclass
class Token:
    """词法单元"""
    type: TokenType
    value: str
    line: int
    column: int


class Lexer:
    """词法分析器"""
    
    # 关键字
    KEYWORDS = {
        'HALT': TokenType.HALT,
        'ADD': TokenType.ADD,
        'OFFSET': TokenType.OFFSET,
        'LOAD': TokenType.LOAD,
        'STORE': TokenType.STORE,
        'CMP': TokenType.CMP,
        'TJUMP': TokenType.TJUMP,
        'ABS': TokenType.ABS,
        'NEG': TokenType.NEG,
    }
    
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.text[self.pos] if self.text else None
    
    def advance(self):
        """前进到下一个字符"""
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
            self.column += 1
        else:
            self.current_char = None
    
    def skip_whitespace(self):
        """跳过空白字符（除了换行）"""
        while self.current_char and self.current_char in ' \t':
            self.advance()
    
    def skip_comment(self):
        """跳过注释（#开头到行尾）"""
        while self.current_char and self.current_char != '\n':
            self.advance()
        # 停在换行符处，让主循环处理换行符
    
    def number(self):
        """读取数字（支持十进制和平衡三进制，包括负数）"""
        result = ''
        while self.current_char and (self.current_char.isdigit() or 
                                     self.current_char in 'Tt-' or
                                     (result and self.current_char.isdigit())):
            result += self.current_char
            self.advance()
        return result
    
    def identifier(self):
        """读取标识符"""
        result = ''
        while self.current_char and (self.current_char.isalnum() or 
                                     self.current_char in 'Tt_'):
            result += self.current_char
            self.advance()
        return result
    
    def get_next_token(self) -> Token:
        """获取下一个词法单元"""
        while self.current_char:
            if self.current_char == ' ' or self.current_char == '\t':
                self.skip_whitespace()
                continue
            
            # #在数字或负号前面是立即数标记，否则是注释
            if self.current_char == '#':
                # 检查下一个字符是否是数字或负号
                next_pos = self.pos + 1
                if next_pos < len(self.text) and (self.text[next_pos].isdigit() or self.text[next_pos] == '-'):
                    # 这是立即数标记
                    token = Token(TokenType.HASH, '#', self.line, self.column)
                    self.advance()
                    return token
                else:
                    # 这是注释
                    self.skip_comment()
                    continue
            
            if self.current_char == '\n':
                token = Token(TokenType.NEWLINE, '\n', self.line, self.column)
                self.advance()
                self.line += 1
                self.column = 1
                return token
            
            if self.current_char == ',':
                token = Token(TokenType.COMMA, ',', self.line, self.column)
                self.advance()
                return token
            
            if self.current_char == '[':
                token = Token(TokenType.LBRACKET, '[', self.line, self.column)
                self.advance()
                return token
            
            if self.current_char == ']':
                token = Token(TokenType.RBRACKET, ']', self.line, self.column)
                self.advance()
                return token
            
            if self.current_char.isalpha():
                ident = self.identifier()
                token_type = self.KEYWORDS.get(ident.upper(), TokenType.REGISTER)
                return Token(token_type, ident.upper(), self.line, self.column)
            
            if self.current_char.isdigit() or self.current_char in 'Tt-':
                number = self.number()
                return Token(TokenType.NUMBER, number, self.line, self.column)
            
            # 未知字符
            token = Token(TokenType.UNKNOWN, self.current_char, self.line, self.column)
            self.advance()
            return token
        
        return Token(TokenType.EOF, '', self.line, self.column)
    
    def tokenize(self) -> List[Token]:
        """词法分析整个文本"""
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens


class Assembler:
    """Trigram-3 汇编器"""
    
    # 操作码定义
    OPCODES = {
        'HALT': '000',
        'ADD': '001',
        'OFFSET': '00T',
        'LOAD': '010',
        'STORE': '0T0',
        'CMP': '100',
        'TJUMP': 'T00',
        'ABS': '01T',
        'NEG': '0T1',
    }
    
    def __init__(self):
        self.symbols = {}  # 符号表
        self.relocations = []  # 重定位表
        self.instructions = []  # 生成的指令
    
    def int_to_balanced_ternary(self, value: int, width: int = 9) -> str:
        """将整数转换为平衡三进制字符串"""
        if value == 0:
            return '0' * width
        
        n = value
        trits = []
        for _ in range(width):
            remainder = n % 3
            if remainder > 1:
                remainder -= 3
                n += 1
            elif remainder < -1:
                remainder += 3
                n -= 1
            
            if remainder == -1:
                trits.append('T')
            elif remainder == 1:
                trits.append('1')
            else:
                trits.append('0')
            
            n = n // 3
        
        return ''.join(reversed(trits))
    
    def reg_to_trits(self, reg: str) -> str:
        """将寄存器号转换为平衡三进制编码"""
        # 支持R0-R8格式
        if reg.startswith('R'):
            reg_num = int(reg[1:])
        else:
            reg_num = int(reg)
        
        if reg_num < 0 or reg_num > 8:
            raise ValueError(f"无效的寄存器号: {reg_num}")
        
        return self.int_to_balanced_ternary(reg_num, width=3)
    
    def parse_immediate(self, value: str) -> int:
        """解析立即数（支持十进制和平衡三进制）"""
        # 检查是否是平衡三进制字符串
        if any(c in 'Tt' for c in value):
            return self.parse_balanced_ternary(value)
        else:
            # 十进制（可能包含负号）
            return int(value)
    
    def parse_balanced_ternary(self, value: str) -> int:
        """解析平衡三进制字符串为整数"""
        result = 0
        power = 1
        for c in reversed(value):
            if c == 'T' or c == 't':
                digit = -1
            elif c == '1':
                digit = 1
            else:
                digit = 0
            result += digit * power
            power *= 3
        return result
    
    def assemble_instruction(self, tokens: List[Token]) -> str:
        """汇编一条指令"""
        if not tokens:
            return ""
        
        # 获取操作码
        opcode_token = tokens[0]
        if opcode_token.type not in [t for t in TokenType if t.name in ['HALT', 'ADD', 'OFFSET', 'LOAD', 'STORE', 'CMP', 'TJUMP', 'ABS', 'NEG']]:
            raise ValueError(f"无效的操作码: {opcode_token.value}")
        
        opcode = self.OPCODES[opcode_token.value]
        
        # HALT指令
        if opcode_token.value == 'HALT':
            return "000000000000000000000000000"
        
        # 单寄存器指令: ABS, NEG
        if opcode_token.value in ['ABS', 'NEG']:
            if len(tokens) < 3:
                raise ValueError(f"{opcode_token.value}指令需要2个操作数")
            
            rd = self.reg_to_trits(tokens[1].value)
            rs1 = self.reg_to_trits(tokens[2].value)
            imm = self.int_to_balanced_ternary(0, width=18)
            return opcode + rd + rs1 + imm
        
        # 双寄存器指令: ADD, CMP
        # 格式: ADD Rd, Rs1, Rs2
        # tokens: [ADD, Rd, Rs1, Rs2]
        if opcode_token.value in ['ADD', 'CMP']:
            if len(tokens) < 4:
                raise ValueError(f"{opcode_token.value}指令需要3个操作数: Rd, Rs1, Rs2")
            
            rd = self.reg_to_trits(tokens[1].value)
            rs1 = self.reg_to_trits(tokens[2].value)
            rs2 = self.reg_to_trits(tokens[3].value)
            imm_15 = self.int_to_balanced_ternary(0, width=15)
            imm = imm_15 + rs2
            return opcode + rd + rs1 + imm
        
        # 立即数指令: OFFSET, LOAD
        # 格式: OFFSET Rd, Rs1, #imm
        # tokens: [OFFSET, Rd, Rs1, HASH, imm] 或 [OFFSET, Rd, Rs1]
        # Imm使用低9 trit，高9 trit保留为0
        if opcode_token.value in ['OFFSET', 'LOAD']:
            if len(tokens) < 3:
                raise ValueError(f"{opcode_token.value}指令需要至少2个操作数: Rd, Rs1")
            
            rd = self.reg_to_trits(tokens[1].value)
            rs1 = self.reg_to_trits(tokens[2].value)
            
            # 检查是否有立即数
            imm_value = 0
            if len(tokens) >= 5 and tokens[3].type == TokenType.HASH:
                imm_value = self.parse_immediate(tokens[4].value)
            
            # 立即数使用低9 trit，高9 trit保留为0
            imm_9 = self.int_to_balanced_ternary(imm_value, width=9)
            imm_high = '0' * 9
            imm = imm_high + imm_9
            return opcode + rd + rs1 + imm
        
        # STORE指令
        # 格式: STORE Rs2, [Rs1, #imm]
        # 过滤后的tokens: [STORE, Rs2, Rs1, HASH, imm]
        # Imm使用低9 trit作为偏移，高9 trit中低3 trit是Rs2
        if opcode_token.value == 'STORE':
            if len(tokens) < 3:
                raise ValueError(f"STORE指令需要至少2个操作数: Rs2, [Rs1]")
            
            rs2 = self.reg_to_trits(tokens[1].value)
            rs1 = self.reg_to_trits(tokens[2].value)
            
            # 检查是否有偏移
            imm_value = 0
            if len(tokens) >= 5 and tokens[3].type == TokenType.HASH:
                imm_value = self.parse_immediate(tokens[4].value)
            
            # STORE指令：Imm的高15 trit是偏移，低3 trit是Rs2
            imm_15 = self.int_to_balanced_ternary(imm_value, width=15)
            rd = self.reg_to_trits('0')  # STORE不使用Rd
            imm = imm_15 + rs2
            return opcode + rd + rs1 + imm
        
        # TJUMP指令
        if opcode_token.value == 'TJUMP':
            # 简化处理：暂时不支持
            raise NotImplementedError("TJUMP指令暂未实现")
        
        raise ValueError(f"未实现的指令: {opcode_token.value}")
    
    def assemble(self, source: str) -> List[str]:
        """汇编源代码"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # 按指令分割
        instructions = []
        current_instr_tokens = []
        
        for token in tokens:
            if token.type == TokenType.NEWLINE or token.type == TokenType.EOF:
                if current_instr_tokens:
                    instr = self.assemble_instruction(current_instr_tokens)
                    if instr:
                        instructions.append(instr)
                    current_instr_tokens = []
            elif token.type not in [TokenType.COMMA, TokenType.LBRACKET, TokenType.RBRACKET]:
                # 跳过标点符号，保留HASH和其他有用token
                current_instr_tokens.append(token)
        
        # 处理最后一条指令
        if current_instr_tokens:
            instr = self.assemble_instruction(current_instr_tokens)
            if instr:
                instructions.append(instr)
        
        return instructions


class Disassembler:
    """Trigram-3 反汇编器"""
    
    OPCODE_NAMES = {
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
    
    def balanced_ternary_to_int(self, trits: str) -> int:
        """将平衡三进制字符串转换为整数"""
        result = 0
        power = 1
        for c in reversed(trits):
            if c == 'T' or c == 't':
                digit = -1
            elif c == '1':
                digit = 1
            else:
                digit = 0
            result += digit * power
            power *= 3
        return result
    
    def trits_to_reg(self, trits: str) -> str:
        """将3 trit转换为寄存器名"""
        reg_num = self.balanced_ternary_to_int(trits)
        return f"R{reg_num}"
    
    def disassemble(self, machine_code: str) -> str:
        """反汇编一条机器码"""
        if len(machine_code) != 27:
            raise ValueError(f"机器码长度错误: 期望27 trit, 实际{len(machine_code)}")
        
        opcode = machine_code[0:3]
        rd = machine_code[3:6]
        rs1 = machine_code[6:9]
        imm = machine_code[9:27]
        
        opcode_name = self.OPCODE_NAMES.get(opcode, "UNKNOWN")
        
        if opcode == '000':
            return "HALT"
        
        elif opcode in ['01T', '0T1']:  # ABS, NEG
            rd_name = self.trits_to_reg(rd)
            rs1_name = self.trits_to_reg(rs1)
            return f"{opcode_name} {rd_name}, {rs1_name}"
        
        elif opcode in ['001', '100']:  # ADD, CMP
            rd_name = self.trits_to_reg(rd)
            rs1_name = self.trits_to_reg(rs1)
            rs2 = imm[15:18]
            rs2_name = self.trits_to_reg(rs2)
            return f"{opcode_name} {rd_name}, {rs1_name}, {rs2_name}"
        
        elif opcode in ['00T', '010']:  # OFFSET, LOAD
            rd_name = self.trits_to_reg(rd)
            rs1_name = self.trits_to_reg(rs1)
            imm_9 = imm[9:18]
            imm_value = self.balanced_ternary_to_int(imm_9)
            return f"{opcode_name} {rd_name}, {rs1_name}, #{imm_value}"
        
        elif opcode == '0T0':  # STORE
            rs2 = imm[15:18]
            rs2_name = self.trits_to_reg(rs2)
            rs1_name = self.trits_to_reg(rs1)
            imm_9 = imm[9:18]
            imm_value = self.balanced_ternary_to_int(imm_9)
            return f"STORE {rs2_name}, [{rs1_name}, #{imm_value}]"
        
        elif opcode == 'T00':  # TJUMP
            rd_name = self.trits_to_reg(rd)
            # 简化处理
            return f"TJUMP {rd_name}, #0, #0, #0"
        
        else:
            return f"UNKNOWN {machine_code}"


class Compiler:
    """Trigram-3 编译器（汇编器前端）"""
    
    def __init__(self):
        self.assembler = Assembler()
        self.disassembler = Disassembler()
    
    def compile_file(self, input_file: str, output_file: str = None):
        """编译汇编文件"""
        with open(input_file, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # 汇编
        instructions = self.assembler.assemble(source)
        
        # 输出
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                for instr in instructions:
                    f.write(instr + '\n')
            print(f"编译完成，输出到: {output_file}")
        else:
            print("编译结果:")
            for instr in instructions:
                print(instr)
        
        return instructions
    
    def disassemble_file(self, input_file: str, output_file: str = None):
        """反汇编机器码文件"""
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        assembly = []
        for line in lines:
            machine_code = line.strip()
            if machine_code:
                asm = self.disassembler.disassemble(machine_code)
                assembly.append(asm)
        
        # 输出
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                for asm in assembly:
                    f.write(asm + '\n')
            print(f"反汇编完成，输出到: {output_file}")
        else:
            print("反汇编结果:")
            for asm in assembly:
                print(asm)
        
        return assembly


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("Trigram-3 汇编器/反汇编器")
        print("用法:")
        print("  编译: python trigram_compiler.py -a input.asm [output.bin]")
        print("  反汇编: python trigram_compiler.py -d input.bin [output.asm]")
        sys.exit(1)
    
    compiler = Compiler()
    
    if sys.argv[1] == '-a':
        # 汇编
        input_file = sys.argv[2]
        output_file = sys.argv[3] if len(sys.argv) > 3 else None
        compiler.compile_file(input_file, output_file)
    
    elif sys.argv[1] == '-d':
        # 反汇编
        input_file = sys.argv[2]
        output_file = sys.argv[3] if len(sys.argv) > 3 else None
        compiler.disassemble_file(input_file, output_file)
    
    else:
        print("无效的参数")
        print("用法:")
        print("  编译: python trigram_compiler.py -a input.asm [output.bin]")
        print("  反汇编: python trigram_compiler.py -d input.bin [output.asm]")
        sys.exit(1)


if __name__ == '__main__':
    main()
