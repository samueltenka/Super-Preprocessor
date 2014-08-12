'''
Literate programming, I think:
    ***declare some integers***
        int a, b, c;
    !!!
To use:
    <<< declare stuff >>>
Starts unravelling at:
    <<< main >>>

Definitions may not nest,
but their bodies may contain Uses.

Recursion breaks program:
    *** A ***
        <<< B >>>
    !!!
    *** B ***
        <<< A >>>
    !!!
'''



TEST_CODE = \
'''
*** ident ***
hey
*** iden**t ***
'''


code_objects = {}
def define(identifier, code):
    if identifier not in code_objects:
        code_objects[identifier] = code
    else:
        print("ERROR!")


def is_def_begin(line):
    line = line.strip()
    return (len(line) > 3) and (line[:3] == "***")


def learn_from(literate):
    generated = ""
    progress = 0 ## parsed up to here.
    
    lines = literate.split('\n')
    for line in lines:
        if is_def_begin(line):
            ident = line.split("***")[1]
            print(ident)
        else:
            generated += line + '\n'



learn_from(TEST_CODE)
