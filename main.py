
f = open("text.txt", "r")
a = f.read().split('.')

b = open("text1.txt", "a")
for seq in a:
    b.write(seq + '\n')
b.close()

print(b)