import secondQuantizationAlgebra as sqa
import writeCode
import geraldCode


# [BM] List of functions used here --------------------------------------------------------------------------
# [BM]   sqa.index                        associates a kind to an index (core,active,virtual)
# [BM]   sqa.sfExOp                       defines a "spin free excitation operator", with indexes
# [BM]   sqa.symmetry                     defines a "symmetry class" applicable to any tensor 
# [BM]   sqa.tensor                       defines a "tensor", with a name, indexes and "sqa.symmetry" classes 
# [BM]   sqa.term                         defines a "term" of an equation with "sqa.tensor" and "sqa.sfExOp"
# [BM]   sqa.commutator                   defines a "commutator" of two "sqa.term"s 
# [BM]
# [BM]   sqa.multiplyTerms                properly multiplies two "sqa.term"s
# [BM]                                    (#what does that mean precisly?) 
# [BM]   sqa.normalOrder                  normal orders a string of "sqa.term"s
# [BM]
# [BM]   sqa.contractCoreOps              set "sqa.term"s that contain only core indexes to "\delta"s 
# [BM]   sqa.removeVirtOps                set "sqa.term"s that contain only virtual indexes to 0 
# [BM]   sqa.termChop                     simplifies a string of "sqa.term"s (1/2) 
# [BM]   sqa.combineTerms                 simplifies a string of "sqa.term"s (2/2) 
# [BM]   contractDeltaFuncs_new           get rid of \delta functions in a string of "sqa.term"s
# [BM]                                    (#what does that mean precisly?) 
# [BM]   replaceRepeatIndicesWithDeltas   (# ??)
# [BM] ------------------------------------------------------------------------------------------------------


# [BM] Remember that ----------------------------------------------------------------------------------------
# [BM]   H_Fink = t^n_m E_n^m + W^{mn}_{op} E_{mn}^{op} (\Delta n_ex  =  0)
# [BM]   V_Fink =               W^{mn}_{op} E_{mn}^{op} (\Delta n_ex \ne 0)
# [BM] ------------------------------------------------------------------------------------------------------


sqa.options.verbose = False


# definitions
# [BM] Need to specify which indices are in which spaces.
# [BM] The commutation rules are the same, but:
# [BM]   - if you get all core, you get deltas
# [BM]   - if you get all active, you get RDMs
# [BM]   - if you get all virtual, you get zeros

tag_core    = sqa.options.core_type
tag_active  = sqa.options.active_type
tag_virtual = sqa.options.virtual_type

a  = sqa.index('Va',  [tag_virtual], True)
b  = sqa.index('Vb',  [tag_virtual], True)
c  = sqa.index('Vc',  [tag_virtual], True)
d  = sqa.index('Vd',  [tag_virtual], True)
i  = sqa.index('Ci',  [tag_core],    True)
j  = sqa.index('Cj',  [tag_core],    True)
k  = sqa.index('Ck',  [tag_core],    True)
l  = sqa.index('Cl',  [tag_core],    True)
p  = sqa.index('Ap',  [tag_active],  True)
q  = sqa.index('Aq',  [tag_active],  True)
r  = sqa.index('Ar',  [tag_active],  True)
s  = sqa.index('As',  [tag_active],  True)


x1  = sqa.index('Au',  [tag_active],  True)
x2  = sqa.index('Av',  [tag_active],  True)
x3  = sqa.index('Aw',  [tag_active],  True)
x4  = sqa.index('Ax',  [tag_active],  True)
i1  = sqa.index('Cm',  [tag_core],    True)
i2  = sqa.index('Cn',  [tag_core],    True)
i3  = sqa.index('Co',  [tag_core],    True)
i4  = sqa.index('Co1',  [tag_core],    True)
a1  = sqa.index('Vg',  [tag_virtual], True)
a2  = sqa.index('Vh',  [tag_virtual], True)
a3  = sqa.index('Ve',  [tag_virtual], True)
a4  = sqa.index('Vf',  [tag_virtual], True)


