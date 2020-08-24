class StreetMap:
    def __init__(self):
        self.intersections = dict()
        self.roads = list()
        self.roads.append(list())

import math

# City class to represent each city in the map. This allows us to keep track of cities,
# its heuristics and the outgoing paths from the city.
class City:
    def __init__(self, name, x, y, h):
        self.name, self.x, self.y, self.h = name, x, y, h
        self.neighbors = []

# For heuristic let us use Euclidian distance
def getH(pointA, pointB):
    return math.sqrt(math.pow(pointA[0]-pointB[0], 2) + math.pow(pointA[1]-pointB[1], 2))

# Actual distance is the Manhattan distance between two points
def getG(pointA, pointB):
    return abs(pointA[0]-pointB[0]) + abs(pointA[1]-pointB[1])

# A* is based on explanding node with lowest cost
# addToQueue adds element with shortest f at end of the list
# getNextCity uses list.pop() to return next node to explore
# hasNextCity returns boolean to understand if all nodes are visited or not 
class OpenQueue:
    def __init__(self):
        self.cityList = []
        self.count = 0
    
    def addToQueue(self, city, f, g, exploredPath):
        index = 0
        while index < self.count and self.cityList[index]['f'] > f:
            index += 1
        self.cityList.insert(index, { 'city': city, 'f': f, 'g': g, 'path': exploredPath })
        self.count += 1
    
    def getNextCity(self):
        if self.count > 0:
            self.count -= 1
            return self.cityList.pop()
        return None
    
    def hasNextCity(self):
        return self.count > 0

def shortest_path(M,start,goal):
    """
    extract intersections and roads from M and combine them into city objects
    """
    cities = []
    for intersection in M.intersections.items():
        # goal node might not be created by this time, so use M.intersection to get the coordinates and calculate h
        h = getH((intersection[1][0], intersection[1][1]), (M.intersections[goal][0], M.intersections[goal][1]))
        city = City(intersection[0], intersection[1][0], intersection[1][1], h)
        cities.append(city)
    
    # when adding neighbors to the city, calculate the distance too so we dont have to do it again
    for index, cityRoads in enumerate(M.roads):
        for city in cityRoads:
            cities[index].neighbors.append({ 'city': city, 'distance': getG((cities[index].x, cities[index].y), (cities[city].x, cities[city].y)) })

    # use queue to get the node with least cost value
    openList = OpenQueue()

    # use dictionary to store the visited cities with city index as key.
    # The cost of accessing an element by key in dictionary is O(1)
    visitedList = dict()

    # if more than one path is found, add it to the priority queue with distance as the cost function value.
    # Since the queue is custom implemented to have node with shortest value at end, it should give us the required value
    pathsFound = OpenQueue()

    # add start to the open list
    openList.addToQueue(start, cities[start].h, 0, [start])
    while (openList.hasNextCity()):
        currentNode = openList.getNextCity()
        if not currentNode['city'] in visitedList:
            if currentNode['city'] == goal:
                pathsFound.addToQueue(currentNode['city'], currentNode['f'], currentNode['g'], currentNode['path'])
            else:
                visitedList[currentNode['city']] = currentNode['f']
                for childElem in cities[currentNode['city']].neighbors:
                    childG = currentNode['g'] + childElem['distance']
                    childF = childG + cities[childElem['city']].h
                    childPath = [*currentNode['path'], childElem['city']]
                    openList.addToQueue(childElem['city'], childF, childG, childPath)

    if pathsFound.hasNextCity():
        return pathsFound.getNextCity()['path']
    return None

