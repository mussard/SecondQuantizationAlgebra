import secondQuantizationAlgebra as sqa
def replaceindex(tensor, a, b) :
    for i in range(len(tensor.indices)):
        if (tensor.indices[i].name == a):
            tensor.indices[i] = b



def replaceAllKdeltaWithDeltas(term, rdmDelta):
    import string
    l = list(string.ascii_lowercase) #list of all printables

    usedIndices = []
    for t in term.tensors:
        for index in t.indices:
            usedIndices.append(index.name)

    unUsedList = sorted(list(set(l) - set(usedIndices)))

    Deltas = []
    import copy
    tensorcopy = copy.deepcopy(term.tensors)

    removeDelta = []
    for t in tensorcopy:
        if (t.name == "kdelta"):
            if (t.indices[0].indType[0] == sqa.options.core_type):
                Deltas.append(rdmDelta[0].copy())
            elif (t.indices[0].indType[0] == sqa.options.active_type):
                Deltas.append(rdmDelta[1].copy())
            elif (t.indices[0].indType[0] == sqa.options.virtual_type):
                Deltas.append(rdmDelta[2].copy())

            Deltas[-1].indices[0].name = t.indices[0].name
            Deltas[-1].indices[1].name = t.indices[1].name

            removeDelta.append(t)
#            term.tensors.remove(t)
#            break

    for t in removeDelta:
#        print(t)
        term.tensors.remove(t)
    for d in Deltas:
#        print(d)
        term.tensors.append(d)
#    exit(0)
    return term

def replaceSingleKdeltaWithDeltas(term, rdmDelta):
    import string
    l = list(string.ascii_lowercase) #list of all printables

    usedIndices = []
    for t in term.tensors:
        for index in t.indices:
            usedIndices.append(index.name)

    unUsedList = sorted(list(set(l) - set(usedIndices)))

    Deltas = []
    import copy
    tensorcopy = copy.copy(term.tensors)

    numNonDeltaTensors = 0
    for t in tensorcopy:
        if (t.name != "kdelta"):
            numNonDeltaTensors += 1

    if (numNonDeltaTensors>0):
        return term

    for t in tensorcopy:
        if (t.name == "kdelta"):
            if (t.indices[0].indType[0] == sqa.options.core_type):
                Deltas.append(rdmDelta[0].copy())
            elif (t.indices[0].indType[0] == sqa.options.active_type):
                Deltas.append(rdmDelta[1].copy())
            elif (t.indices[0].indType[0] == sqa.options.virtual_type):
                Deltas.append(rdmDelta[2].copy())

            Deltas[-1].indices[0].name = t.indices[0].name
            Deltas[-1].indices[1].name = t.indices[1].name

            term.tensors.remove(t)
            break
    for d in Deltas:
        term.tensors.append(d)
    return term


def replaceRepeatIndicesWithDeltas(term, rdmDelta):
    import string
    l = list(string.ascii_lowercase) #list of all printables

    usedIndices = []
    for t in term.tensors:
        for index in t.indices:
            usedIndices.append(index.name)

    unUsedList = sorted(list(set(l) - set(usedIndices)))

    Deltas = []
    for t in term.tensors:
        if (t.name == "kdelta"):
            continue
        uniques = list(set(t.indices))
        numRepeats = len(uniques)*[0]
        for index in t.indices:
            numRepeats[ uniques.index(index) ] +=1

        for i in range(len(numRepeats)):
            if (numRepeats[i] > 2):
                print("more than a double repeat in tensor ", t)
                exit(0)

            if (numRepeats[i] == 2):
                repeatIndex = uniques[i]
                repeatPositions = [j for j, x in enumerate(t.indices) if x == uniques[i]]
                if ( len(repeatPositions) != 2):
                    print(uniques[i].name," should occur twice in ", t)
                    exit(0)
                newName = unUsedList[0]
                unUsedList.remove(newName)
                t.indices[ repeatPositions[1] ].name = newName

                if (t.indices[ repeatPositions[1] ].indType[0] == sqa.options.core_type):
                    Deltas.append(rdmDelta[0].copy())
                elif (t.indices[ repeatPositions[1] ].indType[0] == sqa.options.active_type):
                    Deltas.append(rdmDelta[1].copy())
                if (t.indices[ repeatPositions[1] ].indType[0] == sqa.options.virtual_type):
                    Deltas.append(rdmDelta[2].copy())

                Deltas[-1].indices[0].name = newName
                Deltas[-1].indices[1].name = uniques[i].name


    for d in Deltas:
        term.tensors.append( d)
    return term

