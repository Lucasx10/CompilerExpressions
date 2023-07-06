erroMsg = 0
error = 0
tokenArr = []

def insertToken(token, cod, line):
    global tokenArr
    
    newToken = {"token": token, "cod": cod, "line": line}
    tokenArr.append(newToken)

def isKeyword(token):
    if token == "int" or token == "float":
        return True
    return False

def AutomatoInteger(string):
    M = [[1, -1, -1], [1, -1, -1], [2, 2, 2]]
    e = 0
    for char in string:
        if char.isdigit():
            c = 2
        elif char == "+":
            c = 0
        elif char == "-":
            c = 1
        else:
            return False
        e = M[c][e]
        if e == -1:
            return False
    if e == 2:
        return True
    else:
        return False

def AutomatoFloat(string):
    M = [[1, -1, -1, -1, -1], [1, -1, -1, -1, -1], [2, 2, 2, 4, 4], [-1, -1, 3, -1, -1]]
    e = 0
    for char in string:
        if char.isdigit():
            c = 2
        elif char == "+":
            c = 0
        elif char == "-":
            c = 1
        elif char == ".":
            c = 3
        else:
            return False
        e = M[c][e]
        if e == -1:
            return False
    if e == 4:
        return True
    else:
        return False

def AutomatoIdentifier(string):
    M = [[-1, 1], [1, 1]]
    e = 0
    for char in string:
        if char.isalpha():
            c = 1
        elif char.isdigit():
            c = 0
        else:
            return False
        e = M[c][e]
        if e == -1:
            return False
    if e == 1:
        return True
    else:
        return False

def isDelimiter(ch):
    if ch == ' ' or ch == ';' or ch == '+' or ch == '-' or ch == '*' or ch == '/' or ch == ',' or ch == '=' or ch == '(' or ch == ')' or ch == '\0' or ch == '\'' or ch == '"':
        return True
    elif '\r' in ch or '\n' in ch:
        return True
    return False

def isDelimiterChar(ch):
    if ch == ',' or ch == '(' or ch == ')' or ch == '\'' or ch == '"':
        return True
    return False

def isOperator(ch):
    if ch == '+' or ch == '-' or ch == '*' or ch == '/' or ch == '=':
        return True
    return False

def analise_lexica(exp, line):
    global erroMsg
    global error
    
    temPontoEVirgula = exp[-1] == ";" if True else False
    tokens = exp.split(';')
    Total_tokens = len(tokens)
    
    for index in range(Total_tokens-1):
        left = 0
        right = 0
        length = len(tokens[index])
        tokens[index] += " "
        while right <= length and left <= right:
            isDelimiterBool = isDelimiter(tokens[index][right])
            
            if isDelimiterBool == False:
                right += 1
            elif isDelimiterBool == True and left == right:
                if isOperator(tokens[index][right]) == True:
                    tokenCH = tokens[index][right]
                    insertToken(tokenCH, 1, line)
                elif isDelimiterChar(tokens[index][right]) == True:
                    tokenCH = tokens[index][right]
                    insertToken(tokenCH, 6, line)
                right += 1
                left = right
            elif isDelimiterBool == True and left != right or (right == length and left != right):
                subStr = tokens[index][left:right]
                if isKeyword(subStr) == True:
                    insertToken(subStr, 2, line)
                elif AutomatoInteger(subStr) == True:
                    insertToken(subStr, 3, line)
                elif AutomatoFloat(subStr) == True:
                    insertToken(subStr, 4, line)
                elif AutomatoIdentifier(subStr) == True and isDelimiter(tokens[index][right - 1]) == False:
                    if len(subStr) > 1:
                        strLine = str(line + 1)
                        erroMsg = "Erro lexico\n"
                        erroMsg += "Linha: " + strLine + " "
                        erroMsg += subStr
                        erroMsg += " eh muito grande este compilador nao esta apto a lidar com indentificadores maiores do que 1 caractere"
                        error = 1
                        break
                    insertToken(subStr, 5, line)
                left = right
            else:
                print("273 " + tokens[index][right] + "</br>")
        
        if temPontoEVirgula or index < Total_tokens - 1:
            insertToken(";", 7, line)

def subString(string, left, right):
    return string[left:right]


################################################# ANALISE SINTATICA #################################################

blockWeakTree = 0
pilha_arvore = []
pilha_arvore_exp = []
blockWeakTreeS = 0
pilha_gen_arvS = []
pilha_gen_arvS_exp = []

class TernaryNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.center = None
        self.right = None

