i = int(input("input"))
sum = 0
if i<1:
  exit()
else:
  while i>0:
    b = 2
    c = 1
    while b<=i:
      c=b*c
      b=b+1
    sum += c
    i = i-1
    # print(c)
print(sum)
