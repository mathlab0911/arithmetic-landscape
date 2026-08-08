# l1check_r50.py (2026-08-08, opus-5 50周目) : fable-5 r49 作業1。
# ‖Φ_q‖_∞ ≤ ‖Φ_q‖₁ = Σ|係数| なので、有限リストの検証は【厳密な整数比較】に落ちる。
#   φ(q) は q≥3 で偶数 ⟹ 3^{φ(q)/2} は整数。浮動小数を一切使わない。
from math import gcd
from fractions import Fraction

def phi(n): return sum(1 for a in range(1,n+1) if gcd(a,n)==1)

def polydiv(a,b):                     # 整数係数の厳密な多項式除算 (a/b、割り切れる前提)
    a=a[:]; q=[0]*(len(a)-len(b)+1)
    for i in range(len(q)-1,-1,-1):
        c=a[i+len(b)-1]//b[-1]
        assert c*b[-1]==a[i+len(b)-1], "not divisible"
        q[i]=c
        for j,bj in enumerate(b): a[i+j]-=c*bj
    assert all(x==0 for x in a), "remainder nonzero"
    return q
def polymul(a,b):
    r=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b): r[i+j]+=x*y
    return r

_cyc={}
def cyclotomic(n):                    # Φ_n(x) の整数係数リスト(低次から)
    if n in _cyc: return _cyc[n]
    num=[0]*(n+1); num[0]=-1; num[n]=1          # x^n - 1
    den=[1]
    for d in range(1,n):
        if n%d==0: den=polymul(den,cyclotomic(d))
    r=polydiv(num,den); _cyc[n]=r; return r

print("="*104)
print("[ℓ¹ 整数チェック]  Σ|係数(Φ_q)|  ≤  3^{φ(q)/2}   —— すべて整数、浮動小数なし")
print("="*104)
print("    q   φ(q)   ‖Φ_q‖₁   3^{φ(q)/2}          判定    (等号?)")
tight=[]; fails=[]
for q in range(3,241):
    c=cyclotomic(q); l1=sum(abs(x) for x in c); ph=phi(q); bd=3**(ph//2)
    ok = l1<=bd
    if not ok: fails.append(q)
    if l1==bd: tight.append(q)
    if q<=24 or q in (30,36,60,105,120,165,180,210,231,240) or not ok:
        print(f"  {q:4d}  {ph:5d}   {l1:7d}   {bd:18d}     {'OK' if ok else '★破れ'}"
              f"     {'等号' if l1==bd else ''}")
print()
print(f"  3 ≤ q ≤ 240 の全域: {'成立' if not fails else '★破れ q='+str(fails)}")
print(f"  等号が起きる q: {tight}")
print()
print("  ※ φ(q) は q≥3 で偶数なので 3^{φ(q)/2} は整数。比較は完全に整数演算。")
print("  ※ ‖Φ_q‖_∞ ≤ ‖Φ_q‖₁ は |z|=1 で |Σc_i z^i| ≤ Σ|c_i| から即座(Lean 化可)。")
print()
# 余裕の推移(大 q で指数的に開くことの確認)
print("  余裕の推移(log スケール、1元素あたり): (log 3^{φ/2} − log‖Φ_q‖₁)/φ(q)")
import math
for q in (3,6,12,30,60,105,120,210,240):
    c=cyclotomic(q); l1=sum(abs(x) for x in c); ph=phi(q)
    print(f"    q={q:4d}  φ={ph:4d}  ‖·‖₁={l1:8d}   余裕={(math.log(3)*ph/2-math.log(l1))/ph:+.5f}")
