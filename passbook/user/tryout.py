# find prime -> 1 to 100
# prime sums

# num = 30
# for i in range(2, num-1):
#     if (num % i) == 0:
#         print(i)
#
#     else:
#         print(f'{num} is prime no')

# num = 30
# for i in range(1,num):
#     if num % i == 0:
#         print(i)

dic = {}

def factors(num):

    parag = []
    for i in range(2, num+1):
        if num % i == 0:
            parag.append(i)
    return parag


print(factors(30))

def number_factor(num):
    for i in range(2, num):
        #print(f'{i} factors are {factors(i)}')
        if len(factors(i)) == 1:
            print(i)
        dic[i] = factors(i)

number_factor(100)

#print(dic)