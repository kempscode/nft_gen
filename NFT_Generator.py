from msilib.schema import Icon
from turtle import color
import PySimpleGUI as sg
import os
from PIL import Image
from itertools import product
import time
import random


folders_dict = {}
probability_dict = {}

# ----------- MAIN FUNCTIONS ---------------------------------------

def folders_unpack(main_dir, img_folder):

    os.chdir(main_dir)

    all_folders = []

    for folders, subfolders, files in os.walk(img_folder):
        all_folders.append(subfolders)

    for x in all_folders[0]:
        folders_dict[x] = []
   
    os.chdir(img_folder)

    for i in folders_dict.keys():
        for folders, subfolders, files in os.walk(i):
            folders_dict[i] = files

    
    return folders_dict 
    
def comb_creating(probability_dict,combinations_amount):
    
    combintaion = []
    all_combinations = []
    
    number_of_current_combination = 0

    while number_of_current_combination < combinations_amount:
        for folder in probability_dict:
            element_for_combination = random.choice(probability_dict[folder])
            
            (element_name, percent_chance, not_featuring_chance) = element_for_combination
            if percent_chance < 100:
                if not_featuring_chance == 'NO':
                    while True:
                        if random.randrange(0,100) < percent_chance:
                            combintaion.append(element_name)
                            break
                        else:
                            element_for_combination = random.choice(probability_dict[folder])
                            (element_name, percent_chance, not_featuring_chance) = element_for_combination
                else:
                    if random.randrange(0,100) < percent_chance:
                        combintaion.append(element_name)
                    else:
                        continue
                    
            else:
                combintaion.append(element_name)
        
        
        if number_of_current_combination < combinations_amount:
            if combintaion in all_combinations:
                combintaion = []
                continue        
            else:
                all_combinations.append(combintaion)
                combintaion = []
                number_of_current_combination += 1
                
        else:
            break

    return all_combinations

def images_compiling(folders_dict, comb_list, output_folder, img_custom_name):
    
    #---------- Taking the 1st image from the library to determine the size --------
    sample_img_folder = list(folders_dict.keys())[0]
    sample_img_name = list(folders_dict.values())[0][0]
    sample_img = Image.open(f'{img_folder}\{sample_img_folder}\{sample_img_name}')
    #-------------------------------------------------------------------------------
        
    current_img_num = 0
    res_img = Image.new(mode='RGBA', size = sample_img.size, color='blue')
    gen_name_suf = 1
    
    list_of_folders = list(folders_dict.keys()) 
    
    progress_bar_num = 0
    current_img_num = 0
    
    for comb in comb_list:
        event, values = window.read(timeout=0, timeout_key='timeout') 
        if event == 'Stop':
            window['Stop'].update(disabled = True)
            break
        elif current_img_num >= combinations_amount:
            break
        else:
            pass
        progress_bar_num += 1
        window['-PROGRESS-'].UpdateBar(progress_bar_num + 1)
        for element in comb: 
            for folder_name in list_of_folders:
                try:
                    source_img = Image.open(f'{img_folder}\{folder_name}\{element}')
                    res_img.paste(source_img, (0,0), mask=source_img)
                except:
                    continue
        res_img.save(f'{output_folder}\{img_custom_name}_{gen_name_suf}.png')
        res_img.close()
        res_img = Image.new(mode='RGBA', size = sample_img.size, color='blue')
        gen_name_suf += 1
        current_img_num += 1
            
                
# ---------------------PySimpleGUI----------------------------------

layout = [
    [sg.Button('Choose images folder', key = "-MAINDIR-", size = (20,2)),  
    sg.Push(), sg.StatusBar('', key = '-STATUS_1-', size=(20,1))],
    [sg.Button('Choose output folder', key = '-OUTPUT-', size = (20,2)), 
    sg.Push(), sg.StatusBar('', key = '-STATUS_2-',  size=(20,1))],
    [sg.Button('Choose folders order', key = '-ORDER-', disabled=True)],
    [sg.Button('Choose probabilities', key = '-PROB-', disabled = True)],
    [sg.Text('Please, input your NFTs name here:'), sg.Input(key = '-INPUT-')],
    [sg.Button('OK', disabled=True, key = '-OK-'), sg.Text('Number of generated images:'), sg.Input(enable_events = True, default_text = '0', key = '-INPUT_2-')],
    [sg.Button('Generate NFTs!', key = '-GENERATE-', disabled = True)],
    [sg.ProgressBar(max_value = 100, orientation = 'h', size = (200,10), key = '-PROGRESS-')],
   [sg.Button('Stop', visible = False, disabled = False),sg.Text('DONE!', visible = False, key = '-DONE-')]
]

