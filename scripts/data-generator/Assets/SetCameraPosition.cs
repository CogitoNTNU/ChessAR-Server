using System;
using System.IO;
using Microsoft.Unity.VisualStudio.Editor;
using Unity.Collections;
using Unity.IO.LowLevel.Unsafe;
using UnityEngine;


public class SetCameraPosition : MonoBehaviour
{
    public int upscale = 2;
    public float min_rho = 5;
    public float max_rho = 7;
    public float min_theta = -Convert.ToSingle(Math.PI)/4;
    public float max_theta = Convert.ToSingle(Math.PI)/4;
    public float min_phi = Convert.ToSingle(Math.PI)/6;
    public float max_phi = Convert.ToSingle(Math.PI)/3;

    public float max_rotation_offset = 1;

    public string screenshotFolderPath = "Assets/Screenshots/";
    public string labelFolderPath = "Assets/Labels/";
    public Camera mainCamera;  // The camera to project onto
    public GameObject chessboard; // The chessboard object
    public SetGameState setGameState;
    public GenerateRandData gendat;
    void Start()
    {
        if (mainCamera == null)
        {
            mainCamera = Camera.main; // Auto-assign if not set
        }
        if (chessboard != null)
        {
            //SetCamera();
        }
        else
        {
            Debug.LogError("Chessboard object not assigned!");
        }
    }
    [ContextMenu("Randomize camera position")]
    public void SetCamera()
    {
        double rho;
        double theta;
        double phi;
        
        int color = UnityEngine.Random.value < 0.5f ? 0 : 1;

        rho = Convert.ToDouble(UnityEngine.Random.Range(min_rho, max_rho));
        theta = Convert.ToDouble(color*Math.PI+UnityEngine.Random.Range(min_theta, max_theta));
        phi = Convert.ToDouble(UnityEngine.Random.Range(min_phi, max_phi));

        Vector3 rotation_offset = new Vector3(UnityEngine.Random.Range(-max_rotation_offset, max_rotation_offset), 0, UnityEngine.Random.Range(-max_rotation_offset, max_rotation_offset));
        chessboard.transform.transform.position += rotation_offset;

        Vector3 position = new Vector3(Convert.ToSingle(rho*Math.Sin(phi)*Math.Cos(theta)), Convert.ToSingle(rho*Math.Cos(phi)), Convert.ToSingle(rho*Math.Sin(phi)*Math.Sin(theta)));
        mainCamera.transform.position = position;
        mainCamera.transform.LookAt(chessboard.transform.transform, new Vector3(0,1,0));
        chessboard.transform.transform.position -= rotation_offset;

        setGameState.setBoardState();

        if (!System.IO.Directory.Exists(screenshotFolderPath))
            System.IO.Directory.CreateDirectory(screenshotFolderPath);
        
        var screenshotName = "Chess_Image_" + System.DateTime.Now.ToString("dd-MM-yyyy-HH-mm-ss") + "-"+gendat.num +".png";
        ScreenCapture.CaptureScreenshot(System.IO.Path.Combine(screenshotFolderPath, screenshotName), upscale);
        Debug.Log(System.IO.Path.Combine(screenshotFolderPath,screenshotName));


        SaveLabels();
    }

    void SaveLabels()
    {
        // Get the mesh bounds of the chessboard
        Renderer boardRenderer = chessboard.GetComponent<Renderer>();
        if (boardRenderer == null)
        {
            Debug.LogError("No Renderer found on the chessboard!");
            return;
        }
        Bounds bounds = boardRenderer.bounds;
        // Define the four corners in world space
        Vector3[] worldCorners = new Vector3[4];
        float cornerOffset = 0.4f; // For chessboard scale 10
        worldCorners[0] = new Vector3(bounds.min.x+cornerOffset, bounds.min.y, bounds.min.z+cornerOffset); // Bottom Left
        worldCorners[1] = new Vector3(bounds.max.x-cornerOffset, bounds.min.y, bounds.min.z+cornerOffset); // Bottom Right
        worldCorners[2] = new Vector3(bounds.min.x+cornerOffset, bounds.min.y, bounds.max.z-cornerOffset); // Top Left
        worldCorners[3] = new Vector3(bounds.max.x-cornerOffset, bounds.min.y, bounds.max.z-cornerOffset); // Top Right
        string[] cornerNames = { "Bottom Left", "Bottom Right", "Top Left", "Top Right" };
        // Project each corner onto the screen

        if (!System.IO.Directory.Exists(labelFolderPath))
            System.IO.Directory.CreateDirectory(labelFolderPath);
        
        string filename = "Label_data_" + System.DateTime.Now.ToString("dd-MM-yyyy-HH-mm-ss") + "-" + gendat.num + ".txt";
        string filepath = System.IO.Path.Combine(labelFolderPath, filename);
        
        using (StreamWriter writer = new StreamWriter(filepath, false)) {     
            for (int i = 0; i < worldCorners.Length; i++)
            {
                Vector3 screenPosition = mainCamera.WorldToScreenPoint(worldCorners[i]);
                if (screenPosition.z > 0) // Ensure it’s visible
                {
                    writer.WriteLine(0 + " " + screenPosition.x/Screen.width + " " + screenPosition.y/Screen.height + " " + "0.1" + " " + "0.1"); // class x y width height
                    Debug.Log($"{cornerNames[i]} projected at: {screenPosition}");
                }
                else
                {
                    Debug.Log($"{cornerNames[i]} is behind the camera!");
                }
            }
        }
    }
}

