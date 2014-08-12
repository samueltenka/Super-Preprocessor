code_objects = {}
def reset():
    code_objects = {}
def make(ident, once=False, occurrences=0):
    if not ident: print("ERROR: identifiers may not be empty!")
    elif ident in code_objects: print("ERROR: redefinitions, including of <<<", ident,">>> not allowed!")
    else:
        code_objects[ident] = ["", once, occurrences]
def add(ident, line):
    if ident not in code_objects: print("ERROR: identifier <<<", ident, ">>> not found.")
    else:
        code_objects[ident][0] += line+'\n'
def code_of(ident):
    if ident not in code_objects: print("ERROR: identifier <<<", ident, ">>> not found.")
    else:
        code, once, occurrences = code_objects[ident]
        if (not once) or (occurrences == 0):
            code_objects[ident][2] += 1;
            return code
        else: ## already included a "once".
            return ""
def display_code_objects():
    for ident, (code, _, _) in code_objects.items():
        print(ident + ':')
        for line in code.split('\n')[:-1]:
            print('\t.' + line)




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
            current_id = line.split("***")[1]
            once = False
            if current_id and current_id[0] == '!':
                current_id = current_id[1:]
                once = True
            current_id = current_id.strip()
            make(current_id, once)
        elif is_def_end(line):
            current_id = None
        else:
            if current_id:
                add(current_id, line)
            else:
                generated += line+'\n'

    return generated




def must_translate(generated):
    return "<<<" in generated
def is_use(line):
    line = line.strip()
    return (len(line) > 3) and (line[:3] == "<<<")
def whitespace_of(line):
    ws_length = len(line) - len(line.lstrip())
    return line[:ws_length]
def bump_up(code, whitespace):
    if not code: return ""
    return "".join(whitespace+line+'\n' for line in code.split('\n') if line)
def translate(generated):
    outsource = ""

    for line in generated.split('\n'):
        if not line:
            pass
        elif is_use(line):
            ident = line.replace("<<<", "").replace(">>>", "").strip()
            translation = code_of(ident)
            if must_translate(translation): ## recurse thru levels (depth-first faster..?)
                translation = translate(translation)
            outsource += bump_up(translation, whitespace_of(line))
        else:
            outsource += line+'\n'

    return outsource

def preprocess(sources, dest):
    reset()
    generateds = []
    for s in sources:
        pps = open(s, mode='r').read()
        generateds.append(learn_from(pps))

    display_code_objects()
    
    out = ""
    for g in generateds:
        out += translate(g)
    open(dest, mode='w').write(out)
        


preprocess(["source.ppc"], "dest.c")

