from util import New_LFSR, calculate_relative_frequency, display_frequency, decode, print_to_file
import sys


def question_2():
    # given equation: 𝑥10 + 𝑥3 + 1
    #
    #          [1,x1,x2,x3,x4,x5,x6,x7,x8,x9]
    equation = [1, 0, 0, 1, 0, 0, 0, 0, 0, 0]
    starting_state = [1, 0, 0, 1, 1, 0, 0, 0, 0, 1]
    starting_state.reverse()
    lfsr = New_LFSR(
        starting_state,
        equation
    )

    size = 512
    length = 64

    print_function = print
    if len(sys.argv) == 3 and sys.argv[1] == 'table->':
        print_function = print_to_file

    print_function('VISUAL DISPLAY OF BIT STREAM GENERATION:')
    bit_string_key = lfsr.shift(times=size, iter=True, display=True, display_function=print_function)

    print(f'\nOUTPUT BIT STREAM GENERATED (size={size}):')
    New_LFSR.display_bit_stream(bit_string_key, length=length)

    print('\nPERIOD OF OUTPUT STREAM:')
    print('1028')
    print('This can be calculated by 2^(number of registers i.e. 10)')
    print(
        'This can be seen if you change the size value to anything over 1028 and copy the path (below) to a google doc and use `crtl+f` to highlight repeated values')
    print(f'PATH:{lfsr.get_path()}')

    print('\nENCRYPT/DECRYPT:')
    bit_str = '11101100000110111011010011111010'
    enc_bit_str = New_LFSR.encrypt_bit_string(bit_string_key[:32], bit_str)
    print(f'original bit string  = {bit_str}')
    print(f'encrypted bit string = {enc_bit_str}')
    print(f'decrypted bit string = {New_LFSR.encrypt_bit_string(bit_string_key[:32], enc_bit_str)}')


def question_1():
    frequency = calculate_relative_frequency()
    display_frequency(frequency)
    decode(
        swap={
            'A': 'e',   'M': 'u',
            'B': 't',   'S': 'p',
            'C': 'a',   'N': 'm',
            'F': 'n',   'Q': 'g',
            'D': 'o',   'P': 'f',
            'I': 'r',   'O': 'w',
            'G': 's',   'R': 'y',
            'E': 'i',   'U': 'v',
            'L': 'c',   'T': 'b',
            'K': 'l',   'V': 'k',
            'H': 'h',   'Y': 'x',
            'J': 'd',

        }
    )
    print('Swapped letters and saved result to `plaintext.txt`')


if __name__ == '__main__':
    question_2()
    question_1()
