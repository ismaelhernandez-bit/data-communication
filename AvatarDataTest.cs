using System;
using System.Collections.Generic;
using UnityEngine;

// Attach to any GameObject and hit Play — no external files needed.
// Check the Console for the loaded avatar data.
public class AvatarDataTest : MonoBehaviour
{
    const string JSON = @"{
  ""version"": ""1.0"",
  ""avatars"": [
    { ""id"": ""avatar_001"", ""label"": ""Adult S"",  ""height_cm"": 162, ""shoulderWidth_cm"": 37, ""chest_cm"": 86,  ""waist_cm"": 68,  ""hips_cm"": 92,  ""inseam_cm"": 74, ""armLength_cm"": 57 },
    { ""id"": ""avatar_002"", ""label"": ""Adult M"",  ""height_cm"": 170, ""shoulderWidth_cm"": 41, ""chest_cm"": 96,  ""waist_cm"": 78,  ""hips_cm"": 100, ""inseam_cm"": 79, ""armLength_cm"": 60 },
    { ""id"": ""avatar_003"", ""label"": ""Adult L"",  ""height_cm"": 175, ""shoulderWidth_cm"": 46, ""chest_cm"": 108, ""waist_cm"": 92,  ""hips_cm"": 112, ""inseam_cm"": 81, ""armLength_cm"": 63 },
    { ""id"": ""avatar_004"", ""label"": ""Adult XL"", ""height_cm"": 178, ""shoulderWidth_cm"": 50, ""chest_cm"": 120, ""waist_cm"": 106, ""hips_cm"": 124, ""inseam_cm"": 82, ""armLength_cm"": 65 },
    { ""id"": ""avatar_005"", ""label"": ""Teen"",     ""height_cm"": 152, ""shoulderWidth_cm"": 34, ""chest_cm"": 78,  ""waist_cm"": 62,  ""hips_cm"": 82,  ""inseam_cm"": 68, ""armLength_cm"": 53 }
  ]
}";

    void Start()
    {
        var data = JsonUtility.FromJson<AvatarTestData>(JSON);
        foreach (var a in data.avatars)
        {
            Debug.Log(
                $"[{a.id}] {a.label} — " +
                $"Height: {a.height_cm}cm | Shoulders: {a.shoulderWidth_cm}cm | " +
                $"Chest: {a.chest_cm}cm | Waist: {a.waist_cm}cm | Hips: {a.hips_cm}cm | " +
                $"Inseam: {a.inseam_cm}cm | Arm: {a.armLength_cm}cm"
            );
        }
        Debug.Log($"[AvatarDataTest] {data.avatars.Count} avatars loaded OK.");
    }

    [Serializable] class AvatarTestData { public List<AvatarEntry> avatars; }

    [Serializable]
    class AvatarEntry
    {
        public string id, label;
        public float height_cm, shoulderWidth_cm, chest_cm, waist_cm, hips_cm, inseam_cm, armLength_cm;
    }
}