def printTensor(tensor, keymap):
    string = tensor.name +"["
    for i in range(len(tensor.indices)):
        if (keymap.has_key(tensor.indices[i].name)):
            string += keymap[tensor.indices[i].name]+","
        else:
            string += tensor.indices[i].name+","
    string = string[:-1]+"]"
    return string

def printIntTensor(tensor, activeInEinsum = False):
    string = tensor.name +"["
    for i in range(len(tensor.indices)):
        if (tensor.indices[i].name[0]=="V"):
            string += "nc:,"
        elif (tensor.indices[i].name[0] == "A"):
            if (not activeInEinsum):
                string += tensor.indices[i].name+"+ncore,"
            else:
                string += "ncore:nc,"

        elif (tensor.indices[i].name[0] == "C"):
            string += tensor.indices[i].name+","
        elif (len(tensor.indices[i].name[0]) == 1):
            if (len(tensor.indices[i].indType) > 1):
                print("Something wrong index is a composite of core/active/virtual")
                exit(0)
            elif (tensor.indices[i].indType[0] == sqa.options.core_type) :
                string += ":ncore,"
            elif (tensor.indices[i].indType[0] == sqa.options.active_type) :
                string += "ncore:nc,"
            elif (tensor.indices[i].indType[0] == sqa.options.virtual_type) :
                string += "nc:,"
        else :
            print("index seems to be neither dummy nor defined")
            exit(0)
    string = string[:-1]+"]"
    return string

def printETensor(tensor, activeInEinsum = False):
    string = tensor.name +"["
    for i in range(len(tensor.indices)):
        if (tensor.indices[i].name[0]=="V"):
            print("RDM cannot have virtual index")
            exit(0)
        elif (tensor.indices[i].name[0] == "A"):
            if (not activeInEinsum):
                string += tensor.indices[i].name+","
            else:
                string += ":,"
        elif (tensor.indices[i].name[0] == "C"):
            print("RDM cannot have core index")
            exit(0)
        elif (len(tensor.indices[i].name[0]) == 1):
            if (len(tensor.indices[i].indType) > 1):
                print("Something wrong index is a composite of core/active/virtual")
                exit(0)
            elif (tensor.indices[i].indType[0] == sqa.options.core_type) :
                print("RDM cannot have core index")
                exit(0)
            elif (tensor.indices[i].indType[0] == sqa.options.active_type) :
                string += ":,"
            elif (tensor.indices[i].indType[0] == sqa.options.virtual_type) :
                print("RDM cannot have virtual index")
                exit(0)
        else :
            print("index seems to be neither dummy nor defined")
            exit(0)
    string = string[:-1]+"]"
    return string

def writeTensors(AllTensors, CommentKey, Domains, Usage,commentE3=False):

    UsageKey = {"A":"USAGE_Amplitude",\
                "R":"USAGE_Residual",\
                "H":"USAGE_Hamiltonian",\
                "D":"USAGE_Density",\
                "I":"USAGE_Intermediate"}
    i = 0
    not_commented=0
    outString=''
    for tensor in AllTensors:
      if (CommentKey[tensor]=="E3" and commentE3):
        intro='//  /*{:3}*/'.format(i)
      else:
        intro='    /*{:3}*/'.format(i)
        not_commented+=1
      outString += intro+'{{"{:8}, "{:10}, "", {:18}}},\n'\
                  .format(CommentKey[tensor]+'"',\
                          Domains[i]+'"',\
                          UsageKey[Usage[i]])
      i += 1
    outString = "  FTensorDecl TensorDecls[%i] = {\n"%(not_commented)\
                +outString[:-1]+"\n  };\n"

    print(outString)
    return not_commented