class TernaryTree:
    def __init__(self):
        self.root = None

    def isEmpty(self):
        return self.root is None

    def insert(self, tree2, data, data2):
        global blockWeakTree

        if self.isEmpty():
            node = TernaryNode(data)
            self.root = node

            node = TernaryNode(data2)
            tree2.root = node
        else:
            self.insertNode(self.root, tree2.root, data, data2)
            blockWeakTree = 0

    def insertNode(self, root, root2, data, data2):
        global blockWeakTree

        if (
            root is None
            or root.data == "+"
            or root.data == "-"
            or root.data == "*"
            or root.data == "/"
            or root.data == "("
            or root.data == ")"
            or root.data == "v"
            or root.data == "&"
            or blockWeakTree == 1
        ):
            return

        if root.left is None and root.center is None and root.right is None:
            root.right = TernaryNode(data)
            root2.right = TernaryNode(data2)

            if data == "v":
                root.center = TernaryNode("&")
                root.left = TernaryNode("&")

                root2.center = TernaryNode("&")
                root2.left = TernaryNode("&")

            blockWeakTree = 1
            return

        elif root.left is None and root.center is None:
            if (
                root.data == "E"
                and root.right.data == "S"
                and data == "+"
            ) or (
                root.data == "S"
                and root.right.data == "M"
                and data == "-"
            ) or (
                root.data == "M"
                and root.right.data == "D"
                and data == "*"
            ) or (
                root.data == "D"
                and root.right.data == "P"
                and data == "/"
            ) or (
                root.data == "P"
                and root.right.data == ")"
                and data == "E"
            ):
                self.check_lower(root.right, root2.right, data, data2)
                if blockWeakTree == 0:
                    root.center = TernaryNode(data)
                    root2.center = TernaryNode(data2)

                    blockWeakTree = 1
                    return
            elif (
                root.right.data == ")"
                and data != "E"
            ):
                root.center = TernaryNode("&")
                root.left = TernaryNode("&")

                root2.center = TernaryNode("&")
                root2.left = TernaryNode("&")

            if (
                root.right.left is not None
                and root.right.center is not None
            ):
                if (
                    root.right.left.data == "&"
                    and root.right.center.data == "&"
                ):
                    root.center = TernaryNode("&")
                    root.left = TernaryNode("&")

                    root2.center = TernaryNode("&")
                    root2.left = TernaryNode("&")
        elif root.left is None:
            if (
                root.data == "E"
                and root.center.data == "+"
                and root.right.data == "S"
                and data == "E"
            ) or (
                root.data == "S"
                and root.center.data == "-"
                and root.right.data == "M"
                and data == "S"
            ) or (
                root.data == "M"
                and root.center.data == "*"
                and root.right.data == "D"
                and data == "M"
            ) or (
                root.data == "D"
                and root.center.data == "/"
                and root.right.data == "P"
                and data == "D"
            ) or (
                root.data == "P"
                and root.center.data == "E"
                and root.right.data == ")"
                and data == "("
            ):
                root.left = TernaryNode(data)
                root2.left = TernaryNode(data2)

                if (
                    root.data == "P"
                    and root.center.data == "E"
                    and root.right.data == ")"
                    and data == "("
                ):
                    self.bloqueia_nao_terminais_filhos(
                        root.center, root2.center
                    )

                blockWeakTree = 1
                return

        self.insertNode(root.right, root2.right, data, data2)
        self.insertNode(root.center, root2.center, data, data2)
        self.insertNode(root.left, root2.left, data, data2)

    def check_lower(self, root, root2, data, data2):
        global blockWeakTree

        if (
            root is None
            or root.data == "+"
            or root.data == "-"
            or root.data == "*"
            or root.data == "/"
            or root.data == "("
            or root.data == ")"
            or root.data == "v"
            or root.data == "&"
            or blockWeakTree == 1
        ):
            return

        if root.left is None and root.center is None:
            if (
                root.data == "E"
                and root.right.data == "S"
                and data == "+"
            ) or (
                root.data == "S"
                and root.right.data == "M"
                and data == "-"
            ) or (
                root.data == "M"
                and root.right.data == "D"
                and data == "*"
            ) or (
                root.data == "D"
                and root.right.data == "P"
                and data == "/"
            ) or (
                root.data == "P"
                and root.right.data == ")"
                and data == "E"
            ):
                self.check_lower(root.right, root.right, data, data2)
                if blockWeakTree == 0:
                    root.center = TernaryNode(data)
                    root2.center = TernaryNode(data2)

                    blockWeakTree = 1
                    return

        self.check_lower(root.right, root2.right, data, data2)
        self.check_lower(root.center, root2.center, data, data2)
        self.check_lower(root.left, root2.left, data, data2)

    def bloqueia_nao_terminais_filhos(self, root, root2):
        global blockWeakTree

        if (
            root is None
            or root.data == "+"
            or root.data == "-"
            or root.data == "-"
            or root.data == "/"
            or root.data == "("
            or root.data == ")"
            or root.data == "v"
            or root.data == "&"
            or blockWeakTree == 1
        ):
            return

        if root.left is None and root.center is None:
            root.center = TernaryNode("&")
            root.left = TernaryNode("&")

            root2.center = TernaryNode("&")
            root2.left = TernaryNode("&")

        self.bloqueia_nao_terminais_filhos(root.right, root2.right)
        self.bloqueia_nao_terminais_filhos(root.center, root2.center)
        self.bloqueia_nao_terminais_filhos(root.left, root2.left)

    def arv_imprime(self):
        return self.arv_imprime_no(self.root)

    def arv_imprime_no(self, root):
        result = "<"
        if root is not None and root.data != "&":
            result += "</t>"
            result += root.data
            result += self.arv_imprime_no(root.left)
            result += self.arv_imprime_no(root.center)
            result += self.arv_imprime_no(root.right)
        result += ">"
        return result

class BinaryNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None

    def is_empty(self):
        return self.root is None

    def simplifica_arvore_fraca(self, arv, arv2, arvS2):
        global blockWeakTreeS
        global pilha_gen_arvS
        global pilha_gen_arvS_exp

        self.cria_pilha_gen(arv.root, arv2.root)
        if self.root is None:
            node = BinaryNode(pilha_gen_arvS[-1])
            self.root = node
            pilha_gen_arvS.pop()

            node = BinaryNode(pilha_gen_arvS_exp[-1])
            arvS2.root = node
            pilha_gen_arvS_exp.pop()

        while len(pilha_gen_arvS) != 0:
            self.constroi_arvS(self.root, arvS2.root)
            blockWeakTreeS = 0

    def cria_pilha_gen(self, root, root2):
        global pilha_gen_arvS
        global pilha_gen_arvS_exp

        if root is not None and root.data != "&":
            if root.data == "v" or root.data == "+" or root.data == "-" or root.data == "*" or root.data == "/":
                pilha_gen_arvS.append(root.data)
                pilha_gen_arvS_exp.append(root2.data)
            self.cria_pilha_gen(root.right, root2.right)
            self.cria_pilha_gen(root.left, root2.left)
            self.cria_pilha_gen(root.center, root2.center)

    def constroi_arvS(self, root, root2):
        global blockWeakTreeS
        global pilha_gen_arvS
        global pilha_gen_arvS_exp

        if root is None or root.data == "v" or blockWeakTreeS == 1:
            return

        if root.left is None and blockWeakTreeS == 0:
            root.left = BinaryNode(pilha_gen_arvS[-1])
            pilha_gen_arvS.pop()

            root2.left = BinaryNode(pilha_gen_arvS_exp[-1])
            pilha_gen_arvS_exp.pop()

            blockWeakTreeS = 1
            return
        elif root.left.data == "+" or root.left.data == "-" or root.left.data == "*" or root.left.data == "/":
            self.check_lowerS(root.left, root2.left)
        if root.right is None and blockWeakTreeS == 0:
            root.right = BinaryNode(pilha_gen_arvS[-1])
            pilha_gen_arvS.pop()

            root2.right = BinaryNode(pilha_gen_arvS_exp[-1])
            pilha_gen_arvS_exp.pop()

            blockWeakTreeS = 1
            return

        self.constroi_arvS(root.left, root2.left)
        self.constroi_arvS(root.right, root2.right)

    def check_lowerS(self, root, root2):
        global blockWeakTreeS
        global pilha_gen_arvS
        global pilha_gen_arvS_exp

        if root is None or root.data == "v" or blockWeakTreeS == 1:
            return

        if root.left is None and blockWeakTreeS == 0:
            root.left = BinaryNode(pilha_gen_arvS[-1])
            pilha_gen_arvS.pop()

            root2.left = BinaryNode(pilha_gen_arvS_exp[-1])
            pilha_gen_arvS_exp.pop()

            blockWeakTreeS = 1
            return
        elif root.left.data == "+" or root.left.data == "-" or root.left.data == "*" or root.left.data == "/":
            self.check_lowerS(root.left, root2.left)
        if root.right is None and blockWeakTreeS == 0:
            root.right = BinaryNode(pilha_gen_arvS[-1])
            pilha_gen_arvS.pop()

            root2.right = BinaryNode(pilha_gen_arvS_exp[-1])
            pilha_gen_arvS_exp.pop()

            blockWeakTreeS = 1
            return

        self.check_lowerS(root.left, root2.left)
        self.check_lowerS(root.right, root2.right)

    def arvS_imprime(self):
        return self.arvS_imprime_no(self.root)

    def arvS_imprime_no(self, root):
        result = "<"
        if root is not None:
            result += "</t>"
            result += root.data
            result += self.arvS_imprime_no(root.left)
            result += self.arvS_imprime_no(root.right)
        result += ">"
        return result

