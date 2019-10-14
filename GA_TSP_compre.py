import random
import math
import matplotlib.pyplot as plt

SCORE_NONE = -1
class Life(object):
    """个体类"""

    def __init__(self, aGene=None):
        self.gene = aGene
        self.score = SCORE_NONE  # 初始化生命值 #

class GA(object):
    """遗传算法类"""

    def __init__(self, aCrossRate, aMutationRage, aLifeCount, aGeneLenght, aMatchFun=lambda life: 1):
        self.croessRate = aCrossRate  # 交叉概率 #
        self.mutationRate = aMutationRage  # 突变概率 #
        self.lifeCount = aLifeCount   # 个体数 #
        self.geneLenght = aGeneLenght  # 基因长度 #
        self.matchFun = aMatchFun  # 适配函数
        self.lives = []  # 种群
        self.best = None  # 保存这一代中最好的个体
        self.generation = 1  # 第几代 #
        self.crossCount = 0  # 交叉数量 #
        self.mutationCount = 0  # 突变个数 #
        self.bounds = 0.0  # 适配值之和，用于选择时计算概率
        self.initPopulation()  # 初始化种群 #

    def initPopulation(self):
        """初始化种群"""
        self.lives = []
        for i in range(self.lifeCount):
            gene = [x for x in range(self.geneLenght)]
            random.shuffle(gene)  # 随机洗牌 #
            life = Life(gene)
            self.lives.append(life)

    def judge(self):
        """评估，计算每一个个体的适配值"""
        self.bounds = 0.0
        self.best = self.lives[0]
        for life in self.lives:
            life.score = self.matchFun(life)
            self.bounds += life.score
            if self.best.score < life.score:   # score为距离的倒数越小越好 #
                self.best = life

    def cross(self, parent1, parent2):
        """
        函数功能：交叉
        函数实现：随机交叉长度为n的片段，n为随机产生
        """
        index1 = random.randint(0, self.geneLenght - 1)  # 随机生成突变起始位置 #
        index2 = random.randint(index1, self.geneLenght - 1)  # 随机生成突变终止位置 #
        tempGene = parent2.gene[index1:index2]  # 交叉的基因片段
        newGene = []
        p1len = 0
        for g in parent1.gene:
            if p1len == index1:
                newGene.extend(tempGene)  # 插入基因片段
                p1len += 1
            if g not in tempGene:
                newGene.append(g)
                p1len += 1
        self.crossCount += 1
        return newGene

    def mutation(self, gene):
        """突变"""
        index1 = random.randint(0, self.geneLenght - 1)
        index2 = random.randint(0, self.geneLenght - 1)
        # 随机选择两个位置的基因交换--变异 #
        newGene = gene[:]  # 产生一个新的基因序列，以免变异的时候影响父种群
        newGene[index1], newGene[index2] = newGene[index2], newGene[index1]
        self.mutationCount += 1
        return newGene

    def getOne(self):
        """选择一个个体"""
        r = random.uniform(0, self.bounds)
        for life in self.lives:
            r -= life.score
            if r <= 0:
                return life

        raise Exception("选择错误", self.bounds)

    def newChild(self):
        """产生新的后代"""
        parent1 = self.getOne()
        rate = random.random()

        # 按概率交叉 #
        if rate < self.croessRate:
            # 交叉 #
            parent2 = self.getOne()
            gene = self.cross(parent1, parent2)
        else:
            gene = parent1.gene

        # 按概率突变 #
        rate = random.random()
        if rate < self.mutationRate:
            gene = self.mutation(gene)

        return Life(gene)

    def next(self):
        """产生下一代"""
        self.judge()
        newLives = []
        newLives.append(self.best)  # 把最好的个体加入下一代 #
        while len(newLives) < self.lifeCount:
            newLives.append(self.newChild())
        self.lives = newLives
        self.generation += 1




