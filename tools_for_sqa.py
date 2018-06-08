#
# List of the tools:
#   - tag_cor/tag_act/tag_vir
#   - used_cor/used_act/used_vir
#   - list_cor/list_act/list_vir
#   - next_cor/next_act/next_vir
#   - gimme
#   - short_type
#   - code
#   - pattern
#   - is_non_zero
#   - indexes_of_ExOp
#   - from basis
#   - sym rules and delta fcts
#   - symmTens/unique_tensor
#   - [old] symmTens/unique_tensor
#
# Specific to PT:
#   - pattern_of
#   - tensors
#
# And:
#   - simplify_all
#   - [geraldCode]
#
import secondQuantizationAlgebra as sqa

def string_of_names(list):
  line=''
  for iter in list:
    if iter.indType[0]==sqa.options.core_type:
      line+='o'
    elif iter.indType[0]==sqa.options.virtual_type:
      line+='v'
  return line.lower()
def code(input_list):
  if any(isinstance(el, list) for el in input_list):
    line=''
    for i in range(len(input_list)):
      line+=code(input_list[i])
    return line
  if len(input_list)==0:
    line=''
  else:
    line=string_of_names(input_list)
  return line.lower()
def pattern(list_of_terms):
  cre=[]
  des=[]
  for term in list_of_terms:
    ExOp=[term.tensors[i] for i in range(len(term.tensors))\
                          if isinstance(term.tensors[i],sqa.sfExOp)]
    order=[len(t.indices) for t in ExOp]
    cre+=[ExOp[i].indices[:order[i]/2] for i in range(len(ExOp))]
    des+=[ExOp[i].indices[order[i]/2:] for i in range(len(ExOp))]
  cre=[inner for outer in cre for inner in outer]
  des=[inner for outer in des for inner in outer]
  countO=0
  countV=0
  for ind in cre:
    if ind.indType[0]==sqa.options.core_type:
      countO+=1
    if ind.indType[0]==sqa.options.virtual_type:
      countV+=1
  for ind in des:
    if ind.indType[0]==sqa.options.core_type:
      countO-=1
    if ind.indType[0]==sqa.options.virtual_type:
      countV-=1
  return [countO,countV]
def is_non_zero(list_of_terms):
  list=pattern(list_of_terms)
  total=abs(list[0])+abs(list[1])
  return total==0
def list_indexes(list_of_terms):
  string=''
  for term in list_of_terms:
    indexes=[term.tensors[i].indices\
             for i in range(len(term.tensors))\
             if isinstance(term.tensors[i],sqa.sfExOp)]
    string+=code(indexes)
  return string
def list_tensors(term):
  string=''
  for tensor in term.tensors:
    if not isinstance(tensor,sqa.sfExOp):
      string+=tensor.name+'.'
  return string[:-1]


# ====================================================
# About indexes: define a list of
# core,active,virtual indexes
# and prepare a list of used indexes
# ====================================================
tag_cor = sqa.options.core_type
tag_act = sqa.options.active_type
tag_vir = sqa.options.virtual_type
used_cor=[]
used_act=[]
used_vir=[]
list_cor=[]
list_act=[]
list_vir=[]
for i in range(40):
  list_cor.append(sqa.index('i%02i'%(i+1), [tag_cor], True))
  list_act.append(sqa.index('p%02i'%(i+1), [tag_act], True))
  list_vir.append(sqa.index('a%02i'%(i+1), [tag_vir], True))


# ====================================================
def next_cor():
# ----------------------------------------------------
# Give the next unused core index
# ====================================================
  if len(used_cor)==40:
    print '[next_cor]: too few indices'
    exit()
  for i in range(40):
    if i not in used_cor:
      break
  used_cor.append(i)
  return list_cor[i]
# ====================================================
def next_act():
# ----------------------------------------------------
# Give the next unused active index
# ====================================================
  if len(used_act)==40:
    print '[next_act]: too few indices'
    exit()
  for i in range(40):
    if i not in used_act:
      break
  used_act.append(i)
  return list_act[i]
# ====================================================
def next_vir():
# ----------------------------------------------------
# Give the next unused virtual index
# ====================================================
  if len(used_vir)==40:
    print '[next_vir]: too few indices'
    exit()
  for i in range(40):
    if i not in used_vir:
      break
  used_vir.append(i)
  return list_vir[i]


