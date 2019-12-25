import time
import re


class CPT:

    def __init__(self, nodeCount, fatherIndexList, probabList, nodeNum):

        self.nodeNum = nodeNum
        self.fatherIndexList = fatherIndexList
        self.qVariableIndex = nodeCount
        self.qIsTrueList = []
        self.qIsFalseList = []
        for i in range(len(probabList)):
            self.qIsTrueList.append(probabList[i][0])
            self.qIsFalseList.append(probabList[i][1])

    def getJointProbability(self, jointInt):
        binaryStr = bin(jointInt).replace("0b", '')
        binaryStrLen = len(binaryStr)
        if binaryStrLen < self.nodeNum:
            for i in range(self.nodeNum - binaryStrLen):
                binaryStr = '0' + binaryStr
        if binaryStr[self.qVariableIndex] == '1':
            # use true list
            if len(self.fatherIndexList) == 0:
                return self.qIsTrueList[0]
            queryBinStr = ''
            for i in range(len(self.fatherIndexList)):
                fatherIndex = self.fatherIndexList[i]
                queryBinStr = queryBinStr + binaryStr[fatherIndex]
            queryNum = int(queryBinStr, base=2)
            return self.qIsTrueList[queryNum]
        else:
            # use false list
            if len(self.fatherIndexList) == 0:
                return self.qIsFalseList[0]
            queryBinStr = ''
            for i in range(len(self.fatherIndexList)):
                fatherIndex = self.fatherIndexList[i]
                queryBinStr = queryBinStr + binaryStr[fatherIndex]
            queryNum = int(queryBinStr, base=2)
            return self.qIsFalseList[queryNum]


class NetWork:

    def __init__(self):
        self.nodeNum = 0
        self.NodeList = []
        self.edges = []
        self.FatherList = {}
        self.CPTS = []  # a list of instances of cpt
        self.jointDis = []

    def initFromFile(self, fileName):
        file = open(fileName, 'r')
        lines = file.readlines()
        self.nodeNum = int(lines[0].strip("\n"))
        self.NodeList = lines[2].strip('\n').split(' ')
        for i in range(4, 4 + self.nodeNum):
            self.edges.append(lines[i].strip('\n').split(' '))
        for i in range(self.nodeNum):
            for j in range(self.nodeNum):
                self.edges[i][j] = int(self.edges[i][j])

        # init father list
        for i in range(self.nodeNum):
            self.FatherList[i] = []

        # init father list
        for j in range(self.nodeNum):
            for i in range(self.nodeNum):
                if (self.edges[i][j] == 1):
                    self.FatherList[j].append(i)

        # create CPTs
        lineCount = 5 + self.nodeNum
        for nodeCount in range(self.nodeNum):
            curLine = lines[lineCount]
            # print(curLine)
            lineCount += 1
            probabList = []
            while (curLine != '\n'):
                probabStrings = curLine.strip('\n').split(' ')
                for i in range(len(probabStrings)):
                    probabStrings[i] = float(probabStrings[i])
                probabList.append(probabStrings)
                curLine = lines[lineCount]
                # print(curLine)
                lineCount += 1

            # creat the cpt for node with index nodeCount
            cpt = CPT(nodeCount, self.FatherList[nodeCount], probabList, self.nodeNum)
            self.CPTS.append(cpt)

        # close the file
        file.close()

        timebefore = time.time()
        self.calculateJoint()
        timeafter = time.time()
        print("the calculate joint distribution function cost: ", timeafter - timebefore)

        '''
        for i in range(len(self.jointDis)):
            print(self.jointDis[i])
        '''

    def calculateJoint(self):
        for i in range(2 ** self.nodeNum):
            mulResult = 1
            for j in range(self.nodeNum):
                mulResult = mulResult * self.CPTS[j].getJointProbability(i)
            self.jointDis.append(mulResult)

    # P(Alarm | Earthquake=true, Burglar=true)
    def query(self, queryStr):
        matchObj = re.match('P\\((.*)\\)', queryStr)
        querAndEvi = matchObj.group(1).split('|')
        queryVariable = querAndEvi[0].strip()
        queryVariIndex = self.NodeList.index(queryVariable)
        evidenceList = querAndEvi[1].split(',')
        evidenceDiction = {}
        for i in range(len(evidenceList)):
            evidence = evidenceList[i].strip()
            evidence = evidence.split('=')
            if evidence[1] == 'true':
                evidenceDiction[evidence[0]] = "1"
            if evidence[1] == 'false':
                evidenceDiction[evidence[0]] = "0"
        evidenceKeys = evidenceDiction.keys()
        queryBin = ""
        for i in range(self.nodeNum):
            node = self.NodeList[i]
            if node in evidenceKeys:
                queryBin = queryBin + evidenceDiction[node]
            else:
                queryBin = queryBin + "\\d"

        # selectedJointList=[]
        trueTotalValue = 0
        falseTotalValue = 0
        for i in range(2 ** self.nodeNum):
            binCount = bin(i).replace('0b', '')
            binaryStrLen = len(binCount)
            if binaryStrLen < self.nodeNum:
                for j in range(self.nodeNum - binaryStrLen):
                    binCount = '0' + binCount
            if re.match(queryBin, binCount) is not None:
                if binCount[queryVariIndex] == "0":
                    falseTotalValue += self.jointDis[i]
                if binCount[queryVariIndex] == "1":
                    trueTotalValue += self.jointDis[i]

        totalValue = trueTotalValue + falseTotalValue

        trueProb = trueTotalValue / totalValue
        falseProb = falseTotalValue / totalValue

        return [trueProb, falseProb]
