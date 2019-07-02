import secondQuantizationAlgebra as sqa
import writeCode
import geraldCode

sqa.options.verbose = False
# definitions

tag_core    = sqa.options.core_type
tag_active  = sqa.options.active_type
tag_virtual = sqa.options.virtual_type

a  = sqa.index('Va',  [tag_virtual], False)
b  = sqa.index('Vb',  [tag_virtual], False)
c  = sqa.index('Vc',  [tag_virtual], False)
d  = sqa.index('Vd',  [tag_virtual], False)
i  = sqa.index('Ci',  [tag_core],    False)
j  = sqa.index('Cj',  [tag_core],    False)
k  = sqa.index('Ck',  [tag_core],    False)
l  = sqa.index('Cl',  [tag_core],    False)
p  = sqa.index('Ap',  [tag_active],  False)
q  = sqa.index('Aq',  [tag_active],  False)
r  = sqa.index('Ar',  [tag_active],  False)
s  = sqa.index('As',  [tag_active],  False)


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
hsym   = sqa.symmetry((1,0), 1)
Dsym_a = sqa.symmetry((2,1, 0,3), 1)
Dsym_b = sqa.symmetry((0,3, 2,1), 1)
Dsym_c = sqa.symmetry((1,0, 3,2), 1)
K_C = sqa.tensor('int1c', [i1,i2], [hsym])
K_A = sqa.tensor('int1a', [x1,x2], [hsym])
K_V = sqa.tensor('int1v', [a1,a2], [hsym])
V_CA1 = sqa.tensor('int2ca1', [i1,x1, i2,x2], [Dsym_a, Dsym_b])
V_CA2 = sqa.tensor('int2ca2', [i1,x1, x2,i2], [])

V_CV1 = sqa.tensor('int2cv1', [i1,a1, i2,a2], [Dsym_a, Dsym_b])
V_CV2 = sqa.tensor('int2cv2', [i1,a1, a2,i2], [])

V_AV1 = sqa.tensor('int2av1', [x1,a1, x2,a2], [Dsym_a, Dsym_b])
V_AV2 = sqa.tensor('int2av2', [x1,a1, a2,x2], [])

V_C = sqa.tensor('int2c', [i1,i2, i3,i4], [Dsym_a, Dsym_b, Dsym_c])
V_A = sqa.tensor('int2a', [x1,x2, x3,x4], [Dsym_a, Dsym_b, Dsym_c])
V_V = sqa.tensor('int2v', [a1,a2, a3,a4], [Dsym_a, Dsym_b, Dsym_c])

deltaC = sqa.tensor('deltac', [i1,i2], [hsym])
deltaA = sqa.tensor('deltaa', [x1,x2], [hsym])
deltaV = sqa.tensor('deltav', [a1,a2], [hsym])

ampstring = "caae" #amplitude string
AllTensors = ["t",       "R",       "int1c",    "int1a",   "int1v",\
              "int2ca1", "int2ca2", "int2cv1",  "int2cv2", "int2av1",\
              "int2av2", "int2c",   "int2a",    "int2v",   "E1",\
              "E2",      "E3",      "S1",       "T",       "p1",\
              "p2",      "Ap1",     "Ap2",      "b1",      "b2",\
              "b",       "P",       "AP",      "B1",       "B2",      "B",\
              "V1",      "V2",      "deltac",   "deltaa",  "deltav",\
              "p",       "Ap",      "f"]
CommentTensors = ["t",   "R",       "k",        "k",       "k",\
                  "W",   "W",       "W",        "W",       "W",\
                  "W",   "W",       "W",        "W",       "E1",\
                  "E2",  "E3",      "S1",       "T",       "p1",\
                  "p2",  "Ap1",     "Ap2",      "b1",      "b2",\
                  "b",   "P",       "AP",      "B1",       "B2",      "B",\
                  "W",   "W",       "delta",    "delta",   "delta",\
                  "p",   "Ap",      "f"]