# ====================================================
def gimme(string):
# ----------------------------------------------------
# Give a list of next unused index
# corresponding to the string
# ====================================================
  list=[]
  for i in range(len(string)):
    if string[i]=='c':
      list.append(next_cor())
    elif string[i]=='a':
      list.append(next_act())
    elif string[i]=='v':
      list.append(next_vir())
    else:
      print '[gimme]: must be c or a or v'
      exit()
  return list


# ====================================================
def short_type(index):
# ----------------------------------------------------
# Give 'c', 'a' or 'v' of an index
# ====================================================
  return index.indType[0][0][0]


# ====================================================
def code(input):
# ----------------------------------------------------
# Give the string of types of a list of indexes
# ====================================================
  if not isinstance(input,list):
    print '[code]: must be a list'
    exit()
  if any(isinstance(el, list) for el in input):
    line=''
    for i in range(len(input)):
      line+=code(input[i])
    return line
  if all(isinstance(el, sqa.index) for el in input):
    return ''.join([short_type(el) for el in input])
  elif all(isinstance(el, sqa.term) for el in input):
    return code([indexes_of_ExOp(el) for el in input])
  else:
    print '[code]: must be a indices or terms'
    exit()


# ====================================================
def pattern(list_of_terms):
# ----------------------------------------------------
# Give the [delta_c,delta_a,delta_v] of a list of terms
# ====================================================
  if not isinstance(list_of_terms,list):
    print '[pattern]: must be a list'
    exit()
  cre=[]
  des=[]
  for term in list_of_terms:
    ExOp=[term.tensors[i] for i in range(len(term.tensors))\
                          if isinstance(term.tensors[i],sqa.sfExOp)]
    order=[len(t.indices) for t in ExOp]
    cre+=[ExOp[i].indices[:order[i]/2] for i in range(len(ExOp))]
    des+=[ExOp[i].indices[order[i]/2:] for i in range(len(ExOp))]
  cre=[inner for outer in cre for inner in outer]
  des=[inner for outer in des for inner in outer]
  countC=0
  countA=0
  countV=0
  for ind in cre:
    if ind.indType[0]==tag_cor:
      countC+=1
    elif ind.indType[0]==tag_act:
      countA+=1
    elif ind.indType[0]==tag_vir:
      countV+=1
    else:
      print '[pattern]: must be c or a or v'
      exit()
  for ind in des:
    if ind.indType[0]==tag_cor:
      countC-=1
    elif ind.indType[0]==tag_act:
      countA-=1
    elif ind.indType[0]==tag_vir:
      countV-=1
    else:
      print '[pattern]: must be c or a or v'
      exit()
  return [countC,countA,countV]


# ====================================================
def is_non_zero(list_of_terms):
# ----------------------------------------------------
# Is <0| list_of_terms |0> non zero
# ====================================================
  list=pattern(list_of_terms)
  total=abs(list[0])+abs(list[1])+abs(list[2])
  return total==0


# ====================================================
def indexes_of_ExOp(term):
# ----------------------------------------------------
# Give the indexes that make up the sfExOp
# ====================================================
  indexes=[term.tensors[i].indices\
           for i in range(len(term.tensors))\
           if isinstance(term.tensors[i],sqa.sfExOp)]
  return indexes


# ====================================================
def from_basis(basis1,basis2):
# ----------------------------------------------------
# Give the list of indexes [1324] from E_12 E_34
# ====================================================
  one=basis1.indices
  two=basis2.indices
  return [one[0],two[0],one[1],two[1]]


# ====================================================
# About symmetry rules and delta functions
# ====================================================
two_sym   = sqa.symmetry((1,0), 1)
four_sym1 = sqa.symmetry((2,1, 0,3), 1)
four_sym2 = sqa.symmetry((0,3, 2,1), 1)
four_sym3 = sqa.symmetry((1,0, 3,2), 1)
deltaC = sqa.tensor('deltac', gimme('cc'), [two_sym])
deltaA = sqa.tensor('deltaa', gimme('aa'), [two_sym])
deltaV = sqa.tensor('deltav', gimme('vv'), [two_sym])


