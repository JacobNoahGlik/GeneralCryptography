import math
import sys


class New_LFSR:
    def __init__(self, init_state, eq, col_len=5):
        self.state = init_state
        self.eq = eq
        self.col_len = col_len
        self.path = f'{self.to_dec()}'

    def get_path(self) -> str:
        return self.path

    def display(self, header: bool = False, size=1, calculate_size=False, iter_val=-1, iter_size=5,
                display_function=print):
        insert = ''
        printable = ''
        if header:
            if iter_val != -1:
                insert = 'num.'.ljust(iter_size)
                printable += ' ' * iter_size
            if calculate_size: size = len(f'{(len(self.state))}') if len(f'{(len(self.state))}') > 3 else 3
            for i in range(len(self.state)):
                printable += '|' + f'x^{i}'.center(size)
            rail = '|' + ('-' * size)
            printable += '|' + 'dec'.center(size) + '|' + 'drp'.center(size) + '|' + 'clc'.center(
                size) + f'|\n{insert}' + (rail * (len(self.state) + 3)) + '|\n'
        if iter_val != -1:
            printable += f'{iter_val}. '.ljust(iter_size)
        for reg in self.state:
            printable += '|' + f'{reg}'.center(size)
        display_function(
            printable + '|' + str(self.to_dec()).center(size) + '|' + str(self.state[0]).center(size) + '|' + str(
                self._preform_operation()).center(size) + '|')

    def to_dec(self) -> int:
        p = 0
        counter = 0
        for reg in self.state:
            counter += reg * 2 ** p
            p += 1
        return counter

    def shift(self, times=1, display=True, iter=False, display_function=print) -> str:
        iterator_length = 2 + len(str(times))
        counter = -1
        if display:
            if iter: counter += 1
            self.display(header=True, size=self.col_len, iter_val=counter, iter_size=iterator_length,
                         display_function=print)
            if iter: counter += 1
        bit_string: str = ''
        for _ in range(times):
            bit_string += str(self._shift_once())
            self.path += f',{self.to_dec()}'
            if display:
                self.display(size=self.col_len, iter_val=counter, iter_size=iterator_length, display_function=print)
            if iter: counter += 1
        return bit_string

    def _shift_once(self) -> int:
        xor = self._preform_operation()
        new_state = []
        dropped_bit = self.state[0]
        for reg in self.state[1:]:
            new_state.append(reg)
        new_state.append(xor)
        self.state = new_state
        return dropped_bit

    def _preform_operation(self) -> int:
        count = -1
        for reg, bit in zip(self.state, self.eq):
            if bit == 1:
                if count != -1:
                    count = count ^ reg
                else:
                    count = reg
        return count if count != -1 else 0

    @staticmethod
    def encrypt_bit_string(bit_string, message):
        resp = ''
        for reg1, reg2 in zip(bit_string, message):
            bit1 = int(reg1)
            bit2 = int(reg2)
            resp += str(bit1 ^ bit2)
        return resp

    @staticmethod
    def display_bit_stream(bit_stream, length=128):
        for start in range(math.ceil(len(bit_stream) / length)):
            print(bit_stream[start * length: start * length + length])


class SmartDictionary:
    def __init__(self):
        self.dictionary: dict[str, int] = {}

    def add(self, id):
        if id in self.dictionary.keys():
            self.dictionary[id] += 1
        else:
            self.dictionary[id] = 1

    def sort(self):
        new_dictionary = {}
        backwards_sorted_keys = sorted(self.dictionary, key=self.dictionary.get)
        backwards_sorted_keys.reverse()
        for key in backwards_sorted_keys:
            new_dictionary[key] = self.dictionary[key]
        self.dictionary = new_dictionary

    def get_dictionary(self):
        return self.dictionary


def read_file(name: str, ignore_chars=[]) -> str:
    with open(name, 'r') as f:
        body = f.read()
    for ch in ignore_chars:
        body = body.replace(ch, '')
    return body


def calculate_relative_frequency(FILE='ciphertext.txt'):
    body = read_file(FILE, ignore_chars=[' ', '\n', '-', ';'])
    frequency = SmartDictionary()
    for ch in body:
        frequency.add(ch)
    frequency.sort()
    return frequency.get_dictionary()


def display_frequency(frequency: dict, col_size: int = 7):
    for i, (key, value) in enumerate(frequency.items()):
        print(
            # f'{i + 1}. '.ljust(len(str(len(frequency) + 1)) + 2) +
            f'{key}: '.ljust(len(max(frequency.keys(), key=len)) + 2) +
            f'{value}',
            end='\t'
        )
        if i % col_size == (col_size - 1):
            print('')
    if i % col_size != (col_size - 1):
        print('')


def decode(
        F_IN: str = 'ciphertext.txt',
        F_OUT: str = 'plaintext.txt',
        swap: dict = []
):
    body = read_file(F_IN)
    replacement_body = ''
    for i, ch in enumerate(body):
        if ch in swap.keys():
            replacement_body += swap[ch]
        else:
            replacement_body += ch
    with open(F_OUT, 'w') as f:
        f.write(replacement_body)


__START__ = True


def print_to_file(text):
    global __START__
    write_type = 'a'
    if __START__:
        write_type = 'w'
    with open(sys.argv[-1], write_type) as f:
        f.write(text)
    __START__ = False
