import secondQuantizationAlgebra as sqa

sqa.options.verbose = False
# definitions

tag_core    = sqa.options.core_type
tag_active  = sqa.options.active_type
tag_virtual = sqa.options.virtual_type


a  = sqa.index('Va',  [tag_virtual], False)
b  = sqa.index('Vb',  [tag_virtual], False)
i  = sqa.index('Ci',  [tag_core],  False)
j  = sqa.index('Cj',  [tag_core],  False)
p  = sqa.index('Ap',  [tag_active],  False)
q  = sqa.index('Aq',  [tag_active], False)

c = sqa.index('Vc', [tag_virtual], False)
k = sqa.index('Ck', [tag_core],  False)
d = sqa.index('Vd', [tag_virtual], False)
l = sqa.index('Cl', [tag_core],  False)

r = sqa.index('Ar', [tag_active],  False)
s = sqa.index('As', [tag_active], False)

u  = sqa.index('Au',  [tag_active],  True)
v  = sqa.index('Av',  [tag_active],  True)
w  = sqa.index('Aw',  [tag_active],  True)
x  = sqa.index('Ax',  [tag_active],  True)

g  = sqa.index('Vg',  [tag_virtual],  True)
h  = sqa.index('Vh',  [tag_virtual],  True)
e  = sqa.index('Ve',  [tag_virtual],  True)
f  = sqa.index('Vf',  [tag_virtual],  True)


#h0 one body term
hsym   = sqa.symmetry((1,0), 1)
Dsym_a = sqa.symmetry((2,1, 0,3), 1)
Dsym_b = sqa.symmetry((0,3, 2,1), 1)
Dsym_c = sqa.symmetry((1,0, 3,2), 1)
V_kl = sqa.tensor('int1', [u,v], [hsym])
V_cd = sqa.tensor('int1', [e,f], [hsym])
V_klcd1 = sqa.tensor('int2', [u,e, v,f], [Dsym_a, Dsym_b, Dsym_c])
V_klcd2 = sqa.tensor('int2', [u,e, f,v], [Dsym_a, Dsym_b, Dsym_c])
V_klcd3 = sqa.tensor('int2', [e,u, f,v], [Dsym_a, Dsym_b, Dsym_c])
V_klcd4 = sqa.tensor('int2', [e,u, v,f], [Dsym_a, Dsym_b, Dsym_c])
V_klmn = sqa.tensor('int2', [u,v, w,x], [Dsym_a, Dsym_b, Dsym_c])
V_cdef = sqa.tensor('int2', [e,f, g,h], [Dsym_a, Dsym_b, Dsym_c])
#V_uvwx = sqa.tensor('int2', [u,v, w,x], [Dsym_a, Dsym_b, Dsym_c])

HD1 = sqa.term( 0.5, ["V1"], [V_klmn, sqa.sfExOp([u,v,w,x])] )
HD2a = sqa.term( 0.5, ["V2"], [V_klcd1, sqa.sfExOp([u,e,v,f])] )
HD2b = sqa.term( 0.5, ["V2"], [V_klcd2, sqa.sfExOp([u,e,f,v])] )
HD2c = sqa.term( 0.5, ["V2"], [V_klcd3, sqa.sfExOp([e,u,f,v])] )
HD2d = sqa.term( 0.5, ["V2"], [V_klcd4, sqa.sfExOp([e,u,v,f])] )
HD3 = sqa.term( 0.5, ["V3"], [V_cdef, sqa.sfExOp([e,f,g,h])] )
HD4 = sqa.term( 1.0, ["ta"], [V_kl, sqa.sfExOp([u,v])] )
HD5 = sqa.term( 1.0, ["tb"], [V_cd, sqa.sfExOp([e,f])] )



#first excitation
E_aiEbj  = sqa.term( 1.0, ["EaiEbj"],  [sqa.sfExOp([a, p]) , sqa.sfExOp([b,q])])
E_aiEbj2 = sqa.term( 1.0, ["EapipEbpjp"],  [sqa.sfExOp([s, d]) , sqa.sfExOp([r,c])])

result = sqa.normalOrder(sqa.multiplyTerms(E_aiEbj2, E_aiEbj))

for t in result:
    t.contractDeltaFuncs_new()

sqa.removeVirtOps_sf(result)
sqa.termChop(result)
#sqa.removeCoreOps_sf(result)
sqa.combineTerms(result)


for r in result:
    print r


'''
for t in result:
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
