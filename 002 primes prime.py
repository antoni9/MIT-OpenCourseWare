def prime():
    prime = 1
    collection = []
    x = input('which consecutive prime do you want [slow over 10 000]: ')
    while len(collection) <= int(x):
            for i in range(2, prime):
                if prime % i == 0:
                    break
            else:
                collection.append(prime)
            prime += 1
    print(prime - 1)



    
