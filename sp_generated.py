code_objects = {}
def reset():
    code_objects = {}
def make(identifier, once=False, occurrences=0):
    if not identifier:
        print("ERROR: identifiers may not be empty!")
        return
    if identifier in code_objects:
        print("ERROR: redefinitions, including of <<<", identifier,">>> not allowed!")
        return
    code_objects[identifier] = ["", once, occurrences]
def add(identifier, line):
    if identifier not in code_objects:
        print("ERROR: identifier <<<", identifier, ">>> not found.")
        return
    code_objects[identifier][0] += line+'\n'
def code_of(identifier):
    if identifier not in code_objects:
        print("ERROR: identifier <<<", identifier, ">>> not found.")
        return
    code, once, occurrences = code_objects[identifier]
    if (not once) or (occurrences == 0):
        code_objects[identifier][2] += 1
        return code
    else: ## already included a "once".
        return ""
def display_code_objects():
    for identifier, (code, _, _) in code_objects.items():
        print(identifier + ':')
        for line in code.split('\n')[:-1]:
            print('\t.' + line)
def whitespace_of(line):
    ws_length = len(line) - len(line.lstrip())
    return line[:ws_length]
def equiv_spaces_of(whitespace, spaces_per_tab=4):
    if len(whitespace) == 1:
        return (spaces_per_tab if whitespace=='\t' else 1)
    return whitespace.count(' ') + \
           whitespace.count('\t') * spaces_per_tab
def bump_down(line, whitespace):
    spaces_so_far = 0
    goal = equiv_spaces_of(whitespace)
    while line and \
          (line[0] in ' \t') and \
          (spaces_so_far < goal):
        spaces_so_far += equiv_spaces_of(line[0])
        line = line[1:]
    return line
def bump_up(code, whitespace):
    if not code: return ""
    return "".join(whitespace+line+'\n' for line in code.split('\n') if line)
def is_def_begin(line):
    line = line.strip()
    return (len(line) > 3) and (line[:3] == "***")
def is_def_end(line):
    return line.strip() == "!!!"
def learn_from(literate):
    generated = ""
    current_id = None
    def_whitespace = ""
    on_def_first_line = False
    for line in literate.split('\n'):
        if not line:
            continue
        if is_def_begin(line):
            current_id = line.split("***")[1]
            once = False
            if current_id and current_id[0] == '!':
                current_id = current_id[1:]
                once = True
            current_id = current_id.strip()
            make(current_id, once)
            on_def_first_line = True
        elif is_def_end(line):
            current_id = None
        else:
            if current_id:
                if on_def_first_line:
                    def_whitespace = whitespace_of(line)
                    on_def_first_line = False
                add(current_id, bump_down(line, def_whitespace))
            else:
                generated += line+'\n'
                
    return generated
def must_translate(generated):
	return "<<<" in generated
def is_use(line):
	line = line.strip()
	return (len(line) > 3) and (line[:3] == "<<<")
def translate(generated):
	outsource = ""
	for line in generated.split('\n'):
		if not line:
		    continue
		elif is_use(line):
			identifier = line.replace("<<<", "").replace(">>>", "").strip()
			T = code_of(identifier)
			if must_translate(T): ## depth-first faster, since must_translate is expensive over large chunks
				T = translate(T)
			outsource += bump_up(T, whitespace_of(line))
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
    f = open(dest, mode='w')
    f.write("")
    f.close()
    dest_file = open(dest, mode='a')
    for g in generateds:
    	dest_file.write(translate(g))
while True:
    destination = input("destination: ")
    sources = []
    s = input("next source: ")
    while s:
        sources.append(s)
        s = input("next source: ")
    print("OK, I'll weave", destination, "from:")
    for i in range(len(sources)):
        print('\t' + str(i) + ". " + sources[i])
    satisfied = (input("satisfied? (y/n) ") == 'y')
    while not satisfied:
        new_dest = input("correct destination: ")
        if new_dest:
            dest = new_dest
        src_index = input("which source to change (#): ")
        while src_index:
            correct_src = input("correct source: ")
            if correct_src:
                sources[int(src_index)] = correct_src
                print("replaced.")
            else:
                del sources[int(src_index)]
                print("deleted.")
            src_index = input("which source to change (#): ")
        new_source = input("source to add: ")
        while new_source:
            sources.append(new_source)
            new_source = input("source to add: ")
        print("OK, I'll weave", destination, "from:")
        for i in range(len(sources)):
            print('\t' + str(i) + ". " + sources[i])
        satisfied = (input("satisfied? (y/n) ") == 'y')
    preprocess(sources, destination)
    print("tada!")
    
