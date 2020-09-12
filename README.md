# device-checker

## Requirements
netmiko==3.2.0
paramiko==2.7.1
prettytable==0.7.2
pyaml==20.4.0

## Online mode
connect to device defined n connection.yaml file via ssh and collect "show run" and additional show command output and check against config in baseline.yaml 
```
python main.py -b [baseline.yaml] -c [connection.yaml]
```

## Offline mode
check config files in directory (one per device) against baseline.yaml file. Please notice that only "show run" output can be checked in offline mode
```
python main.py -b [baseline.yaml] -d [config directory]
```

## Optional parameters
```
-f
```
display/log only failed check/ suppress passed checks

```
-r [report.json]
```
log also to json file additional to console output

Samples for baseline.yaml and connection.yaml in examples directory

## Convert to windows exe
To convert the python file use python package auto-py-to-exe.exe
pip install auto-py-to-exe
auto-py-to-exe
