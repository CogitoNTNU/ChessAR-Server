using UnityEditor;
using UnityEngine;

[CustomEditor(typeof(SetRandomPosition))]
public class GenerateSingleSnapshot : Editor
{
    public override void OnInspectorGUI()
    {
        DrawDefaultInspector(); // Keep default fields visible
        SetRandomPosition script = (SetRandomPosition)target;
        if (GUILayout.Button("Save a random position screenshot and label"))
        {
            script.UpdatePosition();
            script.SaveImage("Chess_Image_" + System.DateTime.Now.ToString("dd-MM-yyyy-HH-mm-ss") + ".png");
            script.SaveLabel("Label_data_" + System.DateTime.Now.ToString("dd-MM-yyyy-HH-mm-ss") + ".txt");
        }
    }
}
