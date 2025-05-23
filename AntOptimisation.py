from random import seed,random,randint,uniform
import time

def processData(filename):
#Function to process the uni data file
    with open(filename, "r") as data:
        facilities = int(data.readline()) #Get number of facilities
        data.readline() #Remove empty line
        #Gather facility distance data in lines according to the number of facilities, removing new lines and double spaced at the same time
        facilityDistanceString = [data.readline().replace("\n", "").replace("  ", " ") for x in range(facilities)]
        data.readline() #Remove empty line
        #Gather student flow data in lines accordingly
        studentFlowString = [data.readline().replace("\n", "").replace("  ", " ") for x in range(facilities)]

    #Initialise corresponding matricies
    facilityDistance = []
    studentFlow = []
    #Convert corresponding sting data to matricies
    strToMatrix(facilityDistanceString, facilityDistance)
    strToMatrix(studentFlowString, studentFlow)
    return(facilities, facilityDistance, studentFlow)

def strToMatrix(string, data):
    for line in string:
        lineData = [] #Initialise array for data
        line = line.strip() #Remove spaces at the start of strings
        dataPoints = line.split(' ') #Split data in lines by spaces
        for dataPoint in dataPoints: #Add every separate data point to the array as integers
            lineData.append(int(dataPoint))
        data.append(lineData) #Add data array to matrix

def generateAntPaths():
    for i in range(M[experiment]): #Number of ants
        #Create deep copies to avoid changing base parameters
        traversable = [*range(facilities)]
        currentFacility = randint(0,facilities-1) #Choose starting node
        traversable.remove(currentFacility) #Remove starting facility from traversable facility
        path = [currentFacility]

        #Works the same as the transition rule
        for traversal in range(facilities):
            pheroSum = 0
            for facility in traversable: #Find sum of all pheromones on possible paths
                pheroSum += pheromones[currentFacility][facility]
            selectFacility = uniform(0, pheroSum) #Choose a path
            pheroCurrent = 0
            for facility in traversable:
                pheroCurrent += pheromones[currentFacility][facility]
                if pheroCurrent > selectFacility:
                    currentFacility = facility #Change current facility to the chosen facility
                    traversable.remove(currentFacility) #Remove current node from traversable nodes
                    path.append(currentFacility) #Add current node to ant path
                    break
        generatedPaths.append(path)
        #print(generatedPaths)
    return

def calcCost(path):
    #Calculate fitness cost by totaling the multiple of the distance between 2 locations and a supposed new student flow to be assigned to the locations
    cost = 0
    for i in range(facilities):
        for j in range(facilities):
            cost += facDistMatrix[i][j] * stdFlowMatrix[path[i]][path[j]]
    return cost

def updatePheromones(bestFitness):
    newBestFitness = bestFitness
    for path in generatedPaths:
        if bestFitness > calcCost(path): #Add pheromones to paths with a fitness better than the previous evaluation fitness
            if newBestFitness > calcCost(path):
                newBestFitness = calcCost(path)
                print(newBestFitness)
            for i in range(len(pheromones[0])-1): #Subtract 1 from range as there are no traversals to the same facility
                pheromones[path[i]][path[i+1]] += 1/calcCost(path)
    if newBestFitness != bestFitness: 
        #Only evaporate pheromones if a pheromone update occurs or else the phormones will eventually tend to 0 breaking the algorithm. This would have no negative effects. (All are evaporated similarly)
        evaporatePheromones()
    return newBestFitness

# def updatePheromones(bestFitness):
#     #Update all paths
#     for path in generatedPaths:
#         if bestFitness > calcCost(path): #Update best fitness
#             bestFitness = calcCost(path)
#             print(bestFitness)
#         for i in range(len(pheromones[0])-1): #Subtract 1 from range as there are no traversals to the same facility
#             pheromones[path[i]][path[i+1]] += 1/calcCost(path)
#     evaporatePheromones()
#     return bestFitness

def evaporatePheromones(): 
    #Evaporate all pheromone values by e
    for i in range(facilities):
        for j in range(facilities):
            pheromones[i][j] *= E[experiment]

def initBestFitness(): 
    #Calculate best fitness with initial data
    cost = 0
    for i in range(facilities):
        for j in range(facilities):
            cost += facDistMatrix[i][j] * stdFlowMatrix[i][j]
    return cost

if __name__ == "__main__":
    facilities, facDistMatrix, stdFlowMatrix = processData("Uni50a.dat")

    #Hyperparameters to modify performance
    TRIALS = 5
    EVALUATIONS = 10000
    M = [100, 100, 10, 10, 100, 10]
    E = [0.9, 0.5, 0.9, 0.5, 0.1, 0.1]
    resultData = ""
    f = open("TimingTrialSeedResults.txt", "a") #Open file to write results for processing
    for experiment in range(0, 6):
        for trial in range(TRIALS):
            startTime = time.time() #Start recording time
            seed(trial) #Seed random numbers according to trial number
            #seed(time.time()) #Seed random numbers according to time
            pheromones = [[random() for j in range(facilities)] for i in range(facilities)]
            bestFitness = initBestFitness() #Initialise best fitness with initial data
            
            evaluations = 0
            currentSecond = -1     
            #while evaluations != EVALUATIONS: #Test according to evaluations
            while int(time.time() - startTime) < 300: #Test according to time
                generatedPaths = []
                generateAntPaths()
                bestFitness = updatePheromones(bestFitness)
                # if evaluations % 10 == 0 and evaluations <= 100: #Write results to file
                #     #f.write("Trial: " + str(trial) + "Evaluations: " + str(evaluations) + "Best Fitness: " + str(bestFitness))
                #     f.write(str(experiment+1) + " " + str(trial+1) + " " + str(evaluations) + " " + str(M[experiment]) + " " + str(E[experiment]) + " " + str(bestFitness) + " " + str(int(time.time() - startTime)) + "\n")
                resultData = str(experiment+1) + " " + str(trial+1) + " " + str(evaluations) + " " + str(M[experiment]) + " " + str(E[experiment]) + " " + str(bestFitness) + " " + str(int(time.time() - startTime)) + "\n"
                #if evaluations % 500 == 0: #Record according to evaluations
                if int(time.time() - startTime) % 10 == 0 and currentSecond != int(time.time() - startTime): #Record according to time
                    currentSecond = int(time.time() - startTime)
                    f.write(resultData)
                    print(resultData)
                evaluations += 1
            #Record 10000th evaluation
            resultData = str(experiment+1) + " " + str(trial+1) + " " + str(evaluations) + " " + str(M[experiment]) + " " + str(E[experiment]) + " " + str(bestFitness) + " " + str(int(time.time() - startTime)) + "\n"
            f.write(resultData)
    f.close()