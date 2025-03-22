using UnityEngine;
public class ChessboardProjection : MonoBehaviour
{
    public Camera mainCamera;  // The camera to project onto
    public GameObject chessboard; // The chessboard object
    void Start()
    {
        if (mainCamera == null)
        {
            mainCamera = Camera.main; // Auto-assign if not set
        }
        if (chessboard != null)
        {
            ProjectBoardCorners();
        }
        else
        {
            Debug.LogError("Chessboard object not assigned!");
        }
    }
    void ProjectBoardCorners()
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
        worldCorners[0] = new Vector3(bounds.min.x, bounds.min.y, bounds.min.z); // Bottom Left
        worldCorners[1] = new Vector3(bounds.max.x, bounds.min.y, bounds.min.z); // Bottom Right
        worldCorners[2] = new Vector3(bounds.min.x, bounds.min.y, bounds.max.z); // Top Left
        worldCorners[3] = new Vector3(bounds.max.x, bounds.min.y, bounds.max.z); // Top Right
        string[] cornerNames = { "Bottom Left", "Bottom Right", "Top Left", "Top Right" };
        // Project each corner onto the screen
        for (int i = 0; i < worldCorners.Length; i++)
        {
            Vector3 screenPosition = mainCamera.WorldToScreenPoint(worldCorners[i]);
            if (screenPosition.z > 0) // Ensure it’s visible
            {
                Debug.Log($"{cornerNames[i]} projected at: {screenPosition}");
            }
            else
            {
                Debug.Log($"{cornerNames[i]} is behind the camera!");
            }
        }
    }
}