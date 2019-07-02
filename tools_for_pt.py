#
# ==================================================
#    TOOLS FOR Second Quantization Algebra (sqa)
# ==================================================
#   This is meant to be a layer of front-end tools
#         to facilitate the derivation of PT
# ==================================================
#
#
# (Tensors have UniqueNames, TypeNames, Domains and Usage)
#
from tools_for_sqa import *
import re


# ====================================================
def h0(h0,df=False):
# ----------------------------------------------------
  '''
  '''
# ====================================================
  if h0=="MRLCC":
    exop=["cc","aa","vv",\
          "aaaa","cccc","vvvv",\
          "caca","caac",\
          "cvcv","cvvc",\
          "avav","avva"]
    factor=[1.,1.,1.,\
            .5,.5,.5,\
            1.,1.,\
            1.,1.,\
            1.,1.]
  elif h0=="NEVPT":
    exop=["cc","aa","vv","aaaa"]
    factor=[1.,1.,1.,.5]
  else:
    print("Only have NEVPT and MRLCC h0s")
    exit(1)

  H=[]
  for i in range(len(exop)):
    list=gimme(exop[i])
    if len(list)==2:
      H.append(sqa.term(factor[i], [""],\
              [sqa.tensor("W"+exop[i],list,symm(list)), sqa.sfExOp(list)]))
    elif (not df):
      H.append(sqa.term(factor[i], [""],\
              [sqa.tensor("W"+exop[i],list,symm(list)), sqa.sfExOp(list)]))
    elif (df):
      L=gimme("L")[0]
      left =[L,list[0],list[2]]
      right=[L,list[1],list[3]]
      nameL="L"+exop[i][0]+exop[i][2]
      nameR="L"+exop[i][1]+exop[i][3]
      H.append(sqa.term(factor[i], [""],\
              [sqa.tensor("W"+nameL,left ,symm(left )),\
               sqa.tensor("W"+nameR,right,symm(right)),\
               sqa.sfExOp(list)]))
  #for t in H:
  #    print t
  return H



# ====================================================
def common_tensors(result,domain,pttype="NEVPT",df=False):
# ----------------------------------------------------
  '''
  '''
