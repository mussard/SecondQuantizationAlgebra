import secondQuantizationAlgebra as sqa
import geraldCode
import re

domain_of_class={}
domain_of_class['NEVPT_AAAC']='caaa'
domain_of_class['NEVPT_AAAV']='eaaa'
domain_of_class['NEVPT_AAVV']='eeaa'
domain_of_class['NEVPT_ACVV']='eeca'
domain_of_class['NEVPT_CAAV']='cAae'
domain_of_class['NEVPT_CCAA']='ccaa'
domain_of_class['NEVPT_CCAV']='ccae'
domain_of_class['NEVPT_CCVV']='eecc'
domain_of_class['MRLCC_AAAC']='caaa'
domain_of_class['MRLCC_AAAV']='eaaa'
domain_of_class['MRLCC_AAVV']='eeaa'
domain_of_class['MRLCC_ACVV']='eeca'
domain_of_class['MRLCC_CAAV']='cAae'
domain_of_class['MRLCC_CCAA']='ccaa'
domain_of_class['MRLCC_CCAV']='ccae'
domain_of_class['MRLCC_CCVV']='eecc'
domain_of_class['AAAC']='caaa'
domain_of_class['AAAV']='eaaa'
domain_of_class['AAVV']='eeaa'
domain_of_class['ACVV']='eeca'
domain_of_class['CAAV']='cAae'
domain_of_class['CCAA']='ccaa'
domain_of_class['CCAV']='ccae'
domain_of_class['CCVV']='eecc'

# --------------------------------------------------------------
# Library of tensors
def make_tensors(domain,pttype='NEVPT',df=False):
  if pttype=="NEVPT":
    f_or_k="f"
  elif pttype=="MRLCC":
    f_or_k="k"
  tensors  =   [["t",         "t",       domain,      "A"],\
             ["T",         "T",       domain,      "A"],\
             ["b",         "b",       domain,      "A"],\
             ["B",         "B",       domain,      "A"],\
             ["p",         "p",       domain,      "A"],\
             ["Ap",        "Ap",      domain,      "A"],\
             ["P",         "P",       domain,      "A"],\
             ["AP",        "AP",      domain,      "A"],\
             ["R",         "R",       domain,      "R"],\
             ["int1c",     f_or_k,    "cc",        "H"],\
             ["int1a",     f_or_k,    "aa",        "H"],\
             ["int1v",     f_or_k,    "ee",        "H"],\
             ["fea",       "f",       "ea",        "H"],\
             ["fca",       "f",       "ca",        "H"],\
             ["fec",       "f",       "ec",        "H"],\
             ["E1",        "E1",      "aa",        "D"],\
             ["E2",        "E2",      "aaaa",      "D"],\
             ["E3",        "E3",      "aaaaaa",    "D"],\
             ["E4",        "E4",      "aaaaaaaa",  "D"],\
             ["deltac",    "delta",   "cc",        "D"],\
             ["deltaa",    "delta",   "aa",        "D"],\
             ["deltav",    "delta",   "ee",        "D"],\
            ]
  if (not df):
    tensors+=  [
             ["int2ca1",   "W",       "caca",      "H"],\
             ["int2ca2",   "W",       "caac",      "H"],\
             ["int2cv1",   "W",       "cece",      "H"],\
             ["int2cv2",   "W",       "ceec",      "H"],\
             ["int2av1",   "W",       "aeae",      "H"],\
             ["int2av2",   "W",       "aeea",      "H"],\
             ["int2c",     "W",       "cccc",      "H"],\
             ["int2a",     "W",       "aaaa",      "H"],\
             ["int2v",     "W",       "e",         "I"],\
            ]
  if (not df and domain=='cAae'):
    tensors+=  [
             ['V1',        'W',       'eaca',       'H'],
             ['V2',        'W',       'aeca',       'H'],
            ]
  if (not df and not domain=='cAae'):
    tensors+=  [
             ["V",         "W",       domain,      "H"],\
            ]
  if (df):
    tensors+=  [
             ["int2Lcc",   "W",       "Lcc",       "H"],\
             ["int2Laa",   "W",       "Laa",       "H"],\
             ["int2Lvv",   "W",       "Lee",       "H"],\
             ["int2Lca",   "W",       "Lca",       "H"],\
             ["int2Lac",   "W",       "Lac",       "H"],\
             ["int2Lcv",   "W",       "Lce",       "H"],\
             ["int2Lvc",   "W",       "Lec",       "H"],\
             ["int2Lva",   "W",       "Lea",       "H"],\
             ["int2Lav",   "W",       "Lae",       "H"],\
            ]
  if (df and domain=='cAae'):
    tensors+=  [
             ["int2Lvc",   "W",       "Lec",       "H"],\
             ["int2Laa",   "W",       "Laa",       "H"],\
             ["int2Lac",   "W",       "Lac",       "H"],\
             ["int2Lva",   "W",       "Lea",       "H"],\
            ]
  if (df and not domain=='cAae'):
    dleft ='L'+domain[0]+domain[2]
    dright='L'+domain[1]+domain[3]
    nameleft =re.sub("e","v","int2"+dleft)
    nameright=re.sub("e","v","int2"+dright)
    tensors+=  [
             [nameleft,    "W",       dleft,       "H"],\
             [nameright,   "W",       dright,      "H"],\
            ]
  return tensors


