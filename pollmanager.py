class Poll():
    def __init__(self, text="New Poll", poss={}, answ={}):
        self.text = text
        self.poss = poss
        self.answ = answ

    def addposs(self, txt):
        i = 0
        while i in self.poss:
            i += 1
        self.poss[i] = txt

    def removeposs(self, index):
        self.poss.pop(index)

    def vote(self, uid, index):
        self.answ[uid] = index

    def removevote(self, uid):
        self.answ.pop(uid)

    def clearvotes(self):
        self.answ = {}

    def displayposs(self):
        text = ""
        for x in self.poss:
            text += f"{x} : {self.poss[x]}\n"
                
        return text

    def displayansw(self):
        results = {}
        for key, value in self.answ.items():
            if value in results:
                results[value] += 1
            else:
                results[value] = 1

        print(results)
        outp = []
        while not len(results) == 0:
            h = 0
            k = None
            for key, value in results.items():
                if value >= h:
                    k = key
                    h = value
            outp.append((k, h))
            results.pop(k)

        print(str(outp) + " " + str(results))

        text = ""
        for y in outp:
            text += f"{self.poss[y[0]]} : {y[1]}"

        return text