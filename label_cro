import os
import time
import json
import uuid


start_time = time.time()
elapsed_time_all = 0




def get_files():
    found = False
    while not found:
        files = os.listdir()
        val = input("Enter the name of your annotation folder (folder name with the config): ")
        if val in files:
            found = True
        else:
            print("I didn't find a folder with such a name, sorry")
    return val

# VAL CORRESPONDS TO FOLDER NAME
val = get_files()
files = os.listdir(val)
if 'schema.txt' not in files:
    print("I didn't find the configuration file schema.txt")
    time.sleep(3.)
    exit()
if 'xac_cro_dataset.jsonl' not in files:
    print("I didn't find the dataset dataset.jsonl.")
    time.sleep(3.)
    exit()

# LOAD THE CONFIG
X = [[_ for _ in x.split(' ') if len(_)>0] for x in open(os.path.join(val, 'schema.txt'), 'r', encoding = 'utf-8').read().split('\n') if len(x)>0] 
print(X)
X = [a for a in X if len(a)>0]
print(X)
X = {x[0]:x[1] for x in X}
print(X)

print(X)
assert 'TYPE' in X
assert X['TYPE'] in {'num', 'class'}
for _, __ in X.items():
    assert __ != 'R'

# LOAD THE DATASET
if 'dataset_modified.jsonl' not in files:
    dics = [json.loads(x) for x in open(os.path.join(val, 'xac_cro_dataset.jsonl'), 'r', encoding = 'utf-8').read().split('\n') if len(x)>0]
    for i, dic in enumerate(dics):
        dics[i]['id'] = str(uuid.uuid4())
    with open(os.path.join(val, 'dataset_modified.jsonl'), 'w', encoding = 'utf-8') as f:
        text = '\n'.join([json.dumps(dic) for dic in dics])
        f.write(text)
if 'annotations' not in files:
    open(os.path.join(val, 'annotations'), 'w')
    if 'timelog' not in files:
        open(os.path.join(val, 'timelog'), 'w')

# LOAD THE CORRECT DATASET
dics = [json.loads(x) for x in open(os.path.join(val, 'dataset_modified.jsonl'), 'r', encoding = 'utf-8').read().split('\n') if len(x)>0]

id_annotation = ""
while len(id_annotation)==0:
    print("Enter your last name without spaces or accent or tabs:")
    id_annotation = input().replace(' ', '_').replace('/', '_').replace('\\', '_').replace('-', '_')
    
    def highlight_text(text, highlighted_words):
        """Returns the input text with the highlighted words highlighted using ANSI escape codes"""
        for word in highlighted_words:
            text = text.replace(word, "\033[1;31m{}\033[0m".format(word))
        return text
    
# Prompt user to enter highlighted words
highlighted_words = input("Enter highlighted words separated by a space: ").split()


if X['TYPE']=='class':
    classes = [x for x in list(X.keys()) if x != 'TYPE']
    hotkeys = [X[k] for k in classes]
    possible_hotkeys = set(hotkeys+['R'])
    file_to_write = os.path.join(val, 'annotations')
    file_to_write_timelog = os.path.join(val, 'timelog')
    rules = "KEYS : R = RETURN (go back to precedent text) | "
    for h,k in zip(classes, hotkeys):
        rules += k + " = " + h.upper() + "| "
    annotated = [x.split('\t') for x in open(file_to_write, 'r', encoding = 'utf-8').read().split('\n') if len(x)>0]
    annotated = set([x[0] for x in annotated if x[1]==id_annotation])
    print("You have already annotated {} documents.".format(len(annotated)))
    dics = [x for x in dics if x['id'] not in annotated]
    time.sleep(1.)


    i = 0
    while i < len(dics):
        os.system('clear')
        elapsed_time = time.time() - start_time
        elapsed_time_all += elapsed_time
        print("Text {a}/{b}".format(a=i + 1, b=len(dics)))
        print(rules)
        print('#####################################################')
        highlighted_text = highlight_text(dics[i]['text'], highlighted_words)
        print(highlighted_text)
        print('#####################################################')
        R = input("Enter your annotation (press 'R' to go back): ")

        if R not in possible_hotkeys:
            continue
        elif R == 'R':
            if i > 0:
                i -= 1
            continue
        else:
            open(file_to_write, 'a', encoding='utf-8').write(
                "{_id}\t{_id_annotation}\t{_annotation}\n".format(_id=dics[i]['id'], _id_annotation=id_annotation,
                                                                  _annotation=R))
        with open(file_to_write_timelog, 'a', encoding='utf-8') as f:
            f.write(
                "{_time}\t{_id_annotation}\t{_annotation}\t{_elapsed_time}\t{_elapsed_time_all}\n".format(_time=time.time(), _id_annotation=id_annotation, _annotation=R, _elapsed_time=elapsed_time, _elapsed_time_all=elapsed_time_all))
        i += 1

        
elif X['TYPE'] == 'num':
    file_to_write_annotations = os.path.join(val, 'annotations')
    file_to_write_timelog = os.path.join(val, 'timelog')
    rules = "R for RETURN (go back to precedent text), N for None (if the answer is not in the text), or numeric answer"
    annotated = [x.split('\t') for x in open(file_to_write_annotations, 'r', encoding = 'utf-8').read().split('\n') if len(x) > 0]
    annotated = set([x[0] for x in annotated if x[1] == id_annotation])
    print("You have already annotated {} documents.".format(len(annotated)))
    dics = [x for x in dics if x['id'] not in annotated]
    time.sleep(1.)

    i = 0
    while i < len(dics):
        os.system('cls')
        elapsed_time = time.time() - start_time
        elapsed_time_all += elapsed_time
        print("Text {a}/{b}".format(a=i, b=len(dics)))
        print(rules)
        print('#####################################################')
        highlighted_text = highlight_text(dics[i]['text'], highlighted_words)
        print(highlighted_text)
        print('#####################################################')
        start_time = time.time()
        R = input()
        if R == 'R':
            if i > 0:
                i -= 1
            continue
        if R != 'N':
            try:
                R = float(R)
            except ValueError:
                continue
        with open(file_to_write_annotations, 'a', encoding='utf-8') as f:
            f.write("{_id}\t{_id_annotation}\t{_annotation}\n".format(_id=dics[i]['id'], _id_annotation=id_annotation, _annotation=R))
        with open(file_to_write_timelog, 'a', encoding='utf-8') as f:
            f.write(
                "{_time}\t{_id_annotation}\t{_annotation}\t{_elapsed_time}\t{_elapsed_time_all}\n".format(_time=time.time(), _id_annotation=id_annotation, _annotation=R, _elapsed_time=elapsed_time, _elapsed_time_all=elapsed_time_all))
        i += 1
       


os.system('clear')

print("Annotation terminée, merci de renvoyer l'ensemble du dossier pour évaluation.")
        
