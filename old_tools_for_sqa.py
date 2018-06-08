import secondQuantizationAlgebra as sqa

#OLD CODE============================================

# USEFUL ROUTINES ---------------------------------------------------------------------------------
# Returns string for indexes
def code(list):
  line=''
  for iter in list:
    line=line+iter.name[0]
  return line.lower()

# Returns string for indexes
# that SHOULD alternate but DON'T: "a^T a^T a a"
# (to feed to "pattern")
def code_rearrange(list):
  if len(list)==4:
    line=list[0].name[0]+list[2].name[0]+list[1].name[0]+list[3].name[0]
  elif len(list)==2:
    line=code(list)
  else:
    print 'ERROR code_rearrange'
    exit()
  return line.lower()

# Returns [Delta_c,Delta_a,Delta_v]
# from a string of indexes
def pattern(string):
  countC=0
  countA=0
  countV=0
  for iter in range(len(string)-1,-1,-1):
    if iter%2==0:
      mult=1
    else:
      mult=-1
    if string[iter]=='c':
      countC=countC+mult
    if string[iter]=='a':
      countA=countA+mult
    if string[iter]=='v':
      countV=countV+mult
  return [countC,countA,countV]

# Outputs the pattern
def output_pattern(string):
  list=pattern(string)
  return '{:3}{:3}{:3}'.format(list[0],list[1],list[2])

# Is the "string" does not change the occupation, then return True
# Give it the total <Psi_0| string |Psi_0> !
def is_non_zero(string):
  list=pattern(string)
  total=abs(list[0])+abs(list[1])+abs(list[2])
  return total==0

# Return of "symm" properties
# CAN I DO BETTER HERE...???
def symm(list):
  symm=[]
  return symm
  if len(list)==2:
    if list[0].name[0]==list[1].name[0]:
      symm.append(hsym)
  elif len(list)==4:
    if list[1].name[0]==list[3].name[0]:
      symm.append(Dsym_b)
    if list[0].name[0]==list[2].name[0]:
      symm.append(Dsym_a)
    if list[0].name[0]==list[1].name[0] and\
       list[2].name[0]==list[3].name[0]:
      symm.append(Dsym_c)
  #print '//',code(list),[s.pattern for s in symm]
  return symm




# TENSORS -----------------------------------------------------------------------------------------
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




# MISC --------------------------------------------------------------------------------------------
# Define needed indexes as being core,active,virtual
tag_core    = sqa.options.core_type
tag_active  = sqa.options.active_type
tag_virtual = sqa.options.virtual_type

# For Onu and Omu
i1 = sqa.index('Ci1',  [tag_core],    True)
i2 = sqa.index('Ci2',  [tag_core],    True)
i3 = sqa.index('Ci3',  [tag_core],    True)
i4 = sqa.index('Ci4',  [tag_core],    True)
i5 = sqa.index('Ci5',  [tag_core],    True)
i6 = sqa.index('Ci6',  [tag_core],    True)
i7 = sqa.index('Ci7',  [tag_core],    True)
i8 = sqa.index('Ci8',  [tag_core],    True)
i9 = sqa.index('Ci9',  [tag_core],    True)
i10= sqa.index('Ci10', [tag_core],    True)
i11= sqa.index('Ci11', [tag_core],    True)
i12= sqa.index('Ci12', [tag_core],    True)
i13= sqa.index('Ci13', [tag_core],    True)
i14= sqa.index('Ci14', [tag_core],    True)
i15= sqa.index('Ci15', [tag_core],    True)
i16= sqa.index('Ci16', [tag_core],    True)
i17= sqa.index('Ci17', [tag_core],    True)
i18= sqa.index('Ci18', [tag_core],    True)
i19= sqa.index('Ci19', [tag_core],    True)
i20= sqa.index('Ci20', [tag_core],    True)

