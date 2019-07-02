import secondQuantizationAlgebra as sqa
import writeCode

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
K_C = sqa.tensor('int1', [i1,i2], [hsym])
K_A = sqa.tensor('int1', [x1,x2], [hsym])
K_V = sqa.tensor('int1', [a1,a2], [hsym])
V_A = sqa.tensor('int2', [x1,x2, x3,x4], [Dsym_a, Dsym_b, Dsym_c])


HD_A   = sqa.term( 0.5, [""], [V_A,   sqa.sfExOp([x1,x2,x3,x4])] )
T_C    = sqa.term( 1.0, [""], [K_C,   sqa.sfExOp([i1,i2])] )
T_A    = sqa.term( 1.0, [""], [K_A,   sqa.sfExOp([x1,x2])] )
T_V    = sqa.term( 1.0, [""], [K_V,   sqa.sfExOp([a1,a2])] )



#first excitation
E_aiEbj  = sqa.term( 1.0, [""],  [sqa.sfExOp([a, i]) , sqa.sfExOp([b,j])])
E_aiEbj2 = sqa.term( 1.0/3.0, [""],  [sqa.sfExOp([k, d]) , sqa.sfExOp([l,c])])
E_aiEbj3 = sqa.term( 0.5/3.0, [""],  [sqa.sfExOp([l, d]) , sqa.sfExOp([k,c])])

commutator = []
commutator +=  sqa.commutator(HD_A, E_aiEbj)
commutator +=  sqa.commutator(T_C, E_aiEbj)
commutator +=  sqa.commutator(T_A, E_aiEbj)
commutator +=  sqa.commutator(T_V, E_aiEbj)
result = []

for t in commutator:
    result += sqa.normalOrder(sqa.multiplyTerms(E_aiEbj2, t))
    result += sqa.normalOrder(sqa.multiplyTerms(E_aiEbj3, t))

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
for t in extendedR:
    print t

print
print
intmapkey = {"Va" : "nc:", "Vb" : "nc:", "Vc" : "nc:", "Vd" : "nc:", "a" : ":ncore", "b" : ":ncore", "c" : ":ncore", "d" : ":ncore"}
RDMmapkey = {"a" : ":", "b" : ":", "c" : ":", "d" : ":"}

writeCode.WriteCode(extendedR, True, intmapkey, RDMmapkey)

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


'''
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
