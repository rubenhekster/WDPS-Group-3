import operator

def Hamming(str1, str2):

    str1_ = str1
    str2_ = str2
    
    if str1 > str2:
        dif = len(str1) - len(str2)
        for i in range(dif):
            str2_ = str2_ + "0"
    elif str1 < str2:
        dif = len(str2) - len(str1)
        for i in range(dif):
            str1_ = str1_ + "0"
        
    print(str1_, str2_)

    ne = operator.ne
    return sum(map(ne, str1_, str2_))

def GetDistance(str1, str2):

    for i in range(len(str2)):
        print("Hamming Distance: ", Hamming(str1, str2[i]))

def main():
    str1 = "Obama"
    str2 = ["Osama", "A lama", "Pyjama", "Futurama", "Alabama"]
    
    GetDistance(str1, str2)

if __name__ == '__main__':
    main()
    print("Done")
