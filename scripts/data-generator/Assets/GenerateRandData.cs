using System;
using UnityEngine;

public class GenerateRandData : MonoBehaviour
{
    public int num_pictures = 10;
    public int frames_per_picture = 20;

    public SetCameraPosition campos;
    public int i = 0;
    public int num = 0;

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {   
        
    }

    // Update is called once per frame
    void Update()
    {
        if (i %20==0 && num < num_pictures) {
            campos.SetCamera();
            num++;
        }
        i++;
    }
}
