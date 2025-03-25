using System;
using System.Text;
using System.Collections.Generic;
using UnityEngine;

public class RandomFENGenerator
{
    private static readonly char[] Pieces = { 'K', 'Q', 'R', 'B', 'N', 'P', 'k', 'q', 'r', 'b', 'n', 'p' };
    private static readonly System.Random Random = new System.Random();

    public static string GenerateRandomFEN()
    {
        string board = GenerateRandomBoard();
        char activeColor = Random.Next(2) == 0 ? 'w' : 'b';
        string castling = GenerateCastlingRights();
        string enPassant = GenerateEnPassantTargetSquare(activeColor);
        int halfMoveClock = Random.Next(0, 50);
        int fullMoveNumber = Random.Next(1, 100);
        
        // return $"{board} {activeColor} {castling} {enPassant} {halfMoveClock} {fullMoveNumber}";
        return $"{board}";
    }

    private static string GenerateRandomBoard()
    {
        StringBuilder board = new StringBuilder();
        for (int i = 0; i < 8; i++)
        {
            int emptyCount = 0;
            for (int j = 0; j < 8; j++)
            {
                if (Random.Next(2) == 0) // 33% chance of empty square
                {
                    emptyCount++;
                }
                else
                {
                    if (emptyCount > 0)
                    {
                        board.Append(emptyCount);
                        emptyCount = 0;
                    }
                    board.Append(Pieces[Random.Next(Pieces.Length)]);
                }
            }
            if (emptyCount > 0)
                board.Append(emptyCount);
            if (i < 7) board.Append('/');
        }
        return board.ToString();
    }

    private static string GenerateCastlingRights()
    {
        string options = "KQkq";
        List<char> rights = new List<char>();
        foreach (char c in options)
        {
            if (Random.Next(2) == 0) // 50% chance of keeping each right
                rights.Add(c);
        }
        return rights.Count > 0 ? string.Join("", rights) : "-";
    }

    private static string GenerateEnPassantTargetSquare(char activeColor)
    {
        if (Random.Next(3) == 0) // 33% chance to have en passant
        {
            char file = (char)('a' + Random.Next(8));
            char rank = activeColor == 'w' ? '6' : '3';
            return $"{file}{rank}";
        }
        return "-";
    }
}
