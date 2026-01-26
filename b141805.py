tasks = set()

class Dummy(object):
    def __hash__(self):
        return 0

class CorrupTrigger():
    counter = 0
    def __hash__(self):
        return 0
    def __eq__(self,other):
        if self.counter < 1:
            self.counter += 1
            tasks.add(self)
        return False

tasks.add(Dummy())
tasks.add(Dummy())
tasks.pop()
tasks.add(CorrupTrigger())
tasks | set()