def AutomatoM(strExpre, str2, line):
    global error
    global erroMsg
    global pilha_arvore
    global pilha_arvore_exp

    # concatenando o simbolo delimitador na sentenca
    strExpre += "$"
    str2 += "$"

    # Declarando a tabela sintatica para o automato M
    M = [['D', '0', '0', '0', '0', 'D', '0', '0'],
         ['R', 'D', '0', '0', '0', 'R', '0', 'R'],
         ['R', 'R', 'D', '0', '0', 'R', '0', 'R'],
         ['R', 'R', 'R', 'D', '0', 'R', '0', 'R'],
         ['R', 'R', 'R', 'R', '0', 'R', '0', 'R'],
         ['0', '0', '0', '0', 'D', '0', 'D', '0'],
         ['0', '0', '0', '0', 'D', '0', 'D', '0'],
         ['0', '0', '0', '0', 'D', '0', 'D', '0'],
         ['0', '0', '0', '0', 'D', '0', 'D', '0'],
         ['0', '0', '0', '0', 'D', '0', 'D', '0'],
         ['R', 'R', 'R', 'R', '0', 'R', '0', 'R'],
         ['R', 'R', 'R', 'R', '0', 'R', '0', 'R'],
         ['0', '0', '0', '0', 'D', '0', 'D', '0']]

    QLinhasProducoes = 10
    producoes = ["E;E+S", "E;S", "S;S-M", "S;M", "M;M*D", "M;D", "D;D/P", "D;P", "P;(E)", "P;v"]

    # Declarando a pilha
    pilha = []
    pilha_aux = []

    # Colocando o simbolo delimitador na pilha
    pilha.append("$")

    # Recebera a indexação referente ao matriz
    c = 0
    l = 0
    i = 0
    Prod = ''

    parentese = 0
    i = 0
    while strExpre[i] != '$':
        if strExpre[i] == '(':
            parentese += 1
        elif strExpre[i] == ')':
            parentese -= 1
        i += 1
    if parentese > 0:
        strLineNum = str(line)
        erroMsg = "Erro Sintatico\n"
        erroMsg += "Linha: " + strLineNum + " "
        erroMsg += " esperava )"
        error = 2
    elif parentese < 0:
        strLineNum = str(line)
        erroMsg = "Erro Sintatico\n"
        erroMsg += "Linha: " + strLineNum + " "
        erroMsg += " esperava ("
        error = 2

    k = 0
    QProd = 0
    i = 0
    while strExpre[i] != '0' and error == 0:
        if strExpre[i] == '+':
            c = 0
        elif strExpre[i] == '-':
            c = 1
        elif strExpre[i] == '*':
            c = 2
        elif strExpre[i] == '/':
            c = 3
        elif strExpre[i] == '(':
            c = 4
        elif strExpre[i] == ')':
            c = 5
        elif strExpre[i] == 'v':
            c = 6
        elif strExpre[i] == '$':
            c = 7
        else:
            return 0

        while True:
            if pilha[-1] == 'E':
                l = 0
            elif pilha[-1] == 'S':
                l = 1
            elif pilha[-1] == 'M':
                l = 2
            elif pilha[-1] == 'D':
                l = 3
            elif pilha[-1] == 'P':
                l = 4
            elif pilha[-1] == '+':
                l = 5
            elif pilha[-1] == '-':
                l = 6
            elif pilha[-1] == '*':
                l = 7
            elif pilha[-1] == '/':
                l = 8
            elif pilha[-1] == '(':
                l = 9
            elif pilha[-1] == ')':
                l = 10
            elif pilha[-1] == 'v':
                l = 11
            elif pilha[-1] == '$':
                l = 12
            else:
                return 0

            # Escolhendo a produção a ser aplicada pela tabela sintática
            Nprod = M[l][c]
            producoes_compativeis = []

            # Fazendo equivalência entre a produção e ordem inversa e o seu número da tabela
            if Nprod == 'D':
                pilha.append(strExpre[i])
                pilha_arvore.append(strExpre[i])
                pilha_arvore_exp.append(str2[i])
                i += 1
            elif Nprod == 'R':
                QProd = 0
                for j in range(QLinhasProducoes):
                    k = len(producoes[j])
                    if producoes[j][k - 1] == pilha[-1]:
                        producoes_compativeis.append(j)
                        QProd += 1

                if QProd == 1:
                    pilha.pop()
                    pilha.append(producoes[producoes_compativeis[QProd - 1]][0])
                    pilha_arvore.append(producoes[producoes_compativeis[QProd - 1]][0])
                    pilha_arvore_exp.append(producoes[producoes_compativeis[QProd - 1]][0])
                else:
                    tamanho = 0
                    block = 0
                    producao_comp = []
                    for j in range(QProd):
                        k = len(producoes[producoes_compativeis[j]])
                        for l in range(k - 1, 1, -1):
                            pilha_aux.append(pilha[-1])
                            producao_comp.append(pilha[-1])
                            tamanho += 1
                            pilha.pop()
                            if len(pilha) == 0 or producoes[producoes_compativeis[j]][l] != pilha_aux[-1]:
                                block = 1
                                break

                        if block == 0:
                            k = 0
                            while producao_comp[k] == pilha_aux[-1]:
                                pilha.append(pilha_aux[-1])
                                pilha_aux.pop()
                                if len(pilha_aux) == 0:
                                    break
                                k += 1

                        if len(pilha_aux) == 0:
                            for l in range(len(producoes[producoes_compativeis[j]]) - 1, 1, -1):
                                pilha.pop()
                            pilha.append(producoes[producoes_compativeis[j]][0])
                            pilha_arvore.append(producoes[producoes_compativeis[j]][0])
                            pilha_arvore_exp.append(producoes[producoes_compativeis[j]][0])
                            break
                        else:
                            while len(pilha_aux) != 0:
                                pilha.append(pilha_aux[-1])
                                pilha_aux.pop()
                            block = 0
                    producao_comp = ''.join(producao_comp)
            else:
                error = 1
                return 0

            # Verificando se há o sentencial no topo da pilha e se o delimitador é o caractere em analise
            if pilha[-1] == 'E' and strExpre[i] == '$':
                return 1
            # Mudança de estado do autômato
            else:
                break


