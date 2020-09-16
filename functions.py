import os
import sys
import re
import yaml
import json
from prettytable import PrettyTable

def func_check_global_export(content,baseline_config,options):

    dict_global = {}

    if "global_commands" in baseline_config:
        for global_command in baseline_config['global_commands']:
            global_pattern = r"(?m)^"+ global_command

            result = re.search(global_pattern,content)
            if result:
                if options['failed_only'] == False:
                    dict_global[global_command] = {"RESULT": "PASS"}
            else:
                dict_global[global_command] = {"RESULT": "FAIL"}

    return dict_global

def  func_check_interface_export(content,baseline_config,options):
    ###########################################
    # function to parse interface commands
    ###########################################
    dict_type = {}

    #or is not working as it should work
    if ("interface_commands" in baseline_config) or  ("uplink_interface_commands" in baseline_config) :
        
        # defining regex search pattern
        pattern_interface_block = r"(?m)^interface[^!]*"

        # get all interface config blocks
        interfaces = re.findall(pattern_interface_block,content,re.DOTALL)
        
        dict_interfaces = {}
        dict_interfaces_excluded = {}
        dict_interfaces_trunk = {}

        # loop through interface blocks
        for interface in interfaces:
            # get interface name via regex
            interface_name = re.match("interface.*",interface)

            # create dictionaries
            dict_interface = {}
            dict_command = {}
            
            exclude_interface = False
            # check if interface is excluded and set flag
            if ("interface_exclude" in baseline_config):
                for exclude in baseline_config['interface_exclude']:
                    #print("Match: " + exclude + " against " + interface_name[0])
                    if re.findall(exclude,interface_name[0]):
                        #print("Match found")
                        exclude_interface = True
            
            #check if interface is trunk and set flag
            trunk_mode_interface = re.search("switchport mode trunk",interface)
            if trunk_mode_interface:
                trunk_interface = True
            else:
                trunk_interface = False 

            
            # this is where the magic happens
            if exclude_interface:
                if options['failed_only'] == False:
                    dict_interfaces_excluded[interface_name[0][10:]] = {}
                    #break
                
            elif trunk_interface == True:
                for command in baseline_config['uplink_interface_commands']:
                    #check if command is there
                    result = re.search(command,interface)
                    if result:
                        if options['failed_only'] == False:
                            dict_command[command] = {"RESULT": "PASS"}
                    else:
                        dict_command[command] = {"RESULT": "FAIL"}
                dict_interface["TESTS"]=dict_command
                dict_interface["RAW_DATA"]=interface
                dict_interfaces_trunk[interface_name[0][10:]] = dict_interface
                
            else:
                if "interface_commands" in baseline_config:
                    for command in baseline_config['interface_commands']:
                        
                        #check if command is there
                        result = re.search(command,interface)
                        if result:
                            if options['failed_only'] == False:
                                dict_command[command] = {"RESULT": "PASS"}
                        else:
                            dict_command[command] = {"RESULT": "FAIL"}
            
                    # entry in json for each interface
                    dict_interface["TESTS"]=dict_command
                    dict_interface["RAW_DATA"]=interface
                    dict_interfaces[interface_name[0][10:]] = dict_interface
        
        dict_type["ACCESS"]= dict_interfaces
        dict_type["TRUNK"]=dict_interfaces_trunk
        dict_type["EXCLUDED"]= dict_interfaces_excluded
        
    return dict_type

def func_check_data(content,baseline_config,options):
 
    dict_data = {}

    global_dict = func_check_global_export(content,baseline_config,options)
    #print(global_dict)
    
    interface_dict = func_check_interface_export(content,baseline_config,options)
    #print(interface_dict)

    dict_data["GLOBAL"]=global_dict
    dict_data["INTERFACES"]=interface_dict

    return dict_data

def func_get_arguments():
    ###########################################
    # function to get command line arguments
    ###########################################

    i=0
    # define dict to hold options / command line switches
    options={}

    # default values for optional switches
    options['failed_only']=False
    options['reporting']=False

    #parse through arguments and fill citionary with value pairs
    for argument in sys.argv:
        i=i+1
        if argument == "-d":
            options['directory'] = sys.argv[i]
        elif argument == "-b":
            options['baseline_yaml'] = sys.argv[i]
        elif argument == "-c":
            options['connection_yaml'] = sys.argv[i]
        elif argument == "-f":
            options['failed_only']=True
        elif argument == "-r":
            options['reporting']= sys.argv[i]
    

    if "baseline_yaml" not in options:  
        print("-b is mandatory")
        #TODO print available options
        sys.exit()
    else:
        if "connection_yaml" in options:
            return options
        elif "directory" in options:
            return options
        else:    
            print("-d (offline mode) or -c (online mode) is mandatory")
            sys.exit()


