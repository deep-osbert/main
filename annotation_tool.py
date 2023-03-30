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
    for word in highlighted_words:
        text = text.replace(word, f"\033[1;31m{word}\033[0m")
    return text

# Streamlit code starts here
st.title("Annotation Tool")

val = st.text_input("Enter the name of your annotation folder (folder name with the config):")
id_annotation = st.text_input("Enter the name of the outcome you will label, without spaces or tabs:")
highlighted_words = st.text_input("Enter highlighted words separated by a space: ").split()

if val:
    found = True
else:
    st.write("I didn't find a folder with such a name, sorry")

# Load the configuration data
config_file = os.path.join(val, 'schema.txt')
if os.path.isfile(config_file):
    X = [[_ for _ in x.split(' ') if len(_)>0] for x in open(config_file, 'r', encoding = 'utf-8').read().split('\n') if len(x)>0]
    X = [a for a in X if len(a)>0]
    X = {x[0]:x[1] for x in X}
    st.write(X)
else:
    X = None
    st.write("Please enter a valid folder name.")

# Load the dataset
data_file = os.path.join(val, 'dataset_modified.jsonl')

if os.path.isfile(config_file) and os.path.isfile(data_file):
    X = {x[0]: x[1] for x in [a.split(' ') for a in open(config_file, 'r', encoding='utf-8').read().split('\n') if a]}
    dics = [json.loads(x) for x in open(data_file, 'r', encoding='utf-8').read().split('\n') if x]

    if X and 'TYPE' in X:
        if X['TYPE'] == 'class':
            classes = [x for x in list(X.keys()) if x != 'TYPE']
            hotkeys = [X[k] for k in classes]
            possible_hotkeys = set(hotkeys + ['R'])
            file_to_write = os.path.join(val, 'annotations')
            file_to_write_timelog = os.path.join(val, 'timelog')
            rules = "KEYS : R = RETURN (go back to precedent text) | "
            for h, k in zip(classes, hotkeys):
                rules += k + " = " + h.upper() + "| "

            annotated = set()
            dics_remaining = [x for x in dics if x['id'] not in annotated]

            for i, dic in enumerate(dics_remaining):
                with st.form(key=f"annotation_input_class_{i}_{uuid.uuid4()}"):
                    st.write(f"Text {i + 1}/{len(dics_remaining)}")
                    st.write(rules)
                    st.write('#####################################################')
                    highlighted_text = highlight_text(dic['text'], highlighted_words)
                    st.write(highlighted_text)
                    st.write('#####################################################')
                    R = st.text_input("Enter your annotation (press 'R' to go back):")
                    submit_button = st.form_submit_button("Submit")

                    if submit_button:
                        if R == 'R' and i > 0:
                            i -= 1
                        elif R in possible_hotkeys:
                            open(os.path.join(val, 'annotations'), 'a', encoding='utf-8').write(f"{dic['id']}\t{id_annotation}\t{R}\n")

     
        elif X['TYPE'] == 'num':
            file_to_write_annotations = os.path.join(val, 'annotations')
            file_to_write_timelog = os.path.join(val, 'timelog')
            rules = "R for RETURN (go back to precedent text), N for None (if the answer is not in the text), or numeric answer"
            annotated = [x.split('\t') for x in open(file_to_write_annotations, 'r', encoding='utf-8').read().split('\n') if len(x) > 0]
            annotated = set([x[0] for x in annotated if x[1] == id_annotation])
            st.write("You have already annotated {} documents.".format(len(annotated)))
            dics = [x for x in dics if x['id'] not in annotated]
            time.sleep(1.)
        
            for i, dic in enumerate(dics):
                elapsed_time = time.time() - start_time
                elapsed_time_all += elapsed_time
                st.write(f"Text {i + 1}/{len(dics)}")
                st.write(rules)
                st.write('#####################################################')
                highlighted_text = highlight_text(dic['text'], highlighted_words)
                st.write(highlighted_text)
                st.write('#####################################################')
                start_time = time.time()
                
                with st.form(key=f'annotation_form_{i}_{uuid.uuid4()}'):
                    R = st.text_input("Enter your annotation (press 'R' to go back):")
                    submit_button = st.form_submit_button(label="Submit")
        
                if submit_button:
                    if R == 'R':
                        if i > 0:
                            i -= 1
                    elif R != 'N':
                        try:
                            R = float(R)
                        except ValueError:
                            continue
                    with open(file_to_write_annotations, 'a', encoding='utf-8') as f:
                        f.write(f"{dic['id']}\t{id_annotation}\t{R}\n")



    else:
        st.write("Invalid or missing config file.")
else:
    st.write("Please enter a valid folder name.")

st.write("Annotation terminée, merci de renvoyer l'ensemble du dossier pour évaluation.")
