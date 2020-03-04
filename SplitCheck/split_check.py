# user inputs
def split_check():
    while True:
        try:
            people = float(input("How many people are splitting the check? "))
            if people > 1:
                break
            else:
                raise ValueError
        except ValueError:
            print('Try that again. Please enter a valid amount of people to split the check.')
    while True:
        try:
            total = float(input("What is the total cost on the check? "))
            if total > 0:
                break
            else:
                raise ValueError
        except ValueError:
            print('Try that again. Please enter a valid check total.')
    while True:
        try:
            tip = float(input("What percentage do you want to tip? "))
            if tip >= 0:
                break
            else:
                raise ValueError
        except ValueError:
            print("Try that again. Please enter a valid number. You don't need to add the % symbol.")
    tip_math = (float(tip)/100) + 1
    total_per_person = round(((total/people) * tip_math),2)
    if tip > 0:
        print('Including tip, each person should pay $' + str(total_per_person))
    else: 
        print('Each person should pay $' + str(total_per_person))

split_check()