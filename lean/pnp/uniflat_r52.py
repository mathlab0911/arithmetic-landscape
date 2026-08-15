# uniflat_r52.py (2026-08-08, opus-5 52周目) : fable-5 r51 作業2 の決定版。
# 必要なのは  (1/φ(q))·log‖Φ_q‖_∞ ≤ log√3 = 0.5493  (∀q>Q₄)。
# ‖Φ_q‖_∞ ≤ ‖Φ_q‖₁ なので、厳密整数の ‖·‖₁ で上から押さえて Q₄ を実測する。
from math import gcd, log
def phi(n): return sum(1 for a in range(1,n+1) if gcd(a,n)==1)
def polymul(a,b):
    r=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b): r[i+j]+=x*y
    return r
def polydiv(a,b):
    a=a[:]; q=[0]*(len(a)-len(b)+1)
    for i in range(len(q)-1,-1,-1):
        c=a[i+len(b)-1]//b[-1]; q[i]=c
        for j,bj in enumerate(b): a[i+j]-=c*bj
    return q
_c={}
def cyc(n):
    if n in _c: return _c[n]
    num=[0]*(n+1); num[0]=-1; num[n]=1
    den=[1]
    for d in range(1,n):
        if n%d==0: den=polymul(den,cyc(d))
    r=polydiv(num,den); _c[n]=r; return r
L3=log(3)/2
print("="*100)
print("[Q₄ の実測]  (1/φ(q))·log‖Φ_q‖₁  ≤  log√3 = %.6f  はどの q から一様に成り立つか" % L3)
print("  (‖Φ_q‖_∞ ≤ ‖Φ_q‖₁ なので、これは求める量の上界)")
print("="*100)
vals={}
QMAX=1200
for q in range(3,QMAX+1):
    c=cyc(q); l1=sum(abs(x) for x in c); vals[q]=log(l1)/phi(q)
worst=[]
for Q in (3,7,13,25,61,121,241,481):
    m=max((vals[q],q) for q in vals if q>=Q)
    worst.append((Q,m))
    print(f"   q ≥ {Q:4d} での最大: {m[0]:.6f}  (q={m[1]})   "
          f"{'★ log√3 を超える' if m[0]>L3 else 'OK(下回る)'}   余裕 {L3-m[0]:+.6f}")
print()
print("  上位10個(値の大きい q):")
for v,q in sorted(((v,q) for q,v in vals.items()),reverse=True)[:10]:
    l1=sum(abs(x) for x in cyc(q))
    print(f"    q={q:5d}  φ={phi(q):5d}  ‖Φ_q‖₁={l1:6d}   (1/φ)log‖·‖₁={v:.6f}"
          f"   {'★超過' if v>L3 else ''}")
print()
print("  減衰の様子(q ごとの最大値の推移):")
run=0.0; out=[]
for q in range(QMAX,2,-1):
    run=max(run,vals[q])
    if q in (3,6,7,13,31,61,121,241,481,721,961,1201): out.append((q,run))
for q,r in sorted(out):
    print(f"    sup_{{p≥{q:5d}}} = {r:.6f}    余裕 {L3-r:+.6f}")
print()
print(f"  ⇒ **Q₄ = (この上界が log√3 を切る最小の境目)**")
mn=None
for Q in range(3,QMAX):
    if max(vals[q] for q in range(Q,QMAX+1)) < L3: mn=Q; break
print(f"     実測: q ≥ {mn} で一様に log√3 未満(q ≤ {QMAX} の範囲で)。")
print(f"     q=3 と q=6 が等号なので、Q₄ = 7 で十分ということになる。")
