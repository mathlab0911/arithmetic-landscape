# r2check_r52.py (2026-08-08, opus-5 52周目) : fable-5 r51 作業1 の検算(最優先箇所)。
#  (A) R2 第3クラス(m > √q)の見積もりを紙で追う → 発散するか
#  (B) ‖Φ_n‖₁ = ‖Φ_{rad(n)}‖₁ (Φ_n(x)=Φ_{rad n}(x^{n/rad n})) の確認 → 平方因子なしだけ見ればよい
#  (C) 積公式 ∏_{s=0}^{Q−1} 2sin(π(x+s/Q)) = 2 sin(πQx) の確認((α)の道具)
from math import gcd, log, sin, pi
import math
def phi(n): return sum(1 for a in range(1,n+1) if gcd(a,n)==1)
def rad(n):
    r=1; m=n; p=2
    while p*p<=m:
        if m%p==0:
            r*=p
            while m%p==0: m//=p
        p+=1
    if m>1: r*=m
    return r
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
def l1(n): return sum(abs(x) for x in cyc(n))

print("="*100)
print("(A) R2 第3クラス(m>√q)の見積もりを紙で追う")
print("="*100)
print("  設計の式:  Σ_{m>√q} (1/m)·|Ĩ(mx)| ,  |Ĩ(mx)| ≤ 2/(mx) ,  x > δ/q")
print("           ⟹ Σ_{m>√q} (1/m)·(2q/(mδ)) = (2q/δ)·Σ_{m>√q} 1/m²  ≤ (2q/δ)·(1/√q) = 2√q/δ")
for q in (100,10_000,1_000_000):
    print(f"    q={q:>9d}:  2√q/δ  =  {2*math.sqrt(q):.1f}/δ    ← q とともに発散")
print("  ⇒ 【設計の『≤ 2/δ』は誤り。実際は 2√q/δ で発散する】")
print()
print("  提案されていた修正(|c_q(m)|/φ(q) ≤ C·loglog q·m/q を併用)も追う:")
print("           Σ_{√q<m≤q} (1/m)·(C loglog q·m/q)·(2q/(mδ)) = (2C loglog q/δ)·Σ_{√q<m≤q} 1/m")
print("           ≈ (2C loglog q/δ)·log(√q) = (C' loglog q · log q)/δ   ← これも発散(対数的に)")
print("  ⇒ 【修正案でも閉じない。項別評価は Ĩ の m 方向の振動を捨てているため本質的に損】")
print()
print("="*100)
print("(B) ‖Φ_n‖₁ は rad(n) だけで決まるか (Φ_n(x) = Φ_{rad n}(x^{n/rad n}))")
print("="*100)
bad=[]
for n in range(3,301):
    if l1(n)!=l1(rad(n)) and rad(n)>=3: bad.append(n)
print(f"    3 ≤ n ≤ 300 で ‖Φ_n‖₁ = ‖Φ_{{rad n}}‖₁ が破れる n: {bad if bad else 'なし(全て一致)'}")
print("    例: ", [(n,rad(n),l1(n),l1(rad(n))) for n in (12,18,24,36,50,108,180,200,288)])
print("  ⇒ **平方因子のない q だけ調べればよい**。しかも φ(n) ≥ φ(rad n) なので")
print("     (1/φ(n))log‖Φ_n‖₁ ≤ (1/φ(rad n))log‖Φ_{rad n}‖₁ ——平方因子は必ず有利に働く")
print()
print("  平方因子のない q での最大値(q ≤ 300):")
sf=[(log(l1(q))/phi(q),q) for q in range(3,301) if rad(q)==q]
for v,q in sorted(sf,reverse=True)[:8]:
    print(f"    q={q:4d}  φ={phi(q):4d}  ‖·‖₁={l1(q):5d}  (1/φ)log‖·‖₁={v:.6f}")
print()
print("="*100)
print("(C) 積公式 ∏_{s=0}^{Q−1} |2 sin(π(x+s/Q))| = |2 sin(πQx)|  ((α)の道具)")
print("="*100)
for Q,x in ((5,0.13),(7,0.31),(12,0.077)):
    lhs=1.0
    for s in range(Q): lhs*=abs(2*sin(pi*(x+s/Q)))
    rhs=abs(2*sin(pi*Q*x))
    print(f"    Q={Q:3d} x={x}:  左辺={lhs:.10f}  右辺={rhs:.10f}  差={lhs-rhs:+.2e}")
print("  ⇒ 成立。Möbius で Σ_{r⊥q} を Σ_{d|rad q} μ(d)·(等差数列の和) に分解すると各項が log|2sin| に潰れる。")
print("     ただし μ(d)=−1 の項は【下界】が要り、log は −∞ に落ちうる —— ここが (α) の要検討点。")
