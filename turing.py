ops = ['5' ,'2' ,'C' ,'D' ,'+']

def calPoints(ops):
    aux = []
    pos = 0
    for info in ops:
        
        if info not in ['+','D','C']:
            aux.append(int(ops[pos]))
        else:
            if info =='+':
                aux.append(aux[len(aux)-1] + aux[len(aux)-2])
            elif info == 'D':
                aux.append(aux[len(aux)-1]*2)
            else:
                aux.pop(pos-1)
                pos-=1
        # print(info, pos, aux, sep=' | ')
        pos+=1

    print(sum(aux))

calPoints(ops)


s = ['(',')','[',']','{','}']
s2 = ['(','[', ')', ']']

def valid(s):

    pos = 0
    for info in s:
        if info in [')', ']']:
            if info == ')' and  s[pos-1] == '[':
                return False
                
            if info == ']' and s[pos-1] == '(':
                return False
        pos+=1

    return  True

print(valid(s))