def WriteCodeSimple(result, AllTensors, commentTensor, scale=1.0, commentE3=False):

     tensorIndexes=[]
     middleLine   =[]
     tensorNumbers=[]
     commentLine  =[]
     commented    =[]
     for t in result:
        commented.append(False)

        # tensorIndexes
        tensorIndexStringList = []
        for i in range(len(t.tensors)):
          tensor = t.tensors[i]
          tensorIndexString = ''
          for index in range(len(tensor.indices)):
            if ( len(tensor.indices[index].name) > 1):
              tensorIndexString += tensor.indices[index].name[-1].capitalize()
            else :
              tensorIndexString += tensor.indices[index].name[0]
          tensorIndexStringList.append(tensorIndexString)  #tensor index string of output
        indexes=''
        for indexstring in tensorIndexStringList:
          indexes += indexstring+','
        tensorIndexes.append('{"'+indexes[:-1]+'",')

        # middleLine
        middleLine.append('{:6}, {:3}, {{'.format(t.numConstant*scale,len(tensorIndexStringList)))

        # tensorNumbers and commentLine
        index = 1
        indexes=''
        commentString = '  //{:6} '.format(t.numConstant*scale)
        for i in range(len(t.tensors)):
          tensor = t.tensors[i]
          if ((tensor.name=="E3" and commentE3) or (tensor.name=="int2v")):
            commented[-1]=True
          indexes+= '{:2},'.format(AllTensors.index(tensor.name))
          commentString += commentTensor[tensor.name]+'['+tensorIndexStringList[index-1]+'] '
          index += 1
        commentLine.append(commentString)
        tensorNumbers.append(indexes[:-1]+'}},')

     width1=len(max(tensorIndexes, key=len))
     width2=len(max(tensorNumbers, key=len))
     print("\tFEqInfo EqsRes[%i] = {" %(commented.count(False)))
     for i in range(len(tensorIndexes)):
       if commented[i]:
         print('//  {:{width1}}{:}{:{width2}}{:}'.format(tensorIndexes[i],middleLine[i],tensorNumbers[i],commentLine[i],width1=width1,width2=width2))
       else:
         print('    {:{width1}}{:}{:{width2}}{:}'.format(tensorIndexes[i],middleLine[i],tensorNumbers[i],commentLine[i],width1=width1,width2=width2))
     print("\t};\n")

     return commented.count(False)

def WriteCode(result, tensors):

     outString = ""
     for t in result:
        tensorString = ""
        ifstatement = "if"

        tensorcopy = t.tensors
        dontprint= []
        indexKey = {'Va': 'Va', 'Vb' : 'Vb'}
        for i in range(len(tensorcopy)):
            tensor = tensorcopy[i]

            #check the delta function
            if (tensor.name == "kdelta"):
                dontprint.append(i)

                if (tensor.indices[0].name == "Vc" or tensor.indices[0].name == "Vd") :
                    indexKey[tensor.indices[1].name] = tensor.indices[0].name
                    for j in range(len(t.tensors)):
                        if (j not in dontprint):
                            replaceindex(t.tensors[j], tensor.indices[0].name, tensor.indices[1].name)
                elif (tensor.indices[1].name == "Vc" or tensor.indices[1].name == "Vd") :
                    indexKey[tensor.indices[0].name] = tensor.indices[1].name
                    for j in range(len(t.tensors)):
                        if (j not in dontprint):
                            replaceindex(t.tensors[j], tensor.indices[1].name, tensor.indices[0].name)
                else :
                    ifstatement += tensor.name +" == " +tensor.name + " and"

        if (len(ifstatement) != 2) :
            outString += ifstatement[:-3]+" : "
        outString += '\t\t{"CDRS,'
        for i in range(len(tensorcopy)):
            tensor = tensorcopy[i]
            if(i not in dontprint):
                for index in range(len(tensor.indices)):
                    if ( len(tensor.indices[index].name) > 1):
                        outString += tensor.indices[index].name[-1].capitalize()
                    else :
                        outString += tensor.indices[index].name[0]
                outString += " ,"
        outString += indexKey["Va"][-1].capitalize()+indexKey["Vb"][-1].capitalize()+'PQ", '+str(t.numConstant)+", 4 , {1"
        for i in range(len(tensorcopy)):
            tensor = tensorcopy[i]
            if(i not in dontprint):
                outString+= " , "+ str(tensors[tensor.name])
        outString += ", 0}},\n"

     print(outString[:-1]+"\n\t};")


