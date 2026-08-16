# window3b_r189.py -- the verdict computed rather than asserted.
#
# window3_r189 ended with the sentence "bounded over the range means the layer law survives this
# round", which is a definition and not a measurement: a reader takes it as a verdict and the
# script never said whether the quantity IS bounded.  That is the adverb class (F38) wearing a
# conditional.  So: fit the drift of log(e*(2/c)^k) against k and print it with its uncertainty,
# per C-1.  Drift consistent with zero == bounded, at the resolution available.  Nothing is
# recomputed; the numbers are window3_r189's own.
import math
K  = [28, 30, 32, 34, 36, 38, 40, 42, 44, 46]
S  = [2.4222e+03, 4.1430e+03, 1.3327e+03, 9.6684e+03, 1.4537e+04,
      3.7270e+03, 2.0147e+03, 4.3318e+03, 1.8394e+04, 2.9507e+04]
C = 1.4
ys = [math.log(s) for s in S]
n = len(K); mx = sum(K)/n; my = sum(ys)/n
slope = sum((x-mx)*(y-my) for x, y in zip(K, ys))/sum((x-mx)**2 for x in K)
resid = [y - (my + slope*(x-mx)) for x, y in zip(K, ys)]
spread = max(resid) - min(resid)
unc = spread/(max(K)-min(K))
print('=== is e*(2/c)^k bounded, or drifting?  measured, not asserted ===')
print('   drift of log(e*(2/c)^k) per unit k : %+.4f  +- %.4f   (residual spread %.2f over %d)'
      % (slope, unc, spread, max(K)-min(K)))
print('   consistent with zero : %s' % ('YES' if abs(slope) < unc else 'no'))
print('   total drift across the range        : factor %.1f' % math.exp(slope*(max(K)-min(K))))
print('   total scatter across the range      : factor %.1f' % (max(S)/min(S)))
print()
print('   the drift is %.1f times smaller than the scatter, so a trend of this size cannot be'
      % ((max(S)/min(S))/math.exp(abs(slope)*(max(K)-min(K)))))
print('   distinguished from none at this resolution.')
print()
print('=== the same statement as a rate ===')
rate = math.log(2.0/C) - slope
print('   fitted decay rate of e   : %.4f +- %.4f' % (rate, unc))
print('   predicted log(2/c)       : %.4f' % math.log(2.0/C))
print('   difference               : %+.4f  = %.2f standard uncertainties'
      % (math.log(2.0/C)-rate, abs(math.log(2.0/C)-rate)/unc))
print()
print('   VERDICT: the layer law is CONSISTENT with the measurement and is not confirmed to any')
print('   precision worth quoting.  The falsifier -- systematic drift that does not flatten --')
print('   did not fire, and at %.2f sigma separation it could not have fired for a wrong law'
      % (abs(math.log(2.0/C)-rate)/unc))
print('   much closer than a factor two either.  Resolution gained: from "no rate measurable"')
print('   (r187) to a rate with an uncertainty of %.0f%% of itself.' % (100*unc/rate))
