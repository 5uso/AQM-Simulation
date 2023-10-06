using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SimulationManager : MonoBehaviour {
    TestSetup[] setups = new TestSetup[4];

    bool active = true;

    Func<double, double, double, (bool, bool)> filter = Filters.qm_filter;
    double a  =  0.0;
    double a_ = 45.0;
    double b  = 22.5;
    double b_ = 67.5;

    public double estimate() {
        return setups[0].estimate() - setups[1].estimate() + setups[2].estimate() + setups[3].estimate();
    }

    // Start is called before the first frame update
    void Start() {
        setups[0] = new TestSetup(a , b , filter);
        setups[1] = new TestSetup(a , b_, filter);
        setups[2] = new TestSetup(a_, b , filter);
        setups[3] = new TestSetup(a_, b_, filter);
    }

    // Update is called once per frame
    void Update() {
        if(!active) return;

        foreach(TestSetup setup in setups) {
            double polarization = UnityEngine.Random.value * 360.0;
            setup.photon(polarization);
        }
    }
}