p1 = sqa.index('Ap1',  [tag_active],  True)
p2 = sqa.index('Ap2',  [tag_active],  True)
p3 = sqa.index('Ap3',  [tag_active],  True)
p4 = sqa.index('Ap4',  [tag_active],  True)
p5 = sqa.index('Ap5',  [tag_active],  True)
p6 = sqa.index('Ap6',  [tag_active],  True)
p7 = sqa.index('Ap7',  [tag_active],  True)
p8 = sqa.index('Ap8',  [tag_active],  True)
p9 = sqa.index('Ap9',  [tag_active],  True)
p10= sqa.index('Ap10', [tag_active],  True)
p11= sqa.index('Ap11', [tag_active],  True)
p12= sqa.index('Ap12', [tag_active],  True)
p13= sqa.index('Ap13', [tag_active],  True)
p14= sqa.index('Ap14', [tag_active],  True)
p15= sqa.index('Ap15', [tag_active],  True)
p16= sqa.index('Ap16', [tag_active],  True)
p17= sqa.index('Ap17', [tag_active],  True)
p18= sqa.index('Ap18', [tag_active],  True)
p19= sqa.index('Ap19', [tag_active],  True)
p20= sqa.index('Ap20', [tag_active],  True)
p21= sqa.index('Ap21', [tag_active],  True)
p22= sqa.index('Ap22', [tag_active],  True)
p23= sqa.index('Ap23', [tag_active],  True)
p24= sqa.index('Ap24', [tag_active],  True)
p25= sqa.index('Ap25', [tag_active],  True)
p26= sqa.index('Ap26', [tag_active],  True)
p27= sqa.index('Ap27', [tag_active],  True)
p28= sqa.index('Ap28', [tag_active],  True)
p29= sqa.index('Ap29', [tag_active],  True)
p30= sqa.index('Ap30', [tag_active],  True)
p31= sqa.index('Ap31', [tag_active],  True)
p32= sqa.index('Ap32', [tag_active],  True)

a1 = sqa.index('Va1',  [tag_virtual], True)
a2 = sqa.index('Va2',  [tag_virtual], True)
a3 = sqa.index('Va3',  [tag_virtual], True)
a4 = sqa.index('Va4',  [tag_virtual], True)
a5 = sqa.index('Va5',  [tag_virtual], True)
a6 = sqa.index('Va6',  [tag_virtual], True)
a7 = sqa.index('Va7',  [tag_virtual], True)
a8 = sqa.index('Va8',  [tag_virtual], True)
a9 = sqa.index('Va9',  [tag_virtual], True)
a10= sqa.index('Va10', [tag_virtual], True)
a11= sqa.index('Va11', [tag_virtual], True)
a12= sqa.index('Va12', [tag_virtual], True)
a13= sqa.index('Va13', [tag_virtual], True)
a14= sqa.index('Va14', [tag_virtual], True)
a15= sqa.index('Va15', [tag_virtual], True)
a16= sqa.index('Va16', [tag_virtual], True)
a17= sqa.index('Va17', [tag_virtual], True)
a18= sqa.index('Va18', [tag_virtual], True)
a19= sqa.index('Va19', [tag_virtual], True)
a20= sqa.index('Va20', [tag_virtual], True)

# For delta functions
i1D = sqa.index('Ci1D',  [tag_core],    True)
i2D = sqa.index('Ci2D',  [tag_core],    True)
p1D = sqa.index('Ap1D',  [tag_active],  True)
p2D = sqa.index('Ap2D',  [tag_active],  True)
a1D = sqa.index('Va1D',  [tag_virtual], True)
a2D = sqa.index('Va2D',  [tag_virtual], True)

# For H
iH = sqa.index('CiH', [tag_core],    True)
jH = sqa.index('CjH', [tag_core],    True)
kH = sqa.index('CkH', [tag_core],    True)
lH = sqa.index('ClH', [tag_core],    True)
pH = sqa.index('ApH', [tag_active],  True)
qH = sqa.index('AqH', [tag_active],  True)
rH = sqa.index('ArH', [tag_active],  True)
sH = sqa.index('AsH', [tag_active],  True)
aH = sqa.index('VaH', [tag_virtual], True)
bH = sqa.index('VbH', [tag_virtual], True)
cH = sqa.index('VcH', [tag_virtual], True)
dH = sqa.index('VdH', [tag_virtual], True)

# Define symmetries and delta functions
hsym   = sqa.symmetry((1,0), 1)
Dsym_a = sqa.symmetry((2,1, 0,3), 1)
Dsym_b = sqa.symmetry((0,3, 2,1), 1)
Dsym_c = sqa.symmetry((1,0, 3,2), 1)
deltaC = sqa.tensor('deltac', [i1D,i2D], [hsym])
deltaA = sqa.tensor('deltaa', [p1D,p2D], [hsym])
deltaV = sqa.tensor('deltav', [a1D,a2D], [hsym])

# Occupation pattern of the classes
#           I      II     III    IV     V      VI     VI     VII    VIII
ClassNames=['vvcc','vvca','ccav','vvaa','ccaa','vaca','avca','vaaa','caaa']
occupations={}
occupations['vvcc'] =[-2, 0, 2]
occupations['vvca'] =[-1,-1, 2]
occupations['ccav'] =[-2, 1, 1]
occupations['vvaa'] =[ 0,-2, 2]
occupations['ccaa'] =[-2, 2, 0]
occupations['vaca'] =[-1, 0, 1]
occupations['avca'] =[-1, 0, 1]
occupations['vaaa'] =[ 0,-1, 1]
occupations['caaa'] =[-1, 1, 0]
occupations['other']=[-5,-5,-5]
occupations['h0']   =[ 0, 0, 0]

