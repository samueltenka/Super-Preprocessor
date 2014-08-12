'''
ABOUT:
Literate programming, I think:
    ***declare some integers***
        int a, b, c;
    !!!
To use:
    <<< declare stuff >>>
Starts unravelling at:
    <<< main >>>


FICKLENESS:
Definitions may not nest,
but their bodies may contain Uses.

Redefinitions overwrite.
Technically, closing "***" unnecessary;
code afterward will be overlooked.
New definitions before "!!!" are OK.

Whitespace matters: we parse line-by-line.
"!!!" lines must have only "!!!" and whitespace

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

    <<<declare some integers>>>
    a = b = c = 7;
    <<<do something amazing>>>


    *** declare some integers ***
        int a, b, c;
    !!!

    *** do something amazing ***
        superfunctionyay(a, b, c);
    !!!
'''


code_objects = {}
def define(ident, code):
    if ident not in code_objects:
        code_objects[ident] = code
    else:
        print("ERROR!")
def display_code_objects():
    for ident, code in code_objects.items():
        print(ident + ':')
        for line in code.split('\n'):
            print('\t' + line)


def is_def_begin(line):
    line = line.strip()
    return (len(line) > 3) and (line[:3] == "***")
def is_def_end(line):
    return line.strip() == "!!!"

def learn_from(literate):
    generated = "START\n"
    progress = 0 ## parsed up to here.

    current_id = None
    for line in literate.split('\n'):
        if not line: ## get rid of whitespace
            pass
        elif is_def_begin(line):
            current_id = line.split("***")[1].strip()
            code_objects[current_id] = ""
        elif is_def_end(line):
            current_id = None
        else:
            if current_id:
                code_objects[current_id] += line.strip() + '\n'
            else:
                generated += line + '\n'

    generated += "END\n"
    return generated


def use(generated):
    pass


print(learn_from(TEST_CODE))
display_code_objects()