#h0 one body term
# [BM] Here the classes of symmetry of indexes are defined.
# [BM] Those classes of symmetry can be applied to any tensor.
# [BM] h[q,p] = h[p,q]
# [BM] D[r,q,p,s] = D[p,q,r,s]
# [BM] D[p,s,r,q] = D[p,q,r,s]
# [BM] D[q,p,s,r] = D[p,q,r,s]
hsym   = sqa.symmetry((1,0), 1)
Dsym_a = sqa.symmetry((2,1, 0,3), 1)
Dsym_b = sqa.symmetry((0,3, 2,1), 1)
Dsym_c = sqa.symmetry((1,0, 3,2), 1)


# [BM] Here are the proper definitions of all the tensors
# [BM] found in the equations (t,W as well as the \delta) 

# [BM] t^{mu2}_{mu1} for core,active,virtual.
# [BM] This has the simple h symmetry.
# [BM] This will give rise to the sqa.term T_C, T_A, T_V 
K_C = sqa.tensor('int1c', [i1,i2], [hsym])
K_A = sqa.tensor('int1a', [x1,x2], [hsym])
K_V = sqa.tensor('int1v', [a1,a2], [hsym])

# [BM] W^{mu2 nu2}_{sigma1 tau1} for indexes to we be paired with:
# [BM]    the "1" kind: E_{i2 x2}^{i1 x1}
# [BM]    the "2" kind: E_{x2 i2}^{i1 x1}
# [BM] # I do not understand those restriction in the symmetries!
# [BM] This will give rise to sqa.term HD_CA, HD_CV, HD_AV
V_CA1 = sqa.tensor('int2ca1', [i1,x1, i2,x2], [Dsym_a, Dsym_b])
V_CA2 = sqa.tensor('int2ca2', [i1,x1, x2,i2], [])

V_CV1 = sqa.tensor('int2cv1', [i1,a1, i2,a2], [Dsym_a, Dsym_b])
V_CV2 = sqa.tensor('int2cv2', [i1,a1, a2,i2], [])

V_AV1 = sqa.tensor('int2av1', [x1,a1, x2,a2], [Dsym_a, Dsym_b])
V_AV2 = sqa.tensor('int2av2', [x1,a1, a2,x2], [])

# [BM] W^{mu3 mu4}_{mu1 mu2} for all four being core,active,virtual indexes
# [BM] This has all symmetries.
# [BM] This will give rise to sqa.term HD_C, HD_A, HD_V 
V_C = sqa.tensor('int2c', [i1,i2, i3,i4], [Dsym_a, Dsym_b, Dsym_c])
V_A = sqa.tensor('int2a', [x1,x2, x3,x4], [Dsym_a, Dsym_b, Dsym_c])
V_V = sqa.tensor('int2v', [a1,a2, a3,a4], [Dsym_a, Dsym_b, Dsym_c])

# [BM] \delta_{mu1 mu2} for core,active,virtual indexes
# [BM] This has of course the simple h symmetry.
deltaC = sqa.tensor('deltac', [i1,i2], [hsym])
deltaA = sqa.tensor('deltaa', [x1,x2], [hsym])
deltaV = sqa.tensor('deltav', [a1,a2], [hsym])


# [BM] #WE_PASS_THIS_FOR_NOW [begin] --------------------------------------------------- 
#AllTensors = ["t", "R", "int1c", "int1a", "int1v", "int2ca1", "int2ca2",\
#              "int2cv1", "int2cv2", "int2av1", "int2av2", "int2c", "int2a", "int2v",\
#              "E1", "E2", "E3", "S1", "S2", "T", "b", "p", "Ap",\
#              "P", "AP", "B", "V", "deltac", "deltaa", "deltav"]
AllTensors = ["b", "B", "t", "T", "p", "P", "Ap", "AP", "R", \
              "int1c", "int1a", "int1v", "int2ca1", "int2ca2",\
              "int2cv1", "int2cv2", "int2av1", "int2av2", "int2c", "int2a", "int2v",\
              "E1", "E2", "E3", "S1", "S2","V", "deltac", "deltaa", "deltav"]

CommentTensors = ["b", "B", "t", "T", "p", "P", "Ap", "AP", "R", 
                  "k", "k", "k", "W", "W",\
                  "W", "W", "W", "W", "W", "W", "W",\
                  "E1", "E2", "E3", "S1", "S2", "W", "delta", "delta", "delta"]

