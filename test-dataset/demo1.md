# demo dataset 1

This handwritten dataset simulates three hosts on a broadcast media with 1ms delay.  
The trace is captured on hostA.

1. At 0ms, hostA expresses an Interest for `/C/1`.
2. At 1ms, hostC responds to interest1.
3. At 10ms, hostB expresses an Interest for `/A/1`.
4. At 11ms, hostA responds to interest3.
5. At 20ms, hostB expresses an Interest for `/C/2`.
6. At 21ms, hostC responds to interest5.
7. At 28ms, hostC becomes offline.
8. At 30ms, hostB expresses an Interest for `/C/1`.
9. At 31ms, hostA responds to interest8 from its cache.
