
def error():
    print("SHOOT")
    print(0/0)

def evaluator(equation:list , KEY_SYMBOLS:list): #Does equations badly
    """
    Docstring for evaluator
    
    :param equation: Its a list hopefully 
    """
    i = len(equation)-1
    while i >=0: #Start with indices these are funky what can I say something something left associativity or is it right?
        if equation[i] == "^":
            equation[i] = equation[i-1] ^ equation[i+1]
            equation.pop(i+1)
            equation.pop(i-1)
            i -= 1
        i -=1

    i = 0
    while i < len(equation):
        if equation[i] == "*":
            equation[i] = equation[i-1] * equation[i+1]
            equation.pop(i+1)
            equation.pop(i-1)
            i -= 1
        elif equation[i] == "/": #The elifs are just for efficiency they are not required from a logical point of view as you will always be on a number (I hope)
            equation[i] = equation[i-1] / equation[i+1]
            equation.pop(i+1)
            equation.pop(i-1)
            i -= 1
        elif equation[i] == "//":
            equation[i] = equation[i-1] // equation[i+1]
            equation.pop(i+1)
            equation.pop(i-1)
            i -= 1
        elif equation[i] == "%":
            equation[i] = equation[i-1] % equation[i+1]
            equation.pop(i+1)
            equation.pop(i-1)
            i -= 1
        i+= 1 
    
    i = 0
    while i < len(equation):
        if equation[i] == "+":
            equation[i] = equation[i-1] + equation[i+1]
            equation.pop(i+1)
            equation.pop(i-1)
            i -= 1
        elif equation[i] == "-":
            if i == 0:
                equation[i] = -equation[i+1]
                equation.pop(i+1)
            else:
                equation[i] = equation[i-1] - equation[i+1]
                equation.pop(i+1)
                equation.pop(i-1)
                i -= 1
        i+= 1 
    return(equation)


def tokeniser(line, KEY_SYMBOLS, NUMS, CHARACTERS, KEY_WORDS): #Something something tokens
    """
    Docstring for tokeniser
    
    :param line: Description
    :param KEY_SYMBOLS: Description
    :param NUMS: Description
    :param CHARACTERS: Description
    """
    working_part = ""
    working_part_type = ""
    string = False
    tokenised = []
    for i in range(len(line)):
            if line[i] in KEY_SYMBOLS and not string and working_part_type != "symbol":
                if len(working_part) != 0:
                    tokenised.append((working_part,working_part_type))
                working_part = "" 
                working_part_type = ""
                if i != len(line)-1:
                    if line[i]+line[i+1] not in KEY_SYMBOLS:
                        tokenised.append((line[i],"symbol"))
                    else:
                        working_part = line[i]
                        working_part_type = "symbol"
                else:
                    working_part = line[i]
                    working_part_type = "symbol"
            elif line[i] in KEY_SYMBOLS and working_part_type == "symbol":
                working_part = working_part + line[i] 
                tokenised.append((working_part,working_part_type))
                working_part = "" 
                working_part_type = ""
            elif len(working_part) == 0 and line[i] in NUMS:
                working_part = line[i]
                working_part_type = "int"
            elif working_part_type == "int" and line[i] in NUMS:
                working_part = working_part + line[i]
            elif len(working_part) != 0 and line[i] == " ":
                if len(working_part) != 0:
                    tokenised.append((working_part,working_part_type))
                working_part = "" 
                working_part_type = ""
            elif len(working_part) == 0 and line[i].upper() in CHARACTERS:
                 working_part = line[i]
                 working_part_type = "string"
            elif working_part_type == "string" and (line[i] in NUMS or line[i].upper() in CHARACTERS):
                working_part = working_part + line[i] 

    if len(working_part) != 0:
        tokenised.append((working_part,working_part_type))
        working_part = "" 
        working_part_type = ""
    for i in range(len(tokenised)):
        if tokenised[i][0] in KEY_WORDS:
            tokenised[i]= (tokenised[i][0],"key word")
    return(tokenised)
                 
def equation(line):

    equation = []
    for x in range(0, len(line)):
        if line[x][1] == "int":
            equation.append(int(line[x][0]))
        if line[x][1] == "symbol":
            equation.append(line[x][0])
        if line[x][1] == "string":
            if line[x][0] in variables:
                equation.append(variables[line[x][0]])
            else:
                equation.append([line[x][0]])
    result = evaluator(equation, KEY_SYMBOLS)
    if len(result) > 1:
        print(result)
        error()
    else:
        result = result[0]
    return(result)

def truth_statement(line):
    return(1)

def expression(line):
    for i in range(len(line)):
        if (line[i][0] == "==" or line[i][0] == "!=" or line[i][0] == ">=" or line[i][0] == "<=" ) and line[i][1] == "symbol":
            return(truth_statement(line))
    return(equation(line))
    


KEY_SYMBOLS = ["=", "+", "*", "^", "/", ")", "(", "%", "//", "-", ","]
NUMS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-"]
CHARACTERS = "QWERTYUIOPASDFGHJKLZXCVBNM_"
KEY_WORDS = ["print"]

file = open("program.txt", "r")

program = file.readlines()

file.close()

print(program[0])

tokenised = []
for i in range(len(program)):
    tokenised.append(tokeniser(program[i], KEY_SYMBOLS, NUMS, CHARACTERS, KEY_WORDS))
print(tokenised)

variables = {}

for i in range(len(tokenised)):
    line = tokenised[i]
    if len(line) == 0:
        continue
    if line[0][1] == "string":
            if line[1][0] == "=":
                result = expression(line[2:])
                variables.update({line[0][0]: result})
            
    if line[0][1] == "key word":
        if line[0][0]== "print":
            if line[1] == ("(", "symbol") and line[-1] == (")", "symbol"):
                running_expression = []
                output = []
                for x in range(2,len(line)-1):
                    if line[x] == (",", "symbol"):
                        print(running_expression)
                        output.append(expression(running_expression))
                        running_expression = []
                    else:
                        running_expression.append(line[x])
                if len(running_expression) != 0:
                    print(running_expression)
                    output.append(expression(running_expression))
                print(output)
                    


print(variables)

