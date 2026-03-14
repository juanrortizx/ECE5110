# 3-Point Numerical Differentiation Results

| Case | Method | Exact | Approx | Abs Error | Rel Error | Tolerance | Pass |
|---|---|---|---|---|---|---|---|
| sin(x) at x = π/4 | central | 7.071068e-01 | 7.071068e-01 | 1.396e-11 | 1.975e-11 | 1e-09 | Yes |
| sin(x) at x = π/4 | forward | 7.071068e-01 | 7.071068e-01 | 3.045e-11 | 4.306e-11 | 1e-09 | Yes |
| sin(x) at x = π/4 | backward | 7.071068e-01 | 7.071068e-01 | 8.241e-12 | 1.165e-11 | 1e-09 | Yes |
| exp(x) at x = 0.3 | central | 1.349859e+00 | 1.349859e+00 | 2.174e-11 | 1.611e-11 | 1e-09 | Yes |
| exp(x) at x = 0.3 | forward | 1.349859e+00 | 1.349859e+00 | 3.377e-11 | 2.501e-11 | 1e-09 | Yes |
| exp(x) at x = 0.3 | backward | 1.349859e+00 | 1.349859e+00 | 8.928e-11 | 6.614e-11 | 1e-09 | Yes |
| x³ − 2x² + x − 5 at x = 1.2 | central | 5.200000e-01 | 5.200000e-01 | 1.260e-10 | 2.423e-10 | 1e-08 | Yes |
| x³ − 2x² + x − 5 at x = 1.2 | forward | 5.200000e-01 | 5.200000e-01 | 1.405e-10 | 2.702e-10 | 1e-08 | Yes |
| x³ − 2x² + x − 5 at x = 1.2 | backward | 5.200000e-01 | 5.200000e-01 | 1.405e-10 | 2.702e-10 | 1e-08 | Yes |
