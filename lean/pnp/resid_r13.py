# resid_r13.py (2026-08-08, opus-5 8周目)
# 持ち越し ②③⑥:
#  (A) リップル振幅比 R_amp(k) と C10.3 の残差 R_dev(k) を k=14..32 で測り、
#      両者が同じベキで動くか(= 同一原因のサブ弧高次補正か)を判別する。
#  (B) E[Gamma(R_k)] の k 依存(Problem 10.4: ~ 2 ln k か)。
import math, cmath, random
from fractions import Fraction

def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(n+1) if s[i]]
ALLP=[p for p in primes_upto(5000) if p%2==1]
Z6=cmath.exp(2j*math.pi/6); SQ=math.sqrt(3)/2

def rep_counts(B):
    tot=sum(B); r=[0]*(tot+1); r[0]=1
    for a in B:
        for m in range(tot,a-1,-1): r[m]+=r[m-a]
    return r
def rget(r,m): return r[m] if 0<=m<len(r) else 0

def ripple_amp_phase(B, q=6, halfwidth=120):
    b=len(B); S=sum(B); V0=sum(a*a for a in B)/4.0
    r=rep_counts(B); c=S//2
    N=(2*halfwidth//q)*q
    acc=0j; used=0
    for t in range(N):
        m=c-N//2+t
        if m<0 or m>=len(r) or r[m]==0: continue
        delta=m-S/2.0
        lg=b*math.log(2)-0.5*math.log(2*math.pi*V0)-delta*delta/(2*V0)
        acc+=(r[m]/math.exp(lg)-1.0)*cmath.exp(-2j*math.pi*m/q); used+=1
    C=(2.0/used)*acc
    return abs(C), -cmath.phase(C), V0, b

def strata_and_dev(A):
    A=sorted(A); k=len(A); T=sum(A); n=T//2
    deg=rep_counts(A)[n]
    if deg==0: return None
    D=(A[-1]-1)//2; lm=deg; dev=0.0
    for d in range(1,D+1):
        Id=[a for a in A if a<=2*d]; Bd=[a for a in A if a>2*d]
        sig=sum(Id); Nd=len(Id); bd=len(Bd)
        rB=rep_counts(Bd)
        lm+=rget(rB,n+d)+rget(rB,n-d-sig)
        F=1+0j
        for a in Bd: F*=(1+Z6**a)
        rel=abs(F)/2.0**bd
        if rel>1e-14:
            V0=sum(a*a for a in Bd)/4.0
            V6=sum(a*a/(math.cos(math.pi*a/6)**2) for a in Bd)/4.0
            Ad=2.0*rel*math.sqrt(V0/V6); ph=cmath.phase(F)
            P=1+0j
            for a in Id: P*=(1+cmath.exp(-1j*math.pi*a/3))
            z=(cmath.exp(1j*math.pi*(n+d)/3)+cmath.exp(1j*math.pi*(n-d-sig)/3)
               -2*cmath.exp(1j*math.pi*n/3)*P/2.0**Nd)
            dev+=2.0**(-Nd)*(Ad*cmath.exp(-1j*ph)*z).real
    G=sum(Fraction(a,2**(j+1)) for j,a in enumerate(A))
    W=float(G+Fraction(A[-1],2**k))
    return dict(k=k,deg=deg,lm=lm,lmdeg=lm/deg,W=W,dev=dev,T=T)

print("="*94)
print("(A) 系統残差の切り分け:  R_amp = 実測振幅/2(√3/2)^(b+1),  R_dev = 予言Dev/実測(lm/deg−W)")
print("="*94)
print("  k    b_2      V0        R_amp     1−R_amp    R_dev    1−R_dev   (1−R_amp)*V0  (1−R_amp)*b")
rows=[]
for k in range(14,33,2):
    A=ALLP[:k]
    B2=[a for a in A if a>4]
    amp,ph,V0,b = ripple_amp_phase(B2)
    R_amp = amp/(2*SQ**(b+1))
    st = strata_and_dev(A)
    obs = st["lmdeg"]-st["W"]; pred = st["dev"]
    R_dev = pred/obs if abs(obs)>1e-9 else float('nan')
    rows.append((k,b,V0,R_amp,R_dev,obs,pred))
    print(f" {k:3d} {b:4d} {V0:10.1f}   {R_amp:8.5f}  {1-R_amp:+9.5f}  {R_dev:8.4f}  {1-R_dev:+8.4f}"
          f"   {(1-R_amp)*V0:10.2f}   {(1-R_amp)*b:8.4f}")

print()
print("  判定材料: 1−R_amp が V0 に反比例(=(1−R_amp)*V0 が一定)なら Edgeworth 由来、")
print("            b に反比例(=(1−R_amp)*b が一定)ならサブ弧の次数由来。")
print()
print("  R_dev は obs が小さい k で不安定になるので、絶対残差でも見る:")
print("  k     obs         pred       obs−pred    |obs−pred|/|obs|   |obs−pred| ÷ (√3/2)^b")
for k,b,V0,Ra,Rd,obs,pred in rows:
    print(f" {k:3d}  {obs:+11.7f} {pred:+11.7f} {obs-pred:+11.7f}    {abs(obs-pred)/abs(obs):8.4f}"
          f"          {abs(obs-pred)/(SQ**b):10.5f}")

print()
print("="*94)
print("(B) Problem 10.4: E[Gamma(R_k)] の k 依存(予想 ~ 2 ln k)")
print("="*94)
print("  k     E[Gamma]   sd      2 ln k    E[G]-2lnk   E[G]/ln k   Gamma(primes)  平均ギャップ")
gs=[]
for k in [8,12,16,20,24,28,32,40,50,64,80,100]:
    maxV=ALLP[k-1]
    cands=[x for x in range(3,maxV+1,2)]
    rng=random.Random(20260808+k); vals=[]
    for _ in range(400):
        R=sorted(rng.sample(cands,k))
        vals.append(float(sum(Fraction(a,2**(j+1)) for j,a in enumerate(R))))
    mu=sum(vals)/len(vals)
    sd=(sum((v-mu)**2 for v in vals)/(len(vals)-1))**0.5
    P=ALLP[:k]
    gP=float(sum(Fraction(a,2**(j+1)) for j,a in enumerate(P)))
    meangap=(P[-1]-P[0])/(k-1)
    gs.append((k,mu))
    print(f" {k:4d}  {mu:8.4f} {sd:7.4f}  {2*math.log(k):8.4f}  {mu-2*math.log(k):+9.4f}"
          f"   {mu/math.log(k):8.4f}     {gP:8.4f}      {meangap:8.3f}")

print()
print("  回帰 E[Gamma] = c1*ln k + c0  (k>=16):")
xs=[math.log(k) for k,_ in gs if k>=16]; ys=[m for k,m in gs if k>=16]
n=len(xs); mx=sum(xs)/n; my=sum(ys)/n
c1=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs)
c0=my-c1*mx
pred=[c0+c1*x for x in xs]
ssr=sum((y-p)**2 for y,p in zip(ys,pred)); sst=sum((y-my)**2 for y in ys)
print(f"    c1 = {c1:.4f}  (予想 2),  c0 = {c0:.4f},  R^2 = {1-ssr/sst:.5f}")
print(f"    → Gamma(primes) は {gP:.4f} に収束するので、比は c1*ln k / Gamma(P) ~ {c1:.2f}ln k/5.35")
