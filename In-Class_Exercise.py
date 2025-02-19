print ("hello, world")

x = 'this is a string'
print(x)
y = 'this is another string'
z = x + y #This is a concatenation
print(z)
d = str(reversed(x))
print(d)
print(type(d))
#reversed command is for list only

print(x[0]) #Prints first letter of x
print(x[0:16]) #This sinclused x[0] to x[16-1]

print(x[3:10:3]) #prints 3-9 with a step of 3
print(x[16:0:-1]) #prints x in reverse order