# ====================================================
  if pttype=="NEVPT":
    f_or_k="f"
  elif pttype=="MRLCC":
    f_or_k="k"

  tensors=[]
  for r in result:
    for t in r.tensors:
      name=t.name
      if name not in [elt[0] for elt in tensors]:
        if re.search(r'^Wvvvv$',name):
          tensors.append([name,'W'    ,'e'                          ,'I'])
        elif re.search(r'^W....$',name):
          tensors.append([name,'W'    ,name[1:].replace('v','e')    ,'H'])
        elif re.search(r'^W...$',name):
          tensors.append([name,'W'    ,name[1:].replace('v','e')    ,'H'])
        elif re.search(r'^W..$',name):
          tensors.append([name,f_or_k ,name[1:].replace('v','e')    ,'H'])
        elif re.search(r'^delta',name):
          tensors.append([name,'delta',(name[-1]*2).replace('v','e'),'D'])
        elif re.search(r'^E[0-9]$',name):
          tensors.append([name,name   ,'a'*2*int(name[-1])          ,'D'])
        elif re.search('E2hom',name) or re.search('E2het',name):
          tensors.append([name,name   ,'aaaa'                       ,'D'])
        elif re.search(r'^Ap',name) or re.search(r'^p',name):
          continue
        else:
          print '?????',name

  # Prepare Amplitudes and common tensors
  tensors+=  [["t",       "t",  domain,   "A"],
              ["T",       "T",  domain,   "A"],
              ["b",       "b",  domain,   "A"],
              ["B",       "B",  domain,   "A"],
              ["p",       "p",  domain,   "A"],
              ["Ap",      "Ap", domain,   "A"],
              ["P",       "P",  domain,   "A"],
              ["AP",      "AP", domain,   "A"],
              ["R",       "R",  domain,   "R"]]
  if (domain=="cAae"):
    tensors+=[["p1",      "p1", "caae",   "A"],
              ["p2",      "p2", "caae",   "A"],
              ["Ap1",    "Ap1", "caae",   "A"],
              ["Ap2",    "Ap2", "caae",   "A"],
              ["b1",      "b1", "caae",   "A"],
              ["b2",      "b2", "caae",   "A"],
              ["B1",      "B1", "caae",   "A"],
              ["B2",      "B2", "caae",   "A"]]

  # Prepare overlaps
  if (domain=="caaa"):
    tensors+=[["S1",      "S1", "aaaaaa", "D"]]
  if (domain=="eaaa"):
    tensors+=[["S1",      "S1", "aaaaaa", "D"]]
  if (domain=="eeaa"):
    tensors+=[["S1",      "S1", "aaaa",   "D"],\
              ["S2",      "S2", "aaaa",   "D"]]
  if (domain=="eeca"):
    tensors+=[["S1",      "S1", "AA",     "D"],\
              ["S2",      "S2", "aa",     "D"]]
  if (domain=="cAae"):
    tensors+=[["S1",      "S1", "AaAa",   "D"]]
  if (domain=="ccaa"):
    tensors+=[["S1",      "S1", "aaaa",   "D"],\
              ["S2",      "S2", "aaaa",   "D"]]
  if (domain=="ccae"):
    tensors+=[["S1",      "S1", "AA",     "D"],\
              ["S2",      "S2", "aa",     "D"]]

  ## Prepare main "W" tensors
  if (not df) and (not domain=="cAae"):
    tensors+=[["W",       "W",  domain,   "H"]]
  if (not df) and (domain=="cAae"):
    tensors+=[["W1",      "W",  "eaca",   "H"],
              ["W2",      "W",  "aeca",   "H"]]
  if (df) and (domain=="cAae"):
    tensors+=[["WLvc",    "W",  "Lec",    "H"],
              ["WLaa",    "W",  "Laa",    "H"],
              ["WLac",    "W",  "Lac",    "H"],
              ["WLva",    "W",  "Lea",    "H"]]
  if (df) and (domain!="cAae"):
    dleft ="L"+domain[0]+domain[2]
    dright="L"+domain[1]+domain[3]
    nameleft =re.sub("e","v","W"+dleft)
    nameright=re.sub("e","v","W"+dright)
    tensors+=[[nameleft,  "W",  dleft,    "H"],
              [nameright, "W",  dright,   "H"]]

  # the tensors needed by bvec
  tensors+=for_bvec(domain,df=df)

  return tensors


# ====================================================
def order_tensors(tensors):
# ----------------------------------------------------
  ''' Order the list of tensors
  '''
# ====================================================
  # sort by name
  names=[tensors[index][0] for index in range(len(tensors))]
  selectR=[i for i in range(len(tensors)) if tensors[i][-1]=='R']
  selectA=[i for i in range(len(tensors)) if tensors[i][-1]=='A']
  selectH=[i for i in range(len(tensors)) if tensors[i][-1]=='H' or tensors[i][-1]=='I']
  selectD=[i for i in range(len(tensors)) if tensors[i][-1]=='D']
  namesR=[names[i] for i in selectR]
  namesA=[names[i] for i in selectA]
  namesH=sorted(list(set([names[i] for i in selectH])), key=lambda s: s.lower())
  namesD=sorted(list(set([names[i] for i in selectD])), key=lambda s: s.lower())
  sorted_names=namesR+namesA+namesH+namesD
  selection=[names.index(name) for name in sorted_names if name!='E3' and name!='E4']
  if "E3" in sorted_names:
    selection+=[names.index("E3")]
  if "E4" in sorted_names:
    selection+=[names.index("E4")]

  return [tensors[i] for i in selection]