window = sg.Window('NFT generator', layout, size = (500,300), icon = r'C:\Users\Workstation\Desktop\My_Phyton_projects\Project_#1\img\bound_selection_icon_227440.ico')

condition_1 = False
condition_2 = False
condition_3 = False
condition_4 = False

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    
    if event == '-MAINDIR-':
        img_folder = sg.popup_get_folder('img_folder', no_window=True)
        if img_folder == '':
            continue
        else:
            img_folder_divided = img_folder.split('/')
            img_folder_divided.pop(-1)
            main_dir ='/'.join(img_folder_divided)
            window['-STATUS_1-'].update(img_folder)
            
            folders_dict = folders_unpack(main_dir, img_folder)
            
        if img_folder:
            condition_1 = True
        else:
            condition_1 = False
    
    if event == '-OUTPUT-':
        output_folder = sg.popup_get_folder('output', no_window=True)
        window['-STATUS_2-'].update(output_folder)
        if output_folder:
            condition_2 = True
        else:
            condition_2 = False

#------------------------------ Window #2 (folders order) ----------------------------------------------------    
    if event == '-ORDER-':

        layout_2 = [[sg.Radio('Order is fine!', group_id = 1, circle_color = 'green', key = '-WARNING-')],
            [sg.Button('Confirm', key = '-CONFIRM_ORDER_BUTTON-', disabled=False)]]
        list_of_folders_for_order = []
        list_of_folders_ordered = []
        folders_dict_ordered = {}

        spin_range = range(1,len(folders_dict.keys()) + 1)
        spin_range_divided = []
    
        all_spin_values = list(spin_range)
    
        spin_dict = {}
        
        for folder_number in spin_range:
            spin_range_divided.append([folder_number])


        spin_init_value = 1
        for x in list(folders_dict.keys()):
            list_of_folders_for_order.append(x)
            list_of_folders_ordered.append('temp')
            layout_2.insert(0, [sg.Text(x), sg.Push(), sg.Spin(spin_range_divided, initial_value = spin_init_value, readonly = True, s= (15,2), key = x + '-SPIN-', enable_events=True) ])
            
            spin_dict[x + '-SPIN-'] = spin_init_value
            spin_init_value += 1
            
        
        window_2 = sg.Window('Folders order', layout_2, modal = True, auto_size_buttons=True, auto_size_text=True, resizable=True)

        while True:
            event_2, values_2 = window_2.read()
            if event_2 == sg.WINDOW_CLOSED:
                break
            
            if '-SPIN-' in event_2:
                
                spin_dict[str(event_2)] = int(values_2[event_2])
                
                if len(set(spin_dict.values())) != len(all_spin_values):
                    window_2['-WARNING-'].update(circle_color = 'red')
                    window_2['-WARNING-'].update(text = 'Doublicated order!')
                    window_2['-CONFIRM_ORDER_BUTTON-'].update(disabled=True)
                else:
                    window_2['-WARNING-'].update(circle_color = 'green')
                    window_2['-WARNING-'].update(text = 'Order is fine!')
                    window_2['-CONFIRM_ORDER_BUTTON-'].update(disabled=False)

            if event_2 == '-CONFIRM_ORDER_BUTTON-':
                folders_dict_ordered = {}
                probability_dict = {}
                for y in list_of_folders_for_order:
                    list_of_folders_ordered[int(values_2[y + '-SPIN-']) - 1] = y
                for z in list_of_folders_ordered:
                    folders_dict_ordered[z] = folders_dict[z]
                    print(f'FOLDERS OREDERED:  {folders_dict_ordered}')
                for i in folders_dict_ordered.keys():
                    probability_dict[i] = [(i2, 100, 0) for i2 in folders_dict_ordered[i]] 
                    print(f'PROB DICT ORDERED:  {probability_dict}')
                window_2['-CONFIRM_ORDER_BUTTON-'].update(disabled=True)
                condition_3 = True
    
