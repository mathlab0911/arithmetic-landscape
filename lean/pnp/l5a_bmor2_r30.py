# l5a_bmor2_r30.py : L5a の k0(eta) を BMOR の【2つの定理を併用】して最適化する。
#   Thm 1.3 : |pi(x;q,a) - Li(x)/phi(q)| < c_pi(q) x/(log x)^2      (x >= x_pi(q) ~ 10^9-10^10)
#   Thm 1.9 : max_{y<=x} |pi(y;q,a) - Li(y)/phi(q)| <= 2.734 sqrt(x)/log x  (x <= x_2(q))
#             x_2(q) = 10^13  (5 < q <= 100, q !== 2 mod 4);  q=2 mod 4 は x_2(q/2) を使う
#   ⇒ 2つの範囲は重なるので、x について切れ目なく評価できる。
#     小さい x では sqrt(x) 型(Thm 1.9)のほうが遥かに強い。
import math
def polydiv(a,b):
    a=a[:]; out=[0]*(len(a)-len(b)+1)
    for i in range(len(a)-len(b),-1,-1):
        c=a[i+len(b)-1]//b[-1]; out[i]=c
        for j in range(len(b)): a[i+j]-=c*b[j]
    return out
CYC={}
def cyclo(n):
    if n in CYC: return CYC[n]
    p=[-1]+[0]*(n-1)+[1]
    for d in range(1,n):
        if n%d==0: p=polydiv(p,cyclo(d))
    CYC[n]=p; return p
def phi_m1(q): return sum(c*((-1)**i) for i,c in enumerate(cyclo(q)))
def euler_phi(n):
    r=n;m=n;p=2
    while p*p<=m:
        if m%p==0:
            while m%p==0: m//=p
            r-=r//p
        p+=1
    if m>1: r-=r//m
    return r
def M(q): return 0.5*abs(phi_m1(q))**(1.0/euler_phi(q))
def Lq(q):
    return max(abs(math.log(abs(math.cos(math.pi*r/q)))) for r in range(1,q) if math.gcd(r,q)==1)
CPI={4:0.0005028,6:0.0004187,8:0.0006091,10:0.0003876}
XPI={4:5438260589,6:7940618683,8:2265738169,10:3375517771}
C0=1.0/840; X0=8e9
def li(x): return x/math.log(x)*(1+1/math.log(x)+2/math.log(x)**2)

def eta_at(q,x):
    """x における eta(2定理のうち良いほう)。b ~ Li(x) で正規化。"""
    ph=euler_phi(q); m=M(q); L=Lq(q); b=li(x)
    # Thm 1.9 (x <= 10^13)
    e19 = 2*2.734*math.sqrt(x)/math.log(x) if x<=1e13 else None
    # Thm 1.3 (x >= x_pi(q))
    c=CPI.get(q,C0); xp=XPI.get(q,X0)
    e13 = 2*c*x/math.log(x)**2 if x>=xp else None
    cands=[e for e in (e19,e13) if e is not None]
    if not cands: return None
    S=ph*min(cands)          # sum_r |e_r|
    return m*(math.exp(L*S/b)-1)

print("="*112)
print("[L5a 改良] BMOR の Thm 1.9(小さい x、sqrt型)と Thm 1.3(大きい x)を併用")
print("="*112)
print("  q   M(q)     L_q     x=10^4     10^5      10^6      10^7      10^9     10^11     10^13")
for q in (4,6,8,10,14,18):
    row=[]
    for e in (4,5,6,7,9,11,13):
        v=eta_at(q,10.0**e)
        row.append("   ----  " if v is None else f"{v:9.2e}")
    print(f" {q:2d}  {M(q):.4f}  {Lq(q):.4f} "+" ".join(row))
print()
print("  (値は eta。M(q)+eta が実際の上界の底になる)")

print()
print("="*112)
print("[k0(eta)] eta を達成する最小の x と、対応する k ~ Li(x)")
print("="*112)
for eta_t in (0.10,0.05,0.01):
    print(f"  --- eta = {eta_t} ---")
    print("   q       必要な x            k0 ~ Li(x)      そこでの eta")
    for q in (4,6,8,10,14,18):
        lo,hi=100.0,1e13
        for _ in range(200):
            mid=math.sqrt(lo*hi)
            v=eta_at(q,mid)
            if v is None or v>eta_t: lo=mid
            else: hi=mid
        v=eta_at(q,hi)
        print(f"  {q:2d}   {hi:14.5g}   {li(hi):14.5g}   {v:.3e}")
print()
print("  ⇒ Thm 1.9 の sqrt(x) 型のおかげで、k0 は 10^8 ではなく 10^4〜10^5 のオーダーに落ちる。")
print("    (前スクリプト l5a_bmor_r30.py は Thm 1.3 だけを使ったため k0 ~ 4e8 と出ていた。")
print("     Thm 1.9 を併用するのが正しい。)")
