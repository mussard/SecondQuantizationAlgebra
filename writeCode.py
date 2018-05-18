import secondQuantizationAlgebra as sqa
def replaceindex(tensor, a, b) :
    for i in range(len(tensor.indices)):
        if (tensor.indices[i].name == a):
            tensor.indices[j] = b

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

def WriteCode(result, SupressActive, intmapkey, RDMmapkey, activeInEinsum = False):
    if (SupressActive):
     for t in result:
        tensorString = ""
        ifstatement = "\tif "
        
        tensorcopy = t.tensors
        dontprint(= [])
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
                    if (tensor.name[:3] == "int" and  len(tensor.indices[index].name) > 1 and tensor.indices[index].name[0] == "V"):
                        outString += tensor.indices[index].name[-1].capitalize()
                    elif len(tensor.indices[index].name) == 1:
                        outString += tensor.indices[index].name[0]
                outString += " ," 
        outString += indexKey["Va"][-1].capitalize()+indexKey["Vb"][-1].capitalize()+" -> CD' "

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
        dontprint(= [])
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


def WriteCode_ccaa(result, SupressActive, intmapkey, RDMmapkey, activeInEinsum = False):
    if (SupressActive):
     for t in result:
        tensorString = ""
        ifstatement = "\tif "
        
        tensorcopy = t.tensors
        dontprint(= [])
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
        dontprint(= [])
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
        dontprint(= [])
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
        dontprint(= [])
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
        dontprint(= [])
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
