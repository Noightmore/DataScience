def censor_number(number_to_censore, end_number):
    for _ in range(1, end_number+1):
        print("*") if number_to_censore == _ else print(_)
