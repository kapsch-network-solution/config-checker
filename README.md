# device-checker
[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/kapsch-network-solution/config-checker)

A script that connects to network devices and checks for the presence of commands (globally/per interface) defined in a basline file

## Requirements
netmiko==3.2.0

paramiko==2.7.1

prettytable==0.7.2

pyaml==20.4.0

## Installation

``` 
git clone https://github.com/catachan/config-checker.git
cd config-checker
```

Create virtual enviroment (optional)

``` 
python3 -m venv config-checker
source config-checker/bin/activate
```

install dependencies

```
pip install -r requirements.txt 
```

## Online mode
connect to device defined in connection.yaml file via ssh and collect "show run" and additional show command output and check against config in baseline.yaml 

```
python main.py -b [baseline.yaml] -c [connection.yaml]
```

![Image of online mode](https://i.ibb.co/ByW9Tvw/online-mode.jpg)


## Offline mode
check config files in directory (one per device) against baseline.yaml file. Please notice that only "show run" output can be checked in offline mode

```
python main.py -b [baseline.yaml] -d [config directory]
```

![Image of of offline](https://i.ibb.co/7NJrgRq/offline-mode.jpg)


## Optional parameters
```
-f
```
display/log only failed check/ suppress passed checks
![Image of of failed mode](https://i.ibb.co/SPMhHqc/failed-mode.jpg)

```
-r [report.json]
```
log also to json file additional to console output. The report file contains also the raw data that was checked

![Image of report mode](https://i.ibb.co/gTyktf4/report-mode.jpg)
![Image of report mode](https://i.ibb.co/yhqHVHK/report-file.jpg)

```
-l [logfile.txt]
```
log console output also to logfile (so you are able to see the complete output later on)

Samples for baseline.yaml and connection.yaml in examples directory

## Convert to windows exe
To convert the python file use python package auto-py-to-exe.exe
pip install auto-py-to-exe
auto-py-to-exe
