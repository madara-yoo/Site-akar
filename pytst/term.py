
import os


def term():
    cmmd = input('Madara--> ')
    try:
        os.system(cmmd)
        term()
    except Exception as e:
        print('not found this commend...!')
    term()
term()