# --------------------------------------------------------------
# Prepare a list of the actually useful tensors
def write_tensors_and_equations(Class,result,tensors,commentE3=False,df=False):
  if 'AAA' in Class or '3' in Class:
    commentE3=False

  names=[tensors[index][0] for index in range(len(tensors))]
  selectA=[]
  selectH=[]
  selectD=[]
  selection=[]
# the residual
  if "R" in names:
    selection.append(names.index("R"))
# all the amplitudes
  for i in range(len(tensors)):
    if tensors[i][3]=="A":
      selectA.append(i)
# the tensors needed by the equations
  for t in result:
    for i in t.tensors:
      try:
        index=names.index(i.name)
      except:
        newlist=[i.name, i.name[:2], i.name[2:].replace('v','e'), 'A']
        selectA.append(len(tensors))
        names.append(i.name)
        index=len(tensors)
        tensors=tensors+[newlist]

      if tensors[index][3]=="D":
        if index not in selectD:
          selectD.append(index)
      elif tensors[index][3]=="H" or tensors[index][3]=="I":
        if index not in selectH:
          selectH.append(index)
      elif tensors[index][3]=="A" or tensors[index][3]=="R":
        if index not in selectA:
          selectA.append(index)
      else:
        print('None of D/H/I/A/R? (in "needed_by_equation")')
        print(tensors[index])
        exit()
# all the overlaps S and all the coefficients D
  for i in range(len(tensors)):
    if re.search('^S',tensors[i][0]):
      if i not in selectD:
        selectD.append(i)
    if re.search('^D',tensors[i][0]):
      if i not in selectH:
        selectH.append(i)
# the manual additions
  addition  = manual(Class,df=df)
  for add in addition:
    index=names.index(add)
    if tensors[index][3]=="D":
      if index not in selectD:
        selectD.append(index)
    elif tensors[index][3]=="H":
      if index not in selectH:
        selectH.append(index)
    elif tensors[index][3]=="A":
      if index not in selectA:
        selectA.append(index)
    else:
      print('None of D/H/A? (in "manual_additions")')
      print(tensors[index])
      exit()
# sort by name
  namesA=[names[i] for i in selectA]
  namesH=sorted([names[i] for i in selectH], key=lambda s: s.lower())
  namesD=sorted([names[i] for i in selectD], key=lambda s: s.lower())
  sorted_names=namesA+namesH+namesD
  selection+=[names.index(name) for name in sorted_names if name is not "E3" and name is not "E4"]
  if "E3" in sorted_names:
    selection+=[names.index("E3")]
  if "E4" in sorted_names:
    selection+=[names.index("E4")]

  AllTensors=    [tensors[index2][0] for index2 in selection]
  CommentTensors=[tensors[index2][1] for index2 in selection]
  Domains=       [tensors[index2][2] for index2 in selection]
  Usage=         [tensors[index2][3] for index2 in selection]
  CommentKey = {}
  for tc in list(zip(AllTensors, CommentTensors)):
      CommentKey[tc[0]] = tc[1]

  # Write out the tensors
  print("namespace "+Class+" {\n")
  nbrTensors=geraldCode.writeTensors(AllTensors, CommentKey, Domains, Usage,commentE3=commentE3)

  # Write out the equation for A.p
  nbrEqs=geraldCode.WriteCodeSimple(result, AllTensors, CommentKey,commentE3=commentE3)

  return AllTensors,nbrTensors,nbrEqs



