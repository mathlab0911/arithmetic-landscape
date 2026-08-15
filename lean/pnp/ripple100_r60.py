# ripple100_r60.py (2026-08-09, opus-5 60周目) : 外部評価 gemini 2.1 への対応。
# prop:ripple(K₂)の照合範囲を k=18..40 から k ≤ 100 に拡張する。
# 測定手続きは k2psi_r20.py と同一(r_B は厳密整数の DP、窓 hw を振る=V3)。
import math, cmath, sys
def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(n+1) if s[i]]
ALLP=[p for p in primes_upto(20000) if p%2==1]
SQ=math.sqrt(3)/2
def rep_counts(B):
    tot=sum(B); r=[0]*(tot+1); r[0]=1
    for a in B:
        for m in range(tot,a-1,-1):
            if r[m-a]: r[m]+=r[m-a]
    return r
def arith(B):
    tau=lambda a: 1 if a%6==1 else (-1 if a%6==5 else 0)
    return (sum(tau(a)*a for a in B), sum(tau(a)*a**3 for a in B), sum(B),
            sum(a*a for a in B), sum(a**4 for a in B),
            sum(1 for a in B if a%6==1), sum(1 for a in B if a%6==5))
def expoK2(B):
    D,D3,S1,S2,S4,c1,c5 = arith(B)
    return (D*D/(8.0*S2) - (3.0/8.0)*S4/S2**2 + D*D3/(4.0*S2**2)
            + (5.0/24.0)*D3*D3/S2**3 - 3.0*S4*D*D/(16.0*S2**3))
def dft(B,r,center,hw=24,q=6):
    b=len(B); S=sum(B); V0=sum(a*a for a in B)/4.0
    N=(2*hw//q)*q; acc=0j; used=0
    for t in range(N):
        m=center-N//2+t
        if m<0 or m>=len(r) or r[m]==0: continue
        d=m-S/2.0
        lg=b*math.log(2)-0.5*math.log(2*math.pi*V0)-d*d/(2*V0)
        acc+=(r[m]/math.exp(lg)-1.0)*cmath.exp(-2j*math.pi*m/q); used+=1
    C=(2.0/used)*acc
    return abs(C), -cmath.phase(C)

KS=list(range(18,41,2))+list(range(44,101,4))
print("="*112)
print("[gemini 2.1 対応] リップル公式 K₂ の照合を k ≤ 100 に拡張(r_B は厳密整数の DP)")
print("="*112)
print("  k    b   c1−c5   実測/K₂ (hw=24)  実測/K₂ (hw=96)   枝    |比−1| (hw=24)")
rows=[]
for k in KS:
    B=[a for a in ALLP[:k] if a>4]; b=len(B)
    r=rep_counts(B)
    D,D3,S1,S2,S4,c1,c5=arith(B)
    out={}
    for hw in (24,96):
        amp,ph=dft(B,r,S1//2,hw)
        out[hw]=(amp/(2*SQ**(b+1)))/math.exp(expoK2(B))
    br='B' if (c1-c5)<=-3 else 'A'
    rows.append((k,b,c1-c5,out[24],out[96],br))
    print(f" {k:4d} {b:4d}  {c1-c5:+5d}     {out[24]:9.4f}        {out[96]:9.4f}      {br}"
          f"     {abs(out[24]-1):.5f}")
    sys.stdout.flush()
print()
old=[x for x in rows if x[0]<=40]; new=[x for x in rows if x[0]>40]
for lab,S in (("k ≤ 40(従来の範囲)",old),("k > 40(今回の拡張)",new),("全体",rows)):
    e24=[abs(x[3]-1) for x in S]; e96=[abs(x[4]-1) for x in S]
    print(f"  {lab:22s}  hw=24: 平均 {sum(e24)/len(e24):.5f} 最大 {max(e24):.5f}"
          f"   |  hw=96: 平均 {sum(e96)/len(e96):.5f} 最大 {max(e96):.5f}   (n={len(S)})")
print()
print("  ※ 論文の主張は「k=18..40 で 0.1% 以内」。上の『全体』が 0.001 台に収まれば主張を拡張できる。")
