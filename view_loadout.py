import pandas as pd
import json
import tkinter as tk
from tkinter import filedialog
import os
import os.path
import subprocess

def get_inventory_data_frame_from_json(x):
    """Input is jsonified version of .sav file."""
    things = [{'key1':'WeaponMods', 'key2':"WeaponModDA"}, \
              {'key1':'GrenadeMods', 'key2':"GrenadeModDA"}, \
              {'key1':'Perks', 'key2':'PerkDA'}]
    out = list()
    for thing in things:
        tmp = x['root']['properties']['AutoSave']['Struct']['value']['Struct'][thing['key1']]['Array']['value']['Struct']['value']
        for idx in range(0, len(tmp)):
            # get status and name
            parse_tmp = tmp[idx]['Struct'][thing['key2']]['Object']['value'].split("/")
            name = parse_tmp[6]
            # fix names (split by '.' grab first and split by '_' grab 2
            name = name.split('.')[0].split('_')[2]
            class_ = parse_tmp[5]
            type_ = parse_tmp[4]
            level = tmp[idx]['Struct']['Level']['Byte']['value']['Byte']
            out.append({"class": class_, "type": type_, "name": name, "level":level})

    df = pd.DataFrame(out)
    df = df.sort_values(['type', 'class', 'name'])

    return(df)

if __name__=="__main__":
    root = tk.Tk()
    root.withdraw()
    
    # select file to use with uesave
    appdata_roaming_dir = os.getenv("LOCALAPPDATA")
    crab_locale = os.path.normpath(appdata_roaming_dir + "/CrabChampions/Saved/")
    
    input_file = filedialog.askopenfilename(initialdir= crab_locale)
    output_file = "blah.json"
    my_command = "uesave to-json -i " + input_file + " -o " + output_file

    # call uesave to write out to output file
    subprocess.run(my_command)
    
    with open(output_file) as f:
        x = json.load(f)

    # remove blah.json
    os.remove("blah.json")
    df = get_inventory_data_frame_from_json(x)
    print(df)

    
        
                
