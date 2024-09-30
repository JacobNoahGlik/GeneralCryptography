from typing import List
from typing import List, Dict, Optional
import aes
import sys

args = ' '.join(sys.argv)
seper = '_' * 160
print(f'{seper}\n\n\n$home > {args}\n')

def bytes_to_bits_binary(byte_data):
    bits_data = bin(int.from_bytes(byte_data, byteorder='big'))[2:]
    return bits_data

def binary_to_hex(binary_str):
    if not set(binary_str).issubset({'0', '1'}):
        raise ValueError("Input string must contain only binary digits (0s and1s).")
    hex_str = hex(int(binary_str, 2))[2:]

    return hex_str

def state_diagram(hex_str) -> List[str]:
    diagram: List[str] = []
    for i in range(0, len(hex_str) // 8):
        diagram.append(hex_str[8*i:8*(i+1)])
    return diagram

def sub_bytes(hex_state: List[str]) -> List[str]:
    substituted_state = []
    for hex_byte in hex_state:
        byte_value = int(hex_byte, 16)
        
        row = (byte_value >> 4) & 0xF
        col = byte_value & 0xF
        
        substituted_byte = aes.s_box[row][col]
        substituted_hex = f'{substituted_byte:02x}'
        substituted_state.append(substituted_hex)
    return substituted_state

def create_matrix(state: List[str]) -> List[List[str]]:
    matrix = [state[i:i+4] for i in range(0, len(state), 4)]
    return matrix

def shift_rows(state_matrix: List[List[str]]) -> List[List[str]]:
    state_matrix[1] = state_matrix[1][1:] + state_matrix[1][:1]
    state_matrix[2] = state_matrix[2][2:] + state_matrix[2][:2]
    state_matrix[3] = state_matrix[3][3:] + state_matrix[3][:3]
    
    return state_matrix

def flatten_matrix(state_matrix: List[List[str]]) -> List[str]:
    return [byte for row in state_matrix for byte in row]

def galois_mult_2(byte):
    result = byte << 1
    if result & 0x100: 
        result ^= 0x1b 
    return result & 0xff 

def galois_mult_3(byte):
    return galois_mult_2(byte) ^ byte

def mix_columns(state_matrix: List[List[str]]) -> List[List[str]]:
    for col in range(4):
        s0 = int(state_matrix[0][col], 16)
        s1 = int(state_matrix[1][col], 16)
        s2 = int(state_matrix[2][col], 16)
        s3 = int(state_matrix[3][col], 16)
        
        new_s0 = galois_mult_2(s0) ^ galois_mult_3(s1) ^ s2 ^ s3
        new_s1 = s0 ^ galois_mult_2(s1) ^ galois_mult_3(s2) ^ s3
        new_s2 = s0 ^ s1 ^ galois_mult_2(s2) ^ galois_mult_3(s3)
        new_s3 = galois_mult_3(s0) ^ s1 ^ s2 ^ galois_mult_2(s3)
        
        state_matrix[0][col] = f'{new_s0:02x}'
        state_matrix[1][col] = f'{new_s1:02x}'
        state_matrix[2][col] = f'{new_s2:02x}'
        state_matrix[3][col] = f'{new_s3:02x}'
    
    return state_matrix

def rotate_word(word):
    return word[1:] + word[:1]

def sub_word(word):
    return [aes.s_box[byte >> 4][byte & 0x0F] for byte in word]

def key_expansion(key):
    expanded_keys = []
    expanded_keys.extend([int(key[i:i+2], 16) for i in range(0, len(key), 2)])

    for i in range(4, 44):
        temp = expanded_keys[4*(i-1):4*i]
        if i % 4 == 0:
            temp = sub_word(rotate_word(temp))
            temp[0] ^= aes.rcon[i//4 - 1]
        expanded_keys += [expanded_keys[4*(i-4) + j] ^ temp[j] for j in range(4)]
    
    round_keys = [expanded_keys[4*i:4*(i+4)] for i in range(11)]
    return round_keys

def add_round_key(state_matrix: List[List[str]], round_key: List[int]) -> List[List[str]]:
    for row in range(4):
        for col in range(4):
            state_matrix[row][col] = f'{int(state_matrix[row][col], 16) ^ round_key[row + 4*col]:02x}'
    return state_matrix

def get_round_key_matrix(round_key: List[int]) -> List[List[int]]:
    return [[round_key[i + j*4] for i in range(4)] for j in range(4)]

aes_input = '01010110111000100001100110110010010001001011001111011011010000111000000100011110100111010011101010011110100001011111001101001111'
aes_key = '2b7e151628aed2a6abf7158809cf4f3c'

hex_str = binary_to_hex(aes_input)
print(f'Input: 0b{aes_input}')
print(f'Hex:   0x{hex_str.upper()}\n')

top_left = '╭'
top_right = '╮'
middle_left = '│'
middle_right = '│'
bottom_left = '╰'
bottom_right = '╯'

print('State Diagram:')
for i in range(0, len(hex_str), 8):
    prefix, postfix = middle_left, middle_right
    if i == 0:
        prefix, postfix = top_left, top_right
    elif i == len(hex_str) - 8:
        prefix, postfix = bottom_left, bottom_right
    print(f'\t{prefix} {hex_str.upper()[i:i+2]} {hex_str.upper()[i+2:i+4]} {hex_str.upper()[i+4:i+6]} {hex_str.upper()[i+6:i+8]} {postfix}')
print('')

hex_state = [hex_str[i:i+2] for i in range(0, len(hex_str), 2)]
print(f"State before SubBytes: {hex_state}")

substituted_state = sub_bytes(hex_state)
print(f"State after SubBytes:  {substituted_state}")

substituted_hex_str = ''.join(substituted_state)
print(f'Substituted Hex: 0x{substituted_hex_str.upper()}\n')

substituted_state = sub_bytes(hex_state)

state_matrix = create_matrix(substituted_state)
print(f"State matrix before ShiftRows: {state_matrix}")

shifted_matrix = shift_rows(state_matrix)
print(f"State matrix after ShiftRows:  {shifted_matrix}")

shifted_state = flatten_matrix(shifted_matrix)
shifted_hex_str = ''.join(shifted_state)
print(f'Shifted Hex: 0x{shifted_hex_str.upper()}\n')

print(f"State matrix after ShiftRows:  {shifted_matrix}")
mixed_matrix = mix_columns(shifted_matrix)
print(f"State matrix after MixColumns: {mixed_matrix}")

mixed_state = flatten_matrix(mixed_matrix)
mixed_hex_str = ''.join(mixed_state)
print(f'Mixed Hex:    0x{mixed_hex_str.upper()}\n')

round_keys = key_expansion(aes_key)

first_round_key = round_keys[0]

substituted_state = sub_bytes(hex_state)
state_matrix = create_matrix(substituted_state)
shifted_matrix = shift_rows(state_matrix)

mixed_matrix = mix_columns(shifted_matrix)

round_key_matrix = get_round_key_matrix(first_round_key)
final_state = add_round_key(mixed_matrix, first_round_key)

print(f"State matrix after AddRoundKey: {final_state}")

final_state_flat = flatten_matrix(final_state)
final_hex_str = ''.join(final_state_flat)
print(f'Final Hex after AddRoundKey: 0x{final_hex_str.upper()}')