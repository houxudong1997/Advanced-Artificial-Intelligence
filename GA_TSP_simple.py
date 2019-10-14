import random
import math

class Life(object):
    def __init__(self, aGene=None):
        self.gene = aGene
        self.score = -1
class GA(object):
    def __init__(self, aCrossRate, aMutationRage, aLifeCount, aGeneLenght, aMatchFun=lambda life: 1):
        self.croessRate = aCrossRate
        self.mutationRate = aMutationRage
        self.lifeCount = aLifeCount
        self.geneLenght = aGeneLenght
        self.matchFun = aMatchFun
        self.lives = []
        self.best = None
        self.generation = 1
        self.crossCount = 0
        self.mutationCount = 0
        self.bounds = 0.0
        self.initPopulation()

    def initPopulation(self):
        self.lives = []
        for i in range(self.lifeCount):
            gene = [x for x in range(self.geneLenght)]
            random.shuffle(gene)
            life = Life(gene)
            self.lives.append(life)

    def judge(self):
        self.bounds = 0.0
        self.best = self.lives[0]
        for life in self.lives:
            life.score = self.matchFun(life)
            self.bounds += life.score
            if self.best.score < life.score:
                self.best = life

    def cross(self, parent1, parent2):
        index1 = random.randint(0, self.geneLenght - 1)
        index2 = random.randint(index1, self.geneLenght - 1)
        tempGene = parent2.gene[index1:index2]
        newGene = []
        p1len = 0
        for g in parent1.gene:
            if p1len == index1:
                newGene.extend(tempGene)
                p1len += 1
            if g not in tempGene:
                newGene.append(g)
                p1len += 1
        self.crossCount += 1
        return newGene

    def mutation(self, gene):
        index1 = random.randint(0, self.geneLenght - 1)
        index2 = random.randint(0, self.geneLenght - 1)
        newGene = gene[:]
        newGene[index1], newGene[index2] = newGene[index2], newGene[index1]
        self.mutationCount += 1
        return newGene

    def getOne(self):
        r = random.uniform(0, self.bounds)
        for life in self.lives:
            r -= life.score
            if r <= 0:
                return life
        raise Exception("选择错误", self.bounds)

    def newChild(self):
        parent1 = self.getOne()
        rate = random.random()
        if rate < self.croessRate:
            parent2 = self.getOne()
            gene = self.cross(parent1, parent2)
        else:
            gene = parent1.gene

        rate = random.random()
        if rate < self.mutationRate:
             gene = self.mutation(parent1.gene)
        else:
            gene = parent1.gene

        return Life(gene)

    def next(self):
        self.judge()
        newLives = []
        newLives.append(self.best)
        while len(newLives) < self.lifeCount:
            newLives.append(self.newChild())
        self.lives = newLives
        self.generation += 1

class TSP(object):
    def __init__(self, aLifeCount=50, ):
        self.initCitys()
        self.lifeCount = aLifeCount
        self.ga = GA(aCrossRate=0.7,
                     aMutationRage=0.02,
                     aLifeCount=self.lifeCount,
                     aGeneLenght=len(self.citys),
                     aMatchFun=self.matchFun())

    def initCitys(self):
        self.citys = [0,1,2,3,4,5]
        self.dist = [
             [0, 5, 3, math.inf, math.inf, math.inf],
             [5, 0, math.inf, 8, 14, 17],
             [3, math.inf, 0, 16, 11, math.inf],
             [math.inf, 8, 16, 0, math.inf, 9],
             [math.inf, 14, 11, math.inf, 0, 10],
             [math.inf, 17, math.inf, 9, 10, 0]
         ]

    def distance(self, order):
        distance = 0.0
        for i in range(-1, len(self.citys) - 1):
            index1, index2 = order[i], order[i + 1]
            city1, city2 = self.citys[index1], self.citys[index2]
            distance += self.dist[city1][city2]
        return distance

    def matchFun(self):
        return lambda life: 1.0 / self.distance(life.gene)

    def run(self, n):
        distance_list = []
        generate = [index for index in range(1, n + 1)]
        while n > 0:
            self.ga.next()
            distance = self.distance(self.ga.best.gene)
            distance_list.append(distance)
            n -= 1
        print(("第%d代 : 最小距离%f") % (self.ga.generation, distance))
        print('当前最优路线:')
        string = ''
        for index in self.ga.best.gene:
            string += str(index) + '->'
        print(string[0:len(string)-2])

if __name__ == '__main__':
    tsp = TSP()
    tsp.run(100)