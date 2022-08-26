import itertools as it
import numpy as np

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
    def ordPref(self,entry):
        cont = 0
        stg = entry
        while len(stg) > 0:
            if cont > len(stg):
                cont = 0
            if '(' in stg:
                init = 0
                cont = 0
                for i in range(cont,len(stg)):
                    if stg[i] == '(':
                        init = i 
                    if stg[i] == ')':
                        fim = i
                        cont = i
                        break
                stg[init] = ''.join(stg[init + 1:fim])
                for j in range(init,fim):
                    del stg[init + 1]
                #stg = stg.replace(str(stg[old:fim+1]) , stg[init:fim].replace(' ',''))
            else:
                break
        return stg
    def execute(self,entry):
        stg = entry
        _operator = [i for i in stg if i in self.operator]
        def del_(i,re):
            stg[i-1] = re
            del stg[i+1]
            del stg[i]
        while len(_operator) > 0:
            for i in range(len(stg)):
                if stg[i] in self.operator:
                    param1 = stg[i-1]
                    param2 = stg[i+1]
                    print(param1,param2)
                    if param1 not in self.operator and param2 not in self.operator:
                        print(stg)
                        if stg[i] == 'or':
                            re = self.ou((param1,param2))
                            print(re)
                            del_(i,re)
                            del _operator[_operator.index('or')]
                            print(stg)
                            break
                        if stg[i] == 'and':
                            re = self.e((param1,param2))
                            print(re)
                            del_(i,re)
                            del _operator[_operator.index('and')]
                            break
                        if stg[i] == '>':
                            re = self.implica((param1,param2))
                            del_(i,re)
                            del _operator[_operator.index('>')]
                            break
                        print(param1,i,param2)
                    else:
                        print("Erro na indentidição dos parametros")
                        break
            _operator = [i for i in stg if i in self.operator]

    def predicade(self,entry: str) -> None:
        #tratar entrada 
        ent = list(entry.split(" "))
        cont = 0
        #Manipular str e fazer operações em ordem
        for i in range(len(ent)):
            if "~" in ent[i]:
                self.nao(ent[i][1])

        if '(' in ent:
            ord = self.ordPref(ent)
    
            for i in range(len(ord)):
                if ord[i] in self.operator:
                    param1 = ord[i -1]
                    #se o param1 não existir no dicionario separ funçoes e adc
                    if param1 not in self.values.keys():
                        try:
                            param1 = param1.replace("and"," and ")
                        except:
                            param1 = param1.replace("or"," or ")
                        for j in range(len(param1)):
                            if param1[j] in self.operator and param1[j + 1] != ' ' and param1[j] != '~':
                                param1 = param1.replace(param1[j]," "+ param1[j] +" ")
                                self.execute(param1.split(" "))
                                j += 2
                    param2 = ord[i + 1]
                    if param2 not in self.values.keys():
                        try:
                            param2 = param2.replace("and"," and ")
                        except:
                            param2 = param1.replace("or"," or ")
                        for j in range(len(param1)):
                            if param1[j] in self.operator and param1[j + 1] != ' ' and param1[j] != '~':
                                param1 = param1.replace(param1[j]," "+ param1[j] +" ")
                                self.execute(param1.split(" "))
                                j += 2
                else:

                    pass
        else:
            self.execute(entry)
        

    
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
            #print(self.values)
            return param[0] + 'or' + param[1]
        except:
            return -1
    def e(self,param: (str)) -> None:
        res = []
        try:
            a = self.values[param[0]]
            b = self.values[param[1]]
            #print(f"{a}\n{b}")
            #print(a)
            #print(b)
            for i in range(len(a)):
                if a[i] != b[i]:
                    res.append(0)
                elif a[i] == b[i] and a[i] == 0:
                    res.append(0)            
                else:
                    res.append(1)
            #print(res)
            self.values[param[0] + 'and' + param[1]] = res
            #print(self.values)
            return param[0] + 'and' + param[1]
        except:
            return -1

    def implica(self,param:(str)) -> None:
        res = []
        try:
            a = self.values[param[0]]
            b = self.values[param[1]]

            for i in range(len(a)):
                if a[i] != b[i] and a[i] == 0:
                    res.append(1)
                elif  a[i] != b[i] and a[i] == 1:
                    res.append(0)
                else:
                    res.append(1)
            self.values[param[0] + '>' + param[1]] = res
            return param[0] + '>' + param[1]
        except:
            return -1

    def show(self):
        dt = self.values
        len_array = len(dt[list(dt.keys())[1]])
        len_dict = len(list(dt.keys()))

        mx = np.zeros((len_array,len_dict),dtype=int)

        c = 0
        l = 0
        for i in dt:
            for j in dt[i]:
                if c > len(dt[i]) - 1:
                    c = 0
                mx[c][l] = j
                c += 1
            l += 1

        for i in dt.keys():
            #print(f"\t{i}")
            print (f"{i:^10}",end="")
        print("\n")
        for i in range(len_array):
            for j in range(len_dict):
                print(f"{mx[i][j]:^10}",end="")
            print("\n")

a = predicade(("p","q","r","s"))
a.predicade("( p > ~q and r ) or ( s and p )")
a.show()

