# k2var_r20.py : Delta3^2 の係数 45/24 と 5/24 のどちらが正しいかを、
# S4*Delta^2 項を入れた上で A枝・B枝それぞれの残差で判定する。
exec(open('k2psi_r20.py').read().split('KS=list')[0])
KS=list(range(18,41,2))
def e2(B,c3,withS4):
    D,D3,S1,S2,S4,c1,c5=arith(B)
    e=D*D/(8.0*S2)-(3.0/8.0)*S4/S2**2+D*D3/(4.0*S2**2)+c3*D3*D3/S2**3
    if withS4: e+=-3.0*S4*D*D/(16.0*S2**3)
    return e
print("  Delta3^2係数  S4*Delta^2項  A枝|比-1|平均   A枝最大   B枝|比-1|平均   B枝最大   k=18の比")
for c3,lab in ((45.0/24,"45/24"),(5.0/24,"5/24")):
    for w in (False,True):
        A=[];Bb=[];k18=None
        for k in KS:
            B=[a for a in ALLP[:k] if a>4]; b=len(B)
            D,D3,S1,S2,S4,c1,c5=arith(B)
            r=rep_counts(B); amp,_=dft(B,r,sum(B)//2)
            v=amp/(2*SQ**(b+1))/math.exp(e2(B,c3,w))
            (Bb if (c1-c5)<=-3 else A).append(abs(v-1))
            if k==18: k18=v
        print(f"     {lab:6s}      {'あり' if w else 'なし':4s}      {sum(A)/len(A):.5f}    {max(A):.5f}"
              f"      {sum(Bb)/len(Bb):.5f}    {max(Bb):.5f}    {k18:.4f}")
print()
print("  注: k=18 は |Delta3^2/S2^3| が最大(1.0e-3)で、係数 45/24 vs 5/24 の差が最も効く点。")
print("      fable-5 は『数値影響 ~1e-6』としていたが、実際は k=18 で 1.7e-3(3桁の見積り違い)。")