erroSyntax = 0
pilha_atribuicao = []
quadrupla = []

def analise_sintatica():
    global tokenArr
    global error
    global erroMsg
    global pilha_atribuicao
    global pilha_arvore
    global pilha_arvore_exp
    global erroSyntax
    global quadrupla
    
    q1 = []
    
    useExp = False
    declaracao = 0
    expIndex = 0
    while expIndex < len(tokenArr) and error == 0:
        exp = ''
        exp2 = ''
        
        while tokenArr[expIndex]["token"] != ";" and expIndex < len(tokenArr):
            
            if tokenArr[expIndex]["cod"] == 2 and tokenArr[expIndex + 1]["cod"] == 5 and tokenArr[expIndex + 2]["cod"] == 7:
                declaracao = 1
                expIndex += 2
                break
            elif (tokenArr[expIndex]["cod"] == 3 or tokenArr[expIndex]["cod"] == 4 or tokenArr[expIndex]["cod"] == 5 or tokenArr[expIndex]["token"] == ")") and expIndex + 1 < len(tokenArr):
                if tokenArr[expIndex + 1]["cod"] != 1 and tokenArr[expIndex + 1]["token"] != ")" and tokenArr[expIndex + 1]["cod"] != 7:
                    strLine = str(tokenArr[expIndex]["line"])
                    erroMsg = "Erro Sintatico\n"
                    erroMsg += "Linha: " + strLine + " "
                    erroMsg += "falta ; antes de "
                    erroMsg += tokenArr[expIndex + 1]["token"]
                    error = 1
                    break
                elif tokenArr[expIndex]["cod"] == 5 and tokenArr[expIndex + 1]["cod"] == 7:
                    useExp = True
            if tokenArr[expIndex + 1]["token"] == "=":
                pilha_atribuicao.append(tokenArr[expIndex]["token"])
            if expIndex < len(tokenArr):
                if useExp == False and (tokenArr[expIndex + 1]["token"] == "+" or tokenArr[expIndex + 1]["token"] == "-" or tokenArr[expIndex + 1]["token"] == "*" or tokenArr[expIndex + 1]["token"] == "/" or tokenArr[expIndex]["token"] == "(" or tokenArr[expIndex]["token"] == ")"):
                    useExp = True
            elif tokenArr[expIndex]["token"] == "(" or tokenArr[expIndex]["token"] == ")":
                useExp = True
            if useExp:
                if tokenArr[expIndex]["token"] == "+" or tokenArr[expIndex]["token"] == "-" or tokenArr[expIndex]["token"] == "*" or tokenArr[expIndex]["token"] == "/" or tokenArr[expIndex]["token"] == "(" or tokenArr[expIndex]["token"] == ")":
                    exp2 += tokenArr[expIndex]["token"]
                elif tokenArr[expIndex]["cod"] == 3 or tokenArr[expIndex]["cod"] == 4 or tokenArr[expIndex]["cod"] == 5:
                    exp2 += "v"
                exp += tokenArr[expIndex]["token"]
            elif tokenArr[expIndex]["token"] == "=":
                pilha_atribuicao.append(tokenArr[expIndex]["token"])
                useExp = True
            expIndex += 1
        
        if declaracao == 0 and error == 0:
            res = AutomatoM(exp2, exp, tokenArr[expIndex]["line"])
            if res == 1:
                arv1 = TernaryTree()
                arvExp1 = TernaryTree()
                arv2 = BinaryTree()
                arvExp2 = BinaryTree()
                while len(pilha_arvore) != 0:
                    topo_pilha_exp = pilha_arvore_exp[-1]
                    topo_pilha = pilha_arvore[-1]
                    arv1.insert(arvExp1, topo_pilha, topo_pilha_exp)
                    pilha_arvore.pop()
                    pilha_arvore_exp.pop()
                arv2.simplifica_arvore_fraca(arv1, arvExp1, arvExp2)
                gera_codigo(arvExp2.root)
            elif error != 2:
                erroSyntax += 1
                if erroSyntax < 2:
                    strLine = str(tokenArr[expIndex]["line"])
                    erroMsg = "Erro Sintatico\n"
                    erroMsg += "Linha: " + strLine + " "
                    erroMsg += "erro de syntax"
                    error = 1
                break
            else:
                break
        
        declaracao = 0
        useExp = False
        expIndex += 1
    
    if error == 0:
        quadrupla_salva(quadrupla)
        salva_cod_itermediario(quadrupla)
        otimiza_cod_intermediario()
        salva_cod_itermediario_otimizado(quadrupla)


