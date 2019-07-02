#
# ==================================================
#    TOOLS FOR Second Quantization Algebra (sqa)
# ==================================================
#   This is meant to be a layer of front-end tools
#         to access the main functionalities
#               of the `sqa` package.
# ==================================================
#
#
# -- INDICES
# A bunch of the tools provide easy-to-use `indices`
# for the core, active and virtual spaces.
#
# The possible indices ready to use are stored in the lists `list_cor`, `list_act` and `list_vir`,
#  while the indices already in use are stored in the lists `used_cor`, `used_act` and `used_vir`.
#
# With this, the user can call for one new sqa.index to be provided using
# the functions `next_cor`, `next_act` and `next_vir`
# or for a list of indices corresponding to a string of `short_types`, using the function `gimme`.
#
# We call `short_type`  a one-character string `c`, `a` or `v` describing the type of a given sqa.index
# (and the function `short_type` returns the short_type of an sqa.index).
#
# Example:
#   next_act()              provides a new active sqa.index.
#   gimme('ccvv')           gives a list of two new core sqa.index and two new virtual sqa.index.
#   short_type(<sqa.index>) gives `c`, `a` or `v` depending on the type of index provided.
#
#
# -- TERMS
# This bundle also offers tools to extract informations from sqa.term or lists of sqa.terms
#
# In particular, see:
#   - code
#   - pattern
#   - is_non_zero
#   - indices_of_ExOp
#   - indices_of_Tensor
#   - reorga_two_to_one
#
#
# -- TENSORS
# Here are defined some useful 2- and 4-index symmetries for sqa.tensor.
#
# The main tools is the `unique_tensor`, with will give a reorganized list of indices
# corresponding to a unique tensor outputed by pyscf.
#
# Example:
#   unique_tensor([i1,i2,a1,a2]) will give back [a1,a2,i1,i2],
#                                because pyscf outputs W:vvcc.npy
#
#
# -- AND:
#   - simplify_all
#   - [geraldCode]
# -- TO DELETE:
#       geraldCode.py geraldCode.save.py mussardCode.py writeCode.py
#
#
import secondQuantizationAlgebra as sqa

# ====================================================
# About indices: prepare a list of predefined
#   core,active,virtual sqa.index
# and a list of such used indices
# ====================================================
tag_cor = sqa.options.core_type
tag_act = sqa.options.active_type
tag_vir = sqa.options.virtual_type
tag_aux = sqa.options.auxiliary_type
used_cor=[]
used_act=[]
used_vir=[]
used_aux=[]
list_cor=[]
list_act=[]
list_vir=[]
list_aux=[]
nprep=99
for i in range(nprep):
  list_cor.append(sqa.index('i%02i'%(i+1), [tag_cor], True))
  list_act.append(sqa.index('p%02i'%(i+1), [tag_act], True))
  list_vir.append(sqa.index('a%02i'%(i+1), [tag_vir], True))
  list_aux.append(sqa.index('L%02i'%(i+1), [tag_aux], True))
# ====================================================
# About symmetry rules and delta functions
# ====================================================
two_sym   = sqa.symmetry((1,0), 1)
three_sym = sqa.symmetry((0, 2,1), 1)
four_sym1 = sqa.symmetry((2,1, 0,3), 1)
four_sym2 = sqa.symmetry((0,3, 2,1), 1)
four_sym3 = sqa.symmetry((1,0, 3,2), 1)
deltaC = sqa.tensor('deltac', [sqa.index('deltaC1', [tag_cor], True),sqa.index('deltaC2', [tag_cor], True)], [two_sym])
deltaA = sqa.tensor('deltaa', [sqa.index('deltaA1', [tag_act], True),sqa.index('deltaA2', [tag_act], True)], [two_sym])
deltaV = sqa.tensor('deltav', [sqa.index('deltaV1', [tag_vir], True),sqa.index('deltaV2', [tag_vir], True)], [two_sym])
deltaL = sqa.tensor('deltaL', [sqa.index('deltaL1', [tag_aux], True),sqa.index('deltaL2', [tag_aux], True)], [two_sym])




# ====================================================
def next_cor():
# ----------------------------------------------------
  '''Gives the next unused core sqa.index
  '''
# ====================================================
  if len(used_cor)==nprep:
    print '[next_cor]: too few indices'
    exit()
  for i in range(nprep):
    if i not in used_cor:
      break
  used_cor.append(i)
  return list_cor[i]
