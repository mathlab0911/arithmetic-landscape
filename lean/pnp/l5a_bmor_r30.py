# l5a_bmor_r30.py (2026-08-08, opus-5 31周目) : L5a の明示定数表。
#
# 出典(現物確認済み・逐語):
#   M. A. Bennett, G. Martin, K. O'Bryant, A. Rechnitzer,
#   "Explicit bounds for primes in arithmetic progressions",
#   Illinois J. Math. 62 (2018), no. 1-4, 427-532. arXiv:1802.00085v3.
#   Theorem 1.3: |pi(x;q,a) - Li(x)/phi(q)| < c_pi(q) x/(log x)^2  for all x >= x_pi(q).
#   c_pi(q) <= c_0(q) = 1/840 (3<=q<=10^4), 1/160 (q>10^4);  x_pi(q) <= x_0(q) = 8e9 (3<=q<=10^5).
#   個別値(論文 p.4 の表、3<=q<=10):
#      q=4 : c_pi=0.0005028, x_pi=5438260589
#      q=6 : c_pi=0.0004187, x_pi=7940618683
#      q=8 : c_pi=0.0006091, x_pi=2265738169
#      q=10: c_pi=0.0003876, x_pi=3375517771
#   q=14,18 は表に無いので一様値 c_0=1/840, x_0=8e9 を使う。
#
# 導出(論文2 の L5a):
#   n_r = #{p in B_d : p = r (mod q)},  e_r = n_r - b/phi(q)
#   |e_r| <= 2 c_pi(q) x/(log x)^2 + O(1),   b ~ x/log x
#   => sum_r |e_r| / b <= 2 phi(q) c_pi(q) / log x  (1+o(1))
#   |G_{B_d}(2pi j/q)| <= M(q)^b exp(L_q sum_r|e_r|)
#                       <= ( M(q) exp(2 phi(q) c_pi(q) L_q / log x) )^b
#   ここで L_q = max_{gcd(r,q)=1} |log|cos(pi r/q)||。
#   (M(q)+eta)^b にしたければ  log x >= 2 phi(q) c_pi(q) L_q / log(1 + eta/M(q)).
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
    best=0.0; arg=None
    for r in range(1,q):
        if math.gcd(r,q)==1:
            v=abs(math.log(abs(math.cos(math.pi*r/q))))
            if v>best: best=v; arg=r
    return best,arg

CPI={4:0.0005028, 6:0.0004187, 8:0.0006091, 10:0.0003876}
XPI={4:5438260589, 6:7940618683, 8:2265738169, 10:3375517771}
C0=1.0/840; X0=8e9

def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(n+1) if s[i]]

print("="*118)
print("[L5a] BMOR (Illinois J. Math. 62 (2018), arXiv:1802.00085v3) Thm 1.3 から出る明示的な k0(eta)")
print("="*118)
print("  q  phi(q)   M(q)     L_q  (最悪 r)   c_pi(q)      x_pi(q)      | eta=0.05 に必要な log x   x     ~ k0 = pi(x)")
for q in (4,6,8,10,14,18):
    ph=euler_phi(q); m=M(q); L,rr=Lq(q)
    c = CPI.get(q, C0); xp = XPI.get(q, X0)
    src = "表" if q in CPI else "一様 c0=1/840"
    need = 2*ph*c*L/math.log1p(0.05/m)
    xneed = math.exp(need)
    xuse = max(xneed, xp)
    # k0 = pi(xuse) を Li で近似
    li = xuse/math.log(xuse)*(1+1/math.log(xuse)+2/math.log(xuse)**2)
    print(f" {q:2d}   {ph:2d}   {m:.4f}  {L:.4f} (r={rr:2d})  {c:.7f} {xp:>12.3g}  |  {need:9.4f}  {xneed:9.3g}  {li:12.4g}   [{src}]")
print()
print("  読み方: 『eta=0.05 に必要な log x』が小さいので、実際の制約は x >= x_pi(q) のほう。")
print("          すなわち BMOR の適用開始点(x ~ 10^9〜10^10)が k0 を決める。")
print()
print("="*118)
print("[参考] x = x_pi(q) のとき、この評価が与える実際の eta")
print("="*118)
print("  q     x_pi(q)      log x    2 phi c_pi L_q / log x   実際の eta = M(q)(e^{...}-1)   M(q)+eta")
for q in (4,6,8,10,14,18):
    ph=euler_phi(q); m=M(q); L,_=Lq(q)
    c = CPI.get(q, C0); xp = float(XPI.get(q, X0))
    t = 2*ph*c*L/math.log(xp)
    eta = m*(math.exp(t)-1)
    print(f" {q:2d}  {xp:>12.4g}  {math.log(xp):7.3f}      {t:.3e}            {eta:.3e}            {m+eta:.6f}")
print()
print("  ⇒ x >= x_pi(q) の範囲では eta は 10^-5 のオーダーで、M(q) の値をほとんど動かさない。")
print("     すなわち L5a の『有限リストの峰は (M(q)+eta)^b で押さえられる』は")
print("     BMOR の定数で eta = 10^-5 という極めて強い形で成立する。")
print()
print("="*118)
print("[k0 の実務的な値] x_pi(q) を超える最小の k(= 先頭 k 個の素数の最大値が x_pi(q) 超)")
print("="*118)
print("  q      x_pi(q)        必要な p_k          おおよその k = pi(x_pi(q))")
for q in (4,6,8,10,14,18):
    xp=float(XPI.get(q,X0))
    li = xp/math.log(xp)*(1+1/math.log(xp)+2/math.log(xp)**2)
    print(f" {q:2d}  {xp:>13.5g}   p_k >= {xp:>12.5g}      k0 ~ {li:12.4g}")
print()
print("  【正直な注意】k0 ~ 4x10^8 は現在の数値実験(k<=44)から遥かに遠い。")
print("  L5a は『十分大きい k で成り立つ』という漸近的な主張であり、")
print("  実験値との橋渡しにはならない。論文にはこの点を明記すること。")
