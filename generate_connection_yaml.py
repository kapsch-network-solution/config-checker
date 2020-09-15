switch_suffix = "switch_"
subnet = "10.0.0."
username = "admin"
password = "password"
start = 1
end = 100

print("device:")
for i in range(start,end+1):
    print("    " + switch_suffix + str(i) + ":")
    print("         device_type: cisco_xe")
    print("         ip: " + subnet + str(i))
    print("         username: " + username)
    print("         password: " + password)
    print("         port: 22")
    print("         secret: \"\"")