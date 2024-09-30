from typing import List, Dict, Optional
import des

import sys

args = ' '.join(sys.argv)
seper = '_' * 160
print(f'{seper}\n\n\n$home > {args}\n')

def bufferize(input_bits) -> str:
    if len(input_bits) != 56:
        return input_bits
    out = ''
    for i in range(0, len(input_bits), 7):
        out += input_bits[i:i + 7]+ ' '
    return out
def repack(input_bits) -> str:
    if len(input_bits) != 64:
        return input_bits
    out = ''
    for i in range(0, len(input_bits), 8):
        out += input_bits[i:i + 7]
    return out
# Permutation function using a given table
def permute(input_bits, permutation_table, reason:str):
    # print(f'{reason=}')
    # print(f'{permutation_table=}\n')
    try:
        permuted = ''.join(input_bits[pos % len(input_bits)] for row in permutation_table for pos in row)
    except IndexError as e:
        # print(f'Inputs: lne={len(input_bits)}, {input_bits=}')
        # for i, row in enumerate(permutation_table):
        #     print(f'{i}. {row}\t{max(row)=}')
        raise e
    return permuted

def expansion_function(input_bits, expansion_table):
    try:
        expanded = ''.join(input_bits[pos % len(input_bits)] for row in expansion_table for pos in row)
    except IndexError as e:
        # print(f'{input_bits=}')
        # print(f'Inputs: lne={len(input_bits)}, {input_bits=}')
        # for i, row in enumerate(expansion_table):
        #     print(f'{i}. {row}\t{max(row)=}')
        raise e
    return expanded

def xor(bits1, bits2):
    return ''.join('1' if b1 != b2 else '0' for b1, b2 in zip(bits1, bits2))

def s_box_substitution(input_bits, s_boxes):
    output_bits = ''
    for i in range(0, len(input_bits), 6):
        block = input_bits[i:i + 6]
        row = int(block[0] + block[5], 2)
        col = int(block[1:5], 2)
        s_box_value = s_boxes[(i // 6) * 4 + row][col]
        output_bits += format(s_box_value, '04b')
    return output_bits

def p_permutation(input_bits, p_table):
    permuted = ''.join(input_bits[pos] for row in p_table for pos in row)
    return permuted

def des_round(right_bits, round_key):
    expanded_right = expansion_function(right_bits, des.expansion_table)
    xored_bits = xor(expanded_right, round_key)
    s_box_output = s_box_substitution(xored_bits, des.s_boxes)
    return p_permutation(s_box_output, des.p_permutation)

def generate_round_keys(key):
    if len(key) != 56:
        raise ValueError(f"Invalid key length: Expected 56 bits, got {len(key)} bits")
    
    left = permute(key, des.permutated_choice_1_c, 'des.permutated_choice_1_c')
    right = permute(key, des.permutated_choice_1_d, 'des.permutated_choice_1_d')
    
    left_shifted = left[1:] + left[0]
    right_shifted = right[1:] + right[0]

    combined = left_shifted + right_shifted
    round_key1 = permute(combined, des.permutated_choice_2, 'des.permutated_choice_2')

    left_shifted = left_shifted[1:] + left_shifted[0]
    right_shifted = right_shifted[1:] + right_shifted[0]

    combined = left_shifted + right_shifted
    round_key2 = permute(combined, des.permutated_choice_2, 'des.permutated_choice_2')

    return round_key1, round_key2

initial_permuted = permute(des.input, des.initial_permutation, 'des.initial_permutation')

left_half = initial_permuted[:32]
right_half = initial_permuted[32:]

round_key1, round_key2 = generate_round_keys(des.key)

new_right_half = xor(left_half, des_round(right_half, round_key1))
new_left_half = right_half

final_right_half = xor(new_left_half, des_round(new_right_half, round_key2))
final_left_half = new_right_half

final_output = permute(final_left_half + final_right_half, des.final_permutation, 'des.final_permutation')

print(f'Original text:                   {des.input}')
print(f'Final Ciphertext after 2 rounds: {final_output}')
