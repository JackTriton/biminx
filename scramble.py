#biminx scrambler
import random
import copy

bminit= [0,1,2,2,3,3,4,5,5,0,1,
         6,7,8,9,10,11,12,13,14,15,
         6,7,16,16,8,9,17,17,10,11,18,18,12,19,19,13,14,20,20,15,
         21,22,22,23,23,24,25,26,27,28,
         21,31,31,32,32,24,25,26,27,28,21]
bminit = [x+1 for x in bminit]

FACES = {"U":  [0,9,8,1,10,7,2,3,4,5,6],
         "F":  [4,5,6,15,16,17,29,30,31,32,33],
         "R":  [6,7,8,17,18,19,33,34,35,36,37],
         "BR": [8,9,0,19,20,11,37,38,39,40,21],
         "BL": [0,1,2,11,12,13,21,22,23,24,25],
         "L":  [2,3,4,13,14,15,25,26,27,28,29],
         "DR": [31,32,33,46,47,34,56,57,58,48,35],
         "DBR":  [35,36,37,48,49,38,58,59,60,50,39],
         "DBL":[23,24,25,42,43,26,52,53,54,44,27],
         "DL": [27,28,29,44,45,30,54,55,56,46,31]}
"""
         "B":[39,40,21,50,41,22,60,51,52,42,23],
         "D":  [60,51,52,59,61,53,58,57,56,55,54]}
"""
def _rotate(fc):
    return [fc[6], fc[3],fc[0],fc[7],fc[4],fc[1],fc[8],fc[9],fc[10],fc[5],fc[2]]

def normalize(cubelist, keepzeros=False):
    """ Normalize a cubelist to get unique bandage shape representation. You
    don't normally need to be calling this. """
    cube = copy.deepcopy(cubelist)
    # handle zeros, which represent non-connected cubies, first
    if not keepzeros:
        blockno = 1 + max([1] + cube)
        for i, v in enumerate(cube):
            if v == 0:
                cube[i] = blockno
                blockno += 1

    # now re-number blocks in reading order
    blockno = 1
    mapping = {0: 0}
    for v in cube:
        if v in mapping or v == 0:
            continue
        else:
            mapping[v] = blockno
            blockno += 1
    return list(map(lambda x: mapping[x], cube))

def turn(move, num, minx):
    face = FACES[move]
    facecontent = [minx[i] for i in face]
    turned = facecontent
    h = 0
    while h < num:
        turned = _rotate(turned)
        h += 1
    newminx = copy.deepcopy(minx)
    for i, fi in enumerate(face):
        newminx[fi] = turned[i]
    c = "2" if num in [2,3] else ""
    d = "-" if num in [3,4] else ""
    n = move + c + d
    return n, normalize(newminx)

def turnable(prev, minx):
    for num in range(33):
        if minx.count(num) == 1:
            h = num
            break
    free = minx.index(h)
    g = []
    for x,y in FACES.items():
        faceb = set([minx[i] for i in y])
        restb = set([minx[i] for i in set(range(62)) - set(y)])
        if free in y and not faceb & restb:
            g.append(x)
    if prev is not None:
        g.remove(prev)
    return g

def movable(move, prev, minx):
    faceb = set([minx[i] for i in FACES[move]])
    restb = set([minx[i] for i in set(range(62)) - set(FACES[move])])
    if faceb & restb:
        return False
    if prev is None:
        return True
    if prev == move:
        return False
    return True
class SCR:
    def __init__(self):
        self.current=[]
        
    def scr(self,minx,depth):
        if depth == 0:
            return True
        prev = self.current[-1].replace("-","").replace("2","") if self.current else None
        tuna = turnable(prev,minx)
        if tuna == []:
            return False
        fd = []
        for a in tuna:
            fd += [[a,1],[a,2],[a,3],[a,4]]
        
        random.shuffle(fd)
        for x in fd:
            m, nminx = turn(x[0], x[1], minx)
            self.current.append(m)
            if self.scr(nminx, depth - 1):
                return True
            self.current.pop()
    def start_scr(self, turns=70):
        TeP = True
        while TeP:
            if self.scr(bminit, turns):
                if "".join(self.current).count("D") >= turns//10:
                    TeP=False
                else:
                    self.current=[]
        e = ""
        n = len(self.current)
        for i,a in enumerate(self.current):
            if i+1 == n:
                e+=a
            else:
                e += f"{a}, "
                if i%10 == 9:
                    e += "\n"
        return e
    def n_scramble(self, turns=70, n=1):
        i = 0
        while i<n:
            self.current=[]
            am = self.start_scr(turns=turns)
            print(f"{i+1}:{am}\n\n")
            i += 1
            
fin = SCR()
fin.n_scramble(n=5)