# ====================================================
def next_act():
# ----------------------------------------------------
  '''Gives the next unused active sqa.index
  '''
# ====================================================
  if len(used_act)==nprep:
    print '[next_act]: too few indices'
    exit()
  for i in range(nprep):
    if i not in used_act:
      break
  used_act.append(i)
  return list_act[i]
# ====================================================
def next_vir():
# ----------------------------------------------------
  '''Gives the next unused virtual sqa.index
  '''
# ====================================================
  if len(used_vir)==nprep:
    print '[next_vir]: too few indices'
    exit()
  for i in range(nprep):
    if i not in used_vir:
      break
  used_vir.append(i)
  return list_vir[i]
# ====================================================
def next_aux():
# ----------------------------------------------------
  '''Gives the next unused auxiliary sqa.index
  '''
# ====================================================
  if len(used_aux)==nprep:
    print '[next_aux]: too few indices'
    exit()
  for i in range(nprep):
    if i not in used_aux:
      break
  used_aux.append(i)
  return list_aux[i]




# ====================================================
def gimme(string_of_short_type):
# ----------------------------------------------------
  '''Gives a list of unused sqa.index
     corresponding to the given string of `short_type`

     Args:
         string of `short_type`
     Returns:
         list of sqa.index
  '''
# ====================================================
  list=[]
  for i in range(len(string_of_short_type)):
    if string_of_short_type[i]=='c':
      list.append(next_cor())
    elif string_of_short_type[i]=='a':
      list.append(next_act())
    elif string_of_short_type[i]=='v':
      list.append(next_vir())
    elif string_of_short_type[i]=='L':
      list.append(next_aux())
    else:
      print '[gimme]: must be c or a or v or L'
      exit()
  return list


# ====================================================
def short_type(index):
# ----------------------------------------------------
  '''Gives 'c', 'a' or 'v' for the given sqa.index

     Args:
         an sqa.index
     Returns:
         the corresponding one-character string `c`, `a` or `v`
  '''
# ====================================================
  Type=index.indType[0][0]
  if Type=='core':
    return 'c'
  elif Type=='active':
    return 'a'
  elif Type=='virtual':
    return 'v'
  elif Type=='aux':
    return 'L'
  else:
    print '[short_type]: unknown type'
    exit()


# ====================================================
def code(input_list):
# ----------------------------------------------------
  '''Gives the string of `short_type` of a list of sqa.index
     or of sqa.term (or of lists of..)

     Args:
         a list (or a list of lists) of sqa.index or of sqa.term
     Returns:
         a string of `short_type`
  '''
# ====================================================
  if not isinstance(input_list,list):
    print '[code]: must be a list'
    exit()
  if any(isinstance(el, list) for el in input_list):
    line=''
    for i in range(len(input_list)):
      line+=code(input_list[i])
    return line
  if   all(isinstance(el, sqa.index) for el in input_list):
    return ''.join([short_type(el)   for el in input_list])
  elif all(isinstance(el, sqa.term)  for el in input_list):
    return code([indices_of_ExOp(el) for el in input_list])
  else:
    print '[code]: must be a indices or terms'
    exit()


# ====================================================
def pattern(input):
# ----------------------------------------------------
  '''Gives the change of occupation
     in the core, active and virtual space [delta_c,delta_a,delta_v]
     of an excitation operator, a term, or a list of terms

     Args:
         sqa.sfExOp, sqa.term or list of sqa.terms
     Returns:
         the corresponding list: [delta_c,delta_a,delta_v]
  '''
# ====================================================
  if isinstance(input,sqa.sfExOp):
    return pattern([sqa.term(10000,[''],[input])])
  if not isinstance(input,list):
    return pattern([input])
  cre=[]
  des=[]
  for term in input:
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
  '''Is <0| list_of_terms |0> non zero?
     (Basically checks if the `pattern` of the terms is [0,0,0])

     Args:
         a list of sqa.terms
     Returns:
         True or False
  '''
# ====================================================
  list=pattern(list_of_terms)
  total=abs(list[0])+abs(list[1])+abs(list[2])
  return total==0


# ====================================================
def indices_of_ExOp(term):
# ----------------------------------------------------
  '''Gives the list of sqa.index that make up the sqa.sfExOp
     found in a sqa.term

     Args:
         an sqa.term
     Returns:
         list of sqa.index of the sqa.sfExOp in the sqa.term
  '''
