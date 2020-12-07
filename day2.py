
class Pass():

    def __init__(self, line, *args, **kwargs):
        a, self.password = line.split(": ")
        nums, self.letter = a.split()
        self.min, self.max = map(int, nums.split("-"))

    def is_valid(self):
        count = self.password.count(self.letter)
        if count < self.min or count > self.max:
            return False
        return True

    def new_is_valid(self):
        valid_letters = 0
        try:
            if self.password[self.min-1] == self.letter:
                valid_letters+=1
        except:
            pass
        try:
            if self.password[self.max-1] == self.letter:
                valid_letters+=1
        except:
            pass
        if valid_letters == 1:
            return True
        return False


with open("input2.txt") as f:
    lines = f.readlines()
print(sum([Pass(p).is_valid() for p in lines]))
print(sum([Pass(p).new_is_valid() for p in lines]))