#--------------------- Windows #3 & #4 (probabilities) -----------------------------------------------------------

    if event == '-PROB-':
        
        
        layout_3 = [[sg.Button('Confirm', key = '-CONFIRM_PROB_BUT-')]]
        layout_4 = [[sg.Button('Confirm')]]

        
        list_of_elements_in_folder = []
        for x in list(folders_dict.keys()):
            layout_3.insert(0, [sg.Text(x)])
            for element in list(probability_dict[x]):
                (element_name, element_probability, not_featuring_chance) = element
                if not_featuring_chance == 0:
                    list_of_elements_in_folder.append([element_name, element_probability, 'NO'])
                else:
                    list_of_elements_in_folder.append([element_name, element_probability, 'YES'])
            layout_3.insert(1, [sg.Table(list_of_elements_in_folder,['Element', 'Probability, %', 'Possibility of non-appearance'], num_rows = 3, bind_return_key=True, key = x + '-PROB_TABLE-', justification='center', auto_size_columns=False, col_widths=[15,15,15], tooltip='Double click to open')])
            list_of_elements_in_folder = []
            

        window_3 = sg.Window('Elements probabilyties', layout_3, resizable=True, auto_size_buttons=False, modal = True)
        
        while True:
            event_3, values_3 = window_3.read()
            if event_3 == sg.WINDOW_CLOSED:
                break
            if '-PROB_TABLE-' in event_3:
                if values_3[event_3] == []:
                    pass
                else:
                    element_index = values_3[event_3][0]
                    elements_folder = event_3.replace('-PROB_TABLE-','')
                    
                    (element_name, element_probability, not_featuring_chance) = probability_dict[elements_folder][(values_3[event_3])[0]]

                    img_name = folders_dict[elements_folder][values_3[event_3][0]]
                    image_path = img_folder + '/' + str(elements_folder) + '/' + img_name
                    image = Image.open(img_folder + '/' + str(elements_folder) + '/' + img_name)
                    
                    window_4 = sg.popup=sg.Window(img_name + ' probability', [[sg.Image(image_path, subsample=2, key='-IMAGE_PROB-', enable_events=True)], 
                    [sg.T('Probability'), sg.Slider(range = (0,100), default_value = element_probability, orientation = 'h', size = (25,15), key = '-PROB_SLIDER-'), sg.Text('Current value: '+ str(element_probability), key = '-CURRENT_PROB_VALUE-')], 
                    [sg.Checkbox('A chance, that element won`t be featured at all', key = '-UNFEATURED_CHANCE-', default=not_featuring_chance)],
                    [sg.Button('Confirm', key = '-CONFIRM_PROB-', disabled = False)]], modal = True)

                    event_4, values_4 = window_4.read()

                    if event_4 == '-CONFIRM_PROB-':
                        if values_4['-UNFEATURED_CHANCE-'] == True:
                            probability_dict[elements_folder][element_index] = (img_name, values_4['-PROB_SLIDER-'], 1)
                            window_3[event_3].update(values = [[img_name, values_4['-PROB_SLIDER-'], 'YES']])
                            window_4['-CONFIRM_PROB-'].update(disabled = True)
                            window_4.close()
                        else:
                            probability_dict[elements_folder][element_index] = (img_name, values_4['-PROB_SLIDER-'], 0)
                            window_3[event_3].update(values = [[img_name, values_4['-PROB_SLIDER-'], 'NO']])
                            window_4['-CONFIRM_PROB-'].update(disabled = True)
                            window_4.close()
            
            if event_3 == '-CONFIRM_PROB_BUT-':
                window_3.close()
                    
#---------------------------- MAIN LOGIC --------------------------------------------------------------------------

    if event == '-INPUT_2-':
        window['-OK-'].update(disabled = False)
        combinations_amount = int(values['-INPUT_2-'])

    if event == '-OK-':
        condition_4 = True

    if condition_1:
         window['-ORDER-'].update(disabled = False)

    if condition_3:
        window['-PROB-'].update(disabled = False)

    if condition_1 and condition_2 and condition_3 and condition_4:   
        window['-GENERATE-'].update(disabled = False)
    else:
        window['-GENERATE-'].update(disabled = True)
    
    if event == '-GENERATE-':
        
        comb_list = comb_creating(probability_dict, combinations_amount)
        bar_max_value = combinations_amount  
        window['-PROGRESS-'].UpdateBar(0, bar_max_value)
        window['Stop'].update(visible = True)
        img_custom_name = values['-INPUT-']   
        images_compiling(folders_dict, comb_list, output_folder, img_custom_name)
        window['-DONE-'].update(visible = True)    
    
window.close()