class TSP(object):
    def __init__(self, aLifeCount=100, ):
        self.initCitys()
        self.lifeCount = aLifeCount
        self.ga = GA(aCrossRate=0.7,
                     aMutationRage=0.02,
                     aLifeCount=self.lifeCount,
                     aGeneLenght=len(self.citys),
                     aMatchFun=self.matchFun())

    def initCitys(self):
        self.citys = []
        """
        for i in range(34):
              x = random.randint(0, 1000)
              y = random.randint(0, 1000)
              self.citys.append((x, y))
        """

        # 47城市经纬度
        self.citys.append((6734, 1453))
        self.citys.append((2233, 10))
        self.citys.append((5530, 1424))
        self.citys.append((3082, 1644))
        self.citys.append((7608, 4458))
        self.citys.append((7573, 3716))
        self.citys.append((7265, 1268))
        self.citys.append((6898, 1885))
        self.citys.append((1112, 2049))
        self.citys.append((5468, 2606))
        self.citys.append((5989, 2873))
        self.citys.append((4706, 2674))
        self.citys.append((4612, 2035))
        self.citys.append((6347, 2683))
        self.citys.append((6107, 669))
        self.citys.append((7611, 5184))
        self.citys.append((7462, 3590))
        self.citys.append((7732, 4723))
        self.citys.append((5900, 3561))
        self.citys.append((4483, 3369))
        self.citys.append((6101, 1110))
        self.citys.append((5199, 2182))
        self.citys.append((1633, 2809))
        self.citys.append((4307, 2322))
        self.citys.append((675, 1006))
        self.citys.append((7555, 4819))
        self.citys.append((7541, 3981))
        self.citys.append((3177, 756))
        self.citys.append((7352, 4506))
        self.citys.append((7545, 2801))
        self.citys.append((3245, 3305))
        self.citys.append((6426, 3173))
        self.citys.append((4608, 1198))
        self.citys.append((23, 2216))
        self.citys.append((7248, 3779))
        self.citys.append((7762, 4595))
        self.citys.append((7392, 2244))
        self.citys.append((3484, 2829))
        self.citys.append((6271, 2135))
        self.citys.append((4985, 140))
        self.citys.append((1916, 1569))
        self.citys.append((7280, 4899))
        self.citys.append((7509, 3239))
        self.citys.append((10, 2676))
        self.citys.append((6807, 2993))
        self.citys.append((5185, 3258))
        self.citys.append((3023, 1942))

    def distance(self, order):
        distance = 0.0
        for i in range(-1, len(self.citys) - 1):  # 取到-1，因为要形成一个回路形成一个哈密顿图 #
            index1, index2 = order[i], order[i + 1]
            city1, city2 = self.citys[index1], self.citys[index2]
            distance += math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)  # 欧式距离 #

            """
            R = 6371.004
            Pi = math.pi
            LatA = city1[1]
            LatB = city2[1]
            MLonA = city1[0]
            MLonB = city2[0]
            C = math.sin(LatA*Pi / 180) * math.sin(LatB * Pi / 180) + math.cos(LatA * Pi / 180) * math.cos(LatB * Pi / 180) * math.cos((MLonA - MLonB) * Pi / 180)
            D = R * math.acos(C) * Pi / 100
            distance += D
            """
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
            print(("第%d代 : 当前最小距离%f") % (self.ga.generation, distance))
            n -= 1
        print('当前最优路线:')
        string = ''
        for index in self.ga.best.gene:
            string += str(index) + '->'
        print(string[0:len(string)-2])

        '''画图函数'''
        plt.plot(generate, distance_list)
        plt.xlabel('generation')
        plt.ylabel('distance')
        plt.title('generation--distance')
        plt.show()

if __name__ == '__main__':


    tsp = TSP()
    tsp.run(100)

    # dist = [
    #     [0, 5, 3, math.inf, math.inf, math.inf],
    #     [5, 0, math.inf, 8, 14, 17],
    #     [3, math.inf, 0, 16, 11, math.inf],
    #     [math.inf, 8, 16, 0, math.inf, 9],
    #     [math.inf, 14, 11, math.inf, 0, 10],
    #     [math.inf, 17, math.inf, 9, 10, 0]
    # ]