Domains = ["eeaa", "eeaa", "eeaa", "eeaa", "eeaa", "eeaa", "eeaa", "eeaa", "eeaa", 
           "cc", "aa", "ee", "caca", "caac",\
           "cece", "ceec", "aeae", "aeea", "cccc", "aaaa", "eeee",\
           "aa", "aaaa", "aaaaaa", "aAaA", "aaaa", "eeaa", "cc", "aa", "ee"]
Usage = ["A", "R", "A", "A", "A", "A", "A", "A", "A", 
         "H", "H", "H", "H", "H",\
         "H", "H", "H", "H", "H", "H", "H",\
         "D", "D", "D", "D", "D", "H", "D", "D", "D"]

# [BM] (uninteresting: write out previously defined stuff)
pDomains  = "\tint f(int i) {\n"
pDomains += "\t\treturn 2*i;\n"
pDomains += "\t}\n"
pDomains += "\tFDomainDecl DomainDecls[1] = {\n"
pDomains += "\t\t{\"A\", \"a\", f}\n"
pDomains += "\t};"
CommentKey = {}
print "namespace MRLCC_AAVV {\n"
for tc in list(zip(AllTensors, CommentTensors)):
    CommentKey[tc[0]] = tc[1]

geraldCode.writeTensors(AllTensors, CommentKey, Domains, Usage)
# [BM] #WE_PASS_THIS_FOR_NOW [end] ----------------------------------------------------- 


# [BM] Definitions of the terms found in the equations,
# [BM] that is to say "tensor.excitation operator".
# [BM] ("sfExOp" is "spin-free Excitation Operator")

# [BM] This is W^{mu3 mu4}_{mu1 mu2} E_{mu3 mu4}^{mu1 mu2} for all indexes in core,active,virtual
HD_C   = sqa.term( 0.5, [""], [V_C,   sqa.sfExOp([i1,i2,i3,i4])] )
HD_A   = sqa.term( 0.5, [""], [V_A,   sqa.sfExOp([x1,x2,x3,x4])] )
HD_V   = sqa.term( 0.5, [""], [V_V,   sqa.sfExOp([a1,a2,a3,a4])] )

# [BM] This is :
# [BM]    the "1" kind: W^{i2 x2}_{i1 x1} E_{i2 x2}^{i1 x1}
# [BM]    the "2" kind: W^{x2 i2}_{i1 x1} E_{x2 i2}^{i1 x1}
HD_CA1 = sqa.term( 1.0, [""], [V_CA1, sqa.sfExOp([i1,x1,i2,x2])] )
HD_CA2 = sqa.term( 1.0, [""], [V_CA2, sqa.sfExOp([i1,x1,x2,i2])] )

HD_CV1 = sqa.term( 1.0, [""], [V_CV1, sqa.sfExOp([i1,a1,i2,a2])] )
HD_CV2 = sqa.term( 1.0, [""], [V_CV2, sqa.sfExOp([i1,a1,a2,i2])] )

HD_AV1 = sqa.term( 1.0, [""], [V_AV1, sqa.sfExOp([x1,a1,x2,a2])] )
HD_AV2 = sqa.term( 1.0, [""], [V_AV2, sqa.sfExOp([x1,a1,a2,x2])] )

# [BM] This is t^{mu2}_{mu1} E_{mu2}^{mu1} for core,active,virtual
T_C    = sqa.term( 1.0, [""], [K_C,   sqa.sfExOp([i1,i2])] )
T_A    = sqa.term( 1.0, [""], [K_A,   sqa.sfExOp([x1,x2])] )
T_V    = sqa.term( 1.0, [""], [K_V,   sqa.sfExOp([a1,a2])] )

# [BM] Those are tensors (understand: a blank slate to be filled by the CPP program)
# [BM] to represent (for an iteration) the test input vector "p" and the final output vector "A.p"
Cin = sqa.tensor("p", [a,b,p,q], [Dsym_c])
Cout = sqa.tensor("Ap", [c,d,r,s], [Dsym_c])

