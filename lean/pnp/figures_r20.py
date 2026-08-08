# figures_r20.py (2026-08-08, opus-5 15周目)
# fable-5 指示書 opus5_報告兼指示書_r19.md の作業5: 論文2の図3点。
#   fig_mq.pdf     : M(q) = (1/2)|Phi_q(-1)|^{1/phi(q)} の棒グラフ(sqrt3/2 と 1/sqrt2 の水平線入り)
#   fig_peaks.pdf  : |G(theta)|/2^b の峰の実測曲線(theta=0, pi/3, 2pi/5, pi/2, pi に印)
#   fig_epsd.pdf   : eps_d(k) 実測 vs (sqrt3/2)^k 参照線
import math, cmath
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------- 円分多項式 Phi_q(x) を整数係数で構成し、Phi_q(-1) を厳密に求める ----------
def polydiv(a, b):
    """整数係数多項式(昇冪リスト)の割り算 a / b。割り切れる前提。"""
    a = a[:]; out = [0]*(len(a)-len(b)+1)
    for i in range(len(a)-len(b), -1, -1):
        c = a[i+len(b)-1] // b[-1]
        out[i] = c
        for j in range(len(b)):
            a[i+j] -= c*b[j]
    return out

CYC = {}
def cyclotomic(n):
    if n in CYC: return CYC[n]
    p = [-1] + [0]*(n-1) + [1]            # x^n - 1
    for d in range(1, n):
        if n % d == 0:
            p = polydiv(p, cyclotomic(d))
    CYC[n] = p
    return p

def phi_at_minus1(q):
    return sum(c*((-1)**i) for i, c in enumerate(cyclotomic(q)))

def euler_phi(n):
    r = n; m = n; p = 2
    while p*p <= m:
        if m % p == 0:
            while m % p == 0: m //= p
            r -= r//p
        p += 1
    if m > 1: r -= r//m
    return r

QS = list(range(3, 21))
M = {q: 0.5*abs(phi_at_minus1(q))**(1.0/euler_phi(q)) for q in QS}

print("[figures_r20] M(q) = (1/2)|Phi_q(-1)|^(1/phi(q))")
print("   q   phi(q)   Phi_q(-1)      M(q)")
for q in QS:
    print(f" {q:3d}   {euler_phi(q):4d}   {phi_at_minus1(q):+8d}   {M[q]:.6f}")
print(f"  検算: M(6) = {M[6]:.6f} vs sqrt3/2 = {math.sqrt(3)/2:.6f}")
print(f"        M(4) = {M[4]:.6f} vs 1/sqrt2 = {1/math.sqrt(2):.6f}")
print(f"        M(10)= {M[10]:.6f} vs 5^(1/4)/2 = {5**0.25/2:.6f}")
print(f"        最大値をとる q = {max(QS, key=lambda q: M[q])}")

fig, ax = plt.subplots(figsize=(7.2, 3.4))
cols = ["#c0392b" if q == 6 else ("#2980b9" if q in (4, 10) else "#95a5a6") for q in QS]
ax.bar([str(q) for q in QS], [M[q] for q in QS], color=cols, width=0.7)
ax.axhline(math.sqrt(3)/2, ls="--", lw=1.1, color="#c0392b")
ax.axhline(1/math.sqrt(2), ls=":", lw=1.1, color="#2980b9")
ax.text(len(QS)-0.4, math.sqrt(3)/2+0.012, r"$\sqrt{3}/2$", ha="right", color="#c0392b", fontsize=9)
ax.text(len(QS)-0.4, 1/math.sqrt(2)-0.045, r"$1/\sqrt{2}$", ha="right", color="#2980b9", fontsize=9)
ax.set_xlabel(r"$q$"); ax.set_ylabel(r"$M(q)$")
ax.set_ylim(0.45, 0.93)
ax.set_title(r"$M(q)=\frac{1}{2}|\Phi_q(-1)|^{1/\varphi(q)}$ : the supremum $\sqrt{3}/2$ is attained only at $q=6$",
             fontsize=9.5)
fig.tight_layout(); fig.savefig("../../paper/fig_mq.pdf"); plt.close(fig)

# ---------- |G(theta)|/2^b の峰 ----------
def primes_upto(n):
    s = [True]*(n+1); s[0] = s[1] = False
    for i in range(2, int(n**0.5)+1):
        if s[i]:
            for j in range(i*i, n+1, i): s[j] = False
    return [i for i in range(n+1) if s[i]]
B = [p for p in primes_upto(200) if p > 4][:24]
b = len(B)

def Gnorm(th):
    v = 0.0
    for a in B:
        c = abs(math.cos(a*th/2.0))
        if c < 1e-300: return 0.0
        v += math.log(c)
    return math.exp(v)                      # |G|/2^b = prod |cos(a theta/2)|

N = 4000
th = [math.pi*i/N for i in range(N+1)]
g = [Gnorm(t) for t in th]
FLOOR = 1e-16
g = [max(x, FLOOR) for x in g]

fig, ax = plt.subplots(figsize=(7.2, 3.6))
ax.semilogy(th, g, lw=0.8, color="#34495e")
marks = [(2*math.pi/6, (math.sqrt(3)/2)**b, r"$q=6$" + "\n" + r"$(\sqrt{3}/2)^b$", "#c0392b"),
         (2*math.pi/4, (1/math.sqrt(2))**b, r"$q=4$" + "\n" + r"$(1/\sqrt{2})^b$", "#2980b9"),
         (2*math.pi/8, M[8]**b, r"$q=8$", "#8e44ad")]
