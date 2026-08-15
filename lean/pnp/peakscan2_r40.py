# peakscan2_r40.py (2026-08-08, opus-5 40周目) : 決定的な量のやり直し。
# 前回 ★超過 と出たのは中央峰(θ=0)の除外半径が小さすぎたため(中央は主要項でありエラーではない)。
# 中央は「Gauss が (√3/2)^b を下回る半径」まで除外する。他の有理点は包絡半径 r_env。
import numpy as np, math
def primes_upto(n):
    s=np.ones(n+1,bool); s[:2]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]: s[i*i::i]=False
    return np.nonzero(s)[0]
L32=math.log(math.sqrt(3)/2)
print("="*104)
print("[決定的な量・修正版] 「中央峰 + q≤60 の有理点の包絡」を除いた領域での max (1/b)log|G|")
print("  中央の除外半径 = Gauss が (√3/2)^b を下回る点(= σ√(2b·0.14384))の 1.5 倍")
print("="*104)
print("   k    b   除外後 max(1/b)log|G|   log(√3/2)=-0.14384   余裕      判定       最大点の正体")
for k in (40,60,100,140):
    P=primes_upto(20000); A=P[P%2==1][:k]; B=A[A>4].astype(float); b=len(B)
    S2=float((B**2).sum()); sig=2.0/math.sqrt(S2); r_env=0.45*math.sqrt(k)*sig
    r0=1.5*sig*math.sqrt(2*b*(-L32))
    MG=6_000_000; th=np.linspace(0.0,math.pi,MG); lg=np.zeros(MG)
    for i in range(0,b,20):
        blk=B[i:i+20][:,None]
        lg+=np.log(np.abs(np.cos(blk*th[None,:]/2.0))+1e-300).sum(axis=0)
    mask=np.abs(th)>r0
    for q in range(2,61):
        for j in range(0,q//2+1):
            c=2*math.pi*j/q
            if 0<c<=math.pi+r_env: mask &= np.abs(th-c)>r_env
    idx=np.nonzero(mask)[0]; jbest=idx[np.argmax(lg[idx])]
    v=lg[jbest]/b; t=th[jbest]
    x=t/(2*math.pi); bq=min(range(1,61), key=lambda q: abs(x-round(x*q)/q))
    ok="OK(下回る)" if v<L32 else "★超過"
    print(f"  {k:3d} {b:4d}       {v:+.5f}                            {L32-v:+.5f}   {ok}"
          f"   θ={t:.5f} ≈ {round(x*bq)}/{bq} (r0={r0:.2e}, r_env={r_env:.2e})")
