from collections import defaultdict 
import heapq

class Matrix:
    def __init__(self, matrix, g=0, h=0):
        self.matrix = matrix
        self.g = g 
        self.h = h  
        self.f = self.g + self.h  
    
    def __lt__(self, other):
        return self.f < other.f 
        
class Graph:
    def __init__(self, initMatrix=[[0,0,0], [0,0,0], [0,0,0]], targetMatrix=[[0,0,0], [0,0,0], [0,0,0]]):
        self.initMatrix = initMatrix
        self.targetMatrix = targetMatrix
    
    def inputInitMatrix(self):
        print("Enter the initial matrix")
        for i in range(3):
            for j in range(3):
                temp = input(f"Enter position {i}, {j}: ")
                if temp == "X":
                    self.initMatrix[i][j] = "X"
                else:
                    self.initMatrix[i][j] = int(temp)
                    
        self.printMatrix(self.initMatrix)
    
    def inputTargetMatrix(self):
        print("Enter the target matrix")
        for i in range(3):
            for j in range(3):
                temp = input(f"Enter position {i}, {j}: ")
                if temp == "X":
                    self.targetMatrix[i][j] = "X"
                else:
                    self.targetMatrix[i][j] = int(temp)
        
        self.printMatrix(self.targetMatrix)
        
    def printMatrix(self, matrix):
        for i in range(3):
            for j in range(3):
                if matrix[i][j] == "X":
                    print(f"\033[91m{matrix[i][j]}\033[0m", end='')
                    # print(" ",end='')
                else:
                    print(matrix[i][j], end='')
            print()
        
    
    def countMahattan(self, currentMatrix):
        coordinateCurrent = defaultdict(lambda: (0,0))
        coordinateTarget = defaultdict(lambda: (0,0))
        
        for i in range(3):
            for j in range(3):
                if currentMatrix[i][j] != "X":
                    coordinateCurrent[currentMatrix[i][j]] = (i, j)
                
                if self.targetMatrix[i][j] != "X":
                    coordinateTarget[self.targetMatrix[i][j]] = (i,j)
        
        h2Value = 0
        for i in range(1, 9):
            h2Value += abs(coordinateCurrent[i][0] - coordinateTarget[i][0])  + abs(coordinateCurrent[i][1] - coordinateTarget[i][1])
        
        return h2Value
        
    def matrixTransform(self, currentMatrix):
        availableMatrix = []
        
        for i in range(3):
            for j in range(3):
                if currentMatrix[i][j] == "X":
                    posX = i   
                    posY = j
                
        if posY>0: #Shift left
            tempMatrix = self.copyMatrix(currentMatrix)
            tempMatrix[posX][posY-1], tempMatrix[posX][posY] = tempMatrix[posX][posY], tempMatrix[posX][posY-1]
            availableMatrix.append(tempMatrix)      
        
        if posY<2: #Shift right
            tempMatrix = self.copyMatrix(currentMatrix)
            tempMatrix[posX][posY+1], tempMatrix[posX][posY] = tempMatrix[posX][posY], tempMatrix[posX][posY+1]
            availableMatrix.append(tempMatrix)
            
        if posX>0: #Shift up
            tempMatrix = self.copyMatrix(currentMatrix)
            tempMatrix[posX-1][posY], tempMatrix[posX][posY] = tempMatrix[posX][posY], tempMatrix[posX-1][posY]
            availableMatrix.append(tempMatrix)

        if posX<2: #Shift down
            tempMatrix = self.copyMatrix(currentMatrix)
            tempMatrix[posX+1][posY], tempMatrix[posX][posY] = tempMatrix[posX][posY], tempMatrix[posX+1][posY]
            availableMatrix.append(tempMatrix)
            
        return availableMatrix
    
    def copyMatrix(self,matrix):
        copied_matrix = []
        
        for row in matrix:
            copied_row = row[:]  
            copied_matrix.append(copied_row)
        
        return copied_matrix
        
    def A_Star(self):
        open_set = []
        close_set = set()
        ancestor = defaultdict(list)
        
        start_state = Matrix(self.initMatrix, 0, self.countMahattan(self.initMatrix))
        heapq.heappush(open_set, (start_state.f, start_state))

        while open_set:
            _, current_state = heapq.heappop(open_set)
    
            if current_state.matrix == self.targetMatrix:
                print("Solution found!")
                break
            else:
                close_set.add(tuple(map(tuple, current_state.matrix)))

                for neighbor_matrix in self.matrixTransform(current_state.matrix):
                    neighbor_state = Matrix(neighbor_matrix, current_state.g + 1, self.countMahattan(neighbor_matrix))
                    if tuple(map(tuple, neighbor_state.matrix)) not in close_set:
                        neighbor_state.f = neighbor_state.g + neighbor_state.h
                        heapq.heappush(open_set, (neighbor_state.f, neighbor_state))
                        ancestor[tuple(map(tuple, neighbor_matrix))] = current_state.matrix
        else:
            print("No path exists!")
            return

        
        print("\n\n\n")
        print("============================================================")
        path = []
        currentMatrix = tuple(map(tuple, self.targetMatrix))
        while currentMatrix != tuple(map(tuple, self.initMatrix)):
            path.append(currentMatrix)
            currentMatrix = tuple(map(tuple, ancestor[currentMatrix]))

        
        path.append(tuple(map(tuple, self.initMatrix)))
        
        path = path[::-1]
        
        solution = defaultdict()
        
        for step, matrix in enumerate(path):
            print(f"Step {step}:")
            self.printMatrix(matrix) 
            solution[step] = matrix 
            if step != len(path)-1:
                print("||")
                print("\/")
        print("============================================================")
        
        return solution
        
# matrix = Graph()
# matrix.inputInitMatrix()
# matrix.inputTargetMatrix()
# matrix.A_Star()


"""
Sample input:
7
2
4
5
X
6
8
3
1
X
1
2
3
4
5
6
7
8

No solution:
7
2
4
5
X
6
8
3
1
1
2
3
8
X
4
7
6
5
"""