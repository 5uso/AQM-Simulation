using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class SimulationDisplay : MonoBehaviour
{
    public TMP_Text text;
    public SimulationManager mgr;

    // Start is called before the first frame update
    void Start() {
        System.Globalization.CultureInfo culture = (System.Globalization.CultureInfo)System.Threading.Thread.CurrentThread.CurrentCulture.Clone();
        culture.NumberFormat.NumberDecimalSeparator = ".";

        System.Threading.Thread.CurrentThread.CurrentCulture = culture;
    }

    // Update is called once per frame
    void Update() {
        double estimate = mgr.estimate();
        text.color = estimate <= 2 ? new Color32(0, 255, 0, 255) : new Color32(255, 0, 0, 255);
        if(double.IsNaN(estimate)) estimate = 0.0;
        text.text = string.Format("<mspace=0.6em>|S| = {0:0.0000} ≤ 2</mspace>", estimate);
    }
}
