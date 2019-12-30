""" 12/28/19 -- Playing around with ideas for computational engine implementation, mostly taken
    from https://en.wikipedia.org/wiki/Subjective_logic
"""
from random import randint
from random import choice


props = ["The sky is red.", "Socrates was a man.", "2+2=4", "Icecream tastes good.", "It's not the case that I'm not going bald.", "The human torch was denied a bank loan."]

#binomial opinion modeling
#x in X can only take on True or False
#random and manual domain generation
domain = {x:bool(randint(0,1)) for x in props}
domain = {props[0]:False, props[1]:True, props[2]:True, props[3]:True, props[4]:False, props[5]:False}

sources = ("Wikipedia", "Donald Trump", "Einstein", "My dad's common sense", "Oxford Dictionary")
actors = ("Me", "Einstein")


#GENERAL NOTES:
#model the constraing of bx,dx,ux,ax in [0,1] with ints to prevent floating point headaches, so
#we'll discretize to the hundredths place and use [0,100] as ints instead.  Might not be viable
#for actual application, but that's an architectural and implementation detail, not a conceptual
#one relevant to the engine prototype, at this time.
#
#we can make things more usable by defining smart defaults; e.g., have ax=100 be the default if more props in the domain
#are True than False, etc...  For now we'll just use dumb defaults
_VALID_PROBABILITY_RANGE = [0, 100]
def numInRange(num):
    return  _VALID_PROBABILITY_RANGE[0] <= num <= _VALID_PROBABILITY_RANGE[1]

class Opinion:
    """default opinion will be one of an actor being completely uncertain of an arbitrary true proposition from an unknown source
    """
    bx = 0
    dx = 0
    ux = 100
    ax = 100
    wx = (bx, dx, ux, ax)
    x = "nothing"
    src = "nobody"

    def __init__(self, *args, **kwords):
        if len(args) == 6:
            self.bx = args[0]
            self.dx = args[1]
            self.ux = args[2]
            self.ax = args[3]
            self.x = args[4]
            self.src = args[5]

    def __str__(self):
        return "{} certain about {}, from {}.".format(self.bx if self.bx > self.dx else self.dx, self.x, self.src)

    def isCoherent(self):
        return self.isComplete() and self.allInRange()
    def isComplete(self):
        return self.bx + self.dx +self.ux == 100
    def allInRange(self):
        return all([numInRange(x) for x in self.wx])

class Actor():
    opinions = []
    name = ""

    def __init__(self, *args, **kwords):
        if len(args) > 0:
            self.name = args[0]

    def isValidActor(self):
        return self.name in actors

    def stateOpinions(self):
        if self.name == "Me" or self.name == "me": self.name = "I"
        x = [print(self.name + " {} ".format("am" if self.name == "I" else "is") + str(o)) for o in self.opinions]

    def addOpinion(self, opi):
        self.opinions.append(opi)

props = {"the sky is red":False, "Socrates was a man":True, "2+2=4":True, "icecream tastes good":True, "it's not the case that I'm not going bald":False, "the human torch was denied a bank loan":False, "this is a sentence":True, "this is not a sentence":False}

numOpinions = len(props)
oprange = range(0, numOpinions)
opinionSet = [[],[],[],[],[],[]]
opinionSet[0] = [x*10 for x in oprange]
opinionSet[1] = [100-(x*10) for x in oprange]
opinionSet[2] = [0 for x in oprange]
opinionSet[3] = [props[list(props.keys())[x]] for x in oprange]
opinionSet[4] = list(props.keys())
opinionSet[5] = [choice(sources) for x in oprange]
#print(opinionSet)


###########runtime utilities and statements###########
def opinion(bx = 0, dx = 0, ux = 0, ax = 0, x = "", src = "", printOnly = False):
    o = Opinion(bx, dx, ux, ax, x, src)
    #give a printable version of the opinion only if the caller wants it
    return [str(o), o.isCoherent()] if printOnly else o

#It's ok to redefine props at runtime, in case something happened on the way that  misaligned props with their truth vals
props = list(domain.keys())
domainLen = len(props)

#Test stuff
#I learned that the sky is red from Donald Trump
me = Actor("Me")

#assume all columns in opinionSet are the same length
numRows = len(opinionSet[0])
os = opinionSet
x = [me.addOpinion(opinion(os[0][r],os[1][r],os[2][r],os[3][r],os[4][r],os[5][r])) for r in range(0,numRows)]

print(me.stateOpinions())




