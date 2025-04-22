using System;
using UnityEngine;

public class DataGenerator : MonoBehaviour
{
  public int numPictures = 1000;
  public int currPicture = 0;
  public int sleep = 10;
  public int interval = 0;

  public SetRandomPosition pos;
  public LightingGenerator lightingGenerator;

  void Update()
  {
    if (interval <= sleep)
    {
      interval++;
      if (currPicture >= numPictures)
      {
        Debug.Log("Finished generating data");
      }
    }
    else
    {
      interval = 0;
      if (currPicture < numPictures)
      {
        string screenshotName = "Chess_Image_" + System.DateTime.Now.ToString("dd-MM-yyyy-HH-mm-ss") + "-" + currPicture + ".png";
        string labelName = "Label_data_" + System.DateTime.Now.ToString("dd-MM-yyyy-HH-mm-ss") + "-" + currPicture + ".txt";
        lightingGenerator.SetRandomLightingValue();
        pos.UpdatePosition();
        pos.SaveImage(screenshotName);
        pos.SaveLabel(labelName);
        currPicture++;
      }
    }
  }
}
