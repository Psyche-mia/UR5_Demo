import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt, cv2

#Create necessary classes and functions
#Create class to handle "cities"
class City:
    def __init__(self, x, y, i):
        self.x = x
        self.y = y
        self.index = i
    
    def distance(self, city):
        xDis = abs(self.x - city.x)
        yDis = abs(self.y - city.y)
        distance = np.sqrt((xDis ** 2) + (yDis ** 2))
        return distance
    
    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + "," + str(self.index) + ")"

#Create a fitness function
class Fitness:
    def __init__(self, route):
        self.route = route
        self.distance = 0
        self.fitness= 0.0
    
    def routeDistance(self):
        if self.distance ==0:
            pathDistance = 0
            for i in range(0, len(self.route)):
                fromCity = self.route[i]
                toCity = None
                if i + 1 < len(self.route):
                    toCity = self.route[i + 1]
                else:
                    toCity = self.route[0]
                pathDistance += fromCity.distance(toCity)
            self.distance = pathDistance
        return self.distance
    
    def routeFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeDistance())
        return self.fitness

#Create our initial population
#Route generator
def createRoute(cityList):
    route = random.sample(cityList, len(cityList))
    return route

#Create first "population" (list of routes)
def initialPopulation(popSize, cityList):
    population = []

    for i in range(0, popSize):
        population.append(createRoute(cityList))
    return population

#Create the genetic algorithm
#Rank individuals

def rankRoutes(population):
    fitnessResults = {}
    for i in range(0,len(population)):
        fitnessResults[i] = Fitness(population[i]).routeFitness()
    return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)

#Create a selection function that will be used to make the list of parent routes
def selection(popRanked, eliteSize):
    selectionResults = []
    df = pd.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
    
    for i in range(0, eliteSize):
        selectionResults.append(popRanked[i][0])
    for i in range(0, len(popRanked) - eliteSize):
        pick = 100*random.random()
        for i in range(0, len(popRanked)):
            if pick <= df.iat[i,3]:
                selectionResults.append(popRanked[i][0])
                break
    return selectionResults


#Create mating pool

def matingPool(population, selectionResults):
    matingpool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])
    return matingpool

#Create a crossover function for two parents to create one child
def breed(parent1, parent2):
    child = []
    childP1 = []
    childP2 = []
    
    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))
    
    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        childP1.append(parent1[i])
        
    childP2 = [item for item in parent2 if item not in childP1]

    child = childP1 + childP2
    return child


def breedPopulation(matingpool, eliteSize):
    children = []
    length = len(matingpool) - eliteSize
    pool = random.sample(matingpool, len(matingpool))

    for i in range(0,eliteSize):
        children.append(matingpool[i])
    
    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool)-i-1])
        children.append(child)
    return children

def mutate(individual, mutationRate):
    for swapped in range(len(individual)):
        if(random.random() < mutationRate):
            swapWith = int(random.random() * len(individual))
            
            city1 = individual[swapped]
            city2 = individual[swapWith]
            
            individual[swapped] = city2
            individual[swapWith] = city1
    return individual

def mutatePopulation(population, mutationRate):
    mutatedPop = []
    
    for ind in range(0, len(population)):
        mutatedInd = mutate(population[ind], mutationRate)
        mutatedPop.append(mutatedInd)
    return mutatedPop


def nextGeneration(currentGen, eliteSize, mutationRate):
    popRanked = rankRoutes(currentGen)
    selectionResults = selection(popRanked, eliteSize)
    matingpool = matingPool(currentGen, selectionResults)
    children = breedPopulation(matingpool, eliteSize)
    nextGeneration = mutatePopulation(children, mutationRate)
    return nextGeneration


def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations):
    pop = initialPopulation(popSize, population)
    print("Initial distance: " + str(1 / rankRoutes(pop)[0][1]))
    
    for i in range(0, generations):
        pop = nextGeneration(pop, eliteSize, mutationRate)

    print("Final distance: " + str(1 / rankRoutes(pop)[0][1]))
    bestRouteIndex = rankRoutes(pop)[0][0]
    bestRoute = pop[bestRouteIndex]
    return bestRoute


def geneticAlgorithmPlot(population, popSize, eliteSize, mutationRate, generations):
    pop = initialPopulation(popSize, population)
    progress = []
    progress.append(1 / rankRoutes(pop)[0][1])
    
    for i in range(0, generations):
        pop = nextGeneration(pop, eliteSize, mutationRate)
        progress.append(1 / rankRoutes(pop)[0][1])
    
    plt.plot(progress)
    plt.ylabel('Distance')
    plt.xlabel('Generation')
    plt.show()

if __name__ == '__main__':
    
    cityList = []
    img = cv2.imread('turtle.jpg')
    img_h, img_w, img_c = img.shape

    draw_height = 0.20	# 20cm
    pen_thickness = 0.004	# 5mm 
    cnt_th = max(int(img_h/draw_height*pen_thickness),1)

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, binary =cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)
    binary,contours, hierarchy =cv2.findContours(binary,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # Skeletonize
    skel = np.zeros(gray.shape,np.uint8)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    done = False
 
    while( not done):
        eroded = cv2.erode(binary,element)
        temp = cv2.dilate(eroded,element)
        temp = cv2.subtract(binary,temp)
        skel = cv2.bitwise_or(skel,temp)
        binary = eroded.copy()
 
        zeros = img_h - cv2.countNonZero(binary)
        if zeros==img_h:
            done = True

    skel = cv2.dilate(skel, np.ones((5,5))) #5
    skel = cv2.erode(skel, np.ones((3,3)))  #3

    cv2.imshow('dst',skel)
    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()

    # Extract contours
    draw_cnt = []
    while True:
        _, contours, hierarchy =cv2.findContours(skel,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        draw_cnt.append(contours[0])
        cv2.drawContours(skel, contours, 0, 0, 11)
    
        if len(contours) < 2:
            break
        
    print('shapes drawn: ', len(draw_cnt))

    # TSP
    for i in range(len(draw_cnt)):
        cityList.append(City(x=int(draw_cnt[i][0][0][0]), y=int(draw_cnt[i][0][0][1]), i=i))
    print cityList

    final_list = geneticAlgorithm(population=cityList, popSize=100, eliteSize=20, mutationRate=0.01, generations=500)

    # Show TSP result
    # Draw in different colors
    n = int(180/len(draw_cnt))
    for i in range(len(final_list)):
        city = final_list[i]
        color = cv2.cvtColor(np.uint8([[[n*i,255,255]]]), cv2.COLOR_HSV2BGR)
        color = color[0][0].tolist()
        cv2.drawContours(img, draw_cnt, city.index, color, cnt_th)
        
        cv2.imshow('dst', img)
        if cv2.waitKey(0) & 0xff == 27:
            cv2.destroyAllWindows()

    #geneticAlgorithmPlot(population=cityList, popSize=100, eliteSize=20, mutationRate=0.01, generations=500)
