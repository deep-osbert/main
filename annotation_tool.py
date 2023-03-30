import os
import time
import json
import uuid
import streamlit as st

start_time = time.time()
elapsed_time_all = 0

def get_files():
    found = False
    while not found:
        files = os.listdir()

def highlight_text(text, highlighted_words):
    """Returns the st.text_input text with the highlighted words highlighted using ANSI escape codes"""
    for word in highlighted_words:
        text = text.replace(word, "\033[1;31m{}\033[0m".format(word))
    return text

# Streamlit code starts here
st.title("Annotation Tool")

# VAL CORRESPONDS TO FOLDER NAME
val = st.text_input("Enter the name of your annotation folder (folder name with the config):")

if val:
    found = True
else:
    st.write("I didn't find a folder with such a name, sorry")

id_annotation = st.text_input("Enter the name of the outcome you will label, without spaces or tabs:")

highlighted_words = st.text_input("Enter highlighted words separated by a space: ").split()

# LOAD CONFIGURATION DATA
if val:
    X = [[_ for _ in x.split(' ') if len(_)>0] for x in open(os.path.join(val, 'schema.txt'), 'r', encoding = 'utf-8').read().split('\n') if len(x)>0]
    X = [a for a in X if len(a)>0]
    X = {x[0]:x[1] for x in X}
    st.write(X)
else:
    st.write("Please enter a valid folder name.")

# Load the dataset
if X and 'TYPE' in X:
    try:
        dics = [json.loads(x) for x in open(os.path.join(val, 'dataset_modified.jsonl'), 'r', encoding='utf-8').read().split('\n') if len(x) > 0]
    except FileNotFoundError:
        st.write("Couldn't find the dataset file in the specified folder.")
        dics = None

if X and dics and 'TYPE' in X:
    if X['TYPE'] == 'class':
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
        st.write("You have already annotated {} documents.".format(len(annotated)))
        dics = [x for x in dics if x['id'] not in annotated]
        time.sleep(1.)


        i = 0
        while i < len(dics):
            elapsed_time = time.time() - start_time
            elapsed_time_all += elapsed_time
            st.write("Text {a}/{b}".format(a=i + 1, b=len(dics)))
            st.write(rules)
            st.write('#####################################################')
            highlighted_text = highlight_text(dics[i]['text'], highlighted_words)
            st.write(highlighted_text)
            st.write('#####################################################')
            start_time = time.time()
            R = st.text_input("Enter your annotation (press 'R' to go back): ", key=f"annotation_input_class_{i}_{uuid.uuid4()}")
            if R not in possible_hotkeys:
                continue
            elif R == 'R':
                if i > 0:
                    i -= 1
                open(file_to_write, 'a', encoding='utf-8').write(
                    "{_id}\t{_id_annotation}\t{_annotation}\n".format(_id=dics[i]['id'], _id_annotation=id_annotation, _annotation=R))
                continue
            else:
                open(file_to_write, 'a', encoding='utf-8').write(
                    "{_id}\t{_id_annotation}\t{_annotation}\n".format(_id=dics[i]['id'], _id_annotation=id_annotation, _annotation=R))
            i += 1
            
    elif X['TYPE'] == 'num':
        file_to_write_annotations = os.path.join(val, 'annotations')
        file_to_write_timelog = os.path.join(val, 'timelog')
        rules = "R for RETURN (go back to precedent text), N for None (if the answer is not in the text), or numeric answer"
        annotated = [x.split('\t') for x in open(file_to_write_annotations, 'r', encoding = 'utf-8').read().split('\n') if len(x) > 0]
        annotated = set([x[0] for x in annotated if x[1] == id_annotation])
        st.write("You have already annotated {} documents.".format(len(annotated)))
        dics = [x for x in dics if x['id'] not in annotated]
        time.sleep(1.)

        i = 0
        while i < len(dics):
            elapsed_time = time.time() - start_time
            elapsed_time_all += elapsed_time
            st.write("Text {a}/{b}".format(a=i, b=len(dics)))
            st.write(rules)
            st.write('#####################################################')
            highlighted_text = highlight_text(dics[i]['text'], highlighted_words)
            st.write(highlighted_text)
            st.write('#####################################################')
            start_time = time.time()
            R = st.text_input("Enter your annotation (press 'R' to go back): ", key=f"annotation_input_num_{i}_{uuid.uuid4()}")
            if R == 'R':
                if i > 0:
                    i -= 1
                open(file_to_write_annotations, 'a', encoding='utf-8').write(
                    "{_id}\t{_id_annotation}\t{_annotation}\n".format(_id=dics[i]['id'], _id_annotation=id_annotation, _annotation=R))
                continue
            if R != 'N':
                try:
                    R = float(R)
                except ValueError:
                    continue
            with open(file_to_write_annotations, 'a', encoding='utf-8') as f:
                f.write("{_id}\t{_id_annotation}\t{_annotation}\n".format(_id=dics[i]['id'], _id_annotation=id_annotation, _annotation=R))
            i += 1
            
else:
    st.write("Invalid or missing config file.")

st.write("Annotation terminée, merci de renvoyer l'ensemble du dossier pour évaluation.")
