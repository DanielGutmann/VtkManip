import sys,math,argparse,glob,os
from numpy import median,mean

#==============================
#---- Usage/argument check
args = None
if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--vtk1',required=True)
    parser.add_argument('--vtk2',default=False)
    parser.add_argument('--outname',required=True)
    parser.add_argument('--divide',default=False,action='store_true')
    parser.add_argument('--multiply',default=False,action='store_true')
    parser.add_argument('--subtract',default=False,action='store_true')
    parser.add_argument('--add',default=False,action='store_true')
    parser.add_argument('--average',default=False,action='store_true')
    parser.add_argument('--rotate',default=False,action='store_true')
    args = parser.parse_args()

#==============================
#---- VtkData is just an extended list object
class VtkData(list):
    #_______________________
    def __init__(self,fileName):
        if not fileName.endswith(".vtk") or not os.path.isfile(fileName):
            print "Error:",fileName,"is not a valid .vtk file"
            sys.exit()
            
        #---- Initialise member data 
        print "Reading file",fileName
        list.__init__(self)
        self.metaData = ""
        #---- Count the number of lines in the file
        nLines = 0
        with open(fileName) as vtkFile:
            nLines = sum(1 for line in vtkFile)        
        #---- Get the metadata
        with open(fileName) as vtkFile:
            for iLine,line in enumerate(vtkFile):
                if iLine < (nLines-1):
                    self.metaData += line
                else:
                    self += [float(x) for x in line.split()]
                    break
        #---- Show some stats
        print "Mean, median, min, max = ",mean(self),median(self),min(self),max(self)

        #---- Get parameters from metadata
        self.parameters = {}
        for line in self.metaData.split("\n"):
            info = line.split()
            nStr = len(info)
            if nStr == 1:
                continue
            for x in info:
                try:
                    float(x)
                    nStr -= 1
                except ValueError:
                    pass
            if nStr == 1:
                self.parameters[info[0]] = [int(float(x)) for x in info[1:]]
        #print "Got parameters",self.parameters
                    
        #---- Generate a dictionary of voxel number --> voxel coordinate
        self.voxelMap,self.allVoxels = self.GenerateVoxels()

    #_______________________
    #---- Function to generate a voxel mapping:
    #---- [i][j][k] --> voxel id
    #---- and n --> [i][j][k]
    def GenerateVoxels(self):
        dimensions = self.parameters["DIMENSIONS"]
        #---- Loop over i,j,k
        n,voxelMap,voxels = 0,{},{}
        for k in range(0,dimensions[2]):
            for j in range(0,dimensions[1]):
                for i in range(0,dimensions[0]):
                    if not i in voxelMap:
                        voxelMap[i] = {}
                    if not j in voxelMap[i]:
                        voxelMap[i][j] = {}
                    #---- Generate the maps
                    voxelMap[i][j][k] = self[n]
                    voxels[n] = [i,j,k]
                    n+=1
        #---
        return voxelMap,voxels

    #_______________________
    #---- self / vtkData
    def DivideBy(self,vtkData):
        newSelf = []
        if type(vtkData) == float or type(vtkData) == int:
            vtkData = [vtkData for x in self]
            
        for x,y in zip(self,vtkData):
            val = "0"
            try:
                val = str(float(x)/float(y))
            except ZeroDivisionError:
                pass
            newSelf.append(val)            
        super(VtkData,self).__init__(newSelf)

    #_______________________
    #---- self * vtkData
    def MultiplyBy(self,vtkData):
        newSelf = []
        if type(vtkData) == float or type(vtkData) == int:
            vtkData = [vtkData for x in self]            
        newSelf = [float(x)*float(y) for x,y in zip(self,vtkData)]
        super(VtkData,self).__init__(newSelf)

    #_______________________
    #---- self - vtkData
    def Subtract(self,vtkData):
        self.Add(vtkData,-1)

    #_______________________
    #---- self + vtkData
    def Add(self,vtkData,flag=1.):
        newSelf = []
        if type(vtkData) == float:
            vtkData = [vtkData for x in self]
           
        for x,y in zip(self,vtkData):
            val = str(float(x) + flag*float(y))
            #            #---- Remove negative values
            #            if float(val) < 0: 
            #                val = "0"                    
            newSelf.append(val)            
        super(VtkData,self).__init__(newSelf)

    #_______________________
    #---- Rotate the file about the centre by 90 degrees
    def Rotate(self):
        print "Rotating by 90 degrees"
        dims = self.parameters["DIMENSIONS"]
        #----
        newSelf = []
        for k in range(0,dims[2]):
            for j in range(0,dims[1]):
                for i in range(0,dims[0]):
                    newSelf.append(self.voxelMap[k][j][i])
        super(VtkData,self).__init__(newSelf)
        
    #_______________________
    #---- Rewrite the data to outName
    def Write(self,outName):
        #---- Check whether the file already exists
        if os.path.isfile(outName):
            while True:
                response = raw_input("Output file "+outName+" already exists. Overwrite? [y or n]\t")
                if response == "n":
                    sys.exit()
                elif response == "y":
                    break
                
        #---- Write the file
        print "Writing file",outName
        with open(outName,"w") as f:
            f.write(self.metaData)
            strData = [str(x) for x in self]
            f.write(" ".join(strData))

            
#==============================
if __name__ == "__main__":    

    #---- Count the number of non-string arguments
    nArgs = 0
    for k,v in vars(args).iteritems():
        if type(v)!=str:
            if int(v) > 0:
                nArgs += 1    
    if nArgs != 1:
        print "Error:\tOnly select one operation"
        sys.exit()

    #----
    vtkData1 = None
        
    #--------------------
    #---- Take the average
    if args.average or (args.add and not args.vtk2):
        fileList = []
        for testFileName in args.vtk1.split(","):
            fileList += glob.glob(testFileName)
        if len(fileList) == 0:
            print "No files found in path",args.vtk1
            sys.exit()
        #---- Loop over the files
        print "Reading",len(fileList),"files from",args.vtk1        
        for vtkFileName in fileList:
            #---- First time assign a value to vtkData1
            if not vtkData1:
                vtkData1 = VtkData(vtkFileName)
            #---- Otherwise add to vtkData1
            else:
                vtkData1.Add(VtkData(vtkFileName))
        #---- Take the average
        if args.average:
            vtkData1.DivideBy(len(fileList))
    #--------------------
    #---- Other operators
    else:
        #----
        if args.rotate:
            args.vtk2 = True

        #---- Check there is a second vtk argument
        if not args.vtk2:
            print "Error:\tArgument vtk2 required when NOT in average mode"
            sys.exit()
        #---- Assign vtk data to vtkData1
        vtkData1 = VtkData(args.vtk1)
        
        #---- Assign either a float or vtk data to vtkData2
        try:
            vtkData2 = float(args.vtk2)
            print "Setting 'vtk2' to constant value of",vtkData2
        except ValueError:
            vtkData2 = VtkData(args.vtk2)
        
        #---- Perform operation
        if args.divide:
            vtkData1.DivideBy(vtkData2)
        elif args.subtract:
            vtkData1.Subtract(vtkData2)
        elif args.add:
            vtkData1.Add(vtkData2)
        elif args.multiply:
            vtkData1.MultiplyBy(vtkData2)
        elif args.rotate:
            vtkData1.Rotate()
        else:
            sys.exit()
            
    #---- Save the file
    vtkData1.Write(args.outname)
    