# --------------------------------------------------------------
# The list to manually add to the tensors (the ones needed by bVec)
def manual(Class,df=False):
  if ('AAAC' in Class):
    manual_list=['b','V','deltaa','fca','E1','E2','E3']
  if ('AAAV' in Class):
    manual_list=['b','V','deltaa','fea','E1','E2','E3']
  if ('AAVV' in Class):
    manual_list=['b','V','E2']
  if ('ACVV' in Class):
    manual_list=['b','V','E1']
  if ('CAAV' in Class):
    manual_list=['b1','b2','V1','V2','E1','E2','fec','deltaa']
  if ('CCAA' in Class):
    manual_list=['b','V','deltaa','E1','E2','S1','S2']
  if ('CCAV' in Class):
    manual_list=['b','V','E1','deltaa']
  if ('CCVV' in Class):
    manual_list=['b','V','deltac']
  if ('MRLCC3' in Class):
    manual_list=['fea','fca','fec']

  if ('MRLCC3' in Class and not df):
    manual_list.append('Wcaav1')
  if ('NEVPT3' in Class):
    manual_list=['fea','fca','fec']

  if (df and not '3' in Class):
    try:
      position=manual_list.index('V')
      dleft ='L'+domain_of_class[Class][0]+domain_of_class[Class][2]
      dright='L'+domain_of_class[Class][1]+domain_of_class[Class][3]
      nameleft =re.sub("e","v","int2"+dleft)
      nameright=re.sub("e","v","int2"+dright)
      manual_list=manual_list[:position]+[nameleft,nameright]+manual_list[position+1:]
    except:
      position=manual_list.index('V1')
      manual_list=manual_list[:position]+['int2Lvc','int2Laa','int2Lac','int2Lva']+manual_list[position+2:]

  return manual_list