M = StreetMap()
M.intersections = {0: [0.7801603911549438, 0.49474860768712914], 1: [0.5249831588690298, 0.14953665513987202], 2: [0.8085335344099086, 0.7696330846542071], 3: [0.2599134798656856, 0.14485659826020547], 4: [0.7353838928272886, 0.8089961609345658], 5: [0.09088671576431506, 0.7222846879290787], 6: [0.313999018186756, 0.01876171413125327], 7: [0.6824813442515916, 0.8016111783687677], 8: [0.20128789391122526, 0.43196344222361227], 9: [0.8551947714242674, 0.9011339078096633], 10: [0.7581736589784409, 0.24026772497187532], 11: [0.25311953895059136, 0.10321622277398101], 12: [0.4813859169876731, 0.5006237737207431], 13: [0.9112422509614865, 0.1839028760606296], 14: [0.04580558670435442, 0.5886703168399895], 15: [0.4582523173083307, 0.1735506267461867], 16: [0.12939557977525573, 0.690016328140396], 17: [0.607698913404794, 0.362322730884702], 18: [0.719569201584275, 0.13985272363426526], 19: [0.8860336256842246, 0.891868301175821], 20: [0.4238357358399233, 0.026771817842421997], 21: [0.8252497121120052, 0.9532681441921305], 22: [0.47415009287034726, 0.7353428557575755], 23: [0.26253385360950576, 0.9768234503830939], 24: [0.9363713903322148, 0.13022993020357043], 25: [0.6243437191127235, 0.21665962402659544], 26: [0.5572917679006295, 0.2083567880838434], 27: [0.7482655725962591, 0.12631654071213483], 28: [0.6435799740880603, 0.5488515965193208], 29: [0.34509802713919313, 0.8800306496459869], 30: [0.021423673670808885, 0.4666482714834408], 31: [0.640952694324525, 0.3232711412508066], 32: [0.17440205342790494, 0.9528527425842739], 33: [0.1332965908314021, 0.3996510641743197], 34: [0.583993110207876, 0.42704536740474663], 35: [0.3073865727705063, 0.09186645974288632], 36: [0.740625863119245, 0.68128520136847], 37: [0.3345284735051981, 0.6569436279895382], 38: [0.17972981733780147, 0.999395685828547], 39: [0.6315322816286787, 0.7311657634689946]}
M.roads = [[36, 34, 31, 28, 17], [35, 31, 27, 26, 25, 20, 18, 17, 15, 6], [39, 36, 21, 19, 9, 7, 4], [35, 20, 15, 11, 6], [39, 36, 21, 19, 9, 7, 2], [32, 16, 14], [35, 20, 15, 11, 1, 3], [39, 36, 22, 21, 19, 9, 2, 4], [33, 30, 14], [36, 21, 19, 2, 4, 7], [31, 27, 26, 25, 24, 18, 17, 13], [35, 20, 15, 3, 6], [37, 34, 31, 28, 22, 17], [27, 24, 18, 10], [33, 30, 16, 5, 8], [35, 31, 26, 25, 20, 17, 1, 3, 6, 11], [37, 30, 5, 14], [34, 31, 28, 26, 25, 18, 0, 1, 10, 12, 15], [31, 27, 26, 25, 24, 1, 10, 13, 17], [21, 2, 4, 7, 9], [35, 26, 1, 3, 6, 11, 15], [2, 4, 7, 9, 19], [39, 37, 29, 7, 12], [38, 32, 29], [27, 10, 13, 18], [34, 31, 27, 26, 1, 10, 15, 17, 18], [34, 31, 27, 1, 10, 15, 17, 18, 20, 25], [31, 1, 10, 13, 18, 24, 25, 26], [39, 36, 34, 31, 0, 12, 17], [38, 37, 32, 22, 23], [33, 8, 14, 16], [34, 0, 1, 10, 12, 15, 17, 18, 25, 26, 27, 28], [38, 5, 23, 29], [8, 14, 30], [0, 12, 17, 25, 26, 28, 31], [1, 3, 6, 11, 15, 20], [39, 0, 2, 4, 7, 9, 28], [12, 16, 22, 29], [23, 29, 32], [2, 4, 7, 22, 28, 36]]

path = shortest_path(M, 5, 34)
print(path)

path = shortest_path(M, 8, 24)
print(path)

path = shortest_path(M, 5, 5)
print(path)
