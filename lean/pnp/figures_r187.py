# figures_r187.py -- the rounded figures quoted in the r187 report and in rem:qcrit, printed to
# four decimals so that every number in the prose exists in a log (C2/F19).  Nothing is computed
# here that was not computed in window_r187 and window2_r187; this file only fixes the precision
# at which those results are quoted, in one place, so that the paper and the report cannot drift
# from each other or from the measurement.
import math
def cfamily(k, c):
    A=[1]
    for j in range(1,k): A.append(A[-1]+2*max(1,int(round(c**j))))
    return A
def odds(k): return [2*i-1 for i in range(1,k+1)]
def gamma_of(A):
    k=len(A); m=[(A[0]-1)//2]+[(A[j]-A[j-1])//2 for j in range(1,k)]
    return 1.0+2.0*sum(m[j]*2.0**(-j) for j in range(k) if m[j])
def rho(A):
    k=len(A); sig2=sum(a*a for a in A)/4.0; dcap=max(1,(A[-1]-1)//2); G=gamma_of(A)
    tot=0.0; idx=0; n=0; l=0.0; s=0.0
    for d in range(1,dcap+1):
        while idx<k and A[idx]<=2*d:
            n+=1; l+=A[idx]; s+=A[idx]*A[idx]; idx+=1
        tot+=2.0**(-n)*((d+l/2.0)**2-s/4.0)
    return (tot/G)/sig2

print('rho_k*(2/c)^k, to four decimals, as quoted:')
for c in (1.4, 1.6, 1.8):
    row=[]
    for k in (12,16,20,24,28):
        row.append('%.4f' % (rho(cfamily(k,c))*(2.0/c)**k))
    print('   c = %.1f : %s' % (c, ', '.join(row)))
print()
print('fitted decay rates, to four decimals, as quoted:')
print('   four-point fit  : c = 1.4 -> 0.3909 ; c = 1.6 -> 0.2374   (window_r187)')
print('   full-range fit  : c = 1.4 -> 0.1141 ; c = 1.6 -> 0.0262   (window2_r187)')
print('   log(2/c)        : c = 1.4 -> %.4f ; c = 1.6 -> %.4f' % (math.log(2/1.4), math.log(2/1.6)))
print('   the four-point fit is the one that agreed and the one that was noise')
