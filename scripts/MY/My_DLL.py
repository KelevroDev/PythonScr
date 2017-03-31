#!/usr/bin/env python

import os
import subprocess

def my(*args):
    for a in args:
        if isfloat(a):
            print("\n\n\t", a, "bigit")
        else:
            print("\n\n\t", a.upper())

def string_to_list(sep, string):
    my_Dict = {}
    counter = 0
    word = ''
    for count in string:
        if count != sep:
            word = word + count
        if count == sep:
            counter = counter + 1
            word = ''
        my_Dict[counter] = word
    for i in my_Dict:
        print((i + 1), my_Dict[i])
    return my_Dict

def ask_me(ask):
    print (ask)
    answer = input("y/n: ")
    if answer == 'y':
        return answer
    elif answer == 'n':
        return answer
    else:
        print("Make your choise, Y or N")
        ask_me(ask)

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def main():
    #arg = input("input string:")
    #my(arg)
    #sep = input("input separator:")
    #dic = string_to_list(sep, arg)
    #print(dic)
    answer = ask_me("Do you want continue?")
    if answer == 'y':
        print("Let's continue")
    elif answer == 'n':
        print("OK, by by")

if __name__ == "__main__":
    main()
