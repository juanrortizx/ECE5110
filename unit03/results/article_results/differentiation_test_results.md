| case | case_display | method | x | h | exact | approx | abs_error | rel_error | tolerance | passed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sin_x | sin(x) at x=pi/4 | central | 0.78539816 | 1e-05 | 0.70710678 | 0.70710678 | 1.3963719e-11 | 1.9747681e-11 | 1e-08 | True |
| sin_x | sin(x) at x=pi/4 | forward | 0.78539816 | 1e-05 | 0.70710678 | 0.70710678 | 3.0445202e-11 | 4.3056017e-11 | 1e-05 | True |
| sin_x | sin(x) at x=pi/4 | backward | 0.78539816 | 1e-05 | 0.70710678 | 0.70710678 | 8.2407414e-12 | 1.1654168e-11 | 1e-05 | True |
| exp_x | exp(x) at x=0.3 | central | 0.3 | 1e-05 | 1.3498588 | 1.3498588 | 2.1744828e-11 | 1.6108965e-11 | 1e-08 | True |
| exp_x | exp(x) at x=0.3 | forward | 0.3 | 1e-05 | 1.3498588 | 1.3498588 | 3.3766323e-11 | 2.5014707e-11 | 2e-05 | True |
| exp_x | exp(x) at x=0.3 | backward | 0.3 | 1e-05 | 1.3498588 | 1.3498588 | 8.9277474e-11 | 6.613838e-11 | 2e-05 | True |
| cubic_poly | x^3 - 2x^2 + x - 5 at x=1.2 | central | 1.2 | 1e-05 | 0.52 | 0.52 | 1.2597479e-10 | 2.422592e-10 | 1e-08 | True |
| cubic_poly | x^3 - 2x^2 + x - 5 at x=1.2 | forward | 1.2 | 1e-05 | 0.52 | 0.52 | 1.4047874e-10 | 2.7015142e-10 | 1e-05 | True |
| cubic_poly | x^3 - 2x^2 + x - 5 at x=1.2 | backward | 1.2 | 1e-05 | 0.52 | 0.52 | 1.4047874e-10 | 2.7015142e-10 | 1e-05 | True |