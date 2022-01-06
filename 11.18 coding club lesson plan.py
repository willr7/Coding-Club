# Convert to Arabic
Converter = { "I":1, "V":5, "X":10, "L":50, "C":100, "D":500, "M":1000, "dummy":0 }

def Check(list,prototype):
    temp=[]
    for i in range(len(list)):
        if list[i] in prototype:
            temp.append(True)
        else:
            temp.append(False)
    if all(temp):
        return True
    else:
        return False

run = True
while run:
    Number = input("Roman Numerals:\n").upper()
    if Number in ['stop', 'end', 'End', 'Stop', 'END', 'STOP']:
        run = False
    else:
        seq = list(Number)
        seq.append("dummy")
        if not Check(seq,Converter):
            print("Invalid")
        else:
            ans = 0
            for i in range(len(seq)-1):
                if Converter[seq[i]] < Converter[seq[i+1]]:
                    ans-=Converter[seq[i]]
                else:
                    ans+=Converter[seq[i]]
            print(ans)