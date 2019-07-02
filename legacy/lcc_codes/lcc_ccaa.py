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

ampstring = "ccaa" #amplitude string
AllTensors = ["t", "R", "int1c", "int1a", "int1v", "int2ca1", "int2ca2",\
              "int2cv1", "int2cv2", "int2av1", "int2av2", "int2c", "int2a", "int2v",\
              "E1", "E2", "E3", "S1", "S2", "T", "b", "p", "Ap",\
              "P", "AP", "B", "V", "deltac", "deltaa", "deltav"]
CommentTensors = ["t", "R", "k", "k", "k", "W", "W",\
                  "W", "W", "W", "W", "W", "W", "W",\
                  "E1", "E2", "E3", "S1", "S2", "T", "b", "p", "Ap",\
                  "P", "AP", "B", "W", "delta", "delta", "delta"]
Domains = [ampstring, ampstring, "cc", "aa", "ee", "caca", "caac",\
           "cece", "ceec", "aeae", "aeea", "cccc", "aaaa", "eeee",\
           "aa", "aaaa", "aaaaaa", "aaaa", "aaaa", ampstring, ampstring, ampstring, ampstring,\
           ampstring, ampstring, ampstring, ampstring, "cc", "aa", "ee"]
Usage = ["A", "R", "H", "H", "H", "H", "H",\
         "H", "H", "H", "H", "H", "H", "H",\
         "D", "D", "D", "D", "D", "A", "A", "A", "A",\
         "A", "A", "A", "H", "D", "D", "D"]

pDomains  = "\tint f(int i) {\n"
pDomains += "\t\treturn 2*i;\n"
pDomains += "\t}\n"
pDomains += "\tFDomainDecl DomainDecls[0] = {\n"
#pDomains += "\t\t{\"A\", \"a\", f}\n"
pDomains += "\t};"
CommentKey = {}
print "namespace MRLCC_CCAA {\n"
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
E_aiEbj  = sqa.term( 1.0, [""],  [sqa.sfExOp([p, i]) , sqa.sfExOp([q,j])])
E_aiEbj2 = sqa.term( 1.0, [""],  [sqa.sfExOp([l, s]) , sqa.sfExOp([k,r])])


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
#for t in extendedR:
#    print t

result = []
rdmDelta = [deltaC, deltaA, deltaV]


#********this adds delta funcstion when we have repeat indices****************#
for r in extendedR:
    result.append(geraldCode.replaceRepeatIndicesWithDeltas(r, rdmDelta))



print "//Number of terms : ", len(result)

print "\tFEqInfo EqsRes[%i] = {\n"%(len(result))
geraldCode.WriteCode_lcc(result, AllTensors, ["Ci", "Cj", "Ap", "Aq"], "KLRS", CommentKey, "p", "Ap")
print "\n\t};"

resultO = sqa.normalOrder(sqa.multiplyTerms(E_aiEbj2, E_aiEbj))
for t in resultO:
    t.contractDeltaFuncs_new()
sqa.removeVirtOps_sf(resultO)
sqa.termChop(resultO)
sqa.combineTerms(resultO)
extendedR=[]
for t in resultO:
    extendedR += sqa.contractCoreOps_sf(t)
for t in extendedR:
    t.contractDeltaFuncs_new()
sqa.termChop(extendedR)
sqa.combineTerms(extendedR)
resultO = []
rdmDelta = [deltaC, deltaA, deltaV]
#********this adds delta funcstion when we have repeat indices****************#
for r in extendedR:
    resultO.append(geraldCode.replaceSingleKdeltaWithDeltas(r, rdmDelta))


#print "\tFEqInfo "+EquationName+"[%i] = {\n"%(len(result))
print "\tFEqInfo Overlap[%i] = {\n"%(len(result))
geraldCode.WriteCode_lcc(resultO, AllTensors, ["Ci", "Cj", "Ap", "Aq"], "KLRS", CommentKey, "V", "b", "Overlap", 0.5)
print "\n\t};"

resultO = []
for r in extendedR:
    resultO.append(geraldCode.replaceAllKdeltaWithDeltas(r, rdmDelta))
#    print resultO[-1]
#geraldCode.WriteCode_lcc(resultO, AllTensors, [], "PQRS", CommentKey, "", "S1", "MakeS1")

