###############################################################################
# !/user/local/bin/python3
#
# This is the file to run for using this API client.
#
# It should work on both Windows and Linux, but it has not been tested there.
#
###############################################################################
"""This is a command line-like interface for the client in interface.py"""

from interface import Interface
from utils import *

client = Interface()

while True:
    command=input('> ')
    if command[:4] == 'exit':
        break
    elif command[:5] == 'login':
        if command[5:].strip()[:6] == '--help':
            print('- Syntax Options:', '-\t\tlogin {email} {password}',
                  '-\t\tlogin {userid} {password}', sep='\n')
            continue
        try:
            creds = command.split()[1:]
            try:
                creds[0] = int(creds[0])
            except ValueError:
                pass
            if client.login(creds[0], creds[1]):
                print('-', 'Login successful')
            else:
                print('-', 'Login failed')
        except IndexError:
            print('- Syntax Options:', '-\t\tlogin {email} {password}',
                  '-\t\tlogin {userid} {password}', sep='\n')
    elif command[:4] == 'view':
        command = command[4:].strip()
        if command[:7] == 'history':
            print(table(client.get_calculation_history()))
        elif command[:5] == 'state':
            print('-', client)
        else:
            print('- Unrecognized attribute')
    elif command[:6] == 'logout':
        client.logout()
        print('-', 'Logout successful')
    elif command[:9] == 'calculate':
        op = command[9:].strip().split()
        ops = client.get_operations()
        if len(op) > 0 and op[0] in ops:
            operator = op[0]
            nums = []
            for i in op[1:]:
                nums.append(i)
            result = client.calculate(operator, *nums)
            if result[0] != '-':
                result = '+'+result
            print('-', result)
        else:
            if len(op) == 0 or op[0] != '--help':
                print('- Unrecognized calculation.')
            print('- Recognized calculations:')
            for i in ops:
                print('-\t\t', i)
    else:
        print('- Unknown command')
print('- Bye')