# ====================================================
# About tensors:
# Define lists of wanted tensors
# and offer a way to find them from any tensors
# ====================================================
symmTens=['vvcc','vvca','ccav','vvaa','ccaa','vaca','avca',\
          'vaaa','caaa','ccca','cccv','vvvc','vvva','caca',\
          'cvcv','avav','cacv','avcv','cccc','aaaa','vvvv']
# ====================================================
def unique_tensor(list):
# ----------------------------------------------------
# Give the unique tensor from a list of indexes
# ====================================================
  name=code(list)
  if len(list)==2:
    trans=[0,1]
    if ''.join(sorted(name))==name:
      trans=[1,0]
  elif len(list)==4:
    if   ''.join([name[i] for i in [0,1,2,3]]) in symmTens:
      trans=[0,1,2,3]
    elif ''.join([name[i] for i in [0,3,2,1]]) in symmTens:
      trans=[0,3,2,1]
    elif ''.join([name[i] for i in [2,1,0,3]]) in symmTens:
      trans=[2,1,0,3]
    elif ''.join([name[i] for i in [2,3,0,1]]) in symmTens:
      trans=[2,3,0,1]
    elif ''.join([name[i] for i in [1,0,3,2]]) in symmTens:
      trans=[1,0,3,2]
    elif ''.join([name[i] for i in [3,0,1,2]]) in symmTens:
      trans=[3,0,1,2]
    elif ''.join([name[i] for i in [1,2,3,0]]) in symmTens:
      trans=[1,2,3,0]
    elif ''.join([name[i] for i in [3,2,1,0]]) in symmTens:
      trans=[3,2,1,0]
    #print '//',name,'=',\
    #      ''.join([name[A]       +str(A) for A in range(4)]),'->',\
    #      ''.join([name[trans[A]]+str(trans[A]) for A in range(4)]),'=',\
    #      symmTens[iterj][0]
    if ''.join([name[i] for i in trans]) not in symmTens:
      print 'ERROR symmTens',name,symmTens
      exit()
  else:
    print '[unique_tensor] is for 2 or 4'
    exit()
  list=[list[i] for i in trans]
  return list


# ====================================================
# About tensors:
# Define lists of equivalent tensors
# and offer a way to find them
# ====================================================
symmTens_old=[
          ['vvcc','ccvv','vccv','cvvc'],
          ['vvca','acvv','avvc','vvac','vcav','cvva','vacv','cavv'],
          ['ccav','accv','ccva','cvac','avcc','vcca','cavc','vacc'],
          ['vvaa','aavv','vaav','avva'],
          ['ccaa','aacc','acca','caac'],
          ['vaca','cava','acav','avac','cava'],
          ['avca','aacv','aavc','cvaa','vaac','acva','vcaa','caav'],
          ['vaaa','aaav','avaa','aava'],
          ['caaa','aaac','acaa','aaca'],
          #
          ['ccca','accc','cacc','ccac'],
          ['cccv','vccc','cvcc','ccvc'],
          ['vvvc','cvvv','vcvv','vvcv'],
          ['vvva','avvv','vavv','vvav'],
          ['caca','acac'],
          ['cvcv','vcvc'],
          ['avav','vava'],
          ['cacv','cvca','vcac','acvc'],
          ['avcv','vavc','vcva','cvav'],
         ]
# Check for errors (that all lists indeed give the same integral)
for elt in symmTens_old:
  comp=elt[0]
  model1=comp[0]+comp[2]
  model2=comp[1]+comp[3]
  for iteri in range(1,len(elt)):
    comp=elt[iteri]
    comp1N=comp[0]+comp[2]
    comp1R=comp[2]+comp[0]
    comp2N=comp[1]+comp[3]
    comp2R=comp[3]+comp[1]
    if((comp1N+comp2N!=model1+model2)and
       (comp1N+comp2R!=model1+model2)and
       (comp1R+comp2N!=model1+model2)and
       (comp1R+comp2R!=model1+model2)and
       (comp2N+comp1N!=model1+model2)and
       (comp2R+comp1N!=model1+model2)and
       (comp2N+comp1R!=model1+model2)and
       (comp2R+comp1R!=model1+model2)):
      print 'ERROR symmTens',elt[0], comp, comp1N, comp2N, comp1R, comp2R
      exit()