def WriteCode_ccaa(result, SupressActive, intmapkey, RDMmapkey, activeInEinsum = False):
    if (SupressActive):
     for t in result:
        tensorString = ""
        ifstatement = "\tif "

        tensorcopy = t.tensors
        dontprint= []
        indexKey = {'Ap': 'Ap', 'Aq' : 'Aq'}
        for i in range(len(tensorcopy)):
            tensor = tensorcopy[i]

            #check the delta function
            if (tensor.name == "kdelta"):
                dontprint.append(i)

                if (tensor.indices[0].name == "Ar" or tensor.indices[0].name == "As") :
                    indexKey[tensor.indices[1].name] = tensor.indices[0].name
                    for j in range(len(t.tensors)):
                        if (j not in dontprint):
                            replaceindex(t.tensors[j], tensor.indices[0].name, tensor.indices[1].name)
                elif (tensor.indices[1].name == "Ar" or tensor.indices[1].name == "As") :
                    indexKey[tensor.indices[0].name] = tensor.indices[1].name
                    for j in range(len(t.tensors)):
                        if (j not in dontprint):
                            replaceindex(t.tensors[j], tensor.indices[1].name, tensor.indices[0].name)

                else :
                    ifstatement += tensor.indices[0].name +" == " +tensor.indices[1].name + " and "

        #start by printint the if statement
        outString = ""
        if (len(ifstatement) != 4) :
            outString += ifstatement[:-4]+" : \n\t"

        #now print(the einsum string)
        outString += "\tCout +=  ("+ str(t.numConstant)+ ") *numpy.einsum( '"
        for i in range(len(tensorcopy)):
            tensor = tensorcopy[i]
            if(i not in dontprint):
                for index in range(len(tensor.indices)):
                    if (tensor.name[:3] == "int" and  len(tensor.indices[index].name) > 1 and tensor.indices[index].name[0] == "A"):
                        outString += tensor.indices[index].name[-1].capitalize()
                    elif (tensor.name[:1] == "E" and  len(tensor.indices[index].name) > 1 and tensor.indices[index].name[0] == "A"):
                        outString += tensor.indices[index].name[-1].capitalize()
                    elif len(tensor.indices[index].name) == 1:
                        outString += tensor.indices[index].name[0]
                outString += " ,"
        outString += indexKey["Ap"][-1].capitalize()+indexKey["Aq"][-1].capitalize()+" -> RS' "

        for i in range(len(tensorcopy)):
            tensor = tensorcopy[i]
            if(i not in dontprint):
                if (tensor.name[:3] == "int") :
                    outString+= " , "+ printIntTensor(tensor, activeInEinsum)
                elif (tensor.name[0] == "E"):
                    outString+= " , "+ printETensor(tensor, activeInEinsum)
                else:
                    outString+= " , "+ printTensor(tensor, {})
        outString += " ,  Cin)"
        print(outString)
    else :
     for t in result:
        tensorString = ""
        ifstatement = "if"

        tensorcopy = t.tensors
        dontprint= []
        indexKey = {'Va': 'Va', 'Vb' : 'Vb'}
        for i in range(len(tensorcopy)):
            tensor = tensorcopy[i]

            #check the delta function
            if (tensor.name == "kdelta"):
                dontprint.append(i)

                if (tensor.indices[0].name == "Vc" or tensor.indices[0].name == "Vd") :
                    indexKey[tensor.indices[1].name] = tensor.indices[0].name
                    for j in range(len(t.tensors)):
                        if (j not in dontprint):
                            replaceindex(t.tensors[j], tensor.indices[0].name, tensor.indices[1].name)
                elif (tensor.indices[1].name == "Vc" or tensor.indices[1].name == "Vd") :
                    indexKey[tensor.indices[0].name] = tensor.indices[1].name
                    for j in range(len(t.tensors)):
                        if (j not in dontprint):
                            replaceindex(t.tensors[j], tensor.indices[1].name, tensor.indices[0].name)
                else :
                    ifstatement += tensor.name +" == " +tensor.name + " and"

        outString = ""
        if (len(ifstatement) != 2) :
            outString += ifstatement[:-3]+" : "
        outString += "\t Cout[Vc,Vd,Ar,As] +=  ("+ str(t.numConstant)+ ") *numpy.einsum( '"
        for i in range(len(tensorcopy)):
            tensor = tensorcopy[i]
            if(i not in dontprint):
                for index in range(len(tensor.indices)):
                    if ( len(tensor.indices[index].name) > 1):
                        outString += tensor.indices[index].name[-1].capitalize()
                    else :
                        outString += tensor.indices[index].name[0]
                outString += " ,"
        outString += indexKey["Va"][-1].capitalize()+indexKey["Vb"][-1].capitalize()+"PQ -> CDRS' "
        for i in range(len(tensorcopy)):
            tensor = tensorcopy[i]
            if(i not in dontprint):
                outString+= " , "+ tensor.__str__()
        outString += " ,  Cin[" + indexKey["Va"]+ ","+ indexKey["Vb"]+ ",Ap,Aq])"
        print(outString)

