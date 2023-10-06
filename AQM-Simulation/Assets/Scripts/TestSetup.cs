using System;
using UnityEngine;

public class TestSetup {
    public double alpha;
    public double beta;

    Func<double, double, double, (bool, bool)> filter;

    private long PP = 0;
    private long PN = 0;
    private long NP = 0;
    private long NN = 0;

    public TestSetup(double alpha, double beta, Func<double, double, double, (bool, bool)> filter) {
        this.alpha = alpha;
        this.beta = beta;
        this.filter = filter;
    }

    public void photon(double polarization) {
        (bool passes_a, bool passes_b) r = filter(alpha, beta, polarization);
        if( r.passes_a &&  r.passes_b) PP++;
        if( r.passes_a && !r.passes_b) PN++;
        if(!r.passes_a &&  r.passes_b) NP++;
        if(!r.passes_a && !r.passes_b) NN++;
    }

    public double estimate() {
        return (double)(PP - PN - NP + NN) / (double)(PP + PN + NP + NN);
    }
}
