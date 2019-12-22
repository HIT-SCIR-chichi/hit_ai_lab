
class CPT:
    
    def __init__(self,nodeCount,fatherIndexList,probabList,nodeNum):

        
        self.nodeNum=nodeNum
        self.fatherIndexList=fatherIndexList
        self.qVariableIndex=nodeCount
        self.qIsTrueList=[]
        self.qIsFalseList=[]
        for i in range(len(probabList)):
            self.qIsTrueList.append(probabList[i][0])
            self.qIsFalseList.append(probabList[i][1])
            
        
    def getJointProbability(self,jointInt):
        binaryStr=bin(jointInt).replace("0b",'')
        binaryStrLen=len(binaryStr)
        if(binaryStrLen<self.nodeNum):
            for i in range(self.nodeNum-binaryStrLen):
                binaryStr='0'+binaryStr
        if(binaryStr[self.qVariableIndex]=='1'):
            #use true list

            if(len(self.fatherIndexList)==0):
                return self.qIsTrueList[0]
            queryBinStr=''
            for i in range(len(self.fatherIndexList)):
                fatherIndex=self.fatherIndexList[i]
                queryBinStr=queryBinStr+binaryStr[fatherIndex]
            queryNum=int(queryBinStr,base=2)
            return self.qIsTrueList[queryNum]
        else:
            #use false list

            if(len(self.fatherIndexList)==0):
                return self.qIsFalseList[0]
            queryBinStr=''
            for i in range(len(self.fatherIndexList)):
                fatherIndex=self.fatherIndexList[i]
                queryBinStr=queryBinStr+binaryStr[fatherIndex]
            queryNum=int(queryBinStr,base=2)
            return self.qIsFalseList[queryNum]