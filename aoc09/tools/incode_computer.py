class IntcodeComputer:

    def __init__(self, memory):
        self.memory = _Memory(memory)
        self.pointer = 0
        self.relative_base = 0
        self.state = _State.running
        self.input_list = []
        self.output_list = []

    def copy(self):
        other = IntcodeComputer(self.memory.mem.copy())
        other.pointer = self.pointer
        other.relative_base = self.relative_base
        other.state = self.state
        other.input_list = self.input_list.copy()
        other.output_list = self.output_list.copy()
        return other

    def run(self, input_list=None):
        if input_list:
            self.input_list = input_list
        self.state = _State.running

        while self.state == _State.running:
            self._interpret()

        return self.memory.get(0)

    def continue_run(self, input_list):
        return self.run(input_list)

    def is_running(self):
        return self.state != _State.done

    def _interpret(self):
        if self.state == _State.done:
            return

        instruction = IntcodeComputer._decode_instruction(self.memory.get(self.pointer))

        def param_address(i):
            first_param_address = self.pointer + 1
            param_i_address = first_param_address + i
            mode = instruction.param_modes[i]
            if mode == _Mode.position:
                address = self.memory.get(param_i_address)
            elif mode == _Mode.immediate:
                address = param_i_address
            elif mode == _Mode.relative:
                address = self.relative_base + self.memory.get(param_i_address)
            else:
                raise Exception("Unknown parameter mode", mode)
            return address

        def param(i):
            return self.memory.get(param_address(i))

        def write_to_memory(result):
            store_location = param_address(instruction.length - 2)  # last param [inst:0, param0:1, param1:2, param2:3]
            self.memory.set(store_location, result)

        # add
        if instruction.code == 1:
            instruction.length = 4
            write_to_memory(param(0) + param(1))
        # multiply
        elif instruction.code == 2:
            instruction.length = 4
            write_to_memory(param(0) * param(1))
        # read
        elif instruction.code == 3:
            instruction.length = 2
            if len(self.input_list) > 0:
                the_input = self.input_list[0]
                self.input_list = self.input_list[1:]
                write_to_memory(the_input)
            else:
                self.state = _State.waiting_for_input
                return  # don't move pointer
        # write
        elif instruction.code == 4:
            instruction.length = 2
            the_output = param(0)
            if self.output_list is not None:
                self.output_list.append(the_output)
        # jump if true
        elif instruction.code == 5:
            instruction.length = 3
            if param(0) > 0:
                self.pointer = param(1)
                return  # don't move the pointer
        # jump if false
        elif instruction.code == 6:
            instruction.length = 3
            if param(0) == 0:
                self.pointer = param(1)
                return  # don't move the pointer
        # less than
        elif instruction.code == 7:
            instruction.length = 4
            write_to_memory(1) if param(0) < param(1) else write_to_memory(0)
        # equals
        elif instruction.code == 8:
            instruction.length = 4
            write_to_memory(1) if param(0) == param(1) else write_to_memory(0)
        # relative base offset
        elif instruction.code == 9:
            instruction.length = 2
            self.relative_base += param(0)
        # end
        elif instruction.code == 99:
            instruction.length = 1
            self.state = _State.done
        else:
            raise Exception("Unknown instruction code", instruction.code)

        self.pointer += instruction.length

    @staticmethod
    def _code_with_param_modes(code):
        instr = code % 100
        modes = [code // 10 ** i % 10 for i in range(2, 5)]
        return instr, modes

    @staticmethod
    def _decode_instruction(full_code):
        (code, param_modes) = IntcodeComputer._code_with_param_modes(full_code)
        return _Instruction(code, param_modes)


class _State:
    running = "r"
    done = "d"
    waiting_for_input = "i"


class _Mode:
    position = 0
    immediate = 1
    relative = 2


class _Instruction:
    def __init__(self, code, param_modes=None):
        if param_modes is None:
            self.param_modes = []
        else:
            self.param_modes = param_modes
        self.code = code
        self.length = 0


class _Memory:
    def __init__(self, mem):
        self.mem = mem.copy()

    def set(self, pointer, value):
        if len(self.mem) <= pointer:
            # extend memory if requested
            self.mem = self.mem + ([0] * (pointer - len(self.mem) + 1))
        self.mem[pointer] = value

    def get(self, pointer):
        return 0 if len(self.mem) <= pointer else self.mem[pointer]

    def dump(self):
        return self.mem.copy()