# ====================================================
def for_bvec(domain,df=False):
# ----------------------------------------------------
  ''' Add to the tensors the ones needed by bVec
  '''
# ====================================================
  list=[]
  if ('caaa'==domain):
    list=[["fca","f","ca","H"],
          ["deltaa","delta","aa","D"]]
  if ('eaaa'==domain):
    list=[["fea","f","ea","H"]]
  if ('cAae'==domain):
    list=[["fec","f","ec","H"],
          ["deltaa","delta","aa","D"]]
  if ('eecc'==domain):
    list=[['deltac','delta','cc','D']]
  if ('ccaa'==domain):
    list=[['deltaa','delta','aa','D']]
  if ('ccae'==domain):
    list=[['deltaa','delta','aa','D']]

  return list


def pt3_tensors(result,pttype):
  if pttype=="NEVPT":
    f_or_k="f"
  elif pttype=="MRLCC":
    f_or_k="k"

  Atensor=[]
  Wtensor=[]
  kftensor=[]
  resttensor=[]
  for t in result:
    for i in t.tensors:
      if i.name not in [this[0] for this in Atensor]:
        if i.name[0]=='A':
          Atensor.append(   [i.name, i.name[:2], i.name[2:].replace('v','e'),   'A'])
          name='W'+i.name[2:]
          if len(i.name)!=4   and name not in [this[0] for this in Wtensor]:
            Wtensor.append( [name,   'W',        i.name[2:].replace('v','e'),   'A'])
          elif len(i.name)==4 and name not in [this[0] for this in kftensor]:
            kftensor.append([name,   f_or_k,     i.name[2:].replace('v','e'),   'A'])
      if i.name not in [this[0] for this in Wtensor]:
        if i.name[0]=='W' and len(i.name)!=3:
          Wtensor.append(   [i.name, 'W',        i.name[1:].replace('v','e'),   'A'])
      if i.name not in [this[0] for this in kftensor]:
        if i.name[0]=='W' and len(i.name)==3:
          kftensor.append(  [i.name, f_or_k,     i.name[1:].replace('v','e'),   'A'])
      if i.name not in [this[0] for this in resttensor]:
        if i.name[0]=='D':
          resttensor.append([i.name, 'D',        i.name[1:].replace('v','e'),   'H'])
        elif i.name=='E2hom' or i.name=='E2het':
          resttensor.append([i.name, i.name,     'aaaa'               ,         'D'])
        elif i.name[0]=='E':
          resttensor.append([i.name, i.name,     'a'*2*int(i.name[-1]),         'D'])
        elif i.name[:5]=='delta':
          resttensor.append([i.name, 'delta',    i.name[-1].replace('v','e')*2, 'D'])
  sort_indA=sorted(xrange(len(Atensor)),    key=lambda ix: Atensor[ix][0])
  sort_indW=sorted(xrange(len(Wtensor)),    key=lambda ix: Wtensor[ix][0])
  sort_ind2=sorted(xrange(len(kftensor)),   key=lambda ix: kftensor[ix][0])
  sort_rest=sorted(xrange(len(resttensor)), key=lambda ix: resttensor[ix][0])
  tensors=[Atensor[i]    for i in sort_indA]+\
          [Wtensor[i]    for i in sort_indW]+\
          [kftensor[i]   for i in sort_ind2]+\
          [resttensor[i] for i in sort_rest]
         #[['Dvvcc',     'D',       'eecc',       'H'], # I    OK
         # ['Dvvca',     'D',       'eeca',       'H'], # II   OK
         # ['Dccav',     'D',       'ccae',       'H'], # III  OK
         # ['Dvvaa',     'D',       'eeaa',       'H'], # IV   OK
         # ['Dccaa',     'D',       'ccaa',       'H'], # V    OK
         # ['Dvaca',     'D',       'eaca',       'H'], # VI   ?
         # ['Davca',     'D',       'aeca',       'H'], # VI   ?
         # ['Dvaaa',     'D',       'eaaa',       'H'], # VII  OK
         # ['Dcaaa',     'D',       'caaa',       'H'], # VIII OK
         # ['E1',        'E1',      'aa',         'D'], # 1RDM
         # ['E2',        'E2',      'aaaa',       'D'], # 2RDM
         # ['E3',        'E3',      'aaaaaa',     'D'], # 3RDM
         # ['E4',        'E4',      'aaaaaaaa',   'D'], # 4RDM
         # ['E5',        'E5',      'aaaaaaaaaa', 'D'], # 5RDM
         # ['deltac',    'delta',   'cc',         'D'], # delta functions...
         # ['deltaa',    'delta',   'aa',         'D'],
         # ['deltav',    'delta',   'ee',         'D']]
  return tensors


