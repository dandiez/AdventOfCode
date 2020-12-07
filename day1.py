

with open("Input1.txt") as f:
    a = [ int(line) for line in f.readlines() if line.strip()]

def find(a, target=2020):
    diff = {}
    for v in a:
        diff[v]=target-v
    for v in a:
        if diff[v] in a:
            return (v, diff[v])
    return None

def multi(li):
    val=1
    for v in li:
        val*=v
    return val

found=find(a)
print(f"Found {found} that multiply to {multi(found)}.")

for v in a:
    e = a.pop()
    diff = 2020-e
    others = find(a, target=diff)
    if others is not None:
        print(f"Found three are {e}, {others} adding up to {multi([e, *others])}.")
    

