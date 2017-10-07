import sys
import re

class Seventeen():

    @staticmethod
    def _strip_comments(source_code):
        return re.sub(r'/\*(.*?)\*/', '', source_code, flags=re.MULTILINE|re.DOTALL)

    @staticmethod
    def _normalize_whitespace(source_code):
        # Strip each line of whitespace, remove empty lines
        non_empty_lines = []
        for line in source_code.splitlines():
            line = line.strip()
            if line:
                # Only allow a single space between each token
                line = re.sub(r'(\s)\s*', r'\1', line)
                non_empty_lines.append(line.strip())

        # Place each token on a separate line
        token_lines = []
        for line in non_empty_lines:
            token_lines.extend(line.split())

        return "\n".join(token_lines)

    @staticmethod
    def _extract_labels(source_code):
        # labels is a map from a string label to a line number (starting at 0)
        labels = {}
        label_pattern = re.compile(r'^(.*?):$')

        lines_without_labels = []
        line_number = 0
        for line in source_code.splitlines():
            match = re.match(label_pattern, line)
            if match:
                labels[match.group(1)] = line_number
            else:
                lines_without_labels.append(line)
                line_number += 1

        source_code = "\n".join(lines_without_labels)
        return labels, source_code

    def __init__(self, source_code, debug=False):
        source_code = Seventeen._strip_comments(source_code)
        source_code = Seventeen._normalize_whitespace(source_code)
        labels, source_code = Seventeen._extract_labels(source_code)
        self._labels = labels
        self._source_lines = source_code.splitlines()
        self._pc = -1
        self.debug = debug

    def _resolve_symbol(self, symbol):
        """takes a symbol and returns the value of it"""
        if isinstance(symbol, int):
            return symbol
        elif symbol in self._labels:
            return self._labels[symbol]
        else:
            return self._vars[symbol]

    def _jump_to_addr(self, addr):
        """sets the value of PC so that the next instruction executed
        is the instruction pointed to by addr"""
        self._pc = (addr - 1) # -1 since we incr pc after each step

    def _do_read_num(self):
        """read_num reads the sysin as an int"""
        if not self._sysin:
            self._do_exit()
            return
        num = int(self._sysin, 10)
        self._sysin = ""
        self._stack.append(num)

    def _do_read_byte(self):
        """read_byte reads a single byte from sysin"""
        if not self._sysin:
            self._do_exit()
            return
        num = ord(self._sysin[0])
        self._sysin = self._sysin[1:]
        self._stack.append(num)

    def _do_print_byte(self):
        """print_byte adds the topmost value of the stack to the output"""
        value = self._resolve_symbol(self._stack.pop())
        self._out.append(chr(value))

    def _do_print_num(self):
        """print_num adds the topmost value of the stack to the output"""
        value = self._resolve_symbol(self._stack.pop())
        self._out.append(str(value))

    def _do_exit(self):
        self._pc = len(self._source_lines)

    def _do_add(self):
        """add replaces the two topmost values of stack with their sum"""
        num1 = self._resolve_symbol(self._stack.pop())
        num2 = self._resolve_symbol(self._stack.pop())
        self._stack.append(num1 + num2)

    def _do_sub(self):
        """sub replaces the two topmost values of stack with the result of
        subtracting them"""
        subtrahend = self._resolve_symbol(self._stack.pop())
        minuend = self._resolve_symbol(self._stack.pop())
        self._stack.append(minuend - subtrahend)

    def _do_mod(self):
        """mod replaces the topmost values of the stack with the result
        of calculating the mod"""
        divend = self._resolve_symbol(self._stack.pop())
        divisor = self._resolve_symbol(self._stack.pop())
        self._stack.append(divisor % divend)

    def _do_xor(self):
        """xor performs the xor operation of the two topmost value of
        the stack"""
        num1 = self._resolve_symbol(self._stack.pop())
        num2 = self._resolve_symbol(self._stack.pop())
        self._stack.append(num1 ^ num2)

    def _do_dup(self):
        """dup copies the topmost value of the stack"""
        self._stack.append(self._stack[-1])

    def _do_store(self):
        """store stores the 2nd topmost value on the stack into the variable
        name on top of the stack"""
        var_name = self._stack.pop()
        value = self._resolve_symbol(self._stack.pop())
        # Resolve all references to the name to the old value if we
        # are replacing the variable value
        if var_name in self._vars:
            old_value = self._vars[var_name]
            self._stack = [v if v != var_name else old_value for v in self._stack]
        self._vars[var_name] = value

    def _do_vstore(self):
        """vstore stores the topmost value on the stack into the vector,
        using the 2nd topmost value as index"""
        value = self._resolve_symbol(self._stack.pop())
        index = self._resolve_symbol(self._stack.pop())
        self._vect[index] = value

    def _do_vload(self):
        """vload replaces the topmost value on the stack with the value
        of the vector, using the topmost value as index"""
        index = self._resolve_symbol(self._stack.pop())
        self._stack.append(self._vect[index])

    def _do_jump(self):
        """jump jumps to the topmost symbol on the stack"""
        addr = self._resolve_symbol(self._stack.pop())
        self._jump_to_addr(addr)

    def _do_ifz(self):
        """ifz compares the topmost value of the stack to 0:
        if true, ifz jumps to 2nd topmost label on the stack
        if false, ifz jumps to the topmost label on the stack"""
        addr_neq_0 = self._resolve_symbol(self._stack.pop())
        addr_eq_0 = self._resolve_symbol(self._stack.pop())
        if self._stack.pop() == 0:
            self._jump_to_addr(addr_eq_0)
        else:
            self._jump_to_addr(addr_neq_0)

    def _do_ifg(self):
        """ifg compares the topmost value of the stack to > 0:
        if true, ifz jumps to 2nd topmost label on the stack
        if false, ifz jumps to the topmost label on the stack"""
        addr_neq_0 = self._resolve_symbol(self._stack.pop())
        addr_eq_0 = self._resolve_symbol(self._stack.pop())
        if self._stack.pop() > 0:
            self._jump_to_addr(addr_eq_0)
        else:
            self._jump_to_addr(addr_neq_0)

    def _do_call(self):
        """call callss the topmost label on the stack. A call is
        a jump, that first pushes the return pc onto the stack"""
        addr = self._resolve_symbol(self._stack.pop())
        self._stack.append(self._pc + 1)
        self._jump_to_addr(addr)

    def _do_instruction(self, instruction):
        if instruction == "read_num":
            self._do_read_num()
        elif instruction == "read_byte":
            self._do_read_byte()
        elif instruction == "print_byte":
            self._do_print_byte()
        elif instruction == "print_num":
            self._do_print_num()
        elif instruction == "exit":
            self._do_exit()
        elif instruction == "add":
            self._do_add()
        elif instruction == "sub":
            self._do_sub()
        elif instruction == "mod":
            self._do_mod()
        elif instruction == "xor":
            self._do_xor()
        elif instruction == "dup":
            self._do_dup()
        elif instruction == "store":
            self._do_store()
        elif instruction == "vload":
            self._do_vload()
        elif instruction == "vstore":
            self._do_vstore()
        elif instruction == "jump":
            self._do_jump()
        elif instruction == "ifz":
            self._do_ifz()
        elif instruction == "ifg":
            self._do_ifg()
        elif instruction == "call":
            self._do_call()
        elif not instruction.isdigit():
            # A symbol (variable or label)
            self._stack.append(instruction)
        else:
            self._stack.append(int(instruction, 10))


    def _step(self):
        instruction = self._source_lines[self._pc]
        if self.debug:
            print("Stack:", self._stack)
            print("Vars:", self._vars)
            print("Vect:", self._vect)
            print("Out:", repr("".join(self._out)))
            print(self._pc, "=>", instruction)
            print("")
        self._do_instruction(instruction)
        self._pc = self._pc + 1
        return self._pc < len(self._source_lines)

    def run(self, sysin):
        self._sysin = sysin
        self._out = []
        self._stack = []
        self._vars = {}
        self._vect = {}

        self._pc = 0
        try:
            while self._step():
                if self.debug:
                    input()
        finally:
            if self.debug:
                print("Final State:")
                print("PC:", self._pc)
                print("Stack:", self._stack)
                print("Vars:", self._vars)
                print("Out:", repr("".join(self._out)))
                print("")

        return "".join(self._out)


def main():
    if len(sys.argv) < 2:
        print("Missing file arg")
        return

    source_file_path = sys.argv[1]
    with open(source_file_path) as source_file:
        program = Seventeen(source_file.read(), False)
        result = program.run(sys.argv[2] + "\n")
        print(result)


if __name__ == '__main__':
    main()