# ====================================================
  if isinstance(term,sqa.term):
    indices=[term.tensors[i].indices\
             for i in range(len(term.tensors))\
             if isinstance(term.tensors[i],sqa.sfExOp)]
  elif isinstance(term,sqa.tensor):
    indices=term.indices

  return indices


# ====================================================
def indices_of_Tensor(term):
# ----------------------------------------------------
  '''Gives the list of sqa.index that make up the sqa.tensor
     found in a sqa.term

     Args:
         an sqa.term
     Returns:
         list of sqa.index of the sqa.tensor in the sqa.term
  '''
# ====================================================
  if isinstance(term,sqa.term):
    indices=[term.tensors[i].indices\
             for i in range(len(term.tensors))\
             if not isinstance(term.tensors[i],sqa.sfExOp)]
  elif isinstance(term,sqa.tensor):
    indices=term.indices
  return indices


# ====================================================
def reorga_two_to_one(basis1,basis2):
# ----------------------------------------------------
  '''Give the list of sqa.index [1324] from E(12) E(34)

     Args:
         two sqa.sfExOp: E(12) and E(34)
     Returns:
         the reorganized indices [1324]
  '''
# ====================================================
  if isinstance(basis1,sqa.sfExOp):
    one=basis1.indices
    two=basis2.indices
  else:
    one=basis1
    two=basis2

  return [one[0],two[0],one[1],two[1]]


# ====================================================
def unique_tensor(list_of_indices):
# ----------------------------------------------------
  '''Gives the reordered list of sqa.index
     that defines a unique tensor, from a given list of sqa.index

     Args:
         a list of sqa.index
     Returns:
         a reordered list of sqa.index pointing to a unique tensor
  '''
# ====================================================
 #return list_of_indices
  # List of wanted tensors
  symmTens=['vvcc','vvca','ccav','vvaa','ccaa','vaca','avca',\
            'vaaa','caaa','ccca','cccv','vvvc','vvva','caca',\
            'cvcv','avav','cacv','avcv','cccc','aaaa','vvvv']

  name=code(list_of_indices)
  # For length 2: alpha-sort
  if len(list_of_indices)==2:
    trans=[0,1]
    if ''.join(sorted(name))==name:
      trans=[1,0]
  # For length 4: find the appropriate translate
  # between the input list and a "wanted" list
  # (i.e. a list correponding to a tensor outputed by pyscf)
  elif len(list_of_indices)==4:
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
  list_of_indices=[list_of_indices[i] for i in trans]
  return list_of_indices


# ====================================================
def unique_tensor_old(list_of_indices):
# ----------------------------------------------------
  '''OLD VERSION

     Gives the reordered list of sqa.index
     that defines a unique tensor, from a given list of sqa.index

     Args:
         a list of sqa.index
     Returns:
         a reordered list of sqa.index pointing to a unique tensor
  '''
# ====================================================
  # Define lists of equivalent tensors
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
  name=code(list_of_indices)
  if len(list_of_indices)==2:
    if name=='ac' or name=='av' or name=='cv':
      list_of_indices=[list_of_indices[1],list_of_indices[0]]
  elif len(list_of_indices)==4:
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
        list_of_indices=[list_of_indices[iterk] for iterk in trans]
        name=''.join([name[iterk] for iterk in trans])
        if name!=symmTens_old[iterj][0]:
          print 'ERROR symmTens_old',name,symmTens_old[iterj][0]
          exit()
  else:
    print '[unique_tensor] is for 2 or 4'
    exit()
  return list_of_indices


# ====================================================
def symm(list_of_indices):
# ----------------------------------------------------
  '''
  '''
# ====================================================
  symm=[]
  #return symm
  if len(list_of_indices)==2:
    if short_type(list_of_indices[0])==short_type(list_of_indices[1]):
      symm.append(two_sym)
  if len(list_of_indices)==3:
    if short_type(list_of_indices[1])==short_type(list_of_indices[2]):
      symm.append(three_sym)
  elif len(list_of_indices)==4:
    if short_type(list_of_indices[0])==short_type(list_of_indices[2]):
      symm.append(four_sym1)
    if short_type(list_of_indices[1])==short_type(list_of_indices[3]):
      symm.append(four_sym2)
    if short_type(list_of_indices[0])==short_type(list_of_indices[1]) and\
       short_type(list_of_indices[2])==short_type(list_of_indices[3]):
      symm.append(four_sym3)
  return symm