Domains = ["cAae", "cAae",   "cc",   "aa",   "ee",\
           "caca", "caac",   "cece", "ceec", "aeae",\
           "aeea", "cccc",   "aaaa", "eeee", "aa",\
           "aaaa", "aaaaaa", "AaAa", "cAae", ampstring,\
            ampstring, ampstring, ampstring, "caae", "caae",\
           "",     "cAae",     "cAae",       "caae", "caae", "",\
           "eaca", "aeca",   "cc",   "aa",   "ee",\
           "",     "",       "ec"]
Usage = [  "A",  "R", "H", "H", "H",\
           "H",  "H", "H", "H", "H",\
           "H",  "H", "H", "H", "D",\
           "D",  "D", "D", "A", "A",\
           "A",  "A", "A", "A", "A",\
           "A",  "A", "A", "A", "A", "A",\
           "H",  "H", "D", "D", "D",\
           "A",  "A", "H"]

pDomains  = "\tint f(int i) {\n"
pDomains += "\t\treturn 2*i;\n"
pDomains += "\t}\n"
pDomains += "\tFDomainDecl DomainDecls[1] = {\n"
pDomains += "\t\t{\"A\", \"a\", f}\n"
pDomains += "\t};"
CommentKey = {}
print "namespace MRLCC_CAAV {\n"
for tc in list(zip(AllTensors, CommentTensors)):
    CommentKey[tc[0]] = tc[1]

geraldCode.writeTensors(AllTensors, CommentKey, Domains, Usage)

HD_C   = sqa.term( 0.5, [""], [V_C,   sqa.sfExOp([i1,i2,i3,i4])] )
HD_A   = sqa.term( 0.5, [""], [V_A,   sqa.sfExOp([x1,x2,x3,x4])] )
HD_V   = sqa.term( 0.5, [""], [V_V,   sqa.sfExOp([a1,a2,a3,a4])] )

HD_CA1 = sqa.term( 1.0, [""], [V_CA1, sqa.sfExOp([i1,x1,i2,x2])] )
HD_CA2 = sqa.term( 1.0, [""], [V_CA2, sqa.sfExOp([i1,x1,x2,i2])] )

HD_CV1 = sqa.term( 1.0, [""], [V_CV1, sqa.sfExOp([i1,a1,i2,a2])] )
HD_CV2 = sqa.term( 1.0, [""], [V_CV2, sqa.sfExOp([i1,a1,a2,i2])] )

HD_AV1 = sqa.term( 1.0, [""], [V_AV1, sqa.sfExOp([x1,a1,x2,a2])] )
HD_AV2 = sqa.term( 1.0, [""], [V_AV2, sqa.sfExOp([x1,a1,a2,x2])] )

T_C    = sqa.term( 1.0, [""], [K_C,   sqa.sfExOp([i1,i2])] )
T_A    = sqa.term( 1.0, [""], [K_A,   sqa.sfExOp([x1,x2])] )
T_V    = sqa.term( 1.0, [""], [K_V,   sqa.sfExOp([a1,a2])] )



#first excitation
E_aiEbj1a  = sqa.term( 1.0, [""],  [sqa.sfExOp([a, i]) , sqa.sfExOp([p,q])])
E_aiEbj1b  = sqa.term( 1.0, [""],  [sqa.sfExOp([p, i]) , sqa.sfExOp([a,q])])
E_aiEbj2a  = sqa.term( 1.0, [""],  [sqa.sfExOp([s, r]) , sqa.sfExOp([j,b])])
E_aiEbj2b  = sqa.term( 1.0, [""],  [sqa.sfExOp([s, b]) , sqa.sfExOp([j,r])])


