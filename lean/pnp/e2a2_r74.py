# e2a2_r74.py  E2a の判定を固める: (R)剛性 vs (D)ドリフト の識別子 = 【ρ 方向の広がり】
#  (R) なら spread_k = max_ρ ratio − min_ρ ratio → 0
#  (D) なら spread_k → 正の定数
# あわせて ρ を 0.20 まで外側に伸ばして剛性を stress する。
import time
from fractions import Fraction
def odd_primes(k):
    out=[]; n=3
    while len(out)<k:
        if all(n%p for p in range(3,int(n**0.5)+1,2)): out.append(n)
        n+=2
    return out
def suffix_dps(A):
    k=len(A); suf=[None]*(k+1); suf[k]=[1]
    for j in range(k-1,-1,-1):
        prev=suf[j+1]; a=A[j]; new=[0]*(len(prev)+a)
        for m,c in enumerate(prev):
            if c: new[m]+=c; new[m+a]+=c
        suf[j]=new
    return suf
RHOS=[0.20,0.25,0.30,0.35,0.40,0.45,0.50]
KS=list(range(24,53,4))
GUARD=10**4
print("="*112)
print("【E2a-2】ρ を 0.20 まで伸ばし、識別子 spread = max_ρ ratio − min_ρ ratio を見る")
print("="*112)
print("   k  " + "".join(f" ρ={r:.2f} " for r in RHOS) + "   spread    max|r−1|   (時間)")
rows={}
for k in KS:
    t0=time.time()
    A=odd_primes(k); T=sum(A)
    G=float(sum(Fraction(a,2**(j+1)) for j,a in enumerate(A)))
    suf=suffix_dps(A); g=lambda arr,m: arr[m] if 0<=m<len(arr) else 0
    D=(max(A)-1)//2
    js=[]
    for d in range(0,D+1):
        j=0
        while j<k and A[j]<=2*d: j+=1
        js.append(j)
    vals=[]; cells=[]
    for rho in RHOS:
        n=int(rho*T); deg=g(suf[0],n); lm=deg
        for d in range(1,D+1):
            arr=suf[js[d]]; lm += g(arr,n+d)+g(arr,T-n+d)
        if deg<GUARD: cells.append("  ---   ")
        else:
            r=(lm/deg)/G; vals.append(r); cells.append(f"{r:8.5f}")
    sp = max(vals)-min(vals) if len(vals)>1 else float('nan')
    mx = max(abs(v-1) for v in vals) if vals else float('nan')
    rows[k]=(sp,mx)
    print(f" {k:3d}  "+"".join(cells)+f"  {sp:.6f}  {mx:.6f}   ({time.time()-t0:.1f}s)")
print()
print("  【識別子の推移】(R) なら spread → 0、(D) なら正の定数に落ち着く")
ks=sorted(rows); print("   k     : "+" ".join(f"{k:8d}" for k in ks))
print("   spread: "+" ".join(f"{rows[k][0]:8.5f}" for k in ks))
print("   max|r−1|: "+" ".join(f"{rows[k][1]:8.5f}" for k in ks))
first,last=rows[ks[0]][0],rows[ks[-1]][0]
print(f"\n   spread は k={ks[0]} の {first:.5f} から k={ks[-1]} の {last:.5f} へ "
      f"({first/last:.1f}倍の縮小)" if last>0 else "")
print("   ⇒ 判定: " + ("【(R) 剛性】ρ に依らず lm/deg → Γ。Γ は中心だけでなく地形全体の不変量"
                        if last < first/3 else "【要検討】spread が縮まない ⟹ (D) の可能性"))