# ====================================================
def bVec(Class,tensors,df=False):
# ----------------------------------------------------
  ''' Write out the bVec informations
  '''
# ====================================================
  UniqueNames =[t[0] for t in tensors]
  bindex  = UniqueNames.index('b')
  try:
    Windex  = UniqueNames.index('W')
  except:
    Windex =-1
  try:
    W1index = UniqueNames.index('W1')
    W2index = UniqueNames.index('W2')
  except:
    W1index=-2
    W2index=-3

  if (Class=='AAAC'):
    E1index = UniqueNames.index('E1')
    E2index = UniqueNames.index('E2')
    E3index = UniqueNames.index('E3')
    bVec_lines=[
      ["ABCE,ABCD,ED",      2.0, 3, '%2i,%2i,%2i'%(bindex, Windex, E1index), '//  2.0 b[abce] W[abcd] E1[ed]'    ],\
      ["ACBE,ABCD,ED",     -1.0, 3, '%2i,%2i,%2i'%(bindex, Windex, E1index), '// -1.0 b[acbe] W[abcd] E1[ed]'    ],\
      ["ABEF,ABCD,CFED",   -1.0, 3, '%2i,%2i,%2i'%(bindex, Windex, E2index), '// -1.0 b[abef] W[abcd] E2[cfed]'  ],\
      ["ACEF,ABCD,BFDE",   -1.0, 3, '%2i,%2i,%2i'%(bindex, Windex, E2index), '// -1.0 b[acef] W[abcd] E2[bfde]'  ],\
      ["AEBF,ABCD,CFDE",   -1.0, 3, '%2i,%2i,%2i'%(bindex, Windex, E2index), '// -1.0 b[aebf] W[abcd] E2[cfde]'  ],\
      ["AECF,ABCD,BFDE",    2.0, 3, '%2i,%2i,%2i'%(bindex, Windex, E2index), '//  2.0 b[aecf] W[abcd] E2[bfde]'  ],\
      ["AEFG,ABCD,BCGDFE", -1.0, 3, '%2i,%2i,%2i'%(bindex, Windex, E3index), '// -1.0 b[aefg] W[abcd] E3[bcgdfe]'],\
    ]

  if (Class=='AAAV'):
    daindex = UniqueNames.index('deltaa')
    E1index = UniqueNames.index('E1')
    E2index = UniqueNames.index('E2')
    E3index = UniqueNames.index('E3')
    bVec_lines=[
      ["AUVW,APQR,WR,QP,VU",  1.0, 5, '%2i,%2i,%2i,%2i,%2i'%(bindex, Windex, E1index, daindex, daindex) , '// 1.0 b[auvw] W[apqr] E1[wr] delta[qp] delta[vu]' ],\
      ["AUVW,APQR,VWRU,QP",   1.0, 4, '%2i,%2i,%2i,%2i'    %(bindex, Windex, E2index, daindex)          , '// 1.0 b[auvw] W[apqr] E2[vwru] delta[qp]'         ],\
      ["AUVW,APQR,VWQR,PU",   1.0, 4, '%2i,%2i,%2i,%2i'    %(bindex, Windex, E2index, daindex)          , '// 1.0 b[auvw] W[apqr] E2[vwqr] delta[pu]'         ],\
      ["AUVW,APQR,PWRQ,VU",   1.0, 4, '%2i,%2i,%2i,%2i'    %(bindex, Windex, E2index, daindex)          , '// 1.0 b[auvw] W[apqr] E2[pwrq] delta[vu]'         ],\
      ["AUVW,APQR,PVWRQU",    1.0, 3, '%2i,%2i,%2i'        %(bindex, Windex, E3index)                   , '// 1.0 b[auvw] W[apqr] E3[pvwrqu]'                 ],\
    ]

  if (Class=='AAVV'):
    E2index = UniqueNames.index('E2')
    bVec_lines=[
      ["ABRS,ABPQ,RSPQ", 0.25, 3, '%2i,%2i,%2i'%(bindex, Windex, E2index), '// 0.5 b[ABRS] W[ABPQ] E2[RSPQ]'],\
      ["BARS,ABPQ,RSQP", 0.25, 3, '%2i,%2i,%2i'%(bindex, Windex, E2index), '// 0.5 b[BARS] W[ABPQ] E2[RSQP]'],\
      ["ABRS,BAPQ,RSQP", 0.25, 3, '%2i,%2i,%2i'%(bindex, Windex, E2index), '// 0.5 b[ABRS] W[BAPQ] E2[RSQP]'],\
      ["BARS,BAPQ,RSPQ", 0.25, 3, '%2i,%2i,%2i'%(bindex, Windex, E2index), '// 0.5 b[BARS] W[BAPQ] E2[RSPQ]'],\
    ]

  if (Class=='ACVV'):
    E1index = UniqueNames.index('E1')
    bVec_lines=[
      ["ABIP,RP,ABIR",  2.0, 3, '%2i,%2i,%2i'%(bindex, E1index, Windex), '//  2.0 b[ABIP] E1[RP] W[ABIR]'],\
      ["ABIP,RP,BAIR", -1.0, 3, '%2i,%2i,%2i'%(bindex, E1index, Windex), '// -1.0 b[ABIP] E1[RP] W[BAIR]'],\
    ]

  if (Class=='CAAV'):
    b1index = UniqueNames.index('b1')
    b2index = UniqueNames.index('b2')
    E1index = UniqueNames.index('E1')
    E2index = UniqueNames.index('E2')
    bVec_lines=[
      ["IPQA,RQSP,ARIS",  2.0, 3, '%2i,%2i,%2i'%(b1index, E2index, W1index), '//  2.0 b1[IPQA] E2[RQSP]           W1[ARIS]'],\
      ["IPQA,SQ,APIS",    2.0, 3, '%2i,%2i,%2i'%(b1index, E1index, W1index), '//  2.0 b1[IPQA] E1[SQ]   delta[PR] W1[ARIS]'],\
      ["IPQA,RQSP,RAIS", -1.0, 3, '%2i,%2i,%2i'%(b1index, E2index, W2index), '// -1.0 b1[IPQA] E2[RQSP]           W2[RAIS]'],\
      ["IPQA,SQ,PAIS",   -1.0, 3, '%2i,%2i,%2i'%(b1index, E1index, W2index), '// -1.0 b1[IPQA] E1[SQ]   delta[PR] W2[RAIS]'],\
      ["IPQA,RQSP,ARIS", -1.0, 3, '%2i,%2i,%2i'%(b2index, E2index, W1index), '// -1.0 b2[IPQA] E2[RQSP]           W1[ARIS]'],\
      ["IPQA,SQ,APIS",   -1.0, 3, '%2i,%2i,%2i'%(b2index, E1index, W1index), '// -1.0 b2[IPQA] E1[SQ]   delta[PR] W1[ARIS]'],\
      ["IPQA,RQPS,RAIS", -1.0, 3, '%2i,%2i,%2i'%(b2index, E2index, W2index), '// -1.0 b2[IPQA] E2[RQPS]           W2[RAIS]'],\
      ["IPQA,SQ,PAIS",    2.0, 3, '%2i,%2i,%2i'%(b2index, E1index, W2index), '//  2.0 b2[IPQA] E1[SQ]   delta[PR] W2[RAIS]'],\
    ]

  if (Class=='CCAA'):
    daindex = UniqueNames.index('deltaa')
    E1index = UniqueNames.index('E1')
    E2index = UniqueNames.index('E2')
    bVec_lines=[
      ["KLRS,PR,KLPS",    2.0, 3, '%2i,%2i,%2i'%(bindex,daindex,Windex), '//  2.0 b[KLRS] delta[PR] delta[QS] W[KLPQ]'],\
      ["KLRS,PS,KLPR",   -1.0, 3, '%2i,%2i,%2i'%(bindex,daindex,Windex), '// -1.0 b[KLRS] delta[PS] delta[QR] W[KLPQ]'],\
      ["KLRS,QS,KLRQ",   -1.0, 3, '%2i,%2i,%2i'%(bindex,E1index,Windex), '// -1.0 b[KLRS] E1[QS]    delta[PR] W[KLPQ]'],\
      ["KLRS,QR,KLSQ",    0.5, 3, '%2i,%2i,%2i'%(bindex,E1index,Windex), '//  0.5 b[KLRS] E1[QR]    delta[PS] W[KLPQ]'],\
      ["KLRS,PS,KLPR",    0.5, 3, '%2i,%2i,%2i'%(bindex,E1index,Windex), '//  0.5 b[KLRS] E1[PS]    delta[QR] W[KLPQ]'],\
      ["KLRS,PR,KLPS",   -1.0, 3, '%2i,%2i,%2i'%(bindex,E1index,Windex), '// -1.0 b[KLRS] E1[PR]    delta[QS] W[KLPQ]'],\
      ["KLRS,PQRS,KLPQ",  0.5, 3, '%2i,%2i,%2i'%(bindex,E2index,Windex), '//  0.5 b[KLRS] E2[PQRS]            W[KLPQ]'],\
      ["KLRS,PS,LKPR",    2.0, 3, '%2i,%2i,%2i'%(bindex,daindex,Windex), '//  2.0 b[KLRS] delta[PS] delta[QR] W[LKPQ]'],\
      ["KLRS,PR,LKPS",   -1.0, 3, '%2i,%2i,%2i'%(bindex,daindex,Windex), '// -1.0 b[KLRS] delta[PR] delta[QS] W[LKPQ]'],\
      ["KLRS,QR,LKSQ",   -1.0, 3, '%2i,%2i,%2i'%(bindex,E1index,Windex), '// -1.0 b[KLRS] E1[QR]    delta[PS] W[LKPQ]'],\
      ["KLRS,QS,LKRQ",    0.5, 3, '%2i,%2i,%2i'%(bindex,E1index,Windex), '//  0.5 b[KLRS] E1[QS]    delta[PR] W[LKPQ]'],\
      ["KLRS,PR,LKPS",    0.5, 3, '%2i,%2i,%2i'%(bindex,E1index,Windex), '//  0.5 b[KLRS] E1[PR]    delta[QS] W[LKPQ]'],\
      ["KLRS,PS,LKPR",   -1.0, 3, '%2i,%2i,%2i'%(bindex,E1index,Windex), '// -1.0 b[KLRS] E1[PS]    delta[QR] W[LKPQ]'],\
      ["KLRS,PQSR,LKPQ",  0.5, 3, '%2i,%2i,%2i'%(bindex,E2index,Windex), '//  0.5 b[KLRS] E2[PQSR]            W[LKPQ]'],\
#'  FEqInfo MakeS1[0] = {',\
#' // {"PQRS,PR,QS",      4.0, 3, {%i,%i,%i}}, //S1[PQRS] +=  4.0 delta[PR] delta[QS]' %(S1index,daindex,daindex),\
#' // {"PQRS,PS,QR",     -2.0, 3, {%i,%i,%i}}, //S1[PQRS] += -2.0 delta[PS] delta[QR]' %(S1index,daindex,daindex),\
#' // {"PQRS,QS,PR",     -2.0, 3, {%i,%i,%i}}, //S1[PQRS] += -2.0 E1[QS]    delta[PR]' %(S1index,E1index,daindex),\
#' // {"PQRS,QR,PS",      1.0, 3, {%i,%i,%i}}, //S1[PQRS] +=  1.0 E1[QR]    delta[PS]' %(S1index,E1index,daindex),\
#' // {"PQRS,PS,QR",      1.0, 3, {%i,%i,%i}}, //S1[PQRS] +=  1.0 E1[PS]    delta[QR]' %(S1index,E1index,daindex),\
#' // {"PQRS,PR,QS",     -2.0, 3, {%i,%i,%i}}, //S1[PQRS] += -2.0 E1[PR]    delta[QS]' %(S1index,E1index,daindex),\
#' // {"PQRS,PQRT,TS",    1.0, 3, {%i,%i,%i}}, //S1[PQRS] +=  1.0 E2[PQRS]'            %(S1index,E2index,daindex),\
#' // {"PQRS,PR,QS",      2.0, 3, {%i,%i,%i}}, //S2[PQRS] +=  2.0 delta[PR] delta[QS]' %(S2index,daindex,daindex),\
#' // {"PQRS,PS,QR",      2.0, 3, {%i,%i,%i}}, //S2[PQRS] +=  2.0 delta[PS] delta[QR]' %(S2index,daindex,daindex),\
#' // {"PQRS,QS,PR",     -1.0, 3, {%i,%i,%i}}, //S2[PQRS] += -1.0 E1[QS]    delta[PR]' %(S2index,E1index,daindex),\
#' // {"PQRS,QR,PS",     -1.0, 3, {%i,%i,%i}}, //S2[PQRS] += -1.0 E1[QR]    delta[PS]' %(S2index,E1index,daindex),\
#' // {"PQRS,PS,QR",     -1.0, 3, {%i,%i,%i}}, //S2[PQRS] += -1.0 E1[PS]    delta[QR]' %(S2index,E1index,daindex),\
#' // {"PQRS,PR,QS",     -1.0, 3, {%i,%i,%i}}, //S2[PQRS] += -1.0 E1[PR]    delta[QS]' %(S2index,E1index,daindex),\
#' // {"PQRS,PQRT,TS",    1.0, 3, {%i,%i,%i}}, //S2[PQRS] +=  1.0 E2[PQRS]'            %(S2index,E2index,daindex),\
#' // {"PQRS,PQTR,TS",    1.0, 3, {%i,%i,%i}}, //S2[PQRS] +=  1.0 E2[PQSR]'            %(S2index,E2index,daindex),\
#'  };',\
    ]

  if (Class=='CCAV'):
    E1index = UniqueNames.index('E1')
    Dindex  = UniqueNames.index('deltaa')
    bVec_lines=[
      ["IJPA,RP,IJRA",  4.0, 3, '%2i,%2i,%2i'%(bindex, Dindex, Windex), '//  4.0 b[IJPA] delta[RP] W[IJRA]'],\
      ["IJPA,RP,IJRA", -2.0, 3, '%2i,%2i,%2i'%(bindex, E1index,Windex), '// -2.0 b[IJPA] E1[RP]    W[IJRA]'],\
      ["IJPA,RP,JIRA", -2.0, 3, '%2i,%2i,%2i'%(bindex, Dindex, Windex), '// -2.0 b[IJPA] delta[RP] W[JIRA]'],\
      ["IJPA,RP,JIRA",  1.0, 3, '%2i,%2i,%2i'%(bindex, E1index,Windex), '//  1.0 b[IJPA] E1[RP]    W[JIRA]'],\
    ]

  if (Class=='CCVV'):
    dcindex = UniqueNames.index('deltac')
    bVec_lines=[
      ["CDKL,LM,CDKM",  2.0, 3, '%2i,%2i,%2i'%(bindex, dcindex, Windex), '//  2.0 b[CDKL] deltac[LM] W[CDKM]'],\
      ["CDKL,LM,DCKM", -1.0, 3, '%2i,%2i,%2i'%(bindex, dcindex, Windex), '// -1.0 b[CDKL] deltac[LM] W[DCKM]'],\
      ["CDKL,LM,CDMK", -1.0, 3, '%2i,%2i,%2i'%(bindex, dcindex, Windex), '// -1.0 b[CDKL] deltac[LM] W[CDMK]'],\
      ["CDKL,LM,DCMK",  2.0, 3, '%2i,%2i,%2i'%(bindex, dcindex, Windex), '//  2.0 b[CDKL] deltac[LM] W[DCMK]'],\
    ]

  convert_bVec_to_df(bVec_lines,Class,UniqueNames,df)

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


