using UnityEngine;
using UnityEditor;
using System.Collections.Generic;
using JetBrains.Annotations;

public class ObjectFinder : MonoBehaviour {
  public int counter = 0;
  List<GameObject> GetAllObjectsOnlyInScene() {
    List<GameObject> objectsInScene = new List<GameObject>();

    foreach (GameObject go in Resources.FindObjectsOfTypeAll(typeof(GameObject))
                 as GameObject[]) {
      if (!EditorUtility.IsPersistent(go.transform.root.gameObject) &&
          !(go.hideFlags == HideFlags.NotEditable ||
            go.hideFlags == HideFlags.HideAndDontSave))
        objectsInScene.Add(go);
    }
    return objectsInScene;
  }

  // Start is called once before the first execution of Update after the
  // MonoBehaviour is created

  private List<GameObject> objects;

  void Start() {
    // Debug.Log("Hello, World! Start");
    objects = GetAllObjectsOnlyInScene();

    foreach (GameObject go in objects) {
      // Debug.Log(go);
      // Debug.Log(go.transform.position);
    }
  }

  // Update is called once per frame
  void Update() {

    foreach (GameObject go in objects) {
      if (go.tag == "piece") {
        Vector3 transformation = new Vector3(-0.001f, 0.0f, 0.0f);
        // go.transform.position += transformation;
        // Debug.Log(go.transform.position);
      }
    }
  }
}
