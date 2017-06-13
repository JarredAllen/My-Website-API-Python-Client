###############################################################################
# !/user/local/bin/python3
#
# This is the file to run for using this API client.
#
# It should work on both Windows and Linux, but it has not been tested there.
#
###############################################################################

from interface import Interface

client = Interface()

while True:
    command=input('> ')
    if command[:4] == 'exit':
        break
    elif command[:5] == 'state':
        print('-', client)
    elif command[:5] == 'login':
        if command[5:].strip()[:6] == '--help':
            print('- Syntax Options:', '-\t\tlogin {email} {password}', '-\t\tlogin {userid} {password}', sep='\n')
            continue
        try:
            creds = command.split()[1:]
            try:
                creds[1]=int(creds[0])
            except ValueError:
                pass
            if client.login(creds[0], creds[1]):
                print('-', 'Login successful')
            else:
                print('-', 'Login failed')
        except IndexError:
            print('- Syntax Options:', '-\t\tlogin {email} {password}', '-\t\tlogin {userid} {password}', sep='\n')
    elif command[:7] == 'history':
        print(client.get_calculation_history())
    else:
        print('- Unknown command')
print('- Bye')
