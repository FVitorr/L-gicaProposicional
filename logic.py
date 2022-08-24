from cmath import sqrt
import itertools as it
from re import S
'''
A ou B
v    v
v    f
f    v
f    f
'''
class predicade:
    def __init__(self,param:(str)) -> None:
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
a.show()

