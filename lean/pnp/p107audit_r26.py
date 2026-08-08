# p107audit_r26.py (2026-08-08, opus-5 21周目)
# 外部文書 Problem_10_7_Approaches.md の監査。
#   主張A: Gamma(A) = sum_{j=1}^{k-1} (a_{j+1}-a_j)/2^j - a_k/2^k
#   主張B: E[Gamma(R_k)] ~ log k
# 論文の定義は Gamma(A) = sum_{j=1}^{k} a_j/2^j = sum_{j=0}^{k-1}(a_{j+1}-a_j)/2^j - a_k/2^k  (a_0=0)
import math, random
def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(n+1) if s[i]]
P=[p for p in primes_upto(400000) if p%2==1]

def gamma_paper(A):           # sum a_j / 2^j
    g=0.0; p=1.0
    for x in A: p/=2.0; g+=p*x
    return g
def gamma_gapform_j0(A):      # 論文の部分和公式(j=0 から)
    g=0.0; prev=0
    for j,x in enumerate(A): g += (x-prev)/2.0**j; prev=x
    return g - A[-1]/2.0**len(A)
def gamma_gapform_j1(A):      # 外部文書の式(j=1 から)
    g=0.0
    for j in range(1,len(A)): g += (A[j]-A[j-1])/2.0**j
    return g - A[-1]/2.0**len(A)

print("="*100)
print("[監査1] Gamma の式が論文の定義と一致するか(A = 3,5,7,11,13 で検算)")
print("="*100)
A=[3,5,7,11,13]
print(f"  論文の定義  sum a_j/2^j          = {gamma_paper(A):.6f}")
print(f"  論文の部分和公式 (j=0 から)       = {gamma_gapform_j0(A):.6f}   ← 一致すべき")
print(f"  外部文書の式    (j=1 から)       = {gamma_gapform_j1(A):.6f}   ← 一致しない")
print()
print("  ⇒ 外部文書は和の下端を j=1 と書いているが、論文は j=0。")
print("     j=0 の項は (a_1 - 0)/2^0 = a_1 で、最大の項。これを落としている。")

print()
print("="*100)
print("[監査2] 係数: sum_{j=0}^{k-1} 2^-j -> 2 なので E[Gamma] ~ 2 * E[gap]")
print("        外部文書は sum_{j=1} 2^-j -> 1 として E[Gamma] ~ log k と結論している")
print("="*100)
random.seed(20260808)
print("     k    p_k     E[Gamma(R_k)] 実測   ln k    2 ln k   実測/ln k   実測/(2 ln k)")
for k in (20,50,100,200,400,800):
    pk=P[k-1]
    cands=[n for n in range(3,pk+1,2)]
    tr=400
    vals=[]
    for _ in range(tr):
        A=sorted(random.sample(cands,k))
        vals.append(gamma_paper(A))
    m=sum(vals)/len(vals)
    print(f"  {k:4d}  {pk:6d}      {m:9.4f}       {math.log(k):6.3f}  {2*math.log(k):6.3f}    {m/math.log(k):7.3f}      {m/(2*math.log(k)):7.3f}")
print()
print("  ⇒ 実測/(2 ln k) が 1 に近ければ 2 ln k が正しい。実測/ln k が 1 に近ければ外部文書が正しい。")

print()
print("="*100)
print("[監査3] 外部文書が触れていない点: lm_P/lm_R は Gamma の比だけでは決まらない")
print("        lm ~ Gamma * 2^k / sqrt(2 pi V0) なので、V0 = S2/4 の比も効く。")
print("        S2(P_k) と E[S2(R_k)] の比が 1 に向かうかを確認する。")
print("="*100)
print("     k    S2(P_k)        E[S2(R_k)]      比 S2(P)/E[S2(R)]   sqrt(比)")
for k in (20,50,100,200,400):
    pk=P[k-1]; A=P[:k]
    S2p=sum(a*a for a in A)
    cands=[n for n in range(3,pk+1,2)]
    tr=200; s=0
    for _ in range(tr):
        R=random.sample(cands,k); s+=sum(a*a for a in R)
    S2r=s/tr
    print(f"  {k:4d}  {S2p:14d}  {S2r:14.0f}      {S2p/S2r:10.4f}        {math.sqrt(S2p/S2r):8.4f}")
print()
print("  ⇒ 比が 1 に向かうなら、deg の比は無視でき、Gamma の比較だけでよい(論文の主張どおり)。")
print("     1 に向かわないなら、Problem 10.7 は Gamma だけの問題ではない。")
