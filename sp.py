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
def code_of(ident):
    if ident not in code_objects:
        print("ERROR!")
    elif not code_objects[ident]:
        print("ERROR!")
    else:
        return code_objects[ident][:-1] ## to remove last newline.
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

    return generated


def use(generated):
    outsource = ""
    
    begins = generated.split("<<<")
    ends = [beg.split(">>>") for beg in begins]
    
    alternating = []
    for begs in ends:
        for text in begs:
            alternating.append(text)

    #print(alternating)

    in_ident = False
    for i in alternating:
        if in_ident: ## todo: recurse thru levels (depth-first faster..?)
            outsource += code_of(i)
        else:
            outsource += i
        in_ident = not in_ident
    return outsource


generated = learn_from(TEST_CODE)
#display_code_objects()
print(generated)
print(use(generated))

