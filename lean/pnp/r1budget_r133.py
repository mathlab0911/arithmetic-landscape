# r1budget_r133.py -- what does the R1 cumulant budget actually demand?
#
# prob:R1 asks for the Edgeworth expansion of the tilted LCLT with EXPLICIT constants at
#     eps = |K3|/K2^{3/2} + K4/K2^2 + W(k)|K3|/K2^2 ,
# uniformly over |m - mu_d(s)| <= W(k) and over layers d <= D(k).
#
# Before designing an attack, measure the thing.  Three questions:
#   (Q1) does eps -> 0, and how fast?
#   (Q2) which term dominates?  A budget is only as good as its worst term.
#   (Q3) is the dominant term the size of the MEASURED residual E_k ~ c_A/k?  If it is,
#        the Edgeworth constant should PREDICT c_A -- currently a conjecture.
#
# Definitions read off the paper (F48):
#   p_a = 1/(1+e^{s a}), s>0 fixed by sum a p_a = n, n = floor(rho T), rho = 1/2 - x
#   K2 = sum a^2 p q, K3 = sum a^3 p q (1-2p), K4 = sum a^4 p q (1-6p+6p^2),  q = 1-p
#   N_d = #{a<=2d}, sigma_d = sum_{a<=2d} a, delta_d = d + sigma_d/2, B_d = {a>2d}
#   W(k) = max{delta_d : 2^{-N_d} delta_d^2 >= 1/k}
import math

def primes_upto(n):
    s=[True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i in range(n+1) if s[i]]

_P=[p for p in primes_upto(3_000_000) if p%2==1]

def profile(name,k):
    if name=='odds':    return [2*i+1 for i in range(k)]
    if name=='primes':  return _P[:k]
    if name=='squares': return [2*((i+1)**2//2)+1 for i in range(k)]
    if name=='alpha32': return [2*(int(round((i+1)**1.5))//2)+1 for i in range(k)]
    raise ValueError(name)

def solve_s(A,n):
    def mean(s): return sum(a/(1.0+math.exp(min(700.0,s*a))) for a in A)
    lo,hi=0.0,1.0
    while mean(hi)>n:
        hi*=2.0
        if hi>1e6: raise RuntimeError('no bracket')
    for _ in range(200):
        mid=0.5*(lo+hi)
        if mean(mid)>n: lo=mid
        else: hi=mid
    return 0.5*(lo+hi)

def cumulants(B,s):
    K2=K3=K4=mu=0.0
    for a in B:
        p=1.0/(1.0+math.exp(min(700.0,s*a))); q=p*(1.0-p)
        mu+=a*p; K2+=a*a*q; K3+=a**3*q*(1.0-2.0*p); K4+=a**4*q*(1.0-6.0*p+6.0*p*p)
    return mu,K2,K3,K4

def window(A,k):
    M=A[-1]; best=0.0; Nd=0; sig=0; idx=0
    for d in range(1,(M-1)//2+1):
        while idx<len(A) and A[idx]<=2*d:
            Nd+=1; sig+=A[idx]; idx+=1
        delta=d+sig/2.0
        if Nd<1000 and (2.0**(-Nd))*delta*delta>=1.0/k: best=max(best,delta)
    return best

def layers(A,dmax):
    out=[]; Nd=0; sig=0; idx=0
    for d in range(1,dmax+1):
        while idx<len(A) and A[idx]<=2*d:
            Nd+=1; sig+=A[idx]; idx+=1
        out.append((d,Nd,sig,d+sig/2.0,A[idx:]))
    return out

def budget(name,k,x):
    A=profile(name,k); T=sum(A); n=int((0.5-x)*T)
    s=solve_s(A,n); W=window(A,k); rows=[]
    for (d,Nd,sig,delta,B) in layers(A,12):
        mu,K2,K3,K4=cumulants(B,s)
        t1=abs(K3)/K2**1.5; t2=abs(K4)/K2**2; t3=W*abs(K3)/K2**2
        rows.append(dict(d=d,Nd=Nd,K2=K2,K3=K3,K4=K4,t1=t1,t2=t2,t3=t3,eps=t1+t2+t3))
    return dict(A=A,T=T,n=n,s=s,W=W,rows=rows)

if __name__=='__main__':
    print('R1 cumulant budget, measured.  Definitions from prob:R1.')
    print()
    for name in ('odds','primes','alpha32','squares'):
        print('='*80); print('profile %s'%name)
        for x in (0.06,0.20,0.30):
            print('  x = %.2f'%x)
            print('    %5s %10s %9s %11s %11s %11s %11s %8s'
                  %('k','s','W(k)','|K3|/K2^1.5','K4/K2^2','W|K3|/K2^2','eps','k*eps'))
            for k in (60,100,140,180,220):
                try: r=budget(name,k,x)
                except Exception as e:
                    print('    k=%d failed: %s'%(k,e)); continue
                row=r['rows'][0]
                print('    %5d %10.3e %9.1f %11.3e %11.3e %11.3e %11.3e %8.4f'
                      %(k,r['s'],r['W'],row['t1'],row['t2'],row['t3'],row['eps'],k*row['eps']))
        print()
    print('='*80)
    print('uniformity in d (prop:tiltlclt claims one eps serves all layers)')
    print('  %8s %5s %4s %11s %8s'%('profile','k','d','eps(d)','/eps(1)'))
    for name in ('odds','primes'):
        for k in (100,220):
            r=budget(name,k,0.20); e1=r['rows'][0]['eps']
            for row in r['rows']:
                if row['d'] in (1,3,6,12):
                    print('  %8s %5d %4d %11.3e %8.3f'%(name,k,row['d'],row['eps'],row['eps']/e1))