# ====================================================
def update_factor(factor,list,print_log=False):
# ----------------------------------------------------
  ''' Detect equivalent excitation operators and skip them
  '''
# ====================================================
  name=code(list)
  skip=False

  if (len(list)==4):
    if ((name[0]==name[1] and name[-2:]!=''.join(sorted(name[-2:])))
     or (''.join(sorted(name[:2]))!=name[:2])):
        skip=True

    if not skip:
      if name not in factor.keys():
        factor[name]=0
      factor[name]=factor[name]+1
      line=' "{:4}" {:} {:4}'.format(code(list),'included as ',name)
    else:
      if name[1]+name[0]+name[3]+name[2] not in factor.keys():
        factor[name[1]+name[0]+name[3]+name[2]]=0
      factor[name[1]+name[0]+name[3]+name[2]]=factor[name[1]+name[0]+name[3]+name[2]]+1
      line=' "{:4}" {:} {:4}'.format(code(list),'skipped (see',name[1]+name[0]+name[3]+name[2]+')')

  elif (len(list)==2):
    if name not in factor.keys():
      factor[name]=1
    line=' "{:4}" {:} {:4}'.format(code(list),'included as ',name)

  if print_log: print '//',line
  return skip
# USEFUL ROUTINES ---------------------------------------------------------------------------------


# ====================================================
# ====================================================


#
#THIS IS MAINLY GERALD's CODE !!!
#
# ====================================================
def simplify_all(result,deltas,cumulantE4=False,cumulantE3=False):
# ----------------------------------------------------
  '''HERE
  '''
# ====================================================
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
    sqa.decomp_4rdms_to_3rdms_sf(result, 'E4',
                                 sqa.tensor('E1'   ,list_act[:2],[]),#two_sym]),
                                 sqa.tensor('E2'   ,list_act[:4],[]),
                                 sqa.tensor('E2hom',list_act[:4],[]),
                                 sqa.tensor('E2het',list_act[:4],[]),
                                 sqa.tensor('E3'   ,list_act[:6],[]))
  if (cumulantE3):
    sqa.decomp_3rdms_to_2rdms_sf(result, 'E3',
                                 sqa.tensor('E1'    ,list_act[:2],[]),
                                 sqa.tensor('E2'    ,list_act[:4],[]))
  return result


# ====================================================
def write_tensors(Class, tensors,commentE3=False):
# ----------------------------------------------------
    '''HERE
    '''
# ====================================================
    TypeNames   =[t[1] for t in tensors]
    Domains     =[t[2] for t in tensors]
    Usage       =[t[3] for t in tensors]
    if 'AAA' in Class or '3' in Class:
      commentE3=False

    UsageKey = {"A":"USAGE_Amplitude",\
                "R":"USAGE_Residual",\
                "H":"USAGE_Hamiltonian",\
                "D":"USAGE_Density",\
                "I":"USAGE_Intermediate"}

    outString=''
    not_commented=0
    print("namespace "+Class+" {\n")
    for t in range(len(TypeNames)):
      tensor=TypeNames[t]
      if (tensor=="E3" and commentE3):
        intro='//  /*{:3}*/'.format(t)
      else:
        intro='    /*{:3}*/'.format(t)
        not_commented+=1
      outString += intro+'{{"{:8}, "{:10}, "", {:18}}},\n'.format(\
                          tensor+'"',\
                          Domains[t]+'"',\
                          UsageKey[Usage[t]])
    outString = "  FTensorDecl TensorDecls[%i] = {\n"%(not_commented)\
                +outString[:-1]+"\n  };\n"
    print(outString)
    return not_commented


# ====================================================
def write_code(Class, tensors, result, scale=1.0, commentE3=False):
# ----------------------------------------------------
     '''HERE
     '''
