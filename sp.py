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

Redefinitions would overwrite, but error checking in "define(ident, code)".
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

import re


TEST_CODE = \
'''
    <<<declare some integers>>>
    a = b = c = 7;
    <<<do something amazing>>>

    *** declare special ***
        int special;
    !!!
    *** declare some integers ***
        int a, b, c;
        <<< declare special >>>
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
        print("ERROR: redefinitions, including of <<<", ident,">>> not allowed!")
def code_of(ident):
    if ident not in code_objects:
        print("ERROR: identifier <<<", ident, ">>> not found.")
    else:
        return code_objects[ident].strip() ## to remove last newline.
def display_code_objects():
    for ident, code in code_objects.items():
        print(ident + ':')
        for line in code.split('\n'):
            print('\t' + line, end="")
        print()


def is_def_begin(line):
    line = line.strip()
    return (len(line) > 3) and (line[:3] == "***")
def is_def_end(line):
    return line.strip() == "!!!"

def learn_from(literate):
    generated = ""

    current_id = None
    for line in literate.split('\n'):
        if not line: ## get rid of blank lines
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

    return generated


def must_translate(generated):
    return "<<<" in generated
def translate(generated):
    outsource = ""

    alternating = re.split("<<<|>>>", generated) ## multi-deliiter split
    
    in_ident = False
    for i in alternating:
        if in_ident:
            translation = code_of(i.strip())
            if must_translate(translation): ## recurse thru levels (depth-first faster..?)
                translation = translate(translation)
            outsource += translation
        else:
            outsource += i
        in_ident = not in_ident
    return outsource
    
        
generated = learn_from(TEST_CODE)
#display_code_objects()
print(generated)
print(translate(generated))

