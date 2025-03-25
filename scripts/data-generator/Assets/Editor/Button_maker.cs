using UnityEditor;
using UnityEngine;

[CustomEditor(typeof(SetCameraPosition))]
public class ButtonExampleEditor : Editor
{
    public override void OnInspectorGUI()
    {
        DrawDefaultInspector(); // Keep default fields visible
        SetCameraPosition script = (SetCameraPosition)target;
        if (GUILayout.Button("Take picture with random position and camera"))
        {
            script.SetCamera();
        }
    }
}
