


#with open("input6.txt") as f:
#    raw = f.read()

#pp = raw.split("\n\n")

#sum = 0
#for a in pp:

#    if not a:
#        continue
#    alist = a.split("\n")
#    a_all = "".join(alist)
#    aset=set()
#    for a in a_all:
#        aset.add(a)
#    sum += len(aset)
    
#print(sum)
    

with open("input6.txt") as f:
    raw = f.read()

pp = raw.split("\n\n")

sum = 0
for a in pp:
    if not a:
        continue
    alist = a.split("\n")
    a_sets = [ set(list(a)) for a in alist]
    sum += len(set.intersection(*a_sets))
print(sum)
    