################################################ GERAÇÃO DE CODIGO ################################################

num = None
codInterGlobal = []
codInterOtimGlobal = []
quadruplaGlobal = []

def gera_codigo(root):
    global num
    num = 1
    le_e_altera_arvore(root)

def le_e_altera_arvore(root):
    global pilha_atribuicao, quadrupla
    while root.left is not None and root.right is not None:
        le_e_altera_arvore2(root)
    if len(pilha_atribuicao) != 0:
        op = pilha_atribuicao[-1]
        pilha_atribuicao.pop()
        result = pilha_atribuicao[-1]
        newLine = {"op": op, "arg1": root.data, "arg2": "&", "result": result}
        quadrupla.append(newLine)
        pilha_atribuicao.pop()

def le_e_altera_arvore2(root):
    global quadrupla, num
    if root is None:
        return
    if root.left is not None and root.right is not None:
        if root.left.data != "+" and root.left.data != "-" and root.left.data != "*" and root.left.data != "/" and \
                root.right.data != "+" and root.right.data != "-" and root.right.data != "*" and root.right.data != "/":
            temp = "_t" + str(num)
            newLine = {"op": root.data, "arg1": root.left.data, "arg2": root.right.data, "result": temp}
            quadrupla.append(newLine)
            root.data = temp
            root.left = None
            root.right = None
            num += 1
    le_e_altera_arvore2(root.right)
    le_e_altera_arvore2(root.left)

def quadrupla_salva(q):
    quadruplaSalva = "op | arg1 | arg2 | result \n"
    for index in range(len(q)):
        quadruplaSalva += q[index]["op"] + " | " + q[index]["arg1"] + " | " + q[index]["arg2"] + " | " + q[index][
            "result"] + "\n"
    global quadruplaGlobal
    
    quadruplaGlobal = quadruplaSalva

    

def salva_cod_itermediario(q):
    codInter = ""
    for index in range(len(q)):
        codInter += q[index]["result"] + " := " + q[index]["arg1"] + " "
        if q[index]["op"] != "=":
            codInter += q[index]["op"] + " "
        if q[index]["arg2"] != "&":
            codInter += q[index]["arg2"]
        codInter += "\n"
    
    global codInterGlobal

    codInterGlobal = codInter

