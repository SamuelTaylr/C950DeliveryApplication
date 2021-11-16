# Samuel Taylor, Student ID #001431573


from prompt import promptInfo, optionOne, optionTwo, optionThree
import sys

promptInfo()

while True:

    print('\n1) Individual Package Status Search')
    print('2) Check Status of Deliveries by Time')
    print('3) Package Info Lookup')
    print('0) Exit Application\n')
    print()
    selected = input('Enter 1,2,3 or 0 to quit: ')

    if selected == '0':

        sys.exit()

    if selected == '1':

        optionOne()

    if selected == '2':

        optionTwo()

    if selected == '3':

        optionThree()

