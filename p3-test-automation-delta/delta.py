"""
Delta Debugging Program 
Authors: andrerod, mnoguier
"""

import os
import sys
import pdb

def main():
    n = int(sys.argv[1])
    curr_set = []
    for i in range (0, n):
        curr_set.append(i)
    print(sorted(list(invoke_dd([], curr_set))))


def invoke_dd(p, curr_set):
    # BASE CASE:
    print(curr_set)
    if len(curr_set) == 1:
        return curr_set

    # Split list and create unions
    first_union = sorted(list_union(p, curr_set[:len(curr_set)//2]))
    second_union = sorted(list_union(p, curr_set[len(curr_set)//2:]))

    #Generate commands based off unions:
    first_command = invoke_command(first_union)
    second_command = invoke_command(second_union)

    # RECURSIVE CASE:
    if os.system(first_command): 
        return invoke_dd(p, curr_set[:len(curr_set)//2])
    if os.system(second_command): 
        return invoke_dd(p, curr_set[len(curr_set)//2:])
    else:
        return sorted(list(list_union(invoke_dd(second_union, curr_set[:len(curr_set)//2]), invoke_dd(first_union, curr_set[len(curr_set)//2:]))))

def invoke_command(union_list):
    command = sys.argv[2]
    command += ' '
    command += ' '.join(str(n) for n in union_list)
    return command

def list_union(l1, l2):
    return list(set(l1 + l2))

if __name__ == "__main__":
    main()