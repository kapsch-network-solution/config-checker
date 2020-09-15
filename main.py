import functions
import os
import yaml
import json
import sys
from netmiko import ConnectHandler

functions.banner()

#get command line arguments
options={}
options = functions.func_get_arguments()

#load yaml file with baseline config
baseline_yaml_file = open(options['baseline_yaml'])
baseline_config = yaml.full_load(baseline_yaml_file)

data = {}

# execute directory/offline mode 
if "directory" in options:

    data["FILE"] = {}
    # get file list in directory
    config_list= os.listdir(options['directory'])

    # loop through config files
    for config in config_list:
        file = options['directory'] + "\\" + config

        # open file and read content
        with open(file) as f_obj:
            content = f_obj.read()

            #check and print data
            data["FILE"][config] = functions.func_check_data(content,baseline_config,options)
            f_obj.close()

# execute online/ssh mode
elif "connection_yaml" in options:

    # load device connection data
    device_file = open(options['connection_yaml'])
    devices=yaml.full_load(device_file)

    data["DEVICE"] = {}
    show_command_output = {}

    # loop through devices 
    for device in devices['device']:

        
        print("Connecting to " + device +" ("+devices['device'][device]['ip']+") ...")
       

        #try:
        if True:
            con_device = ConnectHandler(
                device_type=devices['device'][device]['device_type'], 
                ip=devices['device'][device]['ip'], 
                username=devices['device'][device]['username'], 
                password=devices['device'][device]['password'],
                secret=devices['device'][device]['secret']
            )
            con_device.enable()

            content = con_device.send_command("show running-config")
        
            if "show_commands" in baseline_config:
                for show_commands in baseline_config['show_commands']:
                    show_command_output[show_commands]=con_device.send_command("show " + show_commands)
                    
            con_device.disconnect()

            #check and print data
            data["DEVICE"][device] = functions.func_check_data(content,baseline_config,options)
            data["DEVICE"][device]["SHOW_COMMANDS"] = functions.func_check_show(show_command_output,baseline_config,options)

            print("     Done ...")

        #except:
        #    print("     Something went wrong. Maybe node is not reachable")

else:    
    print("Unknown Error --> you should never see this")



# export json data if possible
if "reporting" in options:
    #print(options['reporting'])
    if options['reporting']!=False:
        with open(options["reporting"], 'w') as outfile:
            json.dump(data, outfile)

# print data
#functions.func_print_database(data)