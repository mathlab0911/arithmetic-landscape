# hwspot_r24.py : 作業3(任意)。k=18 で振幅を hw=16 と hw=24 で測り差を見る。
exec(open('k2psi_r20.py').read().split('KS=list')[0])
k=18; B=[a for a in ALLP[:k] if a>4]; b=len(B); r=rep_counts(B)
D,D3,S1,S2,S4,c1,c5=arith(B)
K2=math.exp(expo(B,'K2'))
print("  hw   窓の周期数   hw/sigma   実測比      実測/K2")
for hw in (12,16,24,32):
    amp,_=dft(B,r,sum(B)//2,hw)
    meas=amp/(2*SQ**(b+1))
    print(f"  {hw:3d}     {2*hw/6:5.1f}     {hw/(math.sqrt(S2)/2):6.3f}   {meas:8.5f}   {meas/K2:8.5f}")
print()
print("  hw=16 と hw=24 の実測/K2 の差が 1% 未満なら、窓幅の選択は結論に影響しない(V3)。")