# --------------------------------------------------------------
# Write out the bVec informations
def bVec(Class,AllTensors,df=False):
  bindex  = AllTensors.index('b')
  try:
    Vindex  = AllTensors.index('V')
  except:
    Vindex =-1
  try:
    V1index = AllTensors.index('V1')
    V2index = AllTensors.index('V2')
  except:
    V1index=-2
    V2index=-3

  if (Class=='AAAC'):
    E1index = AllTensors.index('E1')
    E2index = AllTensors.index('E2')
    E3index = AllTensors.index('E3')
    bVec_lines=[
      ["ABCE,ABCD,ED",      2.0, 3, '%2i,%2i,%2i'%(bindex, Vindex, E1index), '//  2.0 b[abce] V[abcd] E1[ed]'    ],\
      ["ACBE,ABCD,ED",     -1.0, 3, '%2i,%2i,%2i'%(bindex, Vindex, E1index), '// -1.0 b[acbe] V[abcd] E1[ed]'    ],\
      ["ABEF,ABCD,CFED",   -1.0, 3, '%2i,%2i,%2i'%(bindex, Vindex, E2index), '// -1.0 b[abef] V[abcd] E2[cfed]'  ],\
      ["ACEF,ABCD,BFDE",   -1.0, 3, '%2i,%2i,%2i'%(bindex, Vindex, E2index), '// -1.0 b[acef] V[abcd] E2[bfde]'  ],\
      ["AEBF,ABCD,CFDE",   -1.0, 3, '%2i,%2i,%2i'%(bindex, Vindex, E2index), '// -1.0 b[aebf] V[abcd] E2[cfde]'  ],\
      ["AECF,ABCD,BFDE",    2.0, 3, '%2i,%2i,%2i'%(bindex, Vindex, E2index), '//  2.0 b[aecf] V[abcd] E2[bfde]'  ],\
      ["AEFG,ABCD,BCGDFE", -1.0, 3, '%2i,%2i,%2i'%(bindex, Vindex, E3index), '// -1.0 b[aefg] V[abcd] E3[bcgdfe]'],\
    ]

  if (Class=='AAAV'):
    daindex = AllTensors.index('deltaa')
    E1index = AllTensors.index('E1')
    E2index = AllTensors.index('E2')
    E3index = AllTensors.index('E3')
    bVec_lines=[
      ["AUVW,APQR,WR,QP,VU",  1.0, 5, '%2i,%2i,%2i,%2i,%2i'%(bindex, Vindex, E1index, daindex, daindex) , '// 1.0 b[auvw] V[apqr] E1[wr] delta[qp] delta[vu]' ],\
      ["AUVW,APQR,VWRU,QP",   1.0, 4, '%2i,%2i,%2i,%2i'    %(bindex, Vindex, E2index, daindex)          , '// 1.0 b[auvw] V[apqr] E2[vwru] delta[qp]'         ],\
      ["AUVW,APQR,VWQR,PU",   1.0, 4, '%2i,%2i,%2i,%2i'    %(bindex, Vindex, E2index, daindex)          , '// 1.0 b[auvw] V[apqr] E2[vwqr] delta[pu]'         ],\
      ["AUVW,APQR,PWRQ,VU",   1.0, 4, '%2i,%2i,%2i,%2i'    %(bindex, Vindex, E2index, daindex)          , '// 1.0 b[auvw] V[apqr] E2[pwrq] delta[vu]'         ],\
      ["AUVW,APQR,PVWRQU",    1.0, 3, '%2i,%2i,%2i'        %(bindex, Vindex, E3index)                   , '// 1.0 b[auvw] V[apqr] E3[pvwrqu]'                 ],\
    ]

  if (Class=='AAVV'):
    E2index = AllTensors.index('E2')
    bVec_lines=[
      ["ABRS,ABPQ,RSPQ", 0.25, 3, '%2i,%2i,%2i'%(bindex, Vindex, E2index), '// 0.5 b[ABRS] V[ABPQ] E2[RSPQ]'],\
      ["BARS,ABPQ,RSQP", 0.25, 3, '%2i,%2i,%2i'%(bindex, Vindex, E2index), '// 0.5 b[BARS] V[ABPQ] E2[RSQP]'],\
      ["ABRS,BAPQ,RSQP", 0.25, 3, '%2i,%2i,%2i'%(bindex, Vindex, E2index), '// 0.5 b[ABRS] V[BAPQ] E2[RSQP]'],\
      ["BARS,BAPQ,RSPQ", 0.25, 3, '%2i,%2i,%2i'%(bindex, Vindex, E2index), '// 0.5 b[BARS] V[BAPQ] E2[RSPQ]'],\
    ]

  if (Class=='ACVV'):
    E1index = AllTensors.index('E1')
    bVec_lines=[
      ["ABIP,RP,ABIR",  2.0, 3, '%2i,%2i,%2i'%(bindex, E1index, Vindex), '//  2.0 b[ABIP] E1[RP] V[ABIR]'],\
      ["ABIP,RP,BAIR", -1.0, 3, '%2i,%2i,%2i'%(bindex, E1index, Vindex), '// -1.0 b[ABIP] E1[RP] V[BAIR]'],\
    ]

  if (Class=='CAAV'):
    b1index = AllTensors.index('b1')
    b2index = AllTensors.index('b2')
    E1index = AllTensors.index('E1')
    E2index = AllTensors.index('E2')
    bVec_lines=[
      ["IPQA,RQSP,ARIS",  2.0, 3, '%2i,%2i,%2i'%(b1index, E2index, V1index), '//  2.0 b1[IPQA] E2[RQSP]           V1[ARIS]'],\
      ["IPQA,SQ,APIS",    2.0, 3, '%2i,%2i,%2i'%(b1index, E1index, V1index), '//  2.0 b1[IPQA] E1[SQ]   delta[PR] V1[ARIS]'],\
      ["IPQA,RQSP,RAIS", -1.0, 3, '%2i,%2i,%2i'%(b1index, E2index, V2index), '// -1.0 b1[IPQA] E2[RQSP]           V2[RAIS]'],\
      ["IPQA,SQ,PAIS",   -1.0, 3, '%2i,%2i,%2i'%(b1index, E1index, V2index), '// -1.0 b1[IPQA] E1[SQ]   delta[PR] V2[RAIS]'],\
      ["IPQA,RQSP,ARIS", -1.0, 3, '%2i,%2i,%2i'%(b2index, E2index, V1index), '// -1.0 b2[IPQA] E2[RQSP]           V1[ARIS]'],\
      ["IPQA,SQ,APIS",   -1.0, 3, '%2i,%2i,%2i'%(b2index, E1index, V1index), '// -1.0 b2[IPQA] E1[SQ]   delta[PR] V1[ARIS]'],\
      ["IPQA,RQPS,RAIS", -1.0, 3, '%2i,%2i,%2i'%(b2index, E2index, V2index), '// -1.0 b2[IPQA] E2[RQPS]           V2[RAIS]'],\
      ["IPQA,SQ,PAIS",    2.0, 3, '%2i,%2i,%2i'%(b2index, E1index, V2index), '//  2.0 b2[IPQA] E1[SQ]   delta[PR] V2[RAIS]'],\
    ]

  if (Class=='CCAA'):
    daindex = AllTensors.index('deltaa')
    E1index = AllTensors.index('E1')
    E2index = AllTensors.index('E2')
    bVec_lines=[
      ["KLRS,PR,KLPS",    2.0, 3, '%2i,%2i,%2i'%(bindex,daindex,Vindex), '//  2.0 b[KLRS] delta[PR] delta[QS] V[KLPQ]'],\
      ["KLRS,PS,KLPR",   -1.0, 3, '%2i,%2i,%2i'%(bindex,daindex,Vindex), '// -1.0 b[KLRS] delta[PS] delta[QR] V[KLPQ]'],\
      ["KLRS,QS,KLRQ",   -1.0, 3, '%2i,%2i,%2i'%(bindex,E1index,Vindex), '// -1.0 b[KLRS] E1[QS]    delta[PR] V[KLPQ]'],\
      ["KLRS,QR,KLSQ",    0.5, 3, '%2i,%2i,%2i'%(bindex,E1index,Vindex), '//  0.5 b[KLRS] E1[QR]    delta[PS] V[KLPQ]'],\
      ["KLRS,PS,KLPR",    0.5, 3, '%2i,%2i,%2i'%(bindex,E1index,Vindex), '//  0.5 b[KLRS] E1[PS]    delta[QR] V[KLPQ]'],\
      ["KLRS,PR,KLPS",   -1.0, 3, '%2i,%2i,%2i'%(bindex,E1index,Vindex), '// -1.0 b[KLRS] E1[PR]    delta[QS] V[KLPQ]'],\
      ["KLRS,PQRS,KLPQ",  0.5, 3, '%2i,%2i,%2i'%(bindex,E2index,Vindex), '//  0.5 b[KLRS] E2[PQRS]            V[KLPQ]'],\
      ["KLRS,PS,LKPR",    2.0, 3, '%2i,%2i,%2i'%(bindex,daindex,Vindex), '//  2.0 b[KLRS] delta[PS] delta[QR] V[LKPQ]'],\
      ["KLRS,PR,LKPS",   -1.0, 3, '%2i,%2i,%2i'%(bindex,daindex,Vindex), '// -1.0 b[KLRS] delta[PR] delta[QS] V[LKPQ]'],\
      ["KLRS,QR,LKSQ",   -1.0, 3, '%2i,%2i,%2i'%(bindex,E1index,Vindex), '// -1.0 b[KLRS] E1[QR]    delta[PS] V[LKPQ]'],\
      ["KLRS,QS,LKRQ",    0.5, 3, '%2i,%2i,%2i'%(bindex,E1index,Vindex), '//  0.5 b[KLRS] E1[QS]    delta[PR] V[LKPQ]'],\
      ["KLRS,PR,LKPS",    0.5, 3, '%2i,%2i,%2i'%(bindex,E1index,Vindex), '//  0.5 b[KLRS] E1[PR]    delta[QS] V[LKPQ]'],\
      ["KLRS,PS,LKPR",   -1.0, 3, '%2i,%2i,%2i'%(bindex,E1index,Vindex), '// -1.0 b[KLRS] E1[PS]    delta[QR] V[LKPQ]'],\
      ["KLRS,PQSR,LKPQ",  0.5, 3, '%2i,%2i,%2i'%(bindex,E2index,Vindex), '//  0.5 b[KLRS] E2[PQSR]            V[LKPQ]'],\
     #'  FEqInfo MakeS1[0] = {',\
     #'        //  {"PQRS,PR,QS",     4.0  , 3, {%i,%i,%i}}, //S1[PQRS] +=  4.0 delta[PR] delta[QS]' %(S1index,daindex,daindex),\
     #'        //  {"PQRS,PS,QR",    -2.0  , 3, {%i,%i,%i}}, //S1[PQRS] += -2.0 delta[PS] delta[QR]' %(S1index,daindex,daindex),\
     #'        //  {"PQRS,QS,PR",    -2.0  , 3, {%i,%i,%i}}, //S1[PQRS] += -2.0 E1[QS]    delta[PR]' %(S1index,E1index,daindex),\
     #'        //  {"PQRS,QR,PS",     1.0  , 3, {%i,%i,%i}}, //S1[PQRS] +=  1.0 E1[QR]    delta[PS]' %(S1index,E1index,daindex),\
     #'        //  {"PQRS,PS,QR",     1.0  , 3, {%i,%i,%i}}, //S1[PQRS] +=  1.0 E1[PS]    delta[QR]' %(S1index,E1index,daindex),\
     #'        //  {"PQRS,PR,QS",    -2.0  , 3, {%i,%i,%i}}, //S1[PQRS] += -2.0 E1[PR]    delta[QS]' %(S1index,E1index,daindex),\
     #'        //  {"PQRS,PQRT,TS",   1.0  , 3, {%i,%i,%i}}, //S1[PQRS] +=  1.0 E2[PQRS]'            %(S1index,E2index,daindex),\
     #'        //  {"PQRS,PR,QS",     2.0  , 3, {%i,%i,%i}}, //S2[PQRS] +=  2.0 delta[PR] delta[QS]' %(S2index,daindex,daindex),\
     #'        //  {"PQRS,PS,QR",     2.0  , 3, {%i,%i,%i}}, //S2[PQRS] +=  2.0 delta[PS] delta[QR]' %(S2index,daindex,daindex),\
     #'        //  {"PQRS,QS,PR",    -1.0  , 3, {%i,%i,%i}}, //S2[PQRS] += -1.0 E1[QS]    delta[PR]' %(S2index,E1index,daindex),\
     #'        //  {"PQRS,QR,PS",    -1.0  , 3, {%i,%i,%i}}, //S2[PQRS] += -1.0 E1[QR]    delta[PS]' %(S2index,E1index,daindex),\
     #'        //  {"PQRS,PS,QR",    -1.0  , 3, {%i,%i,%i}}, //S2[PQRS] += -1.0 E1[PS]    delta[QR]' %(S2index,E1index,daindex),\
     #'        //  {"PQRS,PR,QS",    -1.0  , 3, {%i,%i,%i}}, //S2[PQRS] += -1.0 E1[PR]    delta[QS]' %(S2index,E1index,daindex),\
     #'        //  {"PQRS,PQRT,TS",   1.0  , 3, {%i,%i,%i}}, //S2[PQRS] +=  1.0 E2[PQRS]'            %(S2index,E2index,daindex),\
     #'        //  {"PQRS,PQTR,TS",   1.0  , 3, {%i,%i,%i}}, //S2[PQRS] +=  1.0 E2[PQSR]'            %(S2index,E2index,daindex),\
     #'  };',\
    ]

  if (Class=='CCAV'):
    E1index = AllTensors.index('E1')
    Dindex  = AllTensors.index('deltaa')
    bVec_lines=[
      ["IJPA,RP,IJRA",  4.0, 3, '%2i,%2i,%2i'%(bindex, Dindex, Vindex), '//  4.0 b[IJPA] delta[RP] V[IJRA]'],\
      ["IJPA,RP,IJRA", -2.0, 3, '%2i,%2i,%2i'%(bindex, E1index,Vindex), '// -2.0 b[IJPA] E1[RP]    V[IJRA]'],\
      ["IJPA,RP,JIRA", -2.0, 3, '%2i,%2i,%2i'%(bindex, Dindex, Vindex), '// -2.0 b[IJPA] delta[RP] V[JIRA]'],\
      ["IJPA,RP,JIRA",  1.0, 3, '%2i,%2i,%2i'%(bindex, E1index,Vindex), '//  1.0 b[IJPA] E1[RP]    V[JIRA]'],\
    ]

  if (Class=='CCVV'):
    dcindex = AllTensors.index('deltac')
    bVec_lines=[
      ["CDKL,LM,CDKM",  2.0, 3, '%2i,%2i,%2i'%(bindex, dcindex, Vindex), '//  2.0 b[CDKL] deltac[LM] V[CDKM]'],\
      ["CDKL,LM,DCKM", -1.0, 3, '%2i,%2i,%2i'%(bindex, dcindex, Vindex), '// -1.0 b[CDKL] deltac[LM] V[DCKM]'],\
      ["CDKL,LM,CDMK", -1.0, 3, '%2i,%2i,%2i'%(bindex, dcindex, Vindex), '// -1.0 b[CDKL] deltac[LM] V[CDMK]'],\
      ["CDKL,LM,DCMK",  2.0, 3, '%2i,%2i,%2i'%(bindex, dcindex, Vindex), '//  2.0 b[CDKL] deltac[LM] V[DCMK]'],\
    ]



  convert_bVec_to_df(bVec_lines,Class,AllTensors,df)

  bVec_size=len(bVec_lines)
  print('  FEqInfo bVec['+str(bVec_size)+'] = {')
  width1=len(max([bVec_lines[i][0] for i in range(len(bVec_lines))],key=len))+1
  width2=  3*max([bVec_lines[i][2] for i in range(len(bVec_lines))])
  for line in bVec_lines:
    print('    {{"{:{width1}},{:6},{:4}, {{{:{width2}}}}, {:}'.format(line[0]+'"',line[1],line[2],line[3]+'}',line[4],width1=width1,width2=width2))
  print('  };\n')

  if (Class=='ACVV' or Class=='CAAV' or Class=='CCAV'):
    # Write out the Domains information
    print('  int f(int i) {')
    print('    return 2*i;')
    print('  }')
    print('  FDomainDecl DomainDecls[1] = {')
    print('    {"A", "a", f}')
    print('  };\n')

  return bVec_size