# ====================================================
     UniqueNames =[t[0] for t in tensors]
     TypeNames   =[t[1] for t in tensors]
     NamesKey = {}
     for tc in list(zip(UniqueNames, TypeNames)):
       NamesKey[tc[0]] = tc[1]
     if 'AAA' in Class or '3' in Class:
       commentE3=False


     tensor_indices=[]
     middleLine    =[]
     tensor_id     =[]
     description   =[]
     commented     =[]

     # A line is for example:
     # {"abcd,ce,abde",        8.0,   3, { 6, 9, 5}},     //   8.0 Ap[abcd] k[ce] p[abde]
     # ----------------     ------------ ------------   ---------------------------------
     #  tensor_indices         middle     tensor_id              description
     for t in result:
        commented.append(False)

        # tensor_indices
        indices_list = []
        for i in range(len(t.tensors)):
          tensor = t.tensors[i]
          string = ''
          for index in range(len(tensor.indices)):
            string += tensor.indices[index].name
            if (len(tensor.indices[index].name)>1):
              print 'LEGACY'
              exit(1)
              #string += tensor.indices[index].name[-1].capitalize()
          indices_list.append(string)
        indices=''
        for string in indices_list:
          indices += string+','
        tensor_indices.append('{"'+indices[:-1]+'",')

        # numConstant and nbr of tensors
        middleLine.append('{:6}, {:3}, {{'.format(t.numConstant*scale,len(indices_list)))

        # tensor_id and description
        index = 1
        indices=''
        comment ='  //{:6} '.format(t.numConstant*scale)
        for i in range(len(t.tensors)):
          tensor = t.tensors[i]
          if ((tensor.name=="E3" and commentE3) or (tensor.name=="Wvvvv")):
            commented[-1]=True
          indices+= '{:2},'.format(UniqueNames.index(tensor.name))
          comment += NamesKey[tensor.name]+'['+indices_list[index-1]+'] '
          index += 1
        description.append(comment)
        tensor_id.append(indices[:-1]+'}},')

     width1=len(max(tensor_indices, key=len))
     width2=len(max(tensor_id, key=len))
     print("  FEqInfo EqsRes[%i] = {" %(commented.count(False)))
     for i in range(len(tensor_indices)):
       if commented[i]:
         print('//  {:{width1}}{:}{:{width2}}{:}'.format(\
                 tensor_indices[i],middleLine[i],tensor_id[i],description[i],width1=width1,width2=width2))
       else:
         print('    {:{width1}}{:}{:{width2}}{:}'.format(\
                 tensor_indices[i],middleLine[i],tensor_id[i],description[i],width1=width1,width2=width2))
     print("  };\n")

     return commented.count(False)


# ====================================================
def write_tensors_legacy(FullNames, ShortKey, Domains, Usage,commentE3=False):
# ----------------------------------------------------
    '''HERE
    '''
# ====================================================
    UsageKey = {"A":"USAGE_Amplitude",\
                "R":"USAGE_Residual",\
                "H":"USAGE_Hamiltonian",\
                "D":"USAGE_Density",\
                "I":"USAGE_Intermediate"}
    i = 0
    not_commented=0
    outString=''
    for tensor in FullNames:
      if (ShortKey[tensor]=="E3" and commentE3):
        intro='//  /*{:3}*/'.format(i)
      else:
        intro='    /*{:3}*/'.format(i)
        not_commented+=1
      outString += intro+'{{"{:8}, "{:10}, "", {:18}}},\n'\
                  .format(ShortKey[tensor]+'"',\
                          Domains[i]+'"',\
                          UsageKey[Usage[i]])
      i += 1
    outString = "  FTensorDecl TensorDecls[%i] = {\n"%(not_commented)\
                +outString[:-1]+"\n  };\n"

    print(outString)
    return not_commented


# ====================================================
def write_code_legacy(result, tensors):
# ----------------------------------------------------
     '''HERE
     '''
# ====================================================
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
        outString += '    {"CDRS,'
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
     print(outString[:-1]+"\n  };")


# ====================================================
def replaceindex(tensor, a, b) :
# ----------------------------------------------------
    '''HERE
    '''
# ====================================================
    for i in range(len(tensor.indices)):
        if (tensor.indices[i].name == a):
            tensor.indices[i] = b


# ====================================================
def replaceAllKdeltaWithDeltas(term, rdmDelta):
# ----------------------------------------------------
    '''HERE
    '''
# ====================================================
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


# ====================================================
def replaceSingleKdeltaWithDeltas(term, rdmDelta):
# ----------------------------------------------------
    '''HERE
    '''
# ====================================================
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


# ====================================================
def replaceRepeatIndicesWithDeltas(term, rdmDelta):
# ----------------------------------------------------
    '''HERE
    '''
# ====================================================
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


# ====================================================
def printTensor(tensor, keymap):
# ----------------------------------------------------
    '''HERE
    '''
