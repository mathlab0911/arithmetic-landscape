"""C20 controls, rerun after the prose/status separation, plus two new ones."""
import shutil, subprocess, os, sys
ROOT='/sessions/friendly-laughing-cerf/mnt/study'
T=os.path.join(ROOT,'paper/paper4.tex'); B='/tmp/lab/p4.bak'
shutil.copy(T,B)
A = r"\begin{remark}[what a surrogate costs, before any equidistribution input]\label{rem:surrogate}"
def run():
    r=subprocess.run([sys.executable,os.path.join(ROOT,'tools/check.py')],capture_output=True,text=True,cwd=ROOT)
    return 'C20/F66:' in r.stdout
cases=[
 ("status: measured only, no proof, not called open", r"\STATUS{measured only; we have no proof.}"),
 ("status: the Japanese form",                         r"\STATUS{測定のみ。証明はない。}"),
 ("status: 'unproved' buried in reassurance",          r"\STATUS{checked at 40000 points, though unproved.}"),
 ("PROSE outside any status, unquarantined",           "@PROSE@"),
 ("the quarantine phrase removed from an existing line","@STRIP@"),
 ("status that names it open -- must NOT fire",        r"\STATUS{measured only; we have no proof. Stated as an open question.}"),
 ("benign phrase SPLIT ACROSS A LINE BREAK -- must NOT fire", "@WRAP@"),
]
fired=[]
for i,(desc,inj) in enumerate(cases,1):
    s=open(B,encoding='utf-8').read()
    if inj=="@WRAP@":   s=s.replace(A,A+"\n"+r"\STATUS{proved. Measured for" + "\n" + r"confirmation only.}",1)
    elif inj=="@PROSE@":  s=s.replace(A,"That constant is measured, not proved.\n"+A,1)
    elif inj=="@STRIP@": s=s.replace("but that is measured, not proved, and the theorem does not need it.",
                                     "but that is measured, not proved.",1)
    else: s=s.replace(A,A+"\n"+inj,1)
    open(T,'w',encoding='utf-8').write(s)
    f=run(); fired.append(f)
    want = "must fire" if i<=5 else "must stay silent"
    ok = f if i<=5 else (not f)
    print(f"  {i}. {'FIRED ' if f else 'silent'}  [{'ok' if ok else 'WRONG'}]  {desc}  ({want})")
shutil.copy(B,T)
print(f"\n  5/5 defects fire: {all(fired[:5])};  escapes stay silent: {not any(fired[5:])}")
print(f"  restored and clean: {not run()}")
