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
V_CA1 = sqa.tensor('int2', [i1,x1, i2,x2], [Dsym_a, Dsym_b, Dsym_c])
V_CA2 = sqa.tensor('int2', [i1,x1, x2,i2], [Dsym_a, Dsym_b, Dsym_c])

V_CV1 = sqa.tensor('int2', [i1,a1, i2,a2], [Dsym_a, Dsym_b, Dsym_c])
V_CV2 = sqa.tensor('int2', [i1,a1, a2,i2], [Dsym_a, Dsym_b, Dsym_c])

V_AV1 = sqa.tensor('int2', [x1,a1, x2,a2], [Dsym_a, Dsym_b, Dsym_c])
V_AV2 = sqa.tensor('int2', [x1,a1, a2,x2], [Dsym_a, Dsym_b, Dsym_c])

V_C = sqa.tensor('int2', [i1,i2, i3,i4], [Dsym_a, Dsym_b, Dsym_c])
V_A = sqa.tensor('int2', [x1,x2, x3,x4], [Dsym_a, Dsym_b, Dsym_c])
V_V = sqa.tensor('int2', [a1,a2, a3,a4], [Dsym_a, Dsym_b, Dsym_c])

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
E_aiEbj  = sqa.term( 1.0, [""],  [sqa.sfExOp([p, i]) , sqa.sfExOp([a,j])])
E_aiEbj2 = sqa.term( 1.0, [""],  [sqa.sfExOp([l, b]) , sqa.sfExOp([k,q])])

result = sqa.normalOrder(sqa.multiplyTerms(E_aiEbj2, E_aiEbj))

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

