using System;
using System.IO;
using Unity.Collections;
using Unity.IO.LowLevel.Unsafe;
using UnityEngine;


public class SetRandomPosition : MonoBehaviour
{
    public int upscale = 2;
    public float min_rho = 5;
    public float max_rho = 7;
    public float min_theta = -Convert.ToSingle(Math.PI) / 4;
    public float max_theta = Convert.ToSingle(Math.PI) / 4;
    public float min_phi = Convert.ToSingle(Math.PI) / 6;
    public float max_phi = Convert.ToSingle(Math.PI) / 3;

    public float max_rotation_offset = 1;

    public string screenshotFolderPath = "./Data/Screenshots/";
    public string labelFolderPath = "./Data/Labels/";

    public Camera mainCamera;
    public GameObject chessboard;
    public ChessStateGenerator setGameState;

    void Start()
    {
        if (mainCamera == null)
        {
            mainCamera = Camera.main; // Auto-assign if not set
        }
        else
        {
            Debug.LogError("Chessboard object not assigned!");
        }
    }

    [ContextMenu("Randomize camera position")]
    public void UpdatePosition()
    {
        int color = UnityEngine.Random.value < 0.5f ? 0 : 1;

        double rho = Convert.ToDouble(UnityEngine.Random.Range(min_rho, max_rho));
        double theta = Convert.ToDouble(color * Math.PI +
                                 UnityEngine.Random.Range(min_theta, max_theta));
        double phi = Convert.ToDouble(UnityEngine.Random.Range(min_phi, max_phi));

        Vector3 rotation_offset = new Vector3(
            UnityEngine.Random.Range(-max_rotation_offset, max_rotation_offset), 0,
            UnityEngine.Random.Range(-max_rotation_offset, max_rotation_offset));
        chessboard.transform.transform.position += rotation_offset;

        Vector3 position = new Vector3(Convert.ToSingle(rho * Math.Sin(phi) * Math.Cos(theta)), Convert.ToSingle(rho * Math.Cos(phi)), Convert.ToSingle(rho * Math.Sin(phi) * Math.Sin(theta)));
        mainCamera.transform.position = position;
        mainCamera.transform.LookAt(chessboard.transform.transform, new Vector3(0, 1, 0));
        chessboard.transform.transform.position -= rotation_offset;

        setGameState.setBoardState();
    }

    public void SaveImage(string fileName)
    {
        if (!System.IO.Directory.Exists(screenshotFolderPath))
            System.IO.Directory.CreateDirectory(screenshotFolderPath);

        ScreenCapture.CaptureScreenshot(System.IO.Path.Combine(screenshotFolderPath, fileName), upscale);
        Debug.Log(System.IO.Path.Combine(screenshotFolderPath, fileName));
    }

    public void SaveLabel(string fileName)
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
        worldCorners[0] = new Vector3(bounds.min.x + cornerOffset, bounds.min.y,
                                      bounds.min.z + cornerOffset); // Bottom Left
        worldCorners[1] = new Vector3(bounds.max.x - cornerOffset, bounds.min.y,
                                      bounds.min.z + cornerOffset); // Bottom Right
        worldCorners[2] = new Vector3(bounds.min.x + cornerOffset, bounds.min.y,
                                      bounds.max.z - cornerOffset); // Top Left
        worldCorners[3] = new Vector3(bounds.max.x - cornerOffset, bounds.min.y,
                                      bounds.max.z - cornerOffset); // Top Right
        string[] cornerNames = { "Bottom Left", "Bottom Right", "Top Left",
                             "Top Right" };
        // Project each corner onto the screen

        if (!System.IO.Directory.Exists(labelFolderPath))
            System.IO.Directory.CreateDirectory(labelFolderPath);

        string filepath = System.IO.Path.Combine(labelFolderPath, fileName);

        using (StreamWriter writer = new StreamWriter(filepath, false))
        {
            for (int i = 0; i < worldCorners.Length; i++)
            {
                Vector3 screenPosition = mainCamera.WorldToScreenPoint(worldCorners[i]);
                if (screenPosition.z > 0) // Ensure it’s visible
                {
                    writer.WriteLine(0 + " " + screenPosition.x / Screen.width + " " + screenPosition.y / Screen.height + " " + "0.1" + " " + "0.1"); // class x y width height
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
