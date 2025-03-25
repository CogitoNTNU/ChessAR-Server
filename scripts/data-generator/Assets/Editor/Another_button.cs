using UnityEditor;
using UnityEngine;

[CustomEditor(typeof(GenerateRandData))]
public class ButtonData : Editor
{
    public override void OnInspectorGUI()
    {
        DrawDefaultInspector(); // Keep default fields visible
        GenerateRandData script = (GenerateRandData)target;
        if (GUILayout.Button("Take pictures with random position and camera"))
        {
            script.i = 0;
            script.num = 0;
        }
    }
}
