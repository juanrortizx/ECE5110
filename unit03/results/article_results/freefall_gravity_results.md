# Free-Fall Gravity Validation

This result uses a quadratic interpolant of position-versus-time data, then applies the central 3-point finite-difference method twice (position -> velocity -> acceleration).

## Gravity Estimate Summary

| case_name | display_name | interpolant_type | evaluation_time | step_size | accel_estimate_signed | accel_estimate_magnitude | target_gravity_magnitude | magnitude_abs_error | tolerance | passed | time_units | position_units | acceleration_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| freefall_gravity_interpolation | Free-fall gravity from quadratic interpolant | quadratic (polyfit degree 2) | 1.743060e-01 | 1.000000e-05 | -9.690388e+00 | 9.690388e+00 | 9.810000e+00 | 1.196123e-01 | 1.500000e-01 | Yes | s | m | m/s^2 |

## Source Data

| index | time_s | position_m |
| --- | --- | --- |
| 0 | 0.000000e+00 | 0.000000e+00 |
| 1 | 1.007640e-01 | -5.000000e-02 |
| 2 | 1.417360e-01 | -1.000000e-01 |
| 3 | 1.743060e-01 | -1.500000e-01 |
| 4 | 2.010420e-01 | -2.000000e-01 |
| 5 | 2.245830e-01 | -2.500000e-01 |
| 6 | 2.475690e-01 | -3.000000e-01 |

## Quadratic Interpolant Coefficients

| coefficient | value |
| --- | --- |
| a2 | -4.845194e+00 |
| a1 | -1.917325e-02 |
| a0 | 2.592830e-04 |
