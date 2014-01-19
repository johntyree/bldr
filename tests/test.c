// bldr: gcc -lm -o %:r %
// bldr: ./%:r
// bldr: rm %:r

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <assert.h>

int main() {
    printf("%f\n", sin(M_PI_4));
    return 0;
}
