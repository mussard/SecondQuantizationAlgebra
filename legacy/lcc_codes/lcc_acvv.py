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

ampstring = "eeca" #amplitude string
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
           "aa", "aaaa", "aaaaaa", "AA", "aa", ampstring, ampstring, ampstring, ampstring,\
           ampstring, ampstring, ampstring, ampstring, "cc", "aa", "ee"]
Usage = ["A", "R", "H", "H", "H", "H", "H",\
         "H", "H", "H", "H", "H", "H", "H",\
         "D", "D", "D", "D", "D", "A", "A", "A", "A",\
         "A", "A", "A", "H", "D", "D", "D"]

pDomains  = "\tint f(int i) {\n"
pDomains += "\t\treturn 2*i;\n"
pDomains += "\t}\n"
pDomains += "\tFDomainDecl DomainDecls[1] = {\n"
pDomains += "\t\t{\"A\", \"a\", f}\n"
pDomains += "\t};"
CommentKey = {}
print "namespace MRLCC_ACVV {\n"
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
E_aiEbj  = sqa.term( 1.0, [""],  [sqa.sfExOp([a, i]) , sqa.sfExOp([b,q])])
E_aiEbj2 = sqa.term( 1.0, [""],  [sqa.sfExOp([r, d]) , sqa.sfExOp([j,c])])

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
#    result += sqa.normalOrder(sqa.multiplyTerms(E_aiEbj3, t))

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


#for r in result:    
#    print "Cout[Vc, Vd, Ci, Aq] =  ", r, " * Cin[Va, Vb, Cj, Ar]"


print "//Number of terms : ", len(result)
#writeCode.WriteCode(result, True, intmapkey, RDMmapkey)


#print "\tFEqInfo "+EquationName+"[%i] = {\n"%(len(result))
print "\tFEqInfo EqsRes[%i] = {\n"%(len(result))
geraldCode.WriteCode_lcc(result, AllTensors, ["Va", "Vb", "Ci", "Aq"], "CDJR", CommentKey)
print "\n\t};"

bindex = AllTensors.index("b")
Vindex = AllTensors.index("V")
E1index = AllTensors.index("E1")

#abir,rp->abip
#abir,rp->baip
print pDomains
print	"\tFEqInfo Overlap[2] = {"
print		"\t\t{\"ABIP,RP,ABIR\", 2.0, 3, {%i, %i, %i}},"%(bindex, E1index, Vindex)
print		"\t\t{\"ABIP,RP,BAIR\",-1.0, 3, {%i, %i, %i}}"%(bindex, E1index, Vindex)
print	"\t};"

print	"\tstatic void GetMethodInfo(FMethodInfo &Out) {"
print	      "\t\tOut = FMethodInfo();"
print	      "\t\tOut.pName = \"MRLCC_ACVV\";"
print         "\t\tOut.perturberClass = \"ACVV\";"
print	      "\t\tOut.pSpinClass = \"restricted\";"
print	      "\t\tOut.pTensorDecls = &TensorDecls[0];"
print	      "\t\tOut.nTensorDecls = %i;"%(len(Usage))
print	      "\t\tOut.pDomainDecls = &DomainDecls[0];"
print	      "\t\tOut.nDomainDecls = 1;"
print	      "\t\tOut.EqsRes = FEqSet(&EqsRes[0], %i, \"MRLCC_ACVV/Res\");"%(len(result))
print	      "\t\tOut.Overlap = FEqSet(&Overlap[0], 2, \"MRLCC_ACVV/Overlap\");"
print	"\t};"
print "};"
