using System;
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class SimulationManager : MonoBehaviour {
    TestSetup[] setups;

    [SerializeField] private TMP_Text text;
    [SerializeField] private TMP_Text[] sliderText;
    [SerializeField] private Toggle[] toggles;

    bool active = true;

    double a  = 0;
    double a_ = 45;
    double b  = 22.5;
    double b_ = 67.5;

    private bool handling_toggle = false;

    public double estimate() {
        return setups[0].estimate() - setups[1].estimate() + setups[2].estimate() + setups[3].estimate();
    }

    void Start() {
        setups = transform.GetComponentsInChildren<TestSetup>();

        System.Globalization.CultureInfo culture = (System.Globalization.CultureInfo)System.Threading.Thread.CurrentThread.CurrentCulture.Clone();
        culture.NumberFormat.NumberDecimalSeparator = ".";

        System.Threading.Thread.CurrentThread.CurrentCulture = culture;
    }

    void Update() {
        handling_toggle = false;
        if (!active) return;

        foreach(TestSetup setup in setups) {
            double polarization = UnityEngine.Random.value * 360.0;
            setup.photon(polarization);
        }

        double s = estimate();
        text.color = s <= 2.1 ? new Color32(0, 255, 0, 255) : new Color32(255, 0, 0, 255);
        if (double.IsNaN(s)) s = 0.0;
        text.text = string.Format("<mspace=0.55em>|S| = {0:0.0000} ≤ 2</mspace>", s);
    }

    public void updateA(float value)
    {
        a = value / 2.0;
        setups[0].alpha = a;
        setups[1].alpha = a;
        sliderText[0].text = string.Format("{0:0.0}º", a);
    }

    public void updateA_(float value)
    {
        a_ = value / 2.0;
        setups[2].alpha = a_;
        setups[3].alpha = a_;
        sliderText[1].text = string.Format("{0:0.0}º", a_);
    }

    public void updateB(float value)
    {
        b = value / 2.0;
        setups[0].beta = b;
        setups[2].beta = b;
        sliderText[2].text = string.Format("{0:0.0}º", b);
    }

    public void updateB_(float value)
    {
        b_ = value / 2.0;
        setups[1].beta = b_;
        setups[3].beta = b_;
        sliderText[3].text = string.Format("{0:0.0}º", b_);
    }

    public void set_qm()
    {
        active = true;
        foreach(TestSetup s in setups)
        {
            s.filter = Filters.qm_filter;
            s.reset();
        }
    }

    public void set_hidden()
    {
        active = true;
        foreach (TestSetup s in setups)
        {
            s.filter = Filters.hidden_filter;
            s.reset();
        }
    }

    public void set_classical()
    {
        active = true;
        foreach (TestSetup s in setups)
        {
            s.filter = Filters.classical_filter;
            s.reset();
        }
    }

    public void set_none()
    {
        active = false;
    }

    public void toggle_qm(bool value)
    {
        if (handling_toggle) return;
        handling_toggle = true;
        if (value)
        {
            set_qm();
            toggles[1].isOn = toggles[2].isOn = false;
            return;
        }

        set_none();
    }

    public void toggle_hidden(bool value)
    {
        if (handling_toggle) return;
        handling_toggle = true;
        if (value)
        {
            set_hidden();
            toggles[0].isOn = toggles[2].isOn = false;
            return;
        }

        set_none();
    }

    public void toggle_classical(bool value)
    {
        if (handling_toggle) return;
        handling_toggle = true;
        if (value)
        {
            set_classical();
            toggles[0].isOn = toggles[1].isOn = false;
            return;
        }

        set_none();
    }
}
