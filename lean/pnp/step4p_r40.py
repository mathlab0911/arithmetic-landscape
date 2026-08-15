# step4p_r40.py (2026-08-08, opus-5 40周目) : N₀ = b^{1/4} → (log b)^3 に取り替えた再スモーク。
# r34 の step4p_r34.py と同じ2判定を、新しい N₀ で回す。
import numpy as np, math
def primes_upto(n):
    s=np.ones(n+1,bool); s[:2]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]: s[i*i::i]=False
    return np.nonzero(s)[0]
P=primes_upto(40000)
rng=np.random.default_rng(20260808)

def run(b):
    B=P[P%2==1][:b].astype(float)
    d0=1.0/math.log(b)
    N0_old=int(b**0.25); N0_new=int(math.log(b)**3)
    out={}
    for tag,N0 in (("旧 b^{1/4}",max(N0_old,1)),("新 (log b)^3",max(N0_new,1))):
        # deep minor 的な θ を 6 点: 黄金比系の無理数まわり
        badr=[];head=[];sel=[]
        for s in range(6):
            th=2*math.pi*((math.sqrt(2)+s*math.sqrt(3)/7)%1.0)
            u=(B*th/(2*math.pi))%1.0
            nb=int(np.sum(np.abs(((u-0.5+0.5)%1.0)-0.5)<d0))
            badr.append(nb/b)
            n=np.arange(1,N0+1)
            S=np.abs(np.exp(2j*math.pi*np.outer(n,u)).sum(axis=1))
            head.append(float((S/n).sum())/b)
            cn=np.minimum(2*d0+1.0/N0, 1.0/n)
            sel.append(float(2*d0+1.0/N0 + (cn*S).sum()/b))   # Selberg 上界 ÷ b
        out[tag]=(N0, max(badr), max(head), max(sel), 1.0/(N0*d0))
    return d0,out

print("="*112)
print("[Step 4′ 再スモーク] N₀ = b^{1/4} → (log b)^3。判定: (a) Selberg上界が実測|B_bad|/b を上回る")
print("                                              (b) 頭の項と尾 C/(N₀δ₀) が小さくなる")
print("="*112)
print("    b   δ₀      版            N₀    実測|B_bad|/b  Selberg上界/b  判定   頭/b     尾 1/(N₀δ₀)")
for b in (99,299,999,1999):
    d0,out=run(b)
    for tag,(N0,br,hd,sl,tail) in out.items():
        ok = "OK" if sl>=br else "★破れ"
        print(f" {b:5d} {d0:.4f}  {tag:12s} {N0:5d}     {br:.4f}        {sl:.4f}      {ok}   {hd:.4f}   {tail:.4f}")
    print()
print("  ※ 尾は o(1) の主張の実測。1 を下回れば実用上意味を持つ。")
