# phigap_r44.py (2026-08-08, opus-5 44周目) : l8check の (B) の符号バグを直し、閾値を正しく出す。
# Φ_q(x) = R(x) - R(0),  R(x)=Σ_n ((-1)^{n+1}/n)(c_q(n)/φ(q)) Re Ĩ(nx),  R(0)=log(2M(q))
# 明示的な尾の評価 |R(x)| ≤ K_q·(2/x)·Σ1/n² ,  K_q := max_n |c_q(n)|/φ(q)  (x≥2)
# ⇒ Φ_q(x) ≤ -log(2M(q)) + C_q/x < 0  は  x > C_q/log(2M(q))  から。
import numpy as np, math
from math import gcd
def mobius(n):
    r=1;m=n
    for p in range(2,int(n**0.5)+1):
        if m%p==0:
            m//=p
            if m%p==0: return 0
            r=-r
    if m>1: r=-r
    return r
def ram(q,n):
    g=gcd(n,q); return sum(d*mobius(q//d) for d in range(1,g+1) if g%d==0)
def phi(q): return sum(1 for a in range(1,q+1) if gcd(a,q)==1)
def Mq(q):
    t=0.0;c=0
    for a in range(1,q):
        if gcd(a,q)==1:
            t+=math.log(abs(1+complex(math.cos(2*math.pi*a/q),math.sin(2*math.pi*a/q))));c+=1
    return 0.5*math.exp(t/c)
NM=400000; nn=np.arange(1,NM+1,dtype=float); sg=(-1.0)**(nn+1)/nn
def ReI(x): return np.where(np.abs(x)<1e-12,1.0,np.sin(x)/np.where(np.abs(x)<1e-12,1.0,x))
print("="*100)
print("[自主監査] Φ_q を『上界』として使うには Φ_q(x) ≤ -c < 0 が要る。明示評価はどの x から効くか")
print("="*100)
for q in (6,10,4):
    ph=phi(q); cs=np.array([ram(q,n) for n in range(1,NM+1)],dtype=float)/ph
    R0=math.log(2*Mq(q)); K=float(np.abs(cs).max()); C=K*2*(math.pi**2/6)
    x_half=C/(R0/2); x_zero=C/R0
    print(f"\n--- q={q}  φ={ph}  log(2M(q))={R0:+.5f}  K_q=max|c_q|/φ={K:.3f}  C_q=2K·ζ(2)={C:.3f}")
    print("      x      Φ_q(x)(級数)   明示上界 -log(2M)+C/x   明示上界で Φ≤-log(2M)/2 と言えるか")
    for x in (1.5,2.0,3.0,6.0,12.0,24.0,48.0):
        R=float((sg*cs*ReI(nn*x)).sum())
        print(f"    {x:6.1f}    {R-R0:+.5f}          {-R0+C/x:+.5f}            "
              f"{'YES' if -R0+C/x <= -R0/2 else 'no'}")
    print(f"    ⇒ 明示評価が Φ≤-log(2M)/2 を保証するのは x ≥ {x_half:.1f}(Φ<0 なら x ≥ {x_zero:.1f})")
print()
print("  L5b 包絡の到達点は x = N·r_env ≈ 1.5。")
print("  ⇒ **q=6 では [1.5, %.0f] が、包絡でも明示尾評価でも押さえられていない**(コンパクトな区間)。" % (2*(2*(math.pi**2/6))/math.log(2*Mq(6))))