print"        FEqInfo MakeS1[7] = {"
print"                {\"PQRS,PR,QS\", 4.0  , 3, {17,28,28}},           //S1[PQRS] += 4.0 delta[PR] delta[QS] delta[IK] delta[JL] []"
print"                {\"PQRS,PS,QR\", -2.0  , 3, {17,28,28}},          //S1[PQRS] += -2.0 delta[PR] delta[QS] delta[IL] delta[JK] []"
print"                {\"PQRS,QS,PR\", -2.0  , 3, {17,14,28}},          //S1[PQRS] += -2.0 E1[QS] delta[PR] delta[IK] delta[JL] []"
print"                {\"PQRS,QR,PS\", 1.0  , 3, {17,14,28}},           //S1[PQRS] += 1.0 E1[PR] delta[QS] delta[IL] delta[JK] []"
print"                {\"PQRS,PS,QR\", 1.0  , 3, {17,14,28}},           //S1[PQRS] += 1.0 E1[QS] delta[PR] delta[IL] delta[JK] []"
print"                {\"PQRS,PR,QS\", -2.0  , 3, {17,14,28}},          //S1[PQRS] += -2.0 E1[PR] delta[QS] delta[IK] delta[JL] []"
print"                {\"PQRS,PQRT,TS\", 1.0  , 3, {17,15,28}},                 //S1[PQRS] += 1.0 E2[PQRS] delta[IK] delta[JL] []"
print"        };"
print"        FEqInfo MakeS2[14] = {"
print"                {\"PQRS,PR,QS\", 4.0  , 5, {18,28,28}},           //S1[PQRS] += 4.0 delta[PR] delta[QS] delta[IK] delta[JL] []"
print"                {\"PQRS,PR,QS\", -2.0  , 5, {18,28,28}},          //S1[PQRS] += -2.0 delta[PR] delta[QS] delta[IL] delta[JK] []"
print"                {\"PQRS,PS,QR\", -2.0  , 5, {18,28,28}},          //S1[PQRS] += -2.0 delta[PS] delta[QR] delta[IK] delta[JL] []"
print"                {\"PQRS,PS,QR\", 4.0  , 5, {18,28,28}},           //S1[PQRS] += 4.0 delta[PS] delta[QR] delta[IL] delta[JK] []"
print"                {\"PQRS,QS,PR\", -2.0  , 5, {18,14,28}},          //S1[PQRS] += -2.0 E1[QS] delta[PR] delta[IK] delta[JL] []"
print"                {\"PQRS,QS,PR\", 1.0  , 5, {18,14,28}},           //S1[PQRS] += 1.0 E1[QS] delta[PR] delta[IL] delta[JK] []"
print"                {\"PQRS,QR,PS\", 1.0  , 5, {18,14,28}},           //S1[PQRS] += 1.0 E1[QR] delta[PS] delta[IK] delta[JL] []"
print"                {\"PQRS,QR,PS\", -2.0  , 5, {18,14,28}},          //S1[PQRS] += -2.0 E1[QR] delta[PS] delta[IL] delta[JK] []"
print"                {\"PQRS,PS,QR\", 1.0  , 5, {18,14,28}},           //S1[PQRS] += 1.0 E1[PS] delta[QR] delta[IK] delta[JL] []"
print"                {\"PQRS,PS,QR\", -2.0  , 5, {18,14,28}},          //S1[PQRS] += -2.0 E1[PS] delta[QR] delta[IL] delta[JK] []"
print"                {\"PQRS,PR,QS\", -2.0  , 5, {18,14,28}},          //S1[PQRS] += -2.0 E1[PR] delta[QS] delta[IK] delta[JL] []"
print"                {\"PQRS,PR,QS\", 1.0  , 5, {18,14,28}},           //S1[PQRS] += 1.0 E1[PR] delta[QS] delta[IL] delta[JK] []"
print"                {\"PQRS,PQRT,TS\", 1.0  , 4, {18,15,28}},         //S1[PQRS] += 1.0 E2[PQRS] delta[IK] delta[JL] []"
print"                {\"PQRS,PQTR,TS\", 1.0  , 4, {18,15,28}},         //S1[PQRS] += 1.0 E2[PQSR] delta[IL] delta[JK] []"
print"        };"


print	"\tstatic void GetMethodInfo(FMethodInfo &Out) {"
print	      "\t\tOut = FMethodInfo();"
print	      "\t\tOut.pName = \"MRLCC_CCAA\";"
print         "\t\tOut.perturberClass = \"CCAA\";"
print	      "\t\tOut.pSpinClass = \"restricted\";"
print	      "\t\tOut.pTensorDecls = &TensorDecls[0];"
print	      "\t\tOut.nTensorDecls = %i;"%(len(Usage))
print	      "\t\tOut.nDomainDecls = 0;"
print	      "\t\tOut.EqsRes = FEqSet(&EqsRes[0], %i, \"MRLCC_CCAA/Res\");"%(len(result))
print	      "\t\tOut.Overlap = FEqSet(&Overlap[0], %i, \"MRLCC_CCAA/Overlap\");"%(len(resultO))
print	      "\t\tOut.MakeS1 = FEqSet(&MakeS1[0], 7, \"MRLCC_CCAA/Overlap\");"
print	      "\t\tOut.MakeS2 = FEqSet(&MakeS2[0], 14, \"MRLCC_CCAA/Overlap\");"
print	"\t};"
print "};"

'''
print
print
intmapkey = {"Va" : "nc:", "Vb" : "nc:", "Vc" : "nc:", "Vd" : "nc:", "a" : ":ncore", "b" : ":ncore", "c" : ":ncore", "d" : ":ncore"}
RDMmapkey = {"a" : ":", "b" : ":", "c" : ":", "d" : ":"}

writeCode.WriteCode_ccaa(extendedR, True, intmapkey, RDMmapkey, True)

exit(0)

extendedR = []
for t in result :
    tensorE = t.tensors[-1]
    del t.tensors[-1]

    Eterm = sqa.term(1.0, ["E"], [tensorE])
    r = sqa.extendedNormalOrder(Eterm)
    for rterm in r:
        r2 = sqa.multiplyTerms(t, rterm)
        r2.contractDeltaFuncs_new()
        extendedR.append(r2)

sqa.combineTerms(extendedR)
for t in extendedR:
    print t
print



for t in extendedR:
    tensorString = ""
    ifstatement = "if "

    for tensor in t.tensors:
        if (tensor.name == "kdelta"):
            ifstatement += "  "+ tensor.indices[0].name+ " == "+ tensor.indices[1].name + " and"
        else :
            tensorString += "es('"
            for index in tensor.indices:
                tensorString += index.name[-1]
            tensorString +=",ab->cd', "+tensor.__str__()+", Cin)"

    print ifstatement[:-3], ":"
    print "\t Cout[Vc,Vd] += (", t.numConstant, ") *" , tensorString
'''