# ====================================================
def unique_tensor_old(list):
# ----------------------------------------------------
# Give the unique tensor from a list of indexes
# ====================================================
  name=code(list)
  if len(list)==2:
    if name=='ac' or name=='av' or name=='cv':
      list=[list[1],list[0]]
  elif len(list)==4:
    for iterj in range(len(symmTens_old)):
      if name in symmTens_old[iterj] and name!=symmTens_old[iterj][0]:
        comp=symmTens_old[iterj][0]
        model1=comp[0]+comp[2]
        model2=comp[1]+comp[3]
        comp1N=name[0]+name[2]
        comp1R=name[2]+name[0]
        comp2N=name[1]+name[3]
        comp2R=name[3]+name[1]
        if(comp1N+comp2N==model1+model2):
          trans=[0,1,2,3]
        elif(comp1N+comp2R==model1+model2):
          trans=[0,3,2,1]
        elif(comp1R+comp2N==model1+model2):
          trans=[2,1,0,3]
        elif(comp1R+comp2R==model1+model2):
          trans=[2,3,0,1]
        elif(comp2N+comp1N==model1+model2):
          trans=[1,0,3,2]
        elif(comp2R+comp1N==model1+model2):
          trans=[3,0,1,2]
        elif(comp2N+comp1R==model1+model2):
          trans=[1,2,3,0]
        elif(comp2R+comp1R==model1+model2):
          trans=[3,2,1,0]
        #print '//',name,'=',\
        #      ''.join([name[A]       +str(A) for A in range(4)]),'->',\
        #      ''.join([name[trans[A]]+str(trans[A]) for A in range(4)]),'=',\
        #      symmTens[iterj][0]
        list=[list[iterk] for iterk in trans]
        name=''.join([name[iterk] for iterk in trans])
        if name!=symmTens_old[iterj][0]:
          print 'ERROR symmTens_old',name,symmTens_old[iterj][0]
          exit()
  else:
    print '[unique_tensor] is for 2 or 4'
    exit()
  return list


# ====================================================
# ====================================================


pattern_of={}
pattern_of['vvcc'] =[-2, 0, 2]
pattern_of['vvca'] =[-1,-1, 2]
pattern_of['ccav'] =[-2, 1, 1]
pattern_of['vvaa'] =[ 0,-2, 2]
pattern_of['ccaa'] =[-2, 2, 0]
pattern_of['vaca'] =[-1, 0, 1]
pattern_of['avca'] =[-1, 0, 1]
pattern_of['vaaa'] =[ 0,-1, 1]
pattern_of['caaa'] =[-1, 1, 0]
pattern_of['other']=[-5,-5,-5]
pattern_of['h0']   =[ 0, 0, 0]

tensors = [['Dvvcc',     'D',       'eecc',       'H'], #I    OK
           ['Dvvca',     'D',       'eeca',       'H'], #II   OK
           ['Dccav',     'D',       'ccae',       'H'], #III  OK
           ['Dvvaa',     'D',       'eeaa',       'H'], #IV   OK
           ['Dccaa',     'D',       'ccaa',       'H'], #V    OK
           ['Dvaca',     'D',       'eaca',       'H'], #VI   ?
           ['Davca',     'D',       'aeca',       'H'], #VI   ?
           ['Dvaaa',     'D',       'eaaa',       'H'], #VII  OK
           ['Dcaaa',     'D',       'caaa',       'H'], #VIII OK
           ['E1',        'E1',      'aa',         'D'], # RDMs...
           ['E2',        'E2',      'aaaa',       'D'],
           ['E3',        'E3',      'aaaaaa',     'D'],
           ['E4',        'E4',      'aaaaaaaa',   'D'],
           ['deltac',    'delta',   'cc',         'D'], # delta functions...
           ['deltaa',    'delta',   'aa',         'D'],
           ['deltav',    'delta',   'ee',         'D'],
          ]


# ====================================================
# ====================================================


