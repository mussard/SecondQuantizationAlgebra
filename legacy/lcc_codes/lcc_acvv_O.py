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
q  = sqa.index('Ap',  [tag_active],  False)
r  = sqa.index('Ar',  [tag_active],  False)


u  = sqa.index('Au',  [tag_active],  True)
v  = sqa.index('Av',  [tag_active],  True)
w  = sqa.index('Aw',  [tag_active],  True)
x  = sqa.index('Ax',  [tag_active],  True)
m  = sqa.index('Cm',  [tag_core],    True)
n  = sqa.index('Cn',  [tag_core],    True)
o  = sqa.index('Co',  [tag_core],    True)
p  = sqa.index('Cp',  [tag_core],    True)
g  = sqa.index('Vg',  [tag_virtual], True)
h  = sqa.index('Vh',  [tag_virtual], True)
e  = sqa.index('Ve',  [tag_virtual], True)
f  = sqa.index('Vf',  [tag_virtual], True)


#h0 one body term
hsym   = sqa.symmetry((1,0), 1)
Dsym_a = sqa.symmetry((2,1, 0,3), 1)
Dsym_b = sqa.symmetry((0,3, 2,1), 1)
Dsym_c = sqa.symmetry((1,0, 3,2), 1)
V_uv = sqa.tensor('int1', [u,v], [hsym])
V_kl = sqa.tensor('int1', [m,n], [hsym])
V_cd = sqa.tensor('int1', [e,f], [hsym])
V_klcd1 = sqa.tensor('int2', [m,e, n,f], [Dsym_a, Dsym_b, Dsym_c])
V_klcd2 = sqa.tensor('int2', [m,e, f,n], [Dsym_a, Dsym_b, Dsym_c])
V_klcd3 = sqa.tensor('int2', [m,u, n,v], [Dsym_a, Dsym_b, Dsym_c])
V_klcd4 = sqa.tensor('int2', [m,u, v,n], [Dsym_a, Dsym_b, Dsym_c])
V_klcd5 = sqa.tensor('int2', [u,e, n,v], [Dsym_a, Dsym_b, Dsym_c])
V_klcd6 = sqa.tensor('int2', [u,e, v,n], [Dsym_a, Dsym_b, Dsym_c])

V_klmn = sqa.tensor('int2', [m,n, o,p], [Dsym_a, Dsym_b, Dsym_c])
V_cdef = sqa.tensor('int2', [e,f, g,h], [Dsym_a, Dsym_b, Dsym_c])
V_uvwx = sqa.tensor('int2', [u,v, w,x], [Dsym_a, Dsym_b, Dsym_c])

HD1 = sqa.term( 0.5, [""], [V_klmn, sqa.sfExOp([m,n,o,p])] )
HD2 = sqa.term( 0.5, [""], [V_cdef, sqa.sfExOp([e,f,g,h])] )
HD3 = sqa.term( 0.5, [""], [V_uvwx, sqa.sfExOp([u,v,w,x])] )
HD2a = sqa.term( 1.0, [""], [V_klcd1, sqa.sfExOp([m,e,n,f])] )
HD2b = sqa.term( 1.0, [""], [V_klcd2, sqa.sfExOp([m,e,f,n])] )
HD2c = sqa.term( 1.0, [""], [V_klcd3, sqa.sfExOp([m,u,n,v])] )
HD2d = sqa.term( 1.0, [""], [V_klcd4, sqa.sfExOp([m,u,v,n])] )
HD2e = sqa.term( 1.0, [""], [V_klcd5, sqa.sfExOp([u,e,n,v])] )
HD2f = sqa.term( 1.0, [""], [V_klcd6, sqa.sfExOp([u,e,v,n])] )
HD4 = sqa.term( 1.0, [""], [V_kl, sqa.sfExOp([m,n])] )
HD5 = sqa.term( 1.0, [""], [V_cd, sqa.sfExOp([e,f])] )
HD6 = sqa.term( 1.0, [""], [V_uv, sqa.sfExOp([u,v])] )



#first excitation
E_aiEbj  = sqa.term( 1.0, [""],  [sqa.sfExOp([a, i]) , sqa.sfExOp([b,q])])
E_aiEbj2 = sqa.term( 1.0, [""],  [sqa.sfExOp([r, d]) , sqa.sfExOp([j,c])])


result = []

result+= sqa.normalOrder((sqa.multiplyTerms(E_aiEbj2, E_aiEbj)))


for t in result:
    t.contractDeltaFuncs_new()

sqa.removeVirtOps_sf(result)
sqa.termChop(result)
sqa.combineTerms(result)

extendedR=[]
for t in result:
    extendedR += sqa.contractCoreOps_sf(t)
for t in extendedR:
#    print t
    t.contractDeltaFuncs_new()
sqa.termChop(extendedR)
sqa.combineTerms(extendedR)
for t in extendedR:
    print t
print
print

#all core
#intmapkey = {"Va" : "nc:", "Vb" : "nc:", "Vc" : "nc:", "Vd" : "nc:", "a" : "ncore:nact", "b" : "ncore:nact", "c" : "ncore:nact", "d" : "ncore:nact"}
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
