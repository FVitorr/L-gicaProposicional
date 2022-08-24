from cmath import sqrt
import itertools as it
from re import S
'''
A ou B
v    v
v    f
f    v
f    f
''''''
class predicade:
    def __init__(self) -> None:
        perm = [i for i in it.permutations([0,1] * len(param), len(param))]

        #Combinaçoes posiveis sem repetição
        comb = []
        for i in perm:
            if list(i) not in comb:
                comb.append(list(i))
        #Retornar uma matriz
        if "~" in list(param):
            a = self.nao(param[list(param).index("~")])
            for i in range(len(a)):
                comb[i].append(a[i])
        self.tbl = comb
        self.param = param

    def ou(self, param) -> None:
        print(self.tbl)
        res = []
        for i in self.tbl:
            if i[0] != i[1]:
                i.append(1)
            elif i[0] == i[1] and i[0] == 1:
                i.append(1)
            else:
                i.append(0)
        return 1

    def e(self) -> None:
        res = []
        for i in self.tbl:
            if i[0] != i[1]:
                res.append(0)
            elif i[0] == i[1] and i[0] == 0:
                res.append(0)
            else:
                res.append(1)
        return res
    
    def implica(self) -> None:
        res = []
        print(self.tbl)
        for i in self.tbl:
            if i[0] != i[1] and i[0] == 0:
                res.append(1)
            elif i[0] != i[1] and i[0] == 1:
                res.append(0)
            else:
                res.append(1)
        return res
    
    def biimplica(self) -> None:
        res = []
        print(self.tbl)
        for i in self.tbl:
            if i[0] != i[1]:
                res.append(0)
            else:
                res.append(1)
        return res
    
    def nao(self,param_: str) -> None:
        try:
            param = list(self.param).index(param_)
            res = []
            for i in self.tbl:
                #print(i[param])
                if i[param] != 0:
                    res.append(0)
                else:
                    res.append(1)
            return res
        except:
            return -1

    def show(self):
        print(self.tbl)
        print(f"{self.param[0]}\t{self.param[1]}")
        for i in self.tbl:
            print(f"{i[0]}\t{i[1]}")
        pass
    

a = predicade(("~a","b"))

print(a.ou("b"))
#print(a.e())
#print(a.implica())
#print(a.biimplica())
#print(a.nao("a"))
a.show()'''

class predicade:
    def __init__(self,param:(str)) -> None:
        self.operator = ["and",">",")","(","or","~"]
        values = { **dict.fromkeys(param, -1) }
        perm = [i for i in it.permutations([0,1] * len(param), len(param))]

        #Combinaçoes posiveis sem repetição
        comb = []
        for i in perm:
            if list(i) not in comb:
                comb.append(list(i))
        cont = 0
        #Criar Dicionarios com nome da preposição e seus valores
        for i in param:
            v = []
            for j in comb:
                v.append(j[cont])
            values[i] = v
            cont += 1
        self.values = values
        #print(values)

    def predicade(self,entry: str) -> None:
        #tratar entrada 
        ent = list(entry.split(" "))
        op = ''
        cont = 0
        #Manipular str e fazer operações em ordem
        print(ent)
        for i in range(len(ent)):
            if "~" in ent[i]:
                self.nao(ent[i][1])

        _operator = [i for i in ent if i in self.operator]
        cont = len(ent)
        j = 0
        while j < len(_operator):
            for i in range(cont):
                #print(self.values)
                if ent[i] in self.operator:
                    parm1 = ent[i - 1]
                    parm2 = ent[i + 1]
                    oper = parm1 + ent[i] + parm2
                    #Operação não realizada ?
                    if oper not in self.values.keys():
                        if ent[i] == 'or':
                            r = self.ou((parm1,parm2))
                            print(r)
                        if ent[i] == 'and':
                            r = self.e((parm1,parm2))
                            print(r)
                        ent.remove(parm1)
                        ent.remove(parm2)
                        ent[0] = r
                        break
            _operator = [i for i in ent if i in self.operator]

    
    def nao(self,param_: str) -> None:
        res = []
        try:
            for i in self.values[param_]:
                #print(i)
                if i == 0:
                    res.append(1)
                else:
                    res.append(0)
            self.values["~" + param_] = res
        except:
            pass
        #print(self.values)

    def ou(self, param: (str)) -> None:
        res = []
        try:
            a = self.values[param[0]]
            b = self.values[param[1]]
            #print(f"{a}\n{b}")
            for i in range(len(a)):
                if a[i] != b[i]:
                    res.append(1)
                elif a[i] == b[i] and a[i] == 1:
                    res.append(1)            
                else:
                    res.append(0)
            self.values[param[0] + 'or' + param[1]] = res
            print(self.values)
            return param[0] + 'or' + param[1]
        except:
            return -1
    def e(self) -> None:
        res = []
        for i in self.tbl:
            if i[0] != i[1]:
                res.append(0)
            elif i[0] == i[1] and i[0] == 0:
                res.append(0)
            else:
                res.append(1)
        return res

a = predicade(("a","b")).predicade("a or ~b and ~a")
