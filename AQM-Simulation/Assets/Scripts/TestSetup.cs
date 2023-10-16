using System;
using TMPro;
using UnityEngine;

public class TestSetup : MonoBehaviour {
    public double alpha;
    public double beta;
    public bool lightMode = false;

    [SerializeField] private TMP_Text text;
    [SerializeField] private TMP_Text sourceText;
    [SerializeField] private TMP_Text[] splitterText;
    [SerializeField] private TMP_Text[] detectorText;

    [SerializeField] private GameObject[] beams;
    private Material[] beamMats;

    public Func<double, double, double, (bool, bool)> filter = Filters.qm_filter;

    private long total = 0;
    private long PP = 0;
    private long PN = 0;
    private long NP = 0;
    private long NN = 0;
    private long LP = 0;
    private long LN = 0;
    private long RP = 0;
    private long RN = 0;

    public void photon(double polarization) {
        total++;
        (bool passes_a, bool passes_b) r = filter(alpha, beta, polarization);
        if(r.passes_a)
        {
            LP++;
            if (r.passes_b) { RP++; PP++; }
            else { RN++; PN++; }
        }
        else
        {
            LN++;
            if (r.passes_b) { RP++; NP++; }
            else { RN++; NN++; }
        }
    }

    public double estimate() {
        return (double)(PP - PN - NP + NN) / (double)(PP + PN + NP + NN);
    }

    private void Start()
    {
        beamMats = new Material[beams.Length];
        for (int i = 0; i < beams.Length; i++)
        {
            beamMats[i] = beams[i].GetComponent<Renderer>().material;
            beamMats[i].SetFloat("_Intensity", 1.0f);
        }
    }

    void Update()
    {
        double sum = PP + PN + NP + NN;
        double a = PP / sum;
        double b = PN / sum;
        double c = NP / sum;
        double d = NN / sum;
        string neutralColor = lightMode ? "#000000" : "#FFFFFF";
        string yellowColor = lightMode ? "#EBC700" : "#F1FF00";
        text.text = string.Format("<mspace=0.5em><#00DDFF>↑<#F000FF>↑<{5}> {0:0.00}   <#00DDFF>↑<{6}>↓<{5}> {1:0.00}\r\n<#FF4040>↓<#F000FF>↑<{5}> {2:0.00}   <#FF4040>↓<{6}>↓<{5}> {3:0.00}\r\n\r\n{4:0.0000}", a, b, c, d, estimate(), neutralColor, yellowColor);

        sourceText.text = string.Format("{0}", total);

        double lpp = LP / sum;
        double lnp = LN / sum;
        double rpp = RP / sum;
        double rnp = RN / sum;
        beamMats[2].SetFloat("_Intensity", (float)lpp);
        beamMats[3].SetFloat("_Intensity", (float)lnp);
        beamMats[4].SetFloat("_Intensity", (float)rpp);
        beamMats[5].SetFloat("_Intensity", (float)rnp);
        detectorText[0].text = string.Format("{0:0.00}", lpp);
        detectorText[1].text = string.Format("{0:0.00}", lnp);
        detectorText[2].text = string.Format("{0:0.00}", rpp);
        detectorText[3].text = string.Format("{0:0.00}", rnp);

        splitterText[0].text = string.Format("{0:0.0}º", alpha);
        splitterText[1].text = string.Format("{0:0.0}º", beta);
    }

    public void reset()
    {
        total = 0;
        PP = 0;
        PN = 0;
        NP = 0;
        NN = 0;
        LP = 0;
        LN = 0;
        RP = 0;
        RN = 0;
    }
}
