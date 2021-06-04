import sys,os,json, boto3

root_path = 'E:\\Research\\Cloud\\AWS\\CDKProjectVer2\\AppStacks\\EC2'

def _parse_json(path):
    file_object = open(path,"r")
    json_data = json.load(file_object)
    file_object.close()
    return json_data

def _update_json(path,json_data):
    file_object = open(path,"w")
    json.dump(json_data, file_object)
    file_object.close()

def create_vpc():
    print('This stack will create a VPC:')
    print('\nStep 1:')
    print('\n+ Create a VPC')
    print('\nStep 2:')
    print('\n+ Create an Internet Gateway and attach it to created VPC')
    print('\nStep 3:')
    print('\n+ Create NAT Gateway for private subnet (if needed)')
    print('\n+ Create a NAT subnet and use NAT Subnet to create a NAT Gateway')
    print('\nStep 4:')
    print('\n+ Create route tables only')
    print('\nStep 5:')
    print('\n+ Attach Internet route to corresponding route tables')
    print('\n+ If public route table, attach Internet Default Route to Internet Gateway')
    print('\n+ If private route table, attach Internet Default Route to NAT Gateway')
    print('\n   ===========   \n')
    print('Config file can be found in \'.\AppStacks\EC2\VPC\stacks\\vpc_conf.py\'')
    print('You must have specified these values in config file include:\n')
    print(' + EIP_NAT_GW')

    choice = input("\n- Do you want to continue (y)?: ")
    if choice == 'y':
        path = root_path + '\\VPC'
        os.system("powershell.exe cd " + path + "; cdk deploy")


def create_subnets():

    choice = input("\n- Do you want to continue (y)?: ")
    if choice == 'y':
        path = root_path + '\\Subnet'
        os.system("powershell.exe cd " + path + "; cdk deploy")

def create_instance():
    print('This stack will create a Instance with specified Subnet.')
    print('Config file can be found in \'.\AppStacks\EC2\Instance\stacks\\instance_conf.py\'')
    print('You must have specified these values in config file include:\n')
    print(' + VPC_ID')
    print(' + SUBNET_ID')
    print(' + PRIVATE_IP')
    choice = input("\n- Do you want to continue (y)?: ")
    if choice == 'y':
        path = root_path + "\\Instance\\stacks\\instance_dynamic_params.json"
        params = _parse_json(path)
        print("Instance's name must match the regular expression: /^[A-Za-z][A-Za-z0-9-]*$/")
        name = input(" + Enter Instance's name: ")
        params['instance_name'] = name
        _update_json(path, params)
        path = root_path + '\\Instance'
        os.system("powershell.exe cd " + path + "; cdk deploy")



def main():
    print("")
    print("###################################################")
    print("#                                                 #")
    print("#------[           EC2 Functions           ]------#")
    print("#                                                 #")
    print("###################################################")
    print("")
    try:
        choice = 'true'
        while choice != '0':
            print("1.1. Create a VPC.")
            print("1.2. Create a Subnets.")
            print("1.3. Create a Instance.")
            print("0. Return")
            choice = input("\n- Enter choice: ")
            if choice == '1':
                create_vpc()
            elif choice == '2':
                print("Thanks for using!")
            elif choice == '3':
                create_instance()
            elif choice == '0':
                print("Thanks for using!")
            else:
                print("Invalid input.")
    except:
        print(sys.exc_info()[0])
