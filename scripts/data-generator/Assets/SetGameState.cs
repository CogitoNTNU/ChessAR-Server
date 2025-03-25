using System;
using Unity.VisualScripting;
using Unity.VisualScripting.FullSerializer;
using UnityEditor.Experimental.GraphView;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;
using UnityEngine.Rendering;

public class SetGameState : MonoBehaviour {
  private Dictionary<char, string> fenPieceMap =
      new Dictionary<char, string>() {
        { 'r', "Rock  Black" },   { 'n', "Knight  Black" },
        { 'b', "Bishop  Black" }, { 'q', "Queen  Black" },
        { 'k', "King  Black" },   { 'p', "Pawn Black" },
        { 'R', "Rock White" },    { 'N', "Knight White" },
        { 'B', "Bishop White" },  { 'Q', "Queen White" },
        { 'K', "King White" },    { 'P', "Pawn White" }
      };
  private List<string> fens = new List<string>() {
    "rnbqkb1r/pp1p1ppp/4p2n/2p5/8/2N1P2N/PPPP1PPP/R1BQKB1R",
    "r6r/1b2k1bq/8/8/7B/8/8/R3K2R",
    "8/8/8/2k5/2pP4/8/B7/4K3",
    "r1bqkbnr/pppppppp/n7/8/8/P7/1PPPPPPP/RNBQKBNR",
    "r3k2r/p1pp1pb1/bn2Qnp1/2qPN3/1p2P3/2N5/PPPBBPPP/R3K2R",
    "2kr3r/p1ppqpb1/bn2Qnp1/3PN3/1p2P3/2N5/PPPBBPPP/R3K2R"
  };
  // https://gist.github.com/peterellisjones/8c46c28141c162d1d8a0f0badbc9cff9


    private List<GameObject> clones = new List<GameObject>();

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
    }

  // Update is called once per frame
  void Update() {}

    public void setBoardState() {
        
        while (clones.Count > 0) {
            
            GameObject c = clones.ElementAt(0);
            clones.RemoveAt(0);
            if (c != null) {
               Destroy(c);
            }
            c = null;
            
        }

        int x = 0;
        //string fen = fens[UnityEngine.Random.Range(0, fens.Count)];
        string fen = RandomFENGenerator.GenerateRandomFEN();
        foreach (char chr in fen) {
            if (chr == '/') {continue;}
            if (Char.IsDigit(chr))
            {                
                x += chr - 48;
            }
            else {
                place(fenPieceMap[chr], x);
                x += 1;  
            }
        }
    }

    void place(string piece, int idx) {
        float square_size = 0.6f;
        float col_zero = (5.0f-0.8f)/2f; // The x position of a1
        float row_zero = (4.98f-0.8f)/2f; // The y position of a1
        

    float col = col_zero - idx % 8 * square_size;
    float row = row_zero - idx / 8 * square_size;

    Vector3 position = new Vector3(row, 0, col);
    Quaternion rotation = Quaternion.Euler(-90, 0, 0);
    GameObject prefab = Resources.Load<GameObject>("Prefabs/" + piece);

    if (prefab == null) {
      Debug.LogError("Could not find prefab at Resources/Prefabs/" + piece);
      return;
    }

        GameObject clone = Instantiate(prefab, position, rotation);
        clone.transform.localScale = new Vector3(1000, 1000, 1000);

        clones.Add(clone);
        
        // Modify the clone to your heart's content
    }


}
