
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

