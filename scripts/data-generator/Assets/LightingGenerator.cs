using UnityEngine;
public class LightingGenerator : MonoBehaviour
{
    public Light light;
    private int temperature = 6570;
    private float intensity = 85915;

    void Start()
    {
        light.intensity = intensity;
        light.colorTemperature = temperature;
    }

    public void SetRandomLightingValue()
    {
        int minTemperature = 1000;
        int maxTemperature = 10000;
        float minIntensity = 0.0f;
        float maxIntensity = 100000.0f;
        temperature = Random.Range(minTemperature, maxTemperature);
        intensity = Random.Range(minIntensity, maxIntensity);
        SetLighting(temperature, intensity);
    }

    private void SetLighting(int temperature, float intensity)
    {
        light.colorTemperature = temperature;
        light.intensity = intensity;
    }
}