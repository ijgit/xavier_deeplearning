import PySimpleGUI as sg
import glob
import os
import io
from PIL import Image

# sg.theme('DarkAmber')  # No gray windows please!

# STEP 1 define the layout
file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("All files (*.*)", "*.*")]
layout = [
    [sg.Text('1: safe / 2: danger / 3: pass')],
    [sg.Input(), sg.Button('Select Path')],

    [sg.Image(key="-IMAGE-")],
    [sg.Input(), sg.Button('Input')],
]

#STEP 2 - create the window
window = sg.Window('My new window', layout, grab_anywhere=True)
img_idx = 0

# STEP3 - the event loop
while True:
    # Read the event that happened and the values dictionary
    event, values = window.read()
    if event == 'Select Path':
        print(event, values)
        root_path = values[0]
        data_dir = f'{root_path}\data'
        output_safe_dif = f'{root_path}\park_safe'
        output_danger_dif = f'{root_path}\park_danger'
        img_path_list = glob.glob(f'{data_dir}\**\*')

        if os.path.exists(img_path_list[img_idx]):
            image = Image.open(img_path_list[img_idx])
            image.thumbnail((1000, 1000))
            bio = io.BytesIO()
            image.save(bio, format="PNG")
            window["-IMAGE-"].update(data=bio.getvalue())

    if event == 'Input':
        print(event, values)
        input = values[1]
        filename = os.path.basename(img_path_list[img_idx])
        image = Image.open(img_path_list[img_idx])
        if input == '1':
            image.save(f'{output_safe_dif}\{filename}')
        elif input == '2':
            image.save(f'{output_danger_dif}\{filename}')
        else:
            pass
        if img_idx < len(img_path_list):
            img_idx += 1

        image = Image.open(img_path_list[img_idx])
        image.thumbnail((1000, 1000))
        bio = io.BytesIO()
        image.save(bio, format="PNG")
        window["-IMAGE-"].update(data=bio.getvalue())

    # If user closeddow with X or if user clicked "Exit" button then exit
    if event in (None, 'Exit'):
        break

window.close()