def convert_bVec_to_df(bVec_lines,Class,AllTensors,df=False):
  if (df):
    try:
      dleft ='L'+domain_of_class[Class][0]+domain_of_class[Class][2]
      dright='L'+domain_of_class[Class][1]+domain_of_class[Class][3]
      nameleft =re.sub("e","v","int2"+dleft)
      nameright=re.sub("e","v","int2"+dright)
      Vl =str(AllTensors.index(nameleft))
      Vr =str(AllTensors.index(nameright))
    except:
      Vl =-1
      Vr =-1
    try:
      V1l=str(AllTensors.index('int2Lvc'))
      V1r=str(AllTensors.index('int2Laa'))
      V2l=str(AllTensors.index('int2Lac'))
      V2r=str(AllTensors.index('int2Lva'))
    except:
      V1l=-1
      V1r=-1
      V2l=-1
      V2r=-1

    for i in range(len(bVec_lines)):
      line=bVec_lines[i]

      # find position of V
      liste=line[3].strip().split(',')
      position=-1
      for j in range(len(liste)):
        if int(liste[j])==-1:
          position=j
          From=liste[position]
          To  ='%s,%s'%(Vl,Vr)
        elif int(liste[j])==-2:
          position=j
          From=liste[position]
          To  ='%s,%s'%(V1l,V1r)
        elif int(liste[j])==-3:
          position=j
          From=liste[position]
          To  ='%s,%s'%(V2l,V2r)

      if position!=-1:
        # replace V by Vl,Vr
        line[3]=re.sub(From,To,line[3])

        # replace the indexes
        if 'l' not in line[0]:
          aux='l'
        elif 'L' not in line[0]:
          aux='L'
        else:
          print('both l/L in the string')
          exit()
        liste=line[0].strip().split(',')
        From=liste[position]
        To  =aux+From[0]+From[2]+','+aux+From[1]+From[3]
        line[0]=re.sub(From,To,line[0])

        # put the nbr of tensors
        line[2]=line[2]+1

        bVec_lines[i]=line

