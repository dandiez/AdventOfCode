


with open("input4.txt") as f:
    raw = f.read()

pp = raw.split("\n\n")
ppd = list()
for p in pp:
    
    p=p.replace("\n", " ")
    p=p.strip()
    if not p:
        continue
    pairs = p.split(" ")
    ppd.append({s.split(":")[0]:s.split(":")[1] for s in pairs})
    
    

def isvalid(p):
    if not {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}.issubset(ks):
        return False
    print(p)
    
    if not len(p["byr"])==4:
        return False
    if not (1920<= int(p["byr"]) <= 2002):
        return False
    if not (2010<= int(p["iyr"]) <=2020):
        return False
    if not (2020<= int(p["eyr"]) <=2030):
        return False

    if p["hgt"].endswith("cm"):
        num = p["hgt"].split("cm")[0]
        if not 150 <= int(num) <=193:
            return False
    elif p["hgt"].endswith("in"):
        num = p["hgt"].split("in")[0]
        if not (59 <= int(num) <=76):
            return False
    else:
        return False

    if not p["hcl"].startswith("#"):
        return False
    if not len(p["hcl"])==7:
        return False
    for c in p["hcl"][1:]:
        if not c in "abcdef0123456789":
            return False

    if not p["ecl"] in ["amb", "blu", "brn", "gry", "grn", "hzl" ,"oth"]:
        return False

    if not len(p["pid"])==9:
        return False
    for c in p["pid"]:
        if not c in "0123456789":
            return False


    return True

ok = 0
for p in ppd:
    ks = set( p.keys())
    if isvalid(p):
        ok+=1
print(ok)