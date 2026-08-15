# spectrum_r22.py (2026-08-08, opus-5 17周目)
# fable-5 指示書 opus5_報告兼指示書_r21.md 作業2:
#   系 M1.6「素数列の生存スペクトル」の数値検証。
#
# 主張(fable-5, M1 Addendum):
#   |1 + zeta_q^a| = 0  <=>  a = q/2 (mod q)  かつ q/2 が奇数
#   ⇒ q = 2m (m 奇) の峰は、B が m を「含む」とき厳密に消える
#   ⇒ 層 d の切断列 B_d = {a in A : a > 2d} では、m <= 2d の素数は落ちているので
#     q = 2m の峰は「復活」する。d が大きくなるほど生き残る q が増える。
#
# 決定的テスト: d=2 では q=6 のみ生存(3 は既に落ちている)。
#               d=3 では q=10 が復活する(5 <= 6 なので B_3 から 5 が落ちる)はず。
import math

def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(n+1) if s[i]]
ALLP=[p for p in primes_upto(20000) if p%2==1]

def polydiv(a,b):
    a=a[:]; out=[0]*(len(a)-len(b)+1)
    for i in range(len(a)-len(b),-1,-1):
        c=a[i+len(b)-1]//b[-1]; out[i]=c
        for j in range(len(b)): a[i+j]-=c*b[j]
    return out
CYC={}
def cyclotomic(n):
    if n in CYC: return CYC[n]
    p=[-1]+[0]*(n-1)+[1]
    for d in range(1,n):
        if n%d==0: p=polydiv(p,cyclotomic(d))
    CYC[n]=p; return p
def phi_at_minus1(q): return sum(c*((-1)**i) for i,c in enumerate(cyclotomic(q)))
def euler_phi(n):
    r=n;m=n;p=2
    while p*p<=m:
        if m%p==0:
            while m%p==0: m//=p
            r-=r//p
        p+=1
    if m>1: r-=r//m
    return r
def M(q): return 0.5*abs(phi_at_minus1(q))**(1.0/euler_phi(q))

def Gnorm(B, q):
    """|G(2pi/q)| / 2^b = prod_{a in B} |cos(pi a / q)|。厳密ゼロは 0.0 を返す。"""
    th = 2*math.pi/q
    v = 0.0
    for a in B:
        c = abs(math.cos(a*th/2.0))
        if c < 1e-14: return 0.0
        v += math.log(c)
    return math.exp(v)

QS = list(range(4, 25))
print("="*116)
print("[作業2] 生存スペクトル: 層 d を振ると、消えていた峰が復活するか")
print("        B_d = {a in A : a > 2d}(A は先頭 k 個の奇素数)")
print("="*116)

for k in (24, 32):
    A = [a for a in ALLP[:k]]
    print()
    print(f"### k = {k}   (A = 先頭 {k} 個の奇素数、3 から始まる)")
    print("  d   |B_d|  落ちた素数        " + "".join(f"  q={q:<3d}" for q in QS))
    for d in (1, 2, 3, 4, 5):
        B = [a for a in A if a > 2*d]
        dropped = [a for a in A if a <= 2*d]
        b = len(B)
        cells = []
        for q in QS:
            g = Gnorm(B, q)
            cells.append("  ---- " if g == 0.0 else f" {g:.1e}".replace("e-0", "e-"))
        print(f" {d:2d}   {b:4d}  {str(dropped):16s}" + "".join(f"{c:>8s}" for c in cells))
    print()
    print("  '----' は厳密にゼロ(その q の峰が消灯)")

print()
print("="*116)
print("[判定(a)] q = 2m (m 奇素数) の峰は、m が B_d から落ちたときに限り復活するか")
print("="*116)
print("  k    d   q    m=q/2   m は B_d に居るか   |G|/2^b        判定")
for k in (24, 32):
    A = [a for a in ALLP[:k]]
    for d in (1, 2, 3, 4, 5):
        B = [a for a in A if a > 2*d]
        for q in (6, 10, 14, 22, 26):
            m = q//2
            inB = m in B
            g = Gnorm(B, q)
            ok = (g == 0.0) == inB
            print(f" {k:3d}  {d:2d}  {q:3d}   {m:4d}      {'居る':6s}" if inB else
                  f" {k:3d}  {d:2d}  {q:3d}   {m:4d}      {'落ちた':6s}", end="")
            print(f"        {g:.4e}   {'OK' if ok else '★不一致':6s}")

print()
print("="*116)
print("[判定(b)] 生存している峰の値は M(q)^b の何倍か(理論の等分布近似の精度)")
print("="*116)
for k in (24, 32):
    A = [a for a in ALLP[:k]]
    print(f"### k = {k}")
    print("  d   b    " + "".join(f"   q={q:<3d}" for q in (4, 6, 8, 10, 12, 14, 16, 18, 20)))
    for d in (2, 3, 4, 5):
        B = [a for a in A if a > 2*d]; b = len(B)
        row = []
        for q in (4, 6, 8, 10, 12, 14, 16, 18, 20):
            g = Gnorm(B, q); mq = M(q)**b
            row.append("  ----" if g == 0.0 else f"{g/mq:6.3f}")
        print(f" {d:2d} {b:4d}    " + "".join(f"{c:>8s}" for c in row))
    print("  (1.000 なら M(q)^b ちょうど。q=4 と q=6 は理論上ちょうど 1 になるはず)")

print()
print("="*116)
print("[判定(c)] 主峰は常に q=6 か(生存している中で最大の M(q))")
print("="*116)
print("  k    d   b    生存している q(値の大きい順に上位4つ)")
for k in (24, 32):
    A = [a for a in ALLP[:k]]
    for d in (2, 3, 4, 5):
        B = [a for a in A if a > 2*d]; b = len(B)
        alive = [(Gnorm(B, q), q) for q in QS if Gnorm(B, q) > 0.0]
        alive.sort(reverse=True)
        top = ", ".join(f"q={q}({g:.2e})" for g, q in alive[:4])
        print(f" {k:3d}  {d:2d} {b:4d}    {top}")