def WriteCode_ccav(result, SupressActive, intmapkey, RDMmapkey, activeInEinsum = False):
    if (SupressActive):
     for t in result:
        tensorString = ""
        ifstatement = "\tif "

        tensorcopy = t.tensors
        dontprint= []
        indexKey = {'Ap': 'Ap', 'Va' : 'Va'}
        for i in range(len(tensorcopy)):
            tensor = tensorcopy[i]

            #check the delta function
            if (tensor.name == "kdelta"):
                dontprint.append(i)

                if (tensor.indices[0].name == "Aq" or tensor.indices[0].name == "Vb") :
                    indexKey[tensor.indices[1].name] = tensor.indices[0].name
                    for j in range(len(t.tensors)):
                        if (j not in dontprint):
                            replaceindex(t.tensors[j], tensor.indices[0].name, tensor.indices[1].name)
                elif (tensor.indices[1].name == "Aq" or tensor.indices[1].name == "Vb") :
                    indexKey[tensor.indices[0].name] = tensor.indices[1].name
                    for j in range(len(t.tensors)):
                        if (j not in dontprint):
                            replaceindex(t.tensors[j], tensor.indices[1].name, tensor.indices[0].name)

                else :
                    ifstatement += tensor.indices[0].name +" == " +tensor.indices[1].name + " and "

        #start by printint the if statement
        outString = ""
        if (len(ifstatement) != 4) :
            outString += ifstatement[:-4]+" : \n\t"

        #now print(the einsum string)
        outString += "\tCout +=  ("+ str(t.numConstant)+ ") *numpy.einsum( '"
        for i in range(len(tensorcopy)):
            tensor = tensorcopy[i]
            if(i not in dontprint):
                for index in range(len(tensor.indices)):
                    if (tensor.name[:3] == "int" and  len(tensor.indices[index].name) > 1 and  (tensor.indices[index].name[0] == "A" or tensor.indices[index].name[0] == "V")):
                        outString += tensor.indices[index].name[-1].capitalize()
                    elif (tensor.name[:1] == "E" and  len(tensor.indices[index].name) > 1 and (tensor.indices[index].name[0] == "A" or tensor.indices[index].name[0] == "V")):
                        outString += tensor.indices[index].name[-1].capitalize()
                    elif len(tensor.indices[index].name) == 1:
                        outString += tensor.indices[index].name[0]
                outString += " ,"
        outString += indexKey["Ap"][-1].capitalize()+indexKey["Va"][-1].capitalize()+" -> QB' "

        for i in range(len(tensorcopy)):
            tensor = tensorcopy[i]
            if(i not in dontprint):
                if (tensor.name[:3] == "int") :
                    outString+= " , "+ printIntTensor(tensor, True)
                elif (tensor.name[0] == "E"):
                    outString+= " , "+ printETensor(tensor, True)
                else:
                    outString+= " , "+ printTensor(tensor, {})
        outString += " ,  Cin)"
        print(outString)
    else :
     for t in result:
        tensorString = ""
        ifstatement = "if"

        tensorcopy = t.tensors
        dontprint= []
        indexKey = {'Va': 'Va', 'Vb' : 'Vb'}
        for i in range(len(tensorcopy)):
            tensor = tensorcopy[i]

            #check the delta function
            if (tensor.name == "kdelta"):
                dontprint.append(i)

                if (tensor.indices[0].name == "Vc" or tensor.indices[0].name == "Vd") :
                    indexKey[tensor.indices[1].name] = tensor.indices[0].name
                    for j in range(len(t.tensors)):
                        if (j not in dontprint):
                            replaceindex(t.tensors[j], tensor.indices[0].name, tensor.indices[1].name)
                elif (tensor.indices[1].name == "Vc" or tensor.indices[1].name == "Vd") :
                    indexKey[tensor.indices[0].name] = tensor.indices[1].name
                    for j in range(len(t.tensors)):
                        if (j not in dontprint):
                            replaceindex(t.tensors[j], tensor.indices[1].name, tensor.indices[0].name)
                else :
                    ifstatement += tensor.name +" == " +tensor.name + " and"

        outString = ""
        if (len(ifstatement) != 2) :
            outString += ifstatement[:-3]+" : "
        outString += "\t Cout[Vc,Vd,Ar,As] +=  ("+ str(t.numConstant)+ ") *numpy.einsum( '"
        for i in range(len(tensorcopy)):
            tensor = tensorcopy[i]
            if(i not in dontprint):
                for index in range(len(tensor.indices)):
                    if ( len(tensor.indices[index].name) > 1):
                        outString += tensor.indices[index].name[-1].capitalize()
                    else :
                        outString += tensor.indices[index].name[0]
                outString += " ,"
        outString += indexKey["Va"][-1].capitalize()+indexKey["Vb"][-1].capitalize()+"PQ -> CDRS' "
        for i in range(len(tensorcopy)):
            tensor = tensorcopy[i]
            if(i not in dontprint):
                outString+= " , "+ tensor.__str__()
        outString += " ,  Cin[" + indexKey["Va"]+ ","+ indexKey["Vb"]+ ",Ap,Aq])"
        print(outString)

