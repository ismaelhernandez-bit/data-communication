using System;
using System.IO;
using System.Collections.Generic;
using UnityEngine;

// Drop assets.json into Assets/StreamingAssets/, then attach this component
// to any GameObject. On Start it loads the catalogue and stores it in Catalogue.
public class AssetInfoLoader : MonoBehaviour
{
    public static AssetCatalogue Catalogue { get; private set; }

    void Start()
    {
        string path = Path.Combine(Application.streamingAssetsPath, "assets.json");
        if (!File.Exists(path))
        {
            Debug.LogError($"[AssetInfoLoader] assets.json not found at: {path}");
            return;
        }

        string json = File.ReadAllText(path);
        Catalogue = JsonUtility.FromJson<AssetCatalogue>(json);
        Debug.Log($"[AssetInfoLoader] Loaded {Catalogue.asset_count} assets.");
    }
}

// ── Data model ────────────────────────────────────────────────────────────────

[Serializable]
public class AssetCatalogue
{
    public string version;
    public int asset_count;
    public List<AssetEntry> assets;
}

[Serializable]
public class AssetEntry
{
    public string id;
    public string name;
    public string category;
    public string material;
    public string colour;
    public AssetDimensions dimensions;
    public string description;
    public string sku;
    public float price_aud;
}

[Serializable]
public class AssetDimensions
{
    public float height_cm;
    public float width_cm;
    public float depth_cm;
}