# ====================================================
    string = tensor.name +"["
    for i in range(len(tensor.indices)):
        if (keymap.has_key(tensor.indices[i].name)):
            string += keymap[tensor.indices[i].name]+","
        else:
            string += tensor.indices[i].name+","
    string = string[:-1]+"]"
    return string

# ====================================================
def printIntTensor(tensor, activeInEinsum = False):
# ----------------------------------------------------
    '''HERE
    '''
# ====================================================
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


# ====================================================
def printETensor(tensor, activeInEinsum = False):
# ----------------------------------------------------
    '''HERE
    '''
# ====================================================
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


# ====================================================
def WriteCode_withSuppressActive(result, SupressActive, intmapkey, RDMmapkey, activeInEinsum = False):
# ----------------------------------------------------
    '''HERE
    '''
# ====================================================
    if (SupressActive):
     for t in result:
        #tensorString = ""
        ifstatement = "  if "

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
            outString += ifstatement[:-4]+" : \n  "

        #now print(the einsum string)
        outString += "  Cout +=  ("+ str(t.numConstant)+ ") *numpy.einsum( '"
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
        outString += "   Cout[Vc,Vd,Ar,As] +=  ("+ str(t.numConstant)+ ") *numpy.einsum( '"
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


# ====================================================
def WriteCode_ccaa(result, SupressActive, intmapkey, RDMmapkey, activeInEinsum = False):
# ----------------------------------------------------
    '''HERE
    '''
# ====================================================
    if (SupressActive):
     for t in result:
        #tensorString = ""
        ifstatement = "  if "

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
            outString += ifstatement[:-4]+" : \n  "

        #now print(the einsum string)
        outString += "  Cout +=  ("+ str(t.numConstant)+ ") *numpy.einsum( '"
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
        outString += "   Cout[Vc,Vd,Ar,As] +=  ("+ str(t.numConstant)+ ") *numpy.einsum( '"
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


# ====================================================
def WriteCode_ccav(result, SupressActive, intmapkey, RDMmapkey, activeInEinsum = False):
# ----------------------------------------------------
    '''HERE
    '''
# ====================================================
    if (SupressActive):
     for t in result:
        #tensorString = ""
        ifstatement = "  if "

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
            outString += ifstatement[:-4]+" : \n  "

        #now print(the einsum string)
        outString += "  Cout +=  ("+ str(t.numConstant)+ ") *numpy.einsum( '"
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
        outString += "   Cout[Vc,Vd,Ar,As] +=  ("+ str(t.numConstant)+ ") *numpy.einsum( '"
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

# ====================================================
def WriteCode_caav(result, SupressActive, intmapkey, RDMmapkey, activeInEinsum = False):
# ----------------------------------------------------
    '''HERE
    '''
# ====================================================
    if (SupressActive):
     for t in result:
        #tensorString = ""
        ifstatement = "  if "

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
            outString += ifstatement[:-4]+" : \n  "

        #now print(the einsum string)
        outString += "  Cout +=  ("+ str(t.numConstant)+ ") *numpy.einsum( '"
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

# ====================================================
def WriteCode_lcc(result, FullNames, inputIndices, outIndicesString, commentTensor, inputtensorname="p", outputtensorname="Ap", EquationName="EqsRes", scale=1.0):
# ----------------------------------------------------
     '''HERE
     '''
# ====================================================

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
        commentString = "    //"
        outString += "    {\""
        for indexstring in tensorIndexStringList:
            outString += indexstring+","
        outString = outString[:-1] +"\","
        outString +=" "+ str(t.numConstant*scale)+"  , "+str(len(tensorIndexStringList))+", {"+str(FullNames.index(outputtensorname))
        commentString += outputtensorname+"["+tensorIndexStringList[0]+"] += "+str(t.numConstant*scale)+" "

        index = 1
        for i in range(len(tensorcopy)):
            tensor = tensorcopy[i]
            if(i not in dontprint):
                outString+= ","+ str(FullNames.index(tensor.name))
                commentString += commentTensor[tensor.name]+"["+tensorIndexStringList[index]+"] "
                index += 1
        commentString += inputtensorname+"["+inputIndicesString+"]"
        if (inputtensorname != "") :
            outString += ","+str(FullNames.index(inputtensorname)) +"}},"+commentString+ "\n"
        else:
            outString = outString[:-1]+"}},"+commentString+ "\n"

     print(outString[:-1])


