class decoder:
    def __init__(self):
        pass

    def decode(self, str):
        encodedStrList = str.split(' ')
        yyyy = int(encodedStrList.pop(-1))
        mm = int(encodedStrList.pop(-1))
        dd = int(encodedStrList.pop(-1))

        str = ''.join(encodedStrList)
        strSplit = list(str)
        strInt = []
        for i in range(len(strSplit)):
            strInt.append(ord(strSplit[i]) - dd - 1 + mm - int(yyyy %
                        100) - int((yyyy - (yyyy % 100))/100))

        decode = []
        for i in range(len(strInt)):
            decode.append(chr(strInt[i]))

        decoded = ''.join(decode)
        return decoded