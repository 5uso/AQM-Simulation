using System;
using UnityEngine;

public static class Filters {
    static bool polar_filter(double alpha, double polarization) {
        double amplitude = Math.Cos((alpha - polarization) * Math.PI / 180.0);
        return UnityEngine.Random.value < amplitude * amplitude;
    }

    public static (bool, bool) classical_filter(double alpha, double beta, double polarization) {
        bool passes_a = polar_filter(alpha, polarization);
        bool passes_b = polar_filter( beta, polarization);

        return (passes_a, passes_b);
    }

    public static (bool, bool) qm_filter(double alpha, double beta, double polarization) {
        bool order = UnityEngine.Random.value > 0.5;
        if(order) {
            double temp = alpha;
            alpha = beta;
            beta = temp;
        }

        bool passes_a = polar_filter(alpha, polarization);
        bool passes_b = polar_filter(beta, passes_a ? alpha : alpha + 90.0);

        return order ? (passes_a, passes_b) : (passes_b, passes_a);
    }

    public static (bool, bool) hidden_filter(double alpha, double beta, double polarization) {
        bool order = UnityEngine.Random.value > 0.5;
        if(order) {
            double temp = alpha;
            alpha = beta;
            beta = temp;
        }

        bool passes_a = polar_filter(alpha, polarization);
        double diff = Math.Abs((alpha % 180) - (beta % 180));
        if (diff > 90.0) diff = 180.0 - diff;
        bool passes_b = passes_a ^ (UnityEngine.Random.value < diff / 90.0);

        return order ? (passes_a, passes_b) : (passes_b, passes_a);
    }
}