for x, y, lab, c in marks:
    ax.plot([x], [y], "o", ms=5, color=c)
    ax.annotate(lab, (x, y), textcoords="offset points", xytext=(6, 8), fontsize=8, color=c)
for q, p in ((10, 5), (14, 7), (22, 11)):
    ax.plot([2*math.pi/q], [FLOOR], "v", ms=5, color="#16a085")
ax.annotate("$q=2p$ with $p\\in B$ : exactly $0$\n(here $q=10,14,22$)", (2*math.pi/10, FLOOR),
            textcoords="offset points", xytext=(4, 22), fontsize=8, color="#16a085")
ax.plot([math.pi], [FLOOR], "v", ms=6, color="#16a085")
ax.annotate(r"$\theta=\pi$ : $0$ (parity)", (math.pi, FLOOR),
            textcoords="offset points", xytext=(-96, 10), fontsize=8, color="#16a085")
ax.set_xlabel(r"$\theta$"); ax.set_ylabel(r"$|G(\theta)|/2^b$")
ax.set_xticks([0, 2*math.pi/10, 2*math.pi/8, 2*math.pi/6, 2*math.pi/4, 2*math.pi/3, math.pi])
ax.set_xticklabels(["0", r"$\frac{2\pi}{10}$", r"$\frac{2\pi}{8}$", r"$\frac{2\pi}{6}$",
                    r"$\frac{2\pi}{4}$", r"$\frac{2\pi}{3}$", r"$\pi$"])
ax.set_ylim(FLOOR/3, 3)
ax.set_title(rf"Secondary peaks of $|G(\theta)|$ for the first $b={b}$ odd primes $\geq 5$", fontsize=9.5)
fig.tight_layout(); fig.savefig("../../paper/fig_peaks.pdf"); plt.close(fig)

print()
print("[peaks] b =", b, " (5 以上の素数を 24 個)")
print("  q   theta=2pi/q    M(q)^b        実測|G|/2^b     比        備考")
for q in (3,4,5,6,7,8,9,10,12,14,16,18,22):
    th=2*math.pi/q; y=M[q]**b if q in M else 0.5**b
    g=Gnorm(th); note=""
    if q%2==0 and (q//2)%2==1 and (q//2) in B: note=f"q/2={q//2} in B -> 厳密に 0"
    print(f" {q:3d}   {th:.6f}   {y:.4e}   {g:.4e}   {(g/y if y>0 else 0):8.4f}   {note}")
print(f"  theta=pi     実測 {Gnorm(math.pi):.3e}  (パリティにより厳密に 0)")
print()
print("  【観測】M(q) は全奇数列にわたる上限。素数列では q=2p (p in B) の峰が厳密に消える。")
print("          |1+zeta_q^a| は a = q/2 (mod q) で 0 になり、a=p はこれを満たすため。")
print("          ⇒ 素数列で q=6 に対抗しうるのは q=4 の (1/sqrt2)^b だけ = 定理E そのもの。")

# ---------- eps_d(k) vs (sqrt3/2)^k ----------
# 数値は flatness_sweep_r6.log(保存済み実測)からの転記。V1: 記憶で書かない。
KS = [8, 10, 12, 14, 16, 18, 20, 22, 24]
EPS = {
    1: [0.2500, 0.0769, 0.0263, 0.0328, 0.0051, 0.0031, 0.0007, 0.0009, 0.0003],
    2: [1.0000, 0.7500, 0.3684, 0.3125, 0.1827, 0.1518, 0.1104, 0.0734, 0.0570],
    3: [None,   0.3333, 0.8571, 0.3200, 0.2386, 0.1944, 0.1462, 0.1112, 0.0789],
    4: [None,   2.0000, 6.0000, 0.5833, 0.6944, 0.4122, 0.2987, 0.2283, 0.1573],
}
fig, ax = plt.subplots(figsize=(7.2, 3.6))
sty = {1: ("o-", "#c0392b"), 2: ("s-", "#2980b9"), 3: ("^-", "#27ae60"), 4: ("d-", "#8e44ad")}
for d in (1, 2, 3, 4):
    xs = [k for k, v in zip(KS, EPS[d]) if v]
    ys = [v for v in EPS[d] if v]
    m, c = sty[d]
    ax.semilogy(xs, ys, m, color=c, ms=4, lw=1.0, label=rf"$\varepsilon_{d}(k)$")
ref = [(math.sqrt(3)/2)**k for k in KS]
sc = EPS[2][-1]/((math.sqrt(3)/2)**24)
ax.semilogy(KS, [sc*r for r in ref], "k--", lw=1.2, label=r"$\propto(\sqrt{3}/2)^{k}$")
ax.set_xlabel(r"$k$"); ax.set_ylabel(r"$\varepsilon_d(k)$")
ax.legend(fontsize=8, ncol=5, loc="upper right")
ax.set_title(r"Measured flatness $\varepsilon_d(k)$ for the primes against the mod-6 rate $(\sqrt{3}/2)^k$",
             fontsize=9.5)
fig.tight_layout(); fig.savefig("../../paper/fig_epsd.pdf"); plt.close(fig)
print()
print("[epsd] 参照線は eps_2(24) で規格化。eps_1 は 3 を含む切断で G(pi/3)=0 のため2桁下にある。")
print("       出力: paper/fig_mq.pdf, paper/fig_peaks.pdf, paper/fig_epsd.pdf")
