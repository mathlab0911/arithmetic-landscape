# peakscan_r40.py (2026-08-08, opus-5 40周目) : 【自主監査】被覆の「半径」側の穴を探す。
# W1 は「分母 q ≤ Q2 の有理点近傍 か deep minor」で分類するが、
# 近傍の半径 1/(qτ) は L5b 包絡の有効半径よりずっと広い。その隙間(環状領域)に
# 峰より高い点があると被覆が破れる。そこで |G| の局所最大を全部拾って正体を突き止める。
import numpy as np, math

def primes_upto(n):
    s=np.ones(n+1,bool); s[:2]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]: s[i*i::i]=False
    return np.nonzero(s)[0]

def M(q):
    if q==1: return 1.0
    if q==2: return 0.0  # (1/2)|Phi_q(-1)|^{1/phi(q)} を数値で: 原始q乗根 zeta^a (gcd(a,q)=1) に対する |1+zeta^a| の幾何平均/2... 
    # 直接 prod|1+e(a/q)| over gcd(a,q)=1 の 1/phi(q) 乗を 2 で割る
    tot=0.0; c=0
    for a in range(1,q):
        if math.gcd(a,q)==1:
            v=abs(1+complex(math.cos(2*math.pi*a/q), math.sin(2*math.pi*a/q)))
            if v==0: return 0.0
            tot+=math.log(v); c+=1
    return 0.5*math.exp(tot/c)

def scan(k, d=2, MG=4_000_000):
    P=primes_upto(20000)
    A=P[P%2==1][:k]; B=A[A>2*d].astype(float); b=len(B)
    S2=float((B**2).sum()); sig=2.0/math.sqrt(S2); Nmax=float(B.max())
    th=np.linspace(0.0, math.pi, MG)
    lg=np.zeros(MG)
    for i in range(0,b,20):                       # メモリ節約のため 20 本ずつ
        blk=B[i:i+20][:,None]
        lg+=np.log(np.abs(np.cos(blk*th[None,:]/2.0))+1e-300).sum(axis=0)
    # 局所最大(離散)
    loc=np.nonzero((lg[1:-1]>lg[:-2])&(lg[1:-1]>=lg[2:]))[0]+1
    order=loc[np.argsort(-lg[loc])]
    r_env=0.45*math.sqrt(k)*sig
    return b,S2,sig,Nmax,th,lg,order,r_env

def ident(t):   # theta/(2pi) に最も近い分母 q<=60 の有理数
    x=t/(2*math.pi); best=(None,None,9e9)
    for q in range(1,61):
        j=round(x*q); e=abs(x-j/q)
        if e<best[2]-1e-15: best=(q,j,e)
    return best

print("="*112)
print("[自主監査] |G| の局所最大を全部拾い、正体(近い有理数)と高さを見る")
print("="*112)
for k in (40,60,100):
    b,S2,sig,Nmax,th,lg,order,r_env=scan(k)
    print(f"\n--- k={k}  b={b}  S2={S2:.4g}  σ={sig:.3e}  包絡半径 r_env={r_env:.3e}  "
          f"Dirichlet 半径の目安 2π/(6·N)={2*math.pi/(6*Nmax):.3e}")
    print(f"    参考: (√3/2)^b={math.log(math.sqrt(3)/2)*b:+.3f}(log)  "
          f"M(18)^b={math.log(M(18))*b:+.3f}  (1/2)^b={math.log(0.5)*b:+.3f}  [すべて log|G| 換算]")
    print("     #   θ         θ/2π≈j/q     |q  |  log|G|    (1/b)log|G|  log M(q)   判定")
    seen=set(); shown=0
    for idx in order:
        t=th[idx]
        if t<1e-9: continue
        q,j,e=ident(t)
        key=(q,j)
        if key in seen: continue
        seen.add(key); shown+=1
        mq=M(q); lmq=math.log(mq) if mq>0 else float('-inf')
        v=lg[idx]/b
        flag="峰=有理点" if e*2*math.pi < r_env else ("環状領域(隙間)" if e*2*math.pi < 2*math.pi/(6*Nmax) else "deep")
        print(f"   {shown:3d}  {t:.6f}  {j:3d}/{q:<3d}      | dist={e*2*math.pi:.2e} | {lg[idx]:9.3f}  {v:+.5f}   "
              f"{lmq:+.5f}   {flag}")
        if shown>=12: break


print("\n"+"="*112)
print("[決定的な量] q ≤ 60 のすべての有理点の包絡(半径 r_env)を除いた領域での max|G|")
print("  ここが (√3/2)^b を超えなければ、半径側の隙間は結論を壊さない")
print("="*112)
print("   k    b   除外後の max (1/b)log|G|   (√3/2) の log = -0.14384   余裕      判定")
for k in (40,60,100):
    b,S2,sig,Nmax,th,lg,order,r_env=scan(k)
    mask=np.ones(len(th),bool)
    for q in range(1,61):
        for j in range(0,q//2+1):
            c=2*math.pi*j/q
            if c<=math.pi+r_env:
                mask &= np.abs(th-c)>r_env
    v=lg[mask].max()/b
    ok = "OK(下回る)" if v < math.log(math.sqrt(3)/2) else "★超過"
    print(f"  {k:3d} {b:4d}        {v:+.5f}                              {math.log(math.sqrt(3)/2)-v:+.5f}   {ok}")
