# VDict Support for Anki

import os, requests, urllib.request, urllib.parse
from bs4 import BeautifulSoup

# pyrefly: ignore [missing-import]
from aqt import gui_hooks, mw
# pyrefly: ignore [missing-import]
from aqt.editor import Editor
# pyrefly: ignore [missing-import]
from aqt.qt import *
# pyrefly: ignore [missing-import]
from aqt.utils import showInfo
from anki.utils import strip_html
from anki.media import media_paths_from_col_path
from time import sleep


# config
config = mw.addonManager.getConfig(__name__)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.3 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.37', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8','Accept-Language': 'en-US,en;q=0.5'}

# Requires all fields except for 'Expression' to be empty
def generate_all_new():
    query = '"deck:'+config['target_deck_name']+'"'
    for note_id in mw.col.find_notes(query):
        note = mw.col.get_note(note_id)
        empty_keys = note.keys()
        empty_keys.remove(config['field_name_expression'])
        if all(not note[k] for k in empty_keys):
            fill_note_fields_using_vdict(note, note[config['field_name_expression']])
            mw.col.update_note(note)
            sleep(1)
    showInfo("Regenerated fields for all new cards!")

def regenerate_all():
    query = '"deck:'+config['target_deck_name']+'"'
    for note_id in mw.col.find_notes(query):
        note = mw.col.get_note(note_id)
        fill_note_fields_using_vdict(note, note[config['field_name_expression']])
        sleep(1)
        mw.col.update_note(note)
    showInfo("Regenerated fields for all target cards!")

# editor_will_show_context_menu hook
def on_context_menu(editor_webview, menu):
    #
    editor: Editor = editor_webview.editor
    
    # pyrefly: ignore [unknown-name]
    current_field: Optional[int] = editor.currentField

    if current_field is not None:
        for field_index, field_name in enumerate(mw.col.models.field_names(editor.note.model())):
            if field_index == current_field and (field_name == config['field_name_expression']):
                search = strip_html(mw.col.media.strip(editor.note[field_name]))
                if search:
                    # pyrefly: ignore [unknown-name]
                    action = menu.addAction(_(f"VDict Card Generation"))
                    # pyrefly: ignore [unknown-name]
                    qconnect(action.triggered, lambda: fill_note_fields_using_vdict(editor.note, search))

    editor.loadNote()

def organize_meaning(html_def):
    meaning = ""
    for item in html_def:
        part_of_speech = item.find(class_ = 'meaning-value').get_text()
        defs = ""
        for x in item.find_all(class_ = 'example'):
            defs = defs + "<li>" + x.get_text() + "</li>"
        meaning = meaning + "<li>" + part_of_speech + "<ul>" + defs + "</ul></li>"
    return "<ol>" + meaning + "</ol>"

def organize_examples(html_def):
    examples = ""
    for item in html_def:
        part_of_speech = item.find(class_ = 'meaning-value').get_text()
        v = ""
        for x in item.find_all(class_ = 'example'):
            v = v + "<li>" + x.get_text() + "</li>"
        examples = examples + "<li>" + part_of_speech + "<ul>" + v + "</ul></li>"
    return examples

def organize_fields(html_def):
    field = ""
    for item in html_def:
        v = item.find(class_ = 'meaning-value').get_text()
        field = field + "<li>" + v + "</li>"
    return "<ul>" + field + "</ul>"

def try_download_image(link, expression):
    media_dir = media_paths_from_col_path(mw.col.path)[0]
    path_to_file = os.path.join(media_dir, os.path.basename(expression + '.png'))
    result = requests.get(link, headers=headers, stream=True)
    result.raise_for_status()
    with open(path_to_file, 'wb+') as file:
        for chunk in result:
            file.write(chunk)

def try_set_audio(note, term):
    media_dir = media_paths_from_col_path(mw.col.path)[0]
    path_to_file = os.path.join(media_dir, os.path.basename(term+".mp3"))
    #add conditional check for file
    note[config['field_name_audio']] = f"[sound:{term}.mp3]"