#
#THIS IS MAINLY GERALD's CODE !!!
#
def simplify_all(result,deltas,cumulantE4=False,cumulantE3=False):
  for t in result:
      t.contractDeltaFuncs_new()
  sqa.removeVirtOps_sf(result)
  sqa.termChop(result)
  sqa.combineTerms(result)
  extendedR=[]
  for t in result:
      extendedR += sqa.contractCoreOps_sf(t)
  for t in extendedR:
      t.contractDeltaFuncs_new()
  sqa.termChop(extendedR)
  sqa.combineTerms(extendedR)
  result = []
  for r in extendedR:
      item1=replaceRepeatIndicesWithDeltas(r, deltas)
      item2=replaceSingleKdeltaWithDeltas(item1, deltas)
      result.append(replaceAllKdeltaWithDeltas(item2, deltas))
  if (cumulantE4):
    x1 = sqa.index('Ax1',  [sqa.options.active_type],  True)
    x2 = sqa.index('Ax2',  [sqa.options.active_type],  True)
    x3 = sqa.index('Ax3',  [sqa.options.active_type],  True)
    x4 = sqa.index('Ax4',  [sqa.options.active_type],  True)
    x5 = sqa.index('Ax5',  [sqa.options.active_type],  True)
    x6 = sqa.index('Ax6',  [sqa.options.active_type],  True)
    sqa.decomp_4rdms_to_3rdms_sf(result, 'E4',
                                         sqa.sfExOp([x1,x2]),
                                         sqa.sfExOp([x1,x2,x3,x4]),
                                         sqa.sfExOp([x1,x2,x3,x4]),
                                         sqa.sfExOp([x1,x2,x3,x4]),
                                         sqa.sfExOp([x1,x2,x3,x4,x5,x6]))
  if (cumulantE3):
    x1 = sqa.index('Ax1',  [sqa.options.active_type],  True)
    x2 = sqa.index('Ax2',  [sqa.options.active_type],  True)
    x3 = sqa.index('Ax3',  [sqa.options.active_type],  True)
    x4 = sqa.index('Ax4',  [sqa.options.active_type],  True)
    sqa.decomp_3rdms_to_2rdms_sf(result, 'E3',
                                         sqa.sfExOp([x1,x2]),
                                         sqa.sfExOp([x1,x2,x3,x4]))
  return result


def replaceindex(tensor, a, b) :
    for i in range(len(tensor.indices)):
        if (tensor.indices[i].name == a):
            tensor.indices[i] = b


def replaceAllKdeltaWithDeltas(term, rdmDelta):
    #import string
    #l = list(string.ascii_lowercase) #list of all printables

    usedIndices = []
    for t in term.tensors:
        for index in t.indices:
            usedIndices.append(index.name)

    #unUsedList = sorted(list(set(l) - set(usedIndices)))

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
    #import string
    #l = list(string.ascii_lowercase) #list of all printables

    usedIndices = []
    for t in term.tensors:
        for index in t.indices:
            usedIndices.append(index.name)

    #unUsedList = sorted(list(set(l) - set(usedIndices)))

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
    call_again=False #THIS, scenario2
    for t in term.tensors:
        if (t.name == "kdelta"):
            continue
        uniques = list(set(t.indices))
        numRepeats = len(uniques)*[0]
        for index in t.indices:
            numRepeats[ uniques.index(index) ] +=1

        for i in range(len(numRepeats)):
            repeatPositions = [j for j, x in enumerate(t.indices) if x == uniques[i]] #THIS, scenario2
            if (numRepeats[i] > 2):
                #THIS,scenario1# print("more than a double repeat in tensor ", t)
                #THIS,scenario1# exit(0)
                numRepeats[i]=2                       #THIS, scenario2
                repeatPositions = repeatPositions[:2] #THIS, scenario2
                call_again=True                       #THIS, scenario2

            if (numRepeats[i] == 2):
                #THIS,scenario1# repeatIndex = uniques[i]
                #THIS,scenario1# repeatPositions = [j for j, x in enumerate(t.indices) if x == uniques[i]]
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
    if call_again:                                   #THIS, scenario2
      replaceRepeatIndicesWithDeltas(term, rdmDelta) #THIS, scenario2
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


def WriteCode_withSuppressActive(result, SupressActive, intmapkey, RDMmapkey, activeInEinsum = False):
    if (SupressActive):
     for t in result:
        #tensorString = ""
        ifstatement = "\tif "

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
        #tensorString = ""
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


def WriteCode(result, tensors):
     outString = ""
     for t in result:
        #tensorString = ""
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
        #tensorString = ""
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
        #tensorString = ""
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
        #tensorString = ""
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
        #tensorString = ""
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
        #tensorString = ""
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
        #tensorString = ""

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