commutator1 = []
commutator1 +=  sqa.commutator(HD_C, E_aiEbj1a)
commutator1 +=  sqa.commutator(HD_A, E_aiEbj1a)
commutator1 +=  sqa.commutator(HD_V, E_aiEbj1a)
commutator1 +=  sqa.commutator(HD_CA1, E_aiEbj1a)
commutator1 +=  sqa.commutator(HD_CA2, E_aiEbj1a)
commutator1 +=  sqa.commutator(HD_CV1, E_aiEbj1a)
commutator1 +=  sqa.commutator(HD_CV2, E_aiEbj1a)
commutator1 +=  sqa.commutator(HD_AV1, E_aiEbj1a)
commutator1 +=  sqa.commutator(HD_AV2, E_aiEbj1a)
commutator1 +=  sqa.commutator(T_C, E_aiEbj1a)
commutator1 +=  sqa.commutator(T_A, E_aiEbj1a)
commutator1 +=  sqa.commutator(T_V, E_aiEbj1a)
commutator2 = []
commutator2 +=  sqa.commutator(HD_C, E_aiEbj1b)
commutator2 +=  sqa.commutator(HD_A, E_aiEbj1b)
commutator2 +=  sqa.commutator(HD_V, E_aiEbj1b)
commutator2 +=  sqa.commutator(HD_CA1, E_aiEbj1b)
commutator2 +=  sqa.commutator(HD_CA2, E_aiEbj1b)
commutator2 +=  sqa.commutator(HD_CV1, E_aiEbj1b)
commutator2 +=  sqa.commutator(HD_CV2, E_aiEbj1b)
commutator2 +=  sqa.commutator(HD_AV1, E_aiEbj1b)
commutator2 +=  sqa.commutator(HD_AV2, E_aiEbj1b)
commutator2 +=  sqa.commutator(T_C, E_aiEbj1b)
commutator2 +=  sqa.commutator(T_A, E_aiEbj1b)
commutator2 +=  sqa.commutator(T_V, E_aiEbj1b)
result1 = []
result2 = []
result3 = []
result4 = []

for t in commutator1:
    result1 += sqa.normalOrder(sqa.multiplyTerms(E_aiEbj2a, t))
    result2 += sqa.normalOrder(sqa.multiplyTerms(E_aiEbj2b, t))
for t in commutator2:
    result3 += sqa.normalOrder(sqa.multiplyTerms(E_aiEbj2a, t))
    result4 += sqa.normalOrder(sqa.multiplyTerms(E_aiEbj2b, t))

for t in result1+result2+result3+result4:
    t.contractDeltaFuncs_new()
sqa.removeVirtOps_sf(result1)
sqa.termChop(result1)
sqa.combineTerms(result1)
sqa.removeVirtOps_sf(result2)
sqa.termChop(result2)
sqa.combineTerms(result2)
sqa.removeVirtOps_sf(result3)
sqa.termChop(result3)
sqa.combineTerms(result3)
sqa.removeVirtOps_sf(result4)
sqa.termChop(result4)
sqa.combineTerms(result4)

extendedR1=[]
for t in result1:
    extendedR1 += sqa.contractCoreOps_sf(t)
for t in extendedR1:
    t.contractDeltaFuncs_new()
sqa.termChop(extendedR1)
sqa.combineTerms(extendedR1)

extendedR2=[]
for t in result2:
    extendedR2 += sqa.contractCoreOps_sf(t)
for t in extendedR2:
    t.contractDeltaFuncs_new()
sqa.termChop(extendedR2)
sqa.combineTerms(extendedR2)

extendedR3=[]
for t in result3:
    extendedR3 += sqa.contractCoreOps_sf(t)
for t in extendedR3:
    t.contractDeltaFuncs_new()
sqa.termChop(extendedR3)
sqa.combineTerms(extendedR3)

extendedR4=[]
for t in result4:
    extendedR4 += sqa.contractCoreOps_sf(t)
for t in extendedR4:
    t.contractDeltaFuncs_new()
sqa.termChop(extendedR4)
sqa.combineTerms(extendedR4)



result1 = []
result2 = []
result3 = []
result4 = []
rdmDelta = [deltaC, deltaA, deltaV]

#********this adds delta funcstion when we have repeat indices****************#
for r in extendedR1:
    result1.append(geraldCode.replaceRepeatIndicesWithDeltas(r, rdmDelta))
for r in extendedR2:
    result2.append(geraldCode.replaceRepeatIndicesWithDeltas(r, rdmDelta))
for r in extendedR3:
    result3.append(geraldCode.replaceRepeatIndicesWithDeltas(r, rdmDelta))
