inp = input("enter a string: ")
output = "hello " + inp
with open('output.txt', 'w') as f:
    f.write(output)
    f.close()