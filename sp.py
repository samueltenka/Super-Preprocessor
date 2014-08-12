'''
ABOUT:
Literate programming, I think:
    ***declare some integers***
        int a, b, c;
    !!!
To use:
    <<< declare stuff >>>
For include-type stuff, start with:
    ***! only do this once***


FICKLENESS:
Definitions may not nest,
but their bodies may contain Uses.

Redefinitions would overwrite, but error checking in "define(ident, code)".
Technically, closing "***" unnecessary;
code afterward will be overlooked.
New definitions before "!!!" are OK.

Whitespace matters: we parse line-by-line.
"!!!" lines must have only "!!!" and whitespace
But identifiers are stripped, so <<<a>>> is like <<< a >>>.

Recursion breaks program:
    <<<A>>>
    *** A ***
        <<< B >>>
    !!!
    *** B ***
        <<< A >>>
    !!!
'''

import re



code_objects = {}
def reset():
    code_objects = {}
def make(ident, once=False, occurrences=0):
    if not ident:
        print("ERROR: identifiers may not be empty!")
    elif ident in code_objects:
        print("ERROR: redefinitions, including of <<<", ident,">>> not allowed!")
    else:
        code_objects[ident] = ["", once, occurrences]
def add(ident, line):
    if ident not in code_objects:
        print("ERROR: identifier <<<", ident, ">>> not found.")
    else:
        code_objects[ident][0] += line + '\n'
def code_of(ident):
    if ident not in code_objects:
        print("ERROR: identifier <<<", ident, ">>> not found.")
    else:
        code, once, occurrences = code_objects[ident]
        if (not once) or (occurrences == 0):
            code_objects[ident][2] += 1;
            return code.strip() ## to remove last newline.
        else: ## already included a "once".
            return ""
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
            once = False
            if current_id and current_id[0] == '!':
                current_id = current_id[1:].strip()
                once = True
            make(current_id, once)
        elif is_def_end(line):
            current_id = None
        else:
            if current_id:
                add(current_id, line)
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


def preprocess(sources, dest):
    reset()
    generateds = []
    for s in sources:
        pps = open(s, mode='r').read()
        generateds.append(learn_from(pps))

    out = ""
    for g in generateds:
        out += translate(g)
    open(dest, mode='w').write(out)
        


preprocess(["source.ppc"], "dest.c")