# fill_note_fields_using jisho.org with given search term
def fill_note_fields_using_vdict(note, search):
    # 
    vdict_search_url = 'https://vdict.com/'
    term = urllib.parse.quote(search.encode('utf8'))
    search_ending = ',4,0,0.' if config['addon_native_language'] == "FRENCH" else ',2,0,0.'
    native_url = vdict_search_url + term + search_ending + 'html#friendly'
    viet_url = vdict_search_url + term + ',3,0,0.html#friendly'
    
    native_HTML = ""
    viet_HTML = ""
    # make url conform to ascii
    try:
        native_response = requests.get(native_url, headers=headers, stream=True)
        native_HTML = native_response.text
        sleep(1)
        viet_response = requests.get(viet_url, headers=headers, stream=True)
        viet_HTML = viet_response.text
    except IOError:
        showInfo("You must have an active internet connection to use automatic card generation.")
        return False

    if not native_HTML:
        return
    if 'alert alert-info mb-4' in native_HTML:
        return

    soup = BeautifulSoup(native_HTML, 'html.parser')
    pho = BeautifulSoup(viet_HTML, 'html.parser')
    soup_fields = [item.get_text().lower() for item in soup.find_all(class_='word-type mb-2')]
    soup_values = [item.find_all(class_ = "meaning mb-3") for item in soup.find_all(class_="meanings-list")]
    pho_values = [item.find_all(class_ = "meaning mb-3") for item in pho.find_all(class_="meanings-list")]
    
    native_dict = dict(zip(soup_fields, soup_values))
    viet_dict = dict(zip(soup_fields, pho_values))

    native_meaning = organize_meaning(native_dict['definition'])
    try_set_field(note, config['field_name_meaning'], native_meaning)
    viet_meaning = organize_meaning(viet_dict['definition'])
    try_set_field(note, config['field_name_meaning-VT'], viet_meaning)

    examples = organize_examples(native_dict['examples']) if 'examples' in soup_fields else organize_examples(native_dict['usage examples'])
    try_set_field(note, config['field_name_examples'], examples)

    if 'synonyms' in soup_fields:
        synonyms = organize_fields(viet_dict['synonyms'])
        try_set_field(note, config['field_name_synonyms'], synonyms)

    usage = organize_fields(native_dict['usage']) if 'usage' in soup_fields else ""
    adv_usage = organize_fields(native_dict['advanced usage']) if 'advanced usage' in soup_fields else ""
    try_set_field(note, config['field_name_notes'], usage + adv_usage)

    image_link = (soup.find("img", class_="illustration-img")).get("data-original-url")
    if image_link:
        try_download_image(image_link, search)
        note[config['field_name_visual']] = f'<img src="{term}.png">'

    try_set_audio(note, term) 
    return

# try_set_field 'field_name' to given value
def try_set_field(note, field_name, value):
    #
    if len(value) > 0:
        try:
            note[field_name] = value
        except KeyError:
            pass

# try_set_all_fields with 'field_name' to given values in value_list
def try_set_all_field(note, field_name, value_list):
    #
    for index, value in enumerate(value_list):
        suffix = str(index) if index > 0 else ""
        try_set_field(note, field_name + suffix, ', '.join(value))

# try_clear_field 'field_name'
def try_clear_field(note, field_name):
    #
    try:
        note[field_name] = ""
    except KeyError:
        pass

# editor_will_show_context_menu hook
gui_hooks.editor_will_show_context_menu.append(on_context_menu)

# add menu items
submenu = mw.form.menuTools.addMenu("VDict Generator")

# pyrefly: ignore [unknown-name]
do_generate_new = QAction("generate all new", mw)
do_generate_new.triggered.connect(generate_all_new)
submenu.addAction(do_generate_new)

# pyrefly: ignore [unknown-name]
do_regenerate_all = QAction("(re)generate all", mw)
do_regenerate_all.triggered.connect(regenerate_all)
submenu.addAction(do_regenerate_all)


