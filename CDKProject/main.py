from AppStacks.EC2.ec2_main import main as ec2_main

def main():
    print("###################################################")
    print("#                                                 #")
    print("#------[ CloudFormation Scripted by BinhLH ]------#")
    print("#                                                 #")
    print("###################################################")
    print("")
    choice = 'true'
    while choice != '0':
        print("1. IAM.")
        print("2. EC2.")
        print("0. Exit")
        choice = input("\n+ Enter choice: ")
        if choice == '1':
            print("Thanks for using!")
        elif choice == '2':
            ec2_main()
        elif choice == '0':
            print("Thanks for using!")
        else:
            print("x Invalid input.")
        print("")

if __name__ == '__main__':
    main()
