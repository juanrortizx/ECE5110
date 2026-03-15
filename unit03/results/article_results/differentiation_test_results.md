# 3-Point Differentiation Test Results

| case_name | display_name | method | x | h | exact | approx | abs_error | rel_error | tolerance | passed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sine_at_pi_over_4 | sin(x) at x = pi/4 | central | 7.853982e-01 | 1.000000e-05 | 7.071068e-01 | 7.071068e-01 | 1.396372e-11 | 1.974768e-11 | 1.000000e-08 | Yes |
| sine_at_pi_over_4 | sin(x) at x = pi/4 | forward | 7.853982e-01 | 1.000000e-05 | 7.071068e-01 | 7.071068e-01 | 3.044520e-11 | 4.305602e-11 | 1.000000e-07 | Yes |
| sine_at_pi_over_4 | sin(x) at x = pi/4 | backward | 7.853982e-01 | 1.000000e-05 | 7.071068e-01 | 7.071068e-01 | 8.240741e-12 | 1.165417e-11 | 1.000000e-07 | Yes |
| exp_at_0p3 | exp(x) at x = 0.3 | central | 3.000000e-01 | 1.000000e-05 | 1.349859e+00 | 1.349859e+00 | 2.174483e-11 | 1.610896e-11 | 1.000000e-08 | Yes |
| exp_at_0p3 | exp(x) at x = 0.3 | forward | 3.000000e-01 | 1.000000e-05 | 1.349859e+00 | 1.349859e+00 | 3.376632e-11 | 2.501471e-11 | 1.000000e-07 | Yes |
| exp_at_0p3 | exp(x) at x = 0.3 | backward | 3.000000e-01 | 1.000000e-05 | 1.349859e+00 | 1.349859e+00 | 8.927747e-11 | 6.613838e-11 | 1.000000e-07 | Yes |
| poly_cubic_minus_quadratic | x^3 - 2x^2 + x - 5 at x = 1.2 | central | 1.200000e+00 | 1.000000e-05 | 5.200000e-01 | 5.200000e-01 | 1.259748e-10 | 2.422592e-10 | 1.000000e-08 | Yes |
| poly_cubic_minus_quadratic | x^3 - 2x^2 + x - 5 at x = 1.2 | forward | 1.200000e+00 | 1.000000e-05 | 5.200000e-01 | 5.200000e-01 | 1.404787e-10 | 2.701514e-10 | 1.000000e-07 | Yes |
| poly_cubic_minus_quadratic | x^3 - 2x^2 + x - 5 at x = 1.2 | backward | 1.200000e+00 | 1.000000e-05 | 5.200000e-01 | 5.200000e-01 | 1.404787e-10 | 2.701514e-10 | 1.000000e-07 | Yes |
