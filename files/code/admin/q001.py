def add(a,b):
	print(int(a)+int(b))

for x in range(0,int(input())):
	x = input().split()
	add(x[0],x[1])