def otimiza_cod_intermediario():
    global quadrupla
    index = 0
    while index < len(quadrupla):
        if quadrupla[index]["op"] == "+" and (quadrupla[index]["arg1"] == "0" or quadrupla[index]["arg2"] == "0"):
            if quadrupla[index]["arg1"] != "0":
                id = quadrupla[index]["arg1"]
                temp = quadrupla[index]["result"]
                quadrupla[index]["result"] = "&"
                if index + 1 < len(quadrupla):
                    if quadrupla[index + 1]["arg1"] == temp:
                        quadrupla[index + 1]["arg1"] = id
                    elif quadrupla[index + 1]["arg2"] == temp:
                        quadrupla[index + 1]["arg2"] = id
            elif quadrupla[index]["arg2"] != "0":
                id = quadrupla[index]["arg2"]
                temp = quadrupla[index]["result"]
                quadrupla[index]["result"] = "&"
                if index + 1 < len(quadrupla):
                    if quadrupla[index + 1]["arg1"] == temp:
                        quadrupla[index + 1]["arg1"] = id
                    elif quadrupla[index + 1]["arg2"] == temp:
                        quadrupla[index + 1]["arg2"] = id
        elif quadrupla[index]["op"] == "-" and quadrupla[index]["arg2"] == "0":
            id = quadrupla[index]["arg1"]
            temp = quadrupla[index]["result"]
            quadrupla[index]["result"] = "&"
            if quadrupla[index + 1]["arg1"] == temp:
                quadrupla[index + 1]["arg1"] = id
            elif quadrupla[index + 1]["arg2"] == temp:
                quadrupla[index + 1]["arg2"] = id
        elif quadrupla[index]["op"] == "*" and (quadrupla[index]["arg1"] == "1" or quadrupla[index]["arg2"] == "1"):
            if quadrupla[index]["arg1"] != "1":
                id = quadrupla[index]["arg1"]
                temp = quadrupla[index]["result"]
                quadrupla[index]["result"] = "&"
                if index + 1 < len(quadrupla):
                    if quadrupla[index + 1]["arg1"] == temp:
                        quadrupla[index + 1]["arg1"] = id
                    elif quadrupla[index + 1]["arg2"] == temp:
                        quadrupla[index + 1]["arg2"] = id
            elif quadrupla[index]["arg2"] != "1":
                id = quadrupla[index]["arg2"]
                temp = quadrupla[index]["result"]
                quadrupla[index]["result"] = "&"
                if index + 1 < len(quadrupla):
                    if quadrupla[index + 1]["arg1"] == temp:
                        quadrupla[index + 1]["arg1"] = id
                    elif quadrupla[index + 1]["arg2"] == temp:
                        quadrupla[index + 1]["arg2"] = id
        elif quadrupla[index]["op"] == "/" and quadrupla[index]["arg2"] == "1":
            id = quadrupla[index]["arg1"]
            temp = quadrupla[index]["result"]
            quadrupla[index]["result"] = "&"
            if quadrupla[index + 1]["arg1"] == temp:
                quadrupla[index + 1]["arg1"] = id
            elif quadrupla[index + 1]["arg2"] == temp:
                quadrupla[index + 1]["arg2"] = id
        index += 1

def salva_cod_itermediario_otimizado(q):
    codInterOtim = ""
    for index in range(len(q)):
        if q[index]["result"] != "&":
            codInterOtim += q[index]["result"] + " := " + q[index]["arg1"] + " "
            if q[index]["op"] != "=":
                codInterOtim += q[index]["op"] + " "
            if q[index]["arg2"] != "&":
                codInterOtim += q[index]["arg2"]
            codInterOtim += "\n"

    global codInterOtimGlobal

    codInterOtimGlobal = codInterOtim

def gera_mips(token):
    with open('saida.txt', 'a') as fp:
        fp.write(token + ": .word\n")