#first excitation
# [BM] Those are the terms \hat{O}_\mu and \hat{O}_\nu that encompass \hat{H} in A 
# [BM] ~~> I understand that "p" should appear we the proper indexes to account for "A.p"
# [BM]   # but it is still unclear for me why the "A.p" tensor should appear...
E_aiEbj  = sqa.term( 1.0, [""],  [Cin, sqa.sfExOp([a, p]) , sqa.sfExOp([b,q])])
E_aiEbj2 = sqa.term( 1.0, [""],  [Cout, sqa.sfExOp([s, d]) , sqa.sfExOp([r,c])])

# [BM] # 
commutator = []
commutator +=  sqa.commutator(HD_C, E_aiEbj)
commutator +=  sqa.commutator(HD_A, E_aiEbj)
commutator +=  sqa.commutator(HD_V, E_aiEbj)
commutator +=  sqa.commutator(HD_CA1, E_aiEbj)
commutator +=  sqa.commutator(HD_CA2, E_aiEbj)
commutator +=  sqa.commutator(HD_CV1, E_aiEbj)
commutator +=  sqa.commutator(HD_CV2, E_aiEbj)
commutator +=  sqa.commutator(HD_AV1, E_aiEbj)
commutator +=  sqa.commutator(HD_AV2, E_aiEbj)
commutator +=  sqa.commutator(T_C, E_aiEbj)
commutator +=  sqa.commutator(T_A, E_aiEbj)
commutator +=  sqa.commutator(T_V, E_aiEbj)
result = []

# [BM] This is all the work done here [begin] -----------------------------
# [BM] i.e. Normal Ordering + Massaging the result to simplify it
for t in commutator:
    result += sqa.normalOrder(sqa.multiplyTerms(E_aiEbj2, t))


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
rdmDelta = [deltaC, deltaA, deltaV]


#********this adds delta funcstion when we have repeat indices****************#
for r in extendedR:
    result.append(geraldCode.replaceRepeatIndicesWithDeltas(r, rdmDelta))
# [BM] This is all the work done here [end] -------------------------------


#for r in result:    
#    print "Cout[Vc, Vd, Ar, As] =  ", r, " * Cin[Va, Vb, Ap, Aq]"


print "//Number of terms : ", len(result)
#writeCode.WriteCode(result, True, intmapkey, RDMmapkey)

#print "\tFEqInfo "+EquationName+"[%i] = {\n"%(len(result))
print "\tFEqInfo EqsRes[%i] = {\n"%(len(result))
#geraldCode.WriteCode_lcc(result, AllTensors, ["Va", "Vb", "Ap", "Aq"], "CDRS", CommentKey)
# [BM] #FIGURE THAT OUT !!!
geraldCode.WriteCode_lccSimple(result, AllTensors, CommentKey)
print "\n\t};"

# [BM] #FIGURE THAT OUT !!!
bindex = AllTensors.index("b")
Vindex = AllTensors.index("V")
E2index = AllTensors.index("E2")
print pDomains
print	"\tFEqInfo Overlap[2] = {"
print		"\t\t{\"ABRS,ABPQ,RSPQ\", 0.5, 3, {%i, %i, %i}},"%(bindex, Vindex, E2index)
print		"\t\t{\"BARS,ABPQ,RSQP\", 0.5, 3, {%i, %i, %i}}"%(bindex, Vindex, E2index)
print	"\t};"

# [BM] #FIGURE THAT OUT !!!
print	"\tstatic void GetMethodInfo(FMethodInfo &Out) {"
print	      "\t\tOut = FMethodInfo();"
print	      "\t\tOut.pName = \"MRLCC_AAVV\";"
print         "\t\tOut.perturberClass = \"AAVV\";"
print	      "\t\tOut.pSpinClass = \"restricted\";"
print	      "\t\tOut.pTensorDecls = &TensorDecls[0];"
print	      "\t\tOut.nTensorDecls = %i;"%(len(Usage))
print	      "\t\tOut.pDomainDecls = &DomainDecls[0];"
print	      "\t\tOut.nDomainDecls = 1;"
print	      "\t\tOut.EqsRes = FEqSet(&EqsRes[0], %i, \"MRLCC_AAVV/Res\");"%(len(result))
print	      "\t\tOut.Overlap = FEqSet(&Overlap[0], 2, \"MRLCC_AAVV/Overlap\");"
print	"\t};"
print "};"
