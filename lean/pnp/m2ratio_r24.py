# m2ratio_r24.py : 「0.97 の謎」の本体判定。
#   analyze_r2.py の P2 絶対公式は  pred = 2^k * Gamma * sqrt(2/(pi*S2))
#   これは 2^k / sqrt(2*pi*V0) * Gamma、すなわち deg を Gauss 近似で置き換えた形。
#   よって ratio = lm/pred = [lm/(Gamma*deg)] * [deg*sqrt(2 pi V0)/2^k]
#   第2因子が M2.4 の主張 1 − S4/(4 S2^2)。第1因子(Q)は 1 のまわりで振動する。
#   ⇒ ratio を (1 − S4/(4S2^2)) で割れば、系統的な下振れが消えて 1 のまわりに戻るはず。
exec(open('m2check_r24.py').read().split('# ---------- V2b')[0])
import statistics
print("="*104)
print("[0.97 判定] ratio = lm/pred と、補正後 ratio/(1 − S4/(4S2^2))")
print("="*104)
print("   k     ratio(素数)   補正後     |   100シード ratio 平均   補正後平均   補正後の標準偏差")
for k in (8,12,16,18,20):
    B=sorted(ODDPRIMES[:k]); S2,S4=moments(B)
    sums=[0]
    for x in B: sums=sums+[s+x for s in sums]
    n=sum(B)//2
    lm=0
    for idx,s in enumerate(sums):
        e=abs(s-n); ok=True
        for i in range(k):
            ns=s-B[i] if (idx>>i)&1 else s+B[i]
            if abs(ns-n)<=e: ok=False; break
        if ok: lm+=1
    g=0.0;p=1.0
    for x in B: p/=2.0; g+=p*x
    pred=2**k*g*math.sqrt(2.0/(math.pi*S2)); corr=1.0-S4/(4.0*S2*S2)
    maxV=ODDPRIMES[:k][-1]; rs=[]
    for i in range(100):
        Br=sorted(rand_odds(k,maxV,(20260807+i*2654435761)&MASK))
        if len(Br)!=k: continue
        S2r,S4r=moments(Br)
        sm=[0]
        for x in Br: sm=sm+[s+x for s in sm]
        nr=sum(Br)//2; lmr=0
        for idx,s in enumerate(sm):
            e=abs(s-nr); ok=True
            for j in range(k):
                ns=s-Br[j] if (idx>>j)&1 else s+Br[j]
                if abs(ns-nr)<=e: ok=False; break
            if ok: lmr+=1
        gr=0.0;pp=1.0
        for x in Br: pp/=2.0; gr+=pp*x
        predr=2**k*gr*math.sqrt(2.0/(math.pi*S2r))
        rs.append((lmr/predr, lmr/predr/(1.0-S4r/(4.0*S2r*S2r))))
    m0=statistics.mean(x for x,_ in rs); m1=statistics.mean(y for _,y in rs)
    sd1=statistics.stdev(y for _,y in rs)
    print(f" {k:3d}    {lm/pred:8.4f}    {lm/pred/corr:8.4f}   |     {m0:8.4f}          {m1:8.4f}       {sd1:8.4f}")
print()
print("  判定: 補正後が 1 に寄れば『0.97 の謎』は M2.4 で説明できたことになる。")