def WriteCode_caav(result, SupressActive, intmapkey, RDMmapkey, activeInEinsum = False):
    if (SupressActive):
     for t in result:
        tensorString = ""
        ifstatement = "\tif "

        tensorcopy = t.tensors
        dontprint= []
        indexKey = {'Ap': 'Ap', 'Aq' : 'Aq', 'Va' : 'Va'}
        for i in range(len(tensorcopy)):
            tensor = tensorcopy[i]

            #check the delta function
            if (tensor.name == "kdelta"):
                dontprint.append(i)

                if (tensor.indices[0].name == "Ar" or tensor.indices[0].name == "As"  or tensor.indices[0].name == "Vb") :
                    indexKey[tensor.indices[1].name] = tensor.indices[0].name
                    for j in range(len(t.tensors)):
                        if (j not in dontprint):
                            replaceindex(t.tensors[j], tensor.indices[0].name, tensor.indices[1].name)
                elif (tensor.indices[1].name == "Ar" or tensor.indices[1].name == "As" or tensor.indices[1].name == "Vb") :
                    indexKey[tensor.indices[0].name] = tensor.indices[1].name
                    for j in range(len(t.tensors)):
                        if (j not in dontprint):
                            replaceindex(t.tensors[j], tensor.indices[1].name, tensor.indices[0].name)

                else :
                    ifstatement += tensor.indices[0].name +" == " +tensor.indices[1].name + " and "

        #start by printint the if statement
        outString = ""
        if (len(ifstatement) != 4) :
            outString += ifstatement[:-4]+" : \n\t"

        #now print(the einsum string)
        outString += "\tCout +=  ("+ str(t.numConstant)+ ") *numpy.einsum( '"
        for i in range(len(tensorcopy)):
            tensor = tensorcopy[i]
            if(i not in dontprint):
                for index in range(len(tensor.indices)):
                    if (tensor.name[:3] == "int" and  len(tensor.indices[index].name) > 1 and  (tensor.indices[index].name[0] == "A" or tensor.indices[index].name[0] == "V")):
                        outString += tensor.indices[index].name[-1].capitalize()
                    elif (tensor.name[:1] == "E" and  len(tensor.indices[index].name) > 1 and (tensor.indices[index].name[0] == "A" or tensor.indices[index].name[0] == "V")):
                        outString += tensor.indices[index].name[-1].capitalize()
                    elif len(tensor.indices[index].name) == 1:
                        outString += tensor.indices[index].name[0]
                outString += " ,"
        outString += indexKey["Ap"][-1].capitalize()+indexKey["Aq"][-1].capitalize()+indexKey["Va"][-1].capitalize()+" -> RSB' "

        for i in range(len(tensorcopy)):
            tensor = tensorcopy[i]
            if(i not in dontprint):
                if (tensor.name[:3] == "int") :
                    outString+= " , "+ printIntTensor(tensor, True)
                elif (tensor.name[0] == "E"):
                    outString+= " , "+ printETensor(tensor, True)
                else:
                    outString+= " , "+ printTensor(tensor, {})
        outString += " ,  Cin)"
        print(outString)

