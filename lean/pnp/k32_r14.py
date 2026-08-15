# k32_r14.py (2026-08-08, opus-5 9周目)
# 持ち越し3: k=32 で振幅比が 1.025 と外れる原因の数値調査。
#   容疑者: (a) c1-c5 の変化で位相が動き、狭窓の m 格子と噛み合わせが悪い
#           (b) 窓の中心 c = S//2 の丸め(S の偶奇)
#           (c) 本当に何か構造がある
# 対策: 位相を実測してから、その位相に合わせた射影で振幅を取り直す(格子依存を消す)。
import math, cmath

def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(n+1) if s[i]]
ALLP=[p for p in primes_upto(5000) if p%2==1]
SQ=math.sqrt(3)/2

def rep_counts(B):
    tot=sum(B); r=[0]*(tot+1); r[0]=1
    for a in B:
        for m in range(tot,a-1,-1): r[m]+=r[m-a]
    return r

def analyze(B, hw=24, q=6):
    b=len(B); S=sum(B); V0=sum(a*a for a in B)/4.0
    r=rep_counts(B); c=S//2
    N=(2*hw//q)*q
    acc=0j; used=0
    for t in range(N):
        m=c-N//2+t
        if m<0 or m>=len(r) or r[m]==0: continue
        d=m-S/2.0
        lg=b*math.log(2)-0.5*math.log(2*math.pi*V0)-d*d/(2*V0)
        acc+=(r[m]/math.exp(lg)-1.0)*cmath.exp(-2j*math.pi*m/q); used+=1
    C=(2.0/used)*acc
    Z=cmath.exp(2j*math.pi/q); F=1+0j
    for a in B: F*=(1+Z**a)
    c1=sum(1 for a in B if a%6==1); c5=sum(1 for a in B if a%6==5)
    return dict(b=b,S=S,amp=abs(C),ph=-cmath.phase(C),
                predph=(math.pi/6)*(c1-c5),c1=c1,c5=c5,Spar=S%2,
                relF=abs(F)/2.0**b)

print("="*100)
print("k=32 外れ値の調査 (B = 5 以上の素数, d=2, hw=24)")
print("="*100)
print("  k   b   a_k   S      S%2  S%6  c1  c5  c1-c5   実測位相   予言位相   位相差    振幅比")
for k in range(20,41,2):
    B=[a for a in ALLP[:k] if a>4]
    r=analyze(B)
    dph=(r["ph"]-r["predph"]+math.pi)%(2*math.pi)-math.pi
    ratio=r["amp"]/(2*SQ**(r["b"]+1))
    mark=" <<<" if abs(ratio-1)>0.02 else ""
    print(f" {k:3d} {r['b']:3d} {ALLP[k-1]:5d} {r['S']:6d}   {r['Spar']}   {r['S']%6}"
          f"  {r['c1']:3d} {r['c5']:3d}  {r['c1']-r['c5']:+4d}  {r['ph']:+9.4f} {r['predph']:+9.4f}"
          f" {dph:+8.4f}   {ratio:7.4f}{mark}")
