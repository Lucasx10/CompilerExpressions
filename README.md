# CompilerExpressions
O objetivo do compilador é aceitar as quatro operações aritméticas básicas com variáveis do tipo float ou integer. Além disso, a gramática permite o uso dos símbolos '(' e ')' e exibe apenas  o dígito mais à esquerda caso o número seja maior que 10. 
O compilador foi desenvolvido em python e para a interface foi utilizado o Flask que é um framework web escrito em python juntamente com HTML e CSS.

# Gramaticas Regulares
Automato1

L = {w|w (+|-|num)(num)num*} essa gramática está presente no automato para checar se um 
número é inteiro.

Automato2

L = {w|w (+|-|num)(num)num*(.)(num)num*} gramática utilizada para reconhecer float.

Automato3

L = {w|w letra(letra|numero)*} gramática utilizada para reconhecer um identificador.

# Gramáticas Livres de Contexto

Foi utilizada uma gramática livre de contexto para a análise sintática do compilador. O tipo de 
autômato escolhido foi de precedência fraca. Foram definidos símbolos não-terminais e 
símbolos terminais, bem como as produções para a análise sintática. Além disso, foi criada 
uma tabela de deslocamento e redução para guiar o processo de análise.

Símbolos não-terminais Vn = {E, S, M, D, P}

Símbolos terminais Vt = {+, -, *, /, (, ), v}

Produções P={E→ E+S, E→ S, S→ S-M, S→ M, M→ M*D, M→ D, D→ D/P, D→ P, P→ (E), 
P→ v}
