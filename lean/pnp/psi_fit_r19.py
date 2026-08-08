# psi_fit_r19.py : fable-5 の予言 x1 だけで測定を説明したときの
#   比例係数 c と R^2 が、窓幅 hw を変えても安定かどうか(V3)。
exec(open('psi_hw_r19.py').read().split('HWS=[')[0])
KS=list(range(20,41,2)); HWS=[24,48,96,192]
D_={}
for k in KS:
    B=[a for a in ALLP[:k] if a>4]; D,D3,S1,S2=arith(B)
    D_[k]=(B,SQ*(D+D3/S2)/S2,rep_counts(B),D)
print("  hw    比例係数c     R^2      (モデル: 実測sl = c * g予言)")
for hw in HWS:
    X=[D_[k][1] for k in KS]; Y=[slope(D_[k][2],D_[k][0],hw) for k in KS]
    c=sum(x*y for x,y in zip(X,Y))/sum(x*x for x in X)
    my=sum(Y)/len(Y)
    ssr=sum((y-c*x)**2 for x,y in zip(X,Y)); sst=sum((y-my)**2 for y in Y)
    print(f"  {hw:4d}   {c:+8.4f}   {1-ssr/sst:8.5f}")
print()
print("  参考: |Delta|>=40 の k(30,32,34,36,38,40)だけに絞った場合")
KB=[30,32,34,36,38,40]
for hw in HWS:
    X=[D_[k][1] for k in KB]; Y=[slope(D_[k][2],D_[k][0],hw) for k in KB]
    c=sum(x*y for x,y in zip(X,Y))/sum(x*x for x in X)
    my=sum(Y)/len(Y)
    ssr=sum((y-c*x)**2 for x,y in zip(X,Y)); sst=sum((y-my)**2 for y in Y)
    print(f"  {hw:4d}   {c:+8.4f}   {1-ssr/sst:8.5f}")
