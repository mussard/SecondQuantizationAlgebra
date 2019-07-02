import secondQuantizationAlgebra as sqa

sqa.options.verbose = False
# definitions

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

pDomains  = "\tint f(int i) {\n"
pDomains += "\t\treturn 2*i;\n"
pDomains += "\t}\n"
pDomains += "\tFDomainDecl DomainDecls[1] = {\n"
pDomains += "\t\t{\"A\", \"a\", f}\n"
pDomains += "\t};"
CommentKey = {}

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

Cin = sqa.tensor("p", [a,b,c,d], [Dsym_c])
Cout = sqa.tensor("Ap", [c,d,r,s], [Dsym_c])

#first excitation
E_aiEbj  = sqa.term( 1.0, [""],  [sqa.sfExOp([a, p]) , sqa.sfExOp([b,q])])
E_aiEbj2 = sqa.term( 1.0, [""],  [sqa.sfExOp([s, d]) , sqa.sfExOp([r,c])])

result = []


result += sqa.normalOrder(sqa.multiplyTerms(sqa.term(1.0, [""], [Cin]), sqa.multiplyTerms(E_aiEbj2, E_aiEbj)))


for t in result:
    t.contractDeltaFuncs_new()

sqa.removeVirtOps_sf(result)
for t in result:
    print t
sqa.termChop(result)
sqa.combineTerms(result)

print result
for t in result:
    print t
exit(0)

extendedR=[]
for t in result:
    extendedR += sqa.contractCoreOps_sf(t)
for t in extendedR:
    t.contractDeltaFuncs_new()
sqa.termChop(extendedR)
sqa.combineTerms(extendedR)

result = []
rdmDelta = [deltaC, deltaA, deltaV]
