# p107exact_r26.py : E[Gamma(R_k)] の厳密な閉形式(漸近不要)を数値で確認する。
#   grid: a = 2i+1, i=1..N,  N=(p_k-3)/2+1
#   順序統計量 E[X_(j)] = j(N+1)/(k+1) は「N 個から k 個を非復元抽出」で厳密。
#   ⇒ E[a_(j)] = 1 + 2j(N+1)/(k+1)
#   ⇒ c=(N+1)/(k+1) として E[Gamma] = (1 - 2^-k) + 2c(2 - (k+2)2^-k)   … 厳密
import math, random
def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(n+1) if s[i]]
P=[p for p in primes_upto(200000) if p%2==1]
def gam(A):
    g=0.0; p=1.0
    for x in A: p/=2.0; g+=p*x
    return g
random.seed(20260809)
print("     k     p_k      N       c        厳密公式     モンテカルロ    比      1+2ln k")
for k,tr in ((20,4000),(50,4000),(100,3000),(200,2000),(400,1200),(800,600)):
    pk=P[k-1]; N=(pk-3)//2+1; c=(N+1)/(k+1)
    exact=(1-2.0**-k)+2*c*(2-(k+2)*2.0**-k)
    cands=list(range(3,pk+1,2))
    s=0.0
    for _ in range(tr):
        s+=gam(sorted(random.sample(cands,k)))
    m=s/tr
    print(f"  {k:4d}  {pk:6d}  {N:6d}  {c:7.4f}  {exact:10.4f}   {m:10.4f}   {m/exact:6.4f}   {1+2*math.log(k):7.3f}")
print()
print("  比が 1.00 前後なら閉形式は正しい。")
print("  Gamma(P_k) -> 5.3493 は有界なので、c -> infinity(すなわち p_k -> infinity)だけで")
print("  Gamma(P_k)/E[Gamma(R_k)] -> 0 が従う。Chebyshev の p_k >= c1 k log k で十分、PNT は不要。")
