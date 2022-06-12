import argparse

def waitLoop():
    print("your action is : " + str(action))
    print("please input your next code")
    num = input("Tell me loop num\n")
    num = int(num)
    for i in range(0,num):
        print(str(i))
    print("end")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="WAVE")
    parser.add_argument('--action', dest='action', type=int, help="0: 1", default=0)

    args = parser.parse_args()

    action = args.action
    if action < 0:
        print("exit")
    else:
        while 1 == 1:
            waitLoop()