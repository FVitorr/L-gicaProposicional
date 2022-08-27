from ast import operator
import itertools as it
import numpy as np

class predicade:
    def __init__(self,param:(str)) -> None:
        self.operator = ["and",">",")","(","or","~","<"] #array onde armazena os operadores da logica
        '''Os dados de saidas são armmazenados em um dict para facilitar na ordem de procedencia
        ( a > b ) and (a > ~b ) -> dict.key [a, b, ~b, a>b, a>~b, a>banda>~b]'''
        values = { **dict.fromkeys(param, -1) }
        perm = [i for i in it.permutations([0,1] * len(param), len(param))] #Gerar (0,1) pros valores em dicionario

        comb = [] #Combinaçoes posiveis sem repetição
        for i in perm:
            if list(i) not in comb:
                comb.append(list(i))

        #Criar Dicionarios com nome do parametro e seu valores
        cont = 0
        for i in param:
            v = [j[cont] for j in comb]
            values[i] = v
            cont += 1
        self.values = values

    def ordPref(self,entry): #funçao para tratar de sentenças com ordem de procedencia "(",")"
        cont = 0
        stg = entry #realizar a copia da entrada 
        while len(stg) > 0: #percorer stg
            if cont > len(stg): cont = 0 # resetar cont (Variavel de controle sobre a posição no vetor), para range(0,max =len(stg))
            if '(' in stg: 
                cont, init = 0, 0
                for i in range(cont,len(stg)): #Objetivo: encontrar os par de "(",")" stg[init],stg[end]
                    if stg[i] == '(': init = i 
                    if stg[i] == ')':
                        end = i
                        cont = i #atribuir valor de i a variavel cont que controla a posição q estamos no vetor stg
                        break #parar de percorrer stg
                #Alterar a posição "(" por conteudo stg[init + 1:end]
                stg[init] = ''.join(stg[init + 1:end])
                for j in range(init,end): #Deletar bloco stg[init] - stg[end] : 
                    del stg[init + 1]
            else: # se a operação anterior não for executada, significa que não existe mais "(" ")" para encontrar
                break
        return stg

    def execute(self,entry): #bloco de operaçoes de sentenças sem ordem de procedencia ou seja da Esquerda para direita
        stg = entry
        _operator = [i for i in stg if i in self.operator] # separar operadores que existem em stg

        #Função de uso unico 
        def del_(i,re,op): #Deletar bloco de operaçoes ja executada
            stg[i-1] = re
            del stg[i+1]
            del stg[i]
            del _operator[_operator.index(op)]

        while len(_operator) > 0: #Interar sobre _operator: garantir que execute de todas as operaçoes logicas
            for i in range(len(stg)): # for (int i = 0; i < len(stg); i++)
                if stg[i] in self.operator: #se stg[i] for um operador param1 stg[i - 1] param2 = stg[i + 1]
                    param1, param2 = stg[i-1], stg[i+1]
                    #Verificar se os parametros não são valores iguais a operaçoes
                    if param1 not in self.operator and param2 not in self.operator:
                    
                        if stg[i] == 'or':
                            re = self.ou((param1,param2))
                            del_(i,re,'or') #deletar operação da stg e do _operator
                            break
                        if stg[i] == 'and':
                            re = self.e((param1,param2))
                            del_(i,re,'and')
                            break
                        if stg[i] == '>':
                            re = self.implica((param1,param2))
                            del_(i,re,'>')
                            break
                        if stg[i] == '<':
                            re = self.biimplica((param1,param2))
                            del_(i,re,'<')
                            break
                    else:
                        print("Erro na Sentença Informada")
                        break
            #_operator = [i for i in stg if i in self.operator]

    def predicade(self,entry: str) -> None:
        #tratar entrada 
        ent = list(entry.split(" "))
        print(ent)
        
        for i in range(len(ent)): #Maior ordem de prioridade no script
            if "~" in ent[i]:
                self.nao(ent[i][1])

        if '(' in ent:
            ord = self.ordPref(ent)
            print("ord",ord)
            _operator = [i for i in ord if i in self.operator]
            while len(_operator) > 0:
                for i in range(len(ord)):
                    if ord[i] in self.operator:
                        param1 = ord[i -1]
                        #se o param1 não existir no dicionario separ funçoes e adc
                        if param1 not in self.values.keys():
                            try:
                                param1 = param1.replace("and"," and ")
                                param1 = param1.replace("or"," or ")
                            except:
                                pass
                            for j in range(len(param1)):
                                if param1[j] in self.operator and param1[j + 1] != ' ' and param1[j] != '~':
                                    param1 = param1.replace(param1[j]," "+ param1[j] +" ")
                                    re = self.execute(param1.split(" "))
                                    #print(self.values.keys())
                                    j += 2
                        param2 = ord[i + 1]
                        if param2 not in self.values.keys():
                            #print(param2)
                            try:
                                param2 = param2.replace("and"," and ")
                            except:
                                param2 = param2.replace("or"," or ")
                            for j in param2:
                                if j in self.operator and j != '~':
                                    param2 = param2.replace(j," " + str(j) + " ")
                            #print(param2)
                            param2 = param2.split(' ')
                            #print(param2)
                            for j in range(len(param2)):
                                if param2[j] in self.operator and param2[j] != '~':
                                    param2[j] = str(param2[j])
                                    #print(param2)
                                    re = self.execute(param2)
                                    break
                            param1 = str(param1).replace(" ",'')
                            #print(ord,ord[i])
                            #print(param1,param2)
                            if ord[i] == 'and':
                                re = self.e((param1,param2[0]))
                            if ord[i] == 'or':
                                self.ou((param1,param2[0]))
                            if ord[i] == '>':
                                self.implica((param1,param2[0]))
                            if ord[i] == '<':
                                re = self.biimplica((param1,param2[0]))

                            ord[i -1] = re
                            del ord[i + 1]
                            del ord[i]
                            del _operator[0]
                            print('ord',ord)
                            break
                        
                    #print(param1.replace(" ",''),param2)
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
            return param[0] + 'or' + param[1]
        except:
            return -1
    def e(self,param: (str)) -> None:
        res = []
        try:
            a = self.values[param[0]]
            b = self.values[param[1]]
            #print(f"{a}\n{b}")

            for i in range(len(a)):
                if a[i] != b[i]:
                    res.append(0)
                elif a[i] == b[i] and a[i] == 0:
                    res.append(0)            
                else:
                    res.append(1)
            #Adc operação ao dicionario
            self.values[param[0] + 'and' + param[1]] = res
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

    def biimplica(self,param:(str)) -> None:
        res = []
        try:
            a = self.values[param[0]]
            b = self.values[param[1]]

            for i in range(len(a)):
                if a[i] == b[i] and a[i] == 1:
                    res.append(1)
                elif  a[i] != b[i]:
                    res.append(0)
                else:
                    res.append(1)
            self.values[param[0] + '<' + param[1]] = res
            return param[0] + '<' + param[1]
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
            for j in range(len_dict): print(f"{mx[i][j]:^10}",end="")
            print("\n")

#"( ~p < ~q ) < ( p and q )"

a = predicade(("p","q"))
entry = '( ~p < ~q ) < ( p and q )'
a.predicade(entry)
a.show()