def WriteCode_lcc(result, AllTensors, inputIndices, outIndicesString, commentTensor, inputtensorname="p", outputtensorname="Ap", EquationName="EqsRes", scale=1.0):

     outString = ""
     for t in result:
        tensorString = ""

        indexKey = {}
        for index in inputIndices:
            indexKey[index] = index

        tensorcopy = t.tensors
        dontprint= []

        for i in range(len(tensorcopy)):
            tensor = tensorcopy[i]

            #check the delta function
            if (tensor.name == "kdelta"):

                #take the delta functions and if one of the index is in Cin then replace that index with other in all tensors
                if (tensor.indices[0].name in indexKey):
                    dontprint.append(i)
                    indexKey[tensor.indices[0].name] = tensor.indices[1].name
                    for j in range(len(t.tensors)):
                        if (j not in dontprint):
                            replaceindex(t.tensors[j], tensor.indices[1].name, tensor.indices[0].name)
                elif (tensor.indices[1].name in indexKey):
                    dontprint.append(i)
                    indexKey[tensor.indices[1].name] = tensor.indices[0].name
                    for j in range(len(t.tensors)):
                        if (j not in dontprint):
                            replaceindex(t.tensors[j], tensor.indices[0].name, tensor.indices[1].name)

        tensorIndexStringList = [outIndicesString]  #output tensor indices
        for i in range(len(tensorcopy)):
            tensor = tensorcopy[i]
            tensorIndexString = ""
            if(i not in dontprint):
                for index in range(len(tensor.indices)):
                    if ( len(tensor.indices[index].name) > 1):
                        tensorIndexString += tensor.indices[index].name[-1].capitalize()
                    else :
                        tensorIndexString += tensor.indices[index].name[0]
                tensorIndexStringList.append(tensorIndexString)  #tensor index string of output


        inputIndicesString = ""
        for key in inputIndices:
            inputIndicesString += indexKey[key][-1].capitalize()

        if (inputIndicesString != ""):
            tensorIndexStringList.append(inputIndicesString)


        #now make the string for the equation
        commentString = "\t\t//"
        outString += "\t\t{\""
        for indexstring in tensorIndexStringList:
            outString += indexstring+","
        outString = outString[:-1] +"\","
        outString +=" "+ str(t.numConstant*scale)+"  , "+str(len(tensorIndexStringList))+", {"+str(AllTensors.index(outputtensorname))
        commentString += outputtensorname+"["+tensorIndexStringList[0]+"] += "+str(t.numConstant*scale)+" "

        index = 1
        for i in range(len(tensorcopy)):
            tensor = tensorcopy[i]
            if(i not in dontprint):
                outString+= ","+ str(AllTensors.index(tensor.name))
                commentString += commentTensor[tensor.name]+"["+tensorIndexStringList[index]+"] "
                index += 1
        commentString += inputtensorname+"["+inputIndicesString+"]"
        if (inputtensorname != "") :
            outString += ","+str(AllTensors.index(inputtensorname)) +"}},"+commentString+ "\n"
        else:
            outString = outString[:-1]+"}},"+commentString+ "\n"

     print(outString[:-1])


