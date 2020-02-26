class IntcodeComputer:
    class Instruction:
        add = 1
        multiply = 2
        read = 3
        write = 4
        jump_if_true = 5
        jump_if_false = 6
        less_than = 7
        equals = 8
        end = 99

        def __init__(self, memory, pointer):
            code = memory[pointer]
            (self.code, param_modes) = self.code_with_param_modes(code)
            self.inputs = []
            if self.code == IntcodeComputer.Instruction.add:
                self.length = 4
                self.inputs.append(
                    IntcodeComputer.Instruction.param(memory, pointer + 1, param_modes[0])
                )
                self.inputs.append(
                    IntcodeComputer.Instruction.param(memory, pointer + 2, param_modes[1])
                )
                self.output = memory[pointer + 3]
            elif self.code == IntcodeComputer.Instruction.multiply:
                self.length = 4
                self.inputs.append(
                    IntcodeComputer.Instruction.param(memory, pointer + 1, param_modes[0])
                )
                self.inputs.append(
                    IntcodeComputer.Instruction.param(memory, pointer + 2, param_modes[1])
                )
                self.output = memory[pointer + 3]
            elif self.code == IntcodeComputer.Instruction.read:
                self.length = 2
                self.output = memory[pointer + 1]
            elif self.code == IntcodeComputer.Instruction.write:
                self.length = 2
                self.inputs.append(
                    IntcodeComputer.Instruction.param(memory, pointer + 1, param_modes[0]),
                )
            elif self.code == IntcodeComputer.Instruction.jump_if_true:
                self.length = 3
                self.inputs.append(
                    IntcodeComputer.Instruction.param(memory, pointer + 1, param_modes[0]),
                )
                self.jump = IntcodeComputer.Instruction.param(memory, pointer + 2, param_modes[1])
            elif self.code == IntcodeComputer.Instruction.jump_if_false:
                self.length = 3
                self.inputs.append(
                    IntcodeComputer.Instruction.param(memory, pointer + 1, param_modes[0]),
                )
                self.jump = IntcodeComputer.Instruction.param(memory, pointer + 2, param_modes[1])
            elif self.code == IntcodeComputer.Instruction.less_than:
                self.length = 4
                self.inputs.append(
                    IntcodeComputer.Instruction.param(memory, pointer + 1, param_modes[0])
                )
                self.inputs.append(
                    IntcodeComputer.Instruction.param(memory, pointer + 2, param_modes[1])
                )
                self.output = memory[pointer + 3]
            elif self.code == IntcodeComputer.Instruction.equals:
                self.length = 4
                self.inputs.append(
                    IntcodeComputer.Instruction.param(memory, pointer + 1, param_modes[0])
                )
                self.inputs.append(
                    IntcodeComputer.Instruction.param(memory, pointer + 2, param_modes[1])
                )
                self.output = memory[pointer + 3]
            elif self.code == IntcodeComputer.Instruction.end:
                self.length = 1
            else:
                raise Exception("Unknown code", code)

        @staticmethod
        def param(memory, index, mode):
            if mode == IntcodeComputer.Mode.position:
                return memory[memory[index]]
            elif mode == IntcodeComputer.Mode.immediate:
                return memory[index]
            else:
                raise Exception("Unknown mode", mode)

        @staticmethod
        def code_with_param_modes(code):
            instr = code % 100
            modes = [code // 10**i % 10 for i in range(2, 5)]
            return instr, modes

    class State:
        running = "r"
        done = "d"
        waiting_for_input = "i"

    class Mode:
        position = 0
        immediate = 1

    def __init__(self, memory):
        self.memory = memory.copy()
        self.pointer = 0
        self.state = IntcodeComputer.State.running
        self.input_list = []
        self.output_list = []

    def interpret(self):
        if self.state == IntcodeComputer.State.done:
            return

        instruction = IntcodeComputer.Instruction(self.memory, self.pointer)
        if instruction.code == IntcodeComputer.Instruction.add:
            self.memory[instruction.output] = instruction.inputs[0] + instruction.inputs[1]
        elif instruction.code == IntcodeComputer.Instruction.multiply:
            self.memory[instruction.output] = instruction.inputs[0] * instruction.inputs[1]
        elif instruction.code == IntcodeComputer.Instruction.read:
            if len(self.input_list) > 0:
                the_input = self.input_list[0]
                self.input_list = self.input_list[1:]
                self.memory[instruction.output] = the_input
            else:
                self.state = IntcodeComputer.State.waiting_for_input
                return  # don't move pointer
        elif instruction.code == IntcodeComputer.Instruction.write:
            the_output = instruction.inputs[0]
            if self.output_list is not None:
                self.output_list.append(the_output)
        elif instruction.code == IntcodeComputer.Instruction.jump_if_true:
            if instruction.inputs[0] > 0:
                self.pointer = instruction.jump
                return  # don't move the pointer
        elif instruction.code == IntcodeComputer.Instruction.jump_if_false:
            if instruction.inputs[0] == 0:
                self.pointer = instruction.jump
                return  # don't move the pointer
        elif instruction.code == IntcodeComputer.Instruction.less_than:
            if instruction.inputs[0] < instruction.inputs[1]:
                self.memory[instruction.output] = 1
            else:
                self.memory[instruction.output] = 0
        elif instruction.code == IntcodeComputer.Instruction.equals:
            if instruction.inputs[0] == instruction.inputs[1]:
                self.memory[instruction.output] = 1
            else:
                self.memory[instruction.output] = 0
        elif instruction.code == IntcodeComputer.Instruction.end:
            self.state = IntcodeComputer.State.done

        self.pointer += instruction.length

    def run(self, input_list=[]):
        self.input_list = input_list
        self.state = IntcodeComputer.State.running

        while self.state == IntcodeComputer.State.running:
            self.interpret()

        return self.memory[0]

    def continue_run(self, input_list):
        return self.run(input_list)