def gera_mips2():
    global quadrupla
    with open('saida.txt', 'a') as fp:
        for index in range(len(quadrupla)):
            line = ""
            if quadrupla[index]["op"] == "+" or quadrupla[index]["op"] == "-":
                if quadrupla[index]["op"] == "+":
                    line += "add "
                else:
                    line += "sub "
                if quadrupla[index]["result"][0] == "_":
                    quadrupla[index]["result"] = "$" + quadrupla[index]["result"][1:]
                line += quadrupla[index]["result"] + ", "
                if quadrupla[index]["arg1"][0] == "_":
                    quadrupla[index]["arg1"] = "$" + quadrupla[index]["arg1"][1:]
                line += quadrupla[index]["arg1"] + ", "
                if quadrupla[index]["arg2"][0] == "_":
                    quadrupla[index]["arg2"] = "$" + quadrupla[index]["arg2"][1:]
                line += quadrupla[index]["arg2"] + "\n"
            elif quadrupla[index]["op"] == "*" or quadrupla[index]["op"] == "/":
                line += "li "
                if quadrupla[index]["result"][0] == "_":
                    quadrupla[index]["result"] = "$" + quadrupla[index]["result"][1:]
                line += quadrupla[index]["result"] + ", "
                if quadrupla[index]["arg1"][0] == "_":
                    quadrupla[index]["arg1"] = "$" + quadrupla[index]["arg1"][1:]
                line += quadrupla[index]["arg1"] + ", "
                if quadrupla[index]["arg2"][0] == "_":
                    quadrupla[index]["arg2"] = "$" + quadrupla[index]["arg2"][1:]
                line += quadrupla[index]["arg2"] + "\n"
                if quadrupla[index]["op"] == "*":
                    line += "mult "
                else:
                    line += "div "
                line += quadrupla[index]["result"] + ", "
                if quadrupla[index]["arg2"][0] == "_":
                    quadrupla[index]["arg2"] = "$" + quadrupla[index]["arg2"][1:]
                line += quadrupla[index]["arg2"] + "\n"
            if quadrupla[index]["op"] == "=":
                line += "lw "
                line += quadrupla[index]["result"] + ", "
                if quadrupla[index]["arg1"][0] == "_":
                    quadrupla[index]["arg1"] = "$" + quadrupla[index]["arg1"][1:]
                line += quadrupla[index]["arg1"] + "\n"
            if quadrupla[index]["result"][0] != "&":
                fp.write(line)


###################################### ANALISADOR SEMANTICO ###############################################

var_declara = []

def lst_cpy_var():
    global tokenArr
    global var_declara
    
    index = 0
    while index < len(tokenArr):
        if tokenArr[index]["cod"] == 2 and index + 2 < len(tokenArr):
            if tokenArr[index + 1]["cod"] == 5 and (tokenArr[index + 2]["token"] == "=" or tokenArr[index + 2]["token"] == ";"):
                newToken = {"token": tokenArr[index + 1]["token"], "cod": tokenArr[index]["cod"], "line": tokenArr[index + 1]["line"] - 1}
                var_declara.append(newToken)
                gera_mips(tokenArr[index + 1]["token"])
        index += 1

def checa_var_declara():
    global tokenArr
    global erroMsg
    global error
    
    index = 0
    while index < len(tokenArr):
        if tokenArr[index]["cod"] == 5:
            flag = busca_identificador(tokenArr[index]["token"], tokenArr[index]["line"] - 1)
            if flag is False:
                strLine = str(tokenArr[index]["line"])
                erroMsg = "Erro Semantico\n"
                erroMsg += "Linha: " + strLine + " "
                erroMsg += tokenArr[index]["token"] + " nao foi declarado neste escopo"
                error = 1
                break
        index += 1

def busca_identificador(token, line):
    global var_declara
    
    index = 0
    while index < len(var_declara):
        if var_declara[index]["token"] == token and var_declara[index]["line"] <= line:
            return True
        index += 1
    return False

def salvar_em_arquivo(texto, nome_arquivo):
    with open(nome_arquivo, 'w') as arquivo:
        arquivo.write(texto)

def Compilar(entrada):
    global erroMsg
    global error
    
    global var_declara
    
    with open('saida.txt', 'w') as fp:
        pass
    
    exp = ""
    i2 = 0
    
    lines = entrada.split('\n')
    Total_lines = len(lines)
    
    for lineNum in range(Total_lines):
        size = len(lines[lineNum])
        
        for i in range(size):
            exp += lines[lineNum][i]
            i2 += 1
            if lines[lineNum][i] == ';':
                analise_lexica(exp, lineNum + 1)
                exp = ""
                i2 = 0
    
    if error == 0:
        analise_sintatica()
    if error == 0:
        lst_cpy_var()
        checa_var_declara()
    if error == 0:
        gera_mips2()
    
    if error == 1 or error == 2:
        salvar_em_arquivo(entrada, "entrada2.txt")
        with open('erro.txt', 'w') as file:
            file.write(erroMsg)
    else:
        salvar_em_arquivo(entrada, "entrada2.txt")
        salvar_em_arquivo(quadruplaGlobal, "quadrupla.txt")
        salvar_em_arquivo(codInterGlobal, "codInterGlobal.txt")
        salvar_em_arquivo(codInterOtimGlobal, "codInterOtimGlobal.txt")
        

def printTokens(tokenArr):
    for token in tokenArr:
        print(f"Token: {token['token']}, Cod: {token['cod']}, Line: {token['line']}")


# Ler o conteúdo do arquivo de entrada
with open('entrada.txt', 'r') as file:
    expression = file.read()

Compilar(expression)