for r in extendedR4:
    result4.append(geraldCode.replaceRepeatIndicesWithDeltas(r, rdmDelta))


print "//Number of terms : ", len(result1+result2+result3+result4)


print "\tFEqInfo EqsRes[%i] = {\n"%(len(result1+result2+result3+result4))
geraldCode.WriteCode_lcc(result1, AllTensors, ["Ci", "Ap", "Aq", "Va"], "JRSB", CommentKey,"p1", "Ap1")
print "//"
geraldCode.WriteCode_lcc(result2, AllTensors, ["Ci", "Ap", "Aq", "Va"], "JRSB", CommentKey,"p1", "Ap2")
print "//"
geraldCode.WriteCode_lcc(result3, AllTensors, ["Ci", "Ap", "Aq", "Va"], "JRSB", CommentKey,"p2", "Ap1")
print "//"
geraldCode.WriteCode_lcc(result4, AllTensors, ["Ci", "Ap", "Aq", "Va"], "JRSB", CommentKey,"p2", "Ap2")
print "\n\t};"

b1index = AllTensors.index("b1")
b2index = AllTensors.index("b2")
W1index = AllTensors.index("V1")
W2index = AllTensors.index("V2")
E1index = AllTensors.index("E1")
E2index = AllTensors.index("E2")

print pDomains
print	"\tFEqInfo Overlap[8] = {"
print		"\t\t{\"IPSA,QS,APIQ\",   2.0, 3, {%i, %i, %i}},"%(b1index, E1index, W1index)
print	        "\t\t{\"IRSA,PSQR,APIQ\", 2.0, 3, {%i, %i, %i}},"%(b1index, E2index, W1index) 

print		"\t\t{\"IPSA,QS,APIQ\",  -1.0, 3, {%i, %i, %i}},"%(b2index, E1index, W1index) 
print		"\t\t{\"IRSA,PSQR,APIQ\",-1.0, 3, {%i, %i, %i}},"%(b2index, E2index, W1index)

print		"\t\t{\"IPSA,QS,PAIQ\",  -1.0, 3, {%i, %i, %i}},"%(b1index, E1index, W2index) 
print		"\t\t{\"IRSA,PSQR,PAIQ\",-1.0, 3, {%i, %i, %i}},"%(b1index, E2index, W2index)

print		"\t\t{\"IPSA,QS,PAIQ\",   2.0, 3, {%i, %i, %i}},"%(b2index, E1index, W2index) 
print		"\t\t{\"IRSA,PSRQ,PAIQ\",-1.0, 3, {%i, %i, %i}},"%(b2index, E2index, W2index)
print	"\t};"
print	"\tstatic void GetMethodInfo(FMethodInfo &Out) {"
print	      "\t\tOut = FMethodInfo();"
print	      "\t\tOut.pName = \"MRLCC_CAAV\";"
print         "\t\tOut.perturberClass = \"CAAV\";"
print	      "\t\tOut.pSpinClass = \"restricted\";"
print	      "\t\tOut.pTensorDecls = &TensorDecls[0];"
print	      "\t\tOut.nTensorDecls = %i;"%(len(Usage))
print	      "\t\tOut.pDomainDecls = &DomainDecls[0];"
print	      "\t\tOut.nDomainDecls = 1;"
print	      "\t\tOut.EqsRes = FEqSet(&EqsRes[0], %i, \"MRLCC_CAAV/Res\");"%(len(result1+result2+result3+result4))
print	      "\t\tOut.Overlap = FEqSet(&Overlap[0], 8, \"MRLCC_CAAV/Overlap\");"
print	"\t};"
print "};"


'''
print
print
intmapkey = {"Va" : "nc:", "Vb" : "nc:", "Vc" : "nc:", "Vd" : "nc:", "a" : ":ncore", "b" : ":ncore", "c" : ":ncore", "d" : ":ncore"}
RDMmapkey = {"a" : ":", "b" : ":", "c" : ":", "d" : ":"}

writeCode.WriteCode_caav(extendedR, True, intmapkey, RDMmapkey, True)

exit(0)
'''
