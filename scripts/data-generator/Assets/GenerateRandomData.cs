using System;
using UnityEngine;

public class GenerateRandomData : MonoBehaviour
{
  public int numPictures = 100;
  public int currPicture = 0;
  public SetRandomPosition pos;
  public int sleep = 200;
  public int interval = 0;

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
        pos.UpdatePosition();
        pos.SaveImage(screenshotName);
        pos.SaveLabel(labelName);
        currPicture++;
      }
    }
  }
}
