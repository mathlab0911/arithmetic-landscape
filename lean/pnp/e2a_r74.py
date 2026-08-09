# e2a_r74.py (2026-08-09, opus-5 74周目) 論文3 E2a: 中心外の lm/deg —— 剛性(R) か ドリフト(D) か
# 仕様: lean/pnp/paper3_experiments_r73.md §1
#   lm_A(n) = deg_A(n) + Σ_{d≥1} [ r_{B_d}(n+d) + r_{B_d}(T−n+d) ],  B_d={a: a>2d}
#   (論文1 定理C 厳密層別 + 定理A 分類定理。すべて厳密整数)
import sys
from fractions import Fraction
def odd_primes(k):
    out=[]; n=3
    while len(out)<k:
        if all(n%p for p in range(3,int(n**0.5)+1,2)): out.append(n)
        n+=2
    return out

def suffix_dps(A):
    """suf[j] = A[j:] の部分和カウント(厳密整数)。suf[len(A)] = 空集合"""
    k=len(A); suf=[None]*(k+1); suf[k]=[1]
    for j in range(k-1,-1,-1):
        prev=suf[j+1]; a=A[j]; new=[0]*(len(prev)+a)
        for m,c in enumerate(prev):
            if c: new[m]+=c; new[m+a]+=c
        suf[j]=new
    return suf

def lm_deg(A, n):
    """厳密層別公式で (lm, deg) を返す"""
    k=len(A); T=sum(A); suf=suffix_dps(A)
    g=lambda arr,m: arr[m] if 0<=m<len(arr) else 0
    deg=g(suf[0],n)
    D=(max(A)-1)//2
    lm=deg
    for d in range(1,D+1):
        j=0
        while j<k and A[j]<=2*d: j+=1     # B_d = A[j:]
        arr=suf[j]
        lm += g(arr,n+d) + g(arr,T-n+d)
    return lm,deg

def brute(A,n):
    """総当たり: 定義そのままで lm, deg を数える(照合用)"""
    k=len(A); best={}
    E=lambda s: abs(s-n)
    sums=[0]*(1<<k)
    for S in range(1,1<<k):
        low=S&-S; i=low.bit_length()-1
        sums[S]=sums[S^low]+A[i]
    deg=sum(1 for S in range(1<<k) if sums[S]==n)
    lm=0
    for S in range(1<<k):
        e=E(sums[S]); ok=True
        for i in range(k):
            if E(sums[S^(1<<i)])<=e: ok=False; break
        if ok: lm+=1
    return lm,deg

print("="*104)
print("【V1 正しさ検査①】層別公式 vs 総当たり (k=12..17、ρ=0.30/0.40/0.50)")
print("="*104)
ok_all=True
for k in (12,14,16,17):
    A=odd_primes(k); T=sum(A)
    for rho in (0.30,0.40,0.50):
        n=int(rho*T)
        a=lm_deg(A,n); b=brute(A,n)
        m = "OK" if a==b else "★不一致"
        if a!=b: ok_all=False
        print(f"  k={k:3d} ρ={rho:.2f} n={n:5d}  層別=(lm={a[0]:9d}, deg={a[1]:8d})  総当たり=(lm={b[0]:9d}, deg={b[1]:8d})  {m}")
print(f"  ⇒ {'全件一致 ✓' if ok_all else '★ 不一致あり'}")
print()
print("="*104)
print("【V1 正しさ検査②】反射定理 lm(n) = lm(T−n)(無料の検査。1件でも破れたらDPのバグ)")
print("="*104)
ok2=True
for k in (16,20,24,26):
    A=odd_primes(k); T=sum(A)
    for rho in (0.30,0.35,0.40,0.45):
        n=int(rho*T)
        l1,d1=lm_deg(A,n); l2,d2=lm_deg(A,T-n)
        good = (l1==l2 and d1==d2)
        if not good: ok2=False
        print(f"  k={k:3d} n={n:5d} vs T−n={T-n:5d}:  lm {l1} / {l2}   deg {d1} / {d2}   {'一致 ✓' if good else '★破れ'}")
print(f"  ⇒ {'全件一致 ✓' if ok2 else '★ 破れあり'}")

print()
print("="*104)
print("【E2a 本測定】ratio(ρ,k) = [lm/deg] ÷ Γ(P_k)   —— 剛性(R): 全ρで→1 / ドリフト(D): ρごとに別値")
print("="*104)
RHOS=[0.30,0.35,0.40,0.45,0.50]
KS=list(range(16,41,2))
GUARD=10**4
raw={}; rat={}
print("  k   Γ(P_k)   " + "".join(f"   ρ={r:.2f}      " for r in RHOS))
for k in KS:
    A=odd_primes(k); T=sum(A)
    G=float(sum(Fraction(a,2**(j+1)) for j,a in enumerate(A)))
    suf=suffix_dps(A); g=lambda arr,m: arr[m] if 0<=m<len(arr) else 0
    D=(max(A)-1)//2
    js=[]
    for d in range(0,D+1):
        j=0
        while j<k and A[j]<=2*d: j+=1
        js.append(j)
    row=[]
    for rho in RHOS:
        n=int(rho*T); deg=g(suf[0],n)
        lm=deg
        for d in range(1,D+1):
            arr=suf[js[d]]; lm += g(arr,n+d)+g(arr,T-n+d)
        raw[(k,rho)]=(lm,deg)
        if deg<GUARD: row.append("   (deg小)  "); rat[(k,rho)]=None
        else:
            r=(lm/deg)/G; rat[(k,rho)]=r; row.append(f"  {r:9.5f}  ")
    print(f" {k:3d}  {G:8.5f} "+"".join(row))
print()
print("  【生値】(粒度ガード deg<10⁴ の確認用)")
print("   k  " + "".join(f"  ρ={r:.2f}: deg / lm            " for r in RHOS[:3]))
for k in KS[::2]:
    print(f" {k:3d}  " + "".join(f"  {raw[(k,r)][1]:>12d} / {raw[(k,r)][0]:<12d}" for r in RHOS[:3]))
print()
print("  【判定材料】各 ρ 列で k↑ のとき ratio が 1 に向かうか(単調性)")
print("   ρ     k=16      k=24      k=32      k=40     |ratio−1| の推移")
for rho in RHOS:
    v=[rat.get((k,rho)) for k in (16,24,32,40)]
    s=" ".join(f"{x:9.5f}" if x else "   ---   " for x in v)
    d=[abs(x-1) for x in v if x]
    trend = "単調減少 ✓" if len(d)>=3 and all(d[i]>d[i+1] for i in range(len(d)-1)) else ("減少(非単調)" if d and d[0]>d[-1] else "★増加/横ばい")
    print(f"  {rho:.2f} {s}    {' → '.join(f'{x:.4f}' for x in d)}   {trend}")
