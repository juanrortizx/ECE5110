# Differentiation Test Results

| case_name | case_display_name | x | h | method | exact | approx | abs_error | rel_error | tolerance | pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sine_at_pi_over_4 | sin(x) at x=pi/4 | 0.7853981634 | 1e-05 | central | 0.7071067812 | 0.7071067812 | 1.396371907e-11 | 1.974768089e-11 | 1e-08 | PASS |
| sine_at_pi_over_4 | sin(x) at x=pi/4 | 0.7853981634 | 1e-05 | forward | 0.7071067812 | 0.7071067812 | 3.044520192e-11 | 4.305601746e-11 | 1e-06 | PASS |
| sine_at_pi_over_4 | sin(x) at x=pi/4 | 0.7853981634 | 1e-05 | backward | 0.7071067812 | 0.7071067812 | 8.240741423e-12 | 1.165416828e-11 | 1e-06 | PASS |
| exp_at_0p3 | exp(x) at x=0.3 | 0.3 | 1e-05 | central | 1.349858808 | 1.349858808 | 2.174482816e-11 | 1.610896491e-11 | 1e-08 | PASS |
| exp_at_0p3 | exp(x) at x=0.3 | 0.3 | 1e-05 | forward | 1.349858808 | 1.349858808 | 3.376632307e-11 | 2.501470738e-11 | 1e-06 | PASS |
| exp_at_0p3 | exp(x) at x=0.3 | 0.3 | 1e-05 | backward | 1.349858808 | 1.349858807 | 8.92774743e-11 | 6.613837966e-11 | 1e-06 | PASS |
| poly_cubic_minus_quadratic | x^3 - 2x^2 + x - 5 at x=1.2 | 1.2 | 1e-05 | central | 0.52 | 0.5200000001 | 1.259747862e-10 | 2.422592042e-10 | 1e-08 | PASS |
| poly_cubic_minus_quadratic | x^3 - 2x^2 + x - 5 at x=1.2 | 1.2 | 1e-05 | forward | 0.52 | 0.5199999999 | 1.404787398e-10 | 2.701514226e-10 | 1e-06 | PASS |
| poly_cubic_minus_quadratic | x^3 - 2x^2 + x - 5 at x=1.2 | 1.2 | 1e-05 | backward | 0.52 | 0.5199999999 | 1.404787398e-10 | 2.701514226e-10 | 1e-06 | PASS |
