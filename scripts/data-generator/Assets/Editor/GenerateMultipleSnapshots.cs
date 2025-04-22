using UnityEditor;
using UnityEngine;

[CustomEditor(typeof(GenerateRandomData))]
public class GenerateMultipleSnapshots : Editor
{
  public override void OnInspectorGUI()
  {
    DrawDefaultInspector(); // Keep default fields visible
    GenerateRandomData script = (GenerateRandomData)target;
    if (GUILayout.Button("Take pictures with random position and camera"))
    {
      script.numPictures = 100;
      script.currPicture = 0;
      script.sleep = 200;
      script.interval = 0;
    }
  }
}