# ====================================================
def convert_bVec_to_df(bVec_lines,Class,UniqueNames,df=False):
# ----------------------------------------------------
  '''
  '''
# ====================================================
  if (df):
    try:
      dleft ='L'+domain_of_class[Class][0]+domain_of_class[Class][2]
      dright='L'+domain_of_class[Class][1]+domain_of_class[Class][3]
      nameleft =re.sub("e","v","W"+dleft)
      nameright=re.sub("e","v","W"+dright)
      Wl =str(UniqueNames.index(nameleft))
      Wr =str(UniqueNames.index(nameright))
    except:
      Wl =-1
      Wr =-1
    try:
      W1l=str(UniqueNames.index('WLvc'))
      W1r=str(UniqueNames.index('WLaa'))
      W2l=str(UniqueNames.index('WLac'))
      W2r=str(UniqueNames.index('WLva'))
    except:
      W1l=-1
      W1r=-1
      W2l=-1
      W2r=-1

    for i in range(len(bVec_lines)):
      line=bVec_lines[i]

      # find position of V
      liste=line[3].strip().split(',')
      position=-1
      for j in range(len(liste)):
        if int(liste[j])==-1:
          position=j
          From=liste[position]
          To  ='%s,%s'%(Wl,Wr)
        elif int(liste[j])==-2:
          position=j
          From=liste[position]
          To  ='%s,%s'%(W1l,W1r)
        elif int(liste[j])==-3:
          position=j
          From=liste[position]
          To  ='%s,%s'%(W2l,W2r)

      if position!=-1:
        # replace W by Wl,Wr
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

def print_GetMethodInfo(PT,Class,nbrTensors,nbrEqs,nbr_bVec):
  print '  static void GetMethodInfo(FMethodInfo &Out) {'
  print '    Out = FMethodInfo();'
  print '    Out.pName = "'+PT+Class+'";'
  if Class!='3':
    print '    Out.perturberClass = "'+Class+'";'
  print '    Out.pSpinClass = "restricted";'
  print '    Out.pTensorDecls = &TensorDecls[0];'
  print '    Out.nTensorDecls = %i;'%(nbrTensors)
  if 'CAAV' in Class or 'ACVV' in Class or 'CCAV' in Class:
    print '    Out.pDomainDecls = &DomainDecls[0];'
    print '    Out.nDomainDecls = 1;'
  print '    Out.EqsRes = FEqSet(&EqsRes[0], %i, "%s%s/Res");'%(nbrEqs,PT,Class)
  if nbr_bVec!=0:
    print '    Out.bVec = FEqSet(&bVec[0], '+str(nbr_bVec)+', "'+PT+Class+'/bVec");'
  print '  };'
  print '};'

