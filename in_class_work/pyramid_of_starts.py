'''Goal: To print following...
     * * *
    * * * *
'''
#First, we print something simpler: a square
#We use a print statement for each row
#We use a loop to go through all 10 rows
row_of_stars_list = []
n=10
for row in range(n): #row goes through the numbers - 0, ... n-1
    row_of_stars_list = []
    for col in range(n-1): #col goes through the numbers - 0, ... n-1
        row_of_stars_list += ['*']
    row_of_stars_list =''.join(row_of_stars_list)
    #print(row_of_stars_list)


#More Efficiency
for row in range(n):
    print('*'*n)

#Now, we print a triangle
for row in range(n):
    print((' ' * (n - 1 - row)) + ('* ' * (row + 1)) + (' ' * (n - 1 - row)))