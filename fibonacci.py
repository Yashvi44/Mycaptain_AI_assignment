def fibonacci (x):
	fn=[0,1]
	for i in range(2,x):
		fn.append(fn[-1]+fn[-2])
	return fn
x=int(input("Enter no. of fibonacci no. you want to generate:"))
seq=fibonacci(x)
print(seq)