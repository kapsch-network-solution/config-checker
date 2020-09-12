# device-checker

Requirements:
netmiko==3.2.0
paramiko==2.7.1
prettytable==0.7.2
pyaml==20.4.0

Online mode:
python main.py -b [baseline.yaml] -c [connection.yaml] 

Offline mode:
python main.py -b [baseline.yaml] -d [config directory]

Optional parameters
-f
display/log only failed check/ suppress passed checks

-r [report.json]
log also to json file additional to console output

Samples for baseline.yaml and connection.yaml in examples directory


To convert the python file use python package auto-py-to-exe.exe
pip install auto-py-to-exe
auto-py-to-exe