def func_check_show(show_command_output,baseline_config,options):
    
    result_show = {}

    if "show_commands" in baseline_config:
        for show_commands in baseline_config['show_commands']:
        
            result_show[show_commands] = {}
            result_show[show_commands]["TESTS"] = {}

  
            for test in baseline_config['show_commands'][show_commands]:
                result = re.findall(test,show_command_output[show_commands],re.DOTALL)
                if result:
                    if options['failed_only'] == False:
                        result_show[show_commands]["TESTS"][test] = { "Result" : "PASS"}
                else:
                    result_show[show_commands]["TESTS"][test]= { "Result" : "FAIL"}

            result_show[show_commands]["RAW_DATA"]=show_command_output[show_commands]

    
    return result_show

def func_check_device_info(device_info):
    info = {}

    #check model number
    result = re.findall("Model Number.*",device_info,re.DOTALL)

    if result:
        model = result[0]
        info["MODEL"] = model[model.rfind(":")+2:]
    else:
        info["MODEL"] = "UNKNOWN"

    return info

def func_print_database(data):

    #print file or device
    for section in data:
        for device in data[section]:
            print("\n############################")
            print("#### "+device)
            
            if data[section][device] == "ERROR":
                print("############################")
                print("Device was offline or other error occured !")
            else:
                print("#### Type: " + data[section][device]["DEVICE_INFO"]["MODEL"])
                print("############################")
                table = PrettyTable()
                table.field_names = ["scope","command","type","result"]

                #print global section
                if "GLOBAL" in data[section][device]:
                    rows=False
                    for section2 in data[section][device]["GLOBAL"]:
                        for command in data[section][device]["GLOBAL"][section2]:
                            table.add_row(["GLOBAL",section2,"GLOBAL",data[section][device]["GLOBAL"][section2][command]])
                            rows=True
                    
                    if rows:
                        table.add_row(["","","",""])
                    

                if "INTERFACES" in data[section][device]:
                    rows=False   
                    for interface_types in data[section][device]["INTERFACES"]:     
                        if interface_types == "EXCLUDED":
                            for interface_name in data[section][device]["INTERFACES"][interface_types]:                           
                                table.add_row([interface_name,"","","EXCLUDED"])
                                rows=True
                        elif interface_types == "ACCESS":
                            for interface_name in data[section][device]["INTERFACES"][interface_types]:
                                for section3 in data[section][device]["INTERFACES"][interface_types][interface_name]:
                                    if section3 == "TESTS":
                                        for commands in data[section][device]["INTERFACES"][interface_types][interface_name][section3]:
                                            table.add_row([interface_name,commands,"ACCESS",data[section][device]["INTERFACES"][interface_types][interface_name][section3][commands]["RESULT"]])
                                            rows=True
                        else:
                            for interface_name in data[section][device]["INTERFACES"][interface_types]:
                                for section3 in data[section][device]["INTERFACES"][interface_types][interface_name]:
                                    if section3 == "TESTS":
                                        for commands in data[section][device]["INTERFACES"][interface_types][interface_name][section3]:
                                            table.add_row([interface_name,commands,"TRUNK",data[section][device]["INTERFACES"][interface_types][interface_name][section3][commands]["RESULT"]])
                                            rows=True
                    
                    if rows: 
                        table.add_row(["","","",""])

                if "SHOW_COMMANDS" in data[section][device]:
                    
                    for show_commands in data[section][device]["SHOW_COMMANDS"]:
                        for sections in data[section][device]["SHOW_COMMANDS"][show_commands]:
                            
                            if sections == "TESTS":
                                for test in data[section][device]["SHOW_COMMANDS"][show_commands][sections]:
                                    table.add_row([show_commands,test,"SHOW",data[section][device]["SHOW_COMMANDS"][show_commands][sections][test]["Result"]])

                print(table)
            print("\n")


def banner():
    print("############################################")
    print("### config checker v0.3                 ####")
    print("### Paul Freitag                        ####")
    print("### github.com/catachan/config-checker  ####")
    print("############################################\n")