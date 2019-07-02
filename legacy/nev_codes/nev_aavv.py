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
K_C = sqa.tensor('int1a', [i1,i2], [hsym])
K_A = sqa.tensor('int1b', [x1,x2], [hsym])
K_V = sqa.tensor('int1c', [a1,a2], [hsym])
V_A = sqa.tensor('int2d', [x1,x2, x3,x4], [Dsym_a, Dsym_b, Dsym_c])


HD_A   = sqa.term( 0.5, [""], [V_A,   sqa.sfExOp([x1,x2,x3,x4])] )
T_C    = sqa.term( 1.0, [""], [K_C,   sqa.sfExOp([i1,i2])] )
T_A    = sqa.term( 1.0, [""], [K_A,   sqa.sfExOp([x1,x2])] )
T_V    = sqa.term( 1.0, [""], [K_V,   sqa.sfExOp([a1,a2])] )

Tensorstring = "namespace NEVPT_AAVV {\n"+\
"\tFTensorDecl TensorDecls[6] = {\n"+\
"\t\t /* 0 */ {\"t\", \"vvaa\", \"01/23\", USAGE_Amplitude},\n"+\
"\t\t /* 1 */ {\"r\", \"vvaa\", \"01/23\", USAGE_Residual},\n"+\
"\t\t /* 2 */ {\"t\", \"cc\", \"01\", USAGE_Hamiltonian},\n"+\
"\t\t /* 3 */ {\"t\", \"aa\", \"01\", USAGE_Hamiltonian},\n"+\
"\t\t /* 4 */ {\"t\", \"vv\", \"01\", USAGE_Hamiltonian},\n"+\
"\t\t /* 5 */ {\"E1\", \"aa\", \"01\", USAGE_Density},\n"+\
"\t\t /* 6 */ {\"E2\", \"aaaa\", \"01/23\", USAGE_Density},\n"+\
"\t\t /* 7 */ {\"E3\", \"aaaaaa\", \"012/345\", USAGE_Density},\n"+\
"\t\t /* 8 */ {\"W\", \"aaaa\", \"01/23\", USAGE_Hamiltonian},\n"+\
"\t\t /* 9 */ {\"W\", \"eeaa\", \"01/23\", USAGE_Hamiltonian}\n\t};"

tensors = {"Cin":0, "Cout":1, "int1a":2, "int1b":3, "int1c":4, "E1":5, "E2":6, "E3":7, "int2d":8}
#first excitation
E_aiEbj  = sqa.term( 1.0, [""],  [sqa.sfExOp([a, p]) , sqa.sfExOp([b,q])])
E_aiEbj2 = sqa.term( 1.0, [""],  [sqa.sfExOp([s, d]) , sqa.sfExOp([r,c])])

commutator = []
commutator +=  sqa.commutator(HD_A, E_aiEbj)
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

result = extendedR
#for r in result:
#    print "Cout[Vc, Vd, Ar, As] =  ", r, " * Cin[Va, Vb, Ap, Aq]"


intmapkey = {"Va" : "nc:", "Vb" : "nc:", "Vc" : "nc:", "Vd" : "nc:", "a" : "ncore:nact", "b" : "ncore:nact", "c" : "ncore:nact", "d" : "ncore:nact"}
RDMmapkey = {"a" : ":", "b" : ":", "c" : ":", "d" : ":"}

print "//Number of terms : ", len(result)
#writeCode.WriteCode(result, False, intmapkey, RDMmapkey)
print Tensorstring
print "\tFEqInfo EqsRes[%i] = {"%(len(result))
geraldCode.WriteCode(result, tensors)

print"\tstatic void GetMethodInfo(FMethodInfo &Out) {"
print"\t      Out = FMethodInfo();"
print"\t      Out.pName = \"NEVPT_AAVV\";"
print"\t      Out.pSpinClass = \"restricted\";"
print"\t      Out.pTensorDecls = &TensorDecls[0];"
print"\t      Out.nTensorDecls = 10;"
print"\t      Out.EqsRes = FEqSet(&EqsRes[0], %i, \"NEVPT_AAVV/Res\");"%(len(result))
print"\t}"
print"}"

