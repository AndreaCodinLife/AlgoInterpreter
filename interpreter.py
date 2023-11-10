import re

constants = {}
variables = {}

def read(var):
    value = input("Enter value for {}: ".format(var))
    variables[var] = value

def write(content):
    print(content)

def execute(lines):
    while lines:
        line = lines.pop(0)
        # Handle variable declarations
        if line.startswith("Variables:"):
            # Read all variable declarations until 'Begin'
            while line.strip() != "Begin":
                line = lines.pop(0)
                # Extract variable name and type
                match = re.match(r"(\w+)\s*:\s*(\w+)", line)
                if match is not None:
                    var, type_ = match.groups() 
                    if type_ == "int":
                        variables[var] = 0
                    elif type_ == "string":
                        variables[var] = ""
                    elif type_ == "bool":
                        variables[var] = False
                    else:
                        raise Exception("Unknown type: {}".format(type_))
        # Handle constant declarations 
        elif line.startswith("Constants:"):
            # Read all variable declarations until 'Begin'
            while line.strip() != "Variables:" and line.strip() != "Begin":
                line = lines.pop(0)
                # Extract variable name and type
                match = re.match(r"(\w+)\s*=\s*(.*)", line)
                if match is not None:
                    var, value = match.groups()
                    constants[var] = eval_expr(value)

        # Handle assignments (with potential name of variable on the right side)
        elif re.match(r"^(\w+)\s*<-\s*(.*)$", line):
            var_name, expr = re.match(r"^(\w+)\s*<-\s*(.*)$", line).groups()
            value = eval_expr(expr)
            variables[var_name] = value
            print("Assign {} <- {}".format(var_name, value))

        # Handle reads
        elif re.match(r"^Read\((.*)\)$", line):
            var_name = re.match(r"^Read\((.*)\)$", line).group(1)
            read(var_name)
        
        # Handle writes
        elif re.match(r"^Write\((.*)\)$", line):
            content = re.match(r"^Write\((.*)\)$", line).group(1)
            write(eval_expr(content))

        # Handle if statements
        elif re.match(r"^If (.*) Then$", line):
            condition = re.match(r"^If (.*) Then$", line).group(1)
            # if the condition is = then replace it with ==
            condition = re.sub(r"=", "==", condition)
            #if the condition is true then execute the block of code, else skip it
            if eval_expr(condition):
                execute_block(lines)
            else:
                while lines:
                    line = lines.pop(0)
                    if line.strip() == "Else" or line.strip() == "End If":
                        break
        # Handle else statements
        elif re.match(r"^Else$", line):
            # Skip the else block
            while lines:
                line = lines.pop(0)
                if line.strip() == "End If":
                    break
        
        # Handle for loops
        elif re.match(r"^For (.*) <- (.*) To (.*) Do$", line):
            var_name, start, end = re.match(r"^For (.*) <- (.*) To (.*) Do$", line).groups()
            start = eval_expr(start)
            end = eval_expr(end)
            variables[var_name] = start
            #get all the lines in the for loop
            lines_in_for_loop = []
            while lines:
                line = lines.pop(0)
                if line.strip() == "End For":
                    break
                lines_in_for_loop.append(line)

            #multiply the lines_in_for_loop by the number of times the for loop will run
            lines_in_for_loop *= (end - start + 1)
            
            #print("Starting for loop from {} to {}".format(start, end))
            print(lines_in_for_loop)
            while variables[var_name] <= end:
                execute_block(lines_in_for_loop)
                #print("Incrementing {}".format(var_name))
                variables[var_name] += 1
            #print("End for loop")

        # Handle while loops  (A dev car il y a un problème dans la gestion de la condition)
        elif re.match(r"^While (.*) Do$", line):
            condition = re.match(r"^While (.*) Do$", line).group(1)
            # if the condition is = then replace it with ==
            condition = re.sub(r"=", "==", condition)
            #get all the lines in the while loop
            lines_in_while_loop = []
            while lines:
                line = lines.pop(0)
                if line.strip() == "End While":
                    break
                lines_in_while_loop.append(line)
            #Multiply the lines_in_while_loop by the number of times the while loop will run (30)
            lines_in_while_loop *= 2
            #print(lines_in_while_loop)
            #print("Starting while loop")
            m = "START"
            while eval_expr(condition):
                #check if the condition is still true
                #print("Checking condition")
                #print(condition)
                print("Condition is: ")
                print(condition)
                print(eval_expr(condition))
                if not eval_expr(condition):
                    m = "STOP"
                    break
                print(m)
                execute_block(lines_in_while_loop)
            #print("End while loop")


        # Handle Begin of block
        elif re.match(r"^Begin$", line):
            execute_block(lines)

        # Handle end of block
        elif line.strip() == "End":
            break
        
        # Ignore comments
        elif re.match(r"^\(\*.*\*\)$", line):
            continue
def execute_block(lines):
    block_lines = []
    while lines:
        line = lines.pop(0)
        if line.strip() == "End":
            break
        block_lines.append(line)
    execute(block_lines)

def eval_expr(expr):
    if expr in variables:
        return variables[expr]
    else:
        return eval(expr, constants, variables)

# Read the program from the file
with open("program.txt") as f:
    lines = f.readlines()

execute(lines)
