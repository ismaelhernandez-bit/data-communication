using UnityEngine;
using UnityEngine.UI;
using TMPro;

// Example: wire up to a UI panel to display info for a clicked object.
// Each clickable GameObject should have an AssetTag component with the correct asset id.
public class AssetInfoPanel : MonoBehaviour
{
    [Header("UI References")]
    public GameObject panel;
    public TMP_Text nameText;
    public TMP_Text categoryText;
    public TMP_Text materialText;
    public TMP_Text colourText;
    public TMP_Text dimensionsText;
    public TMP_Text descriptionText;
    public TMP_Text priceText;

    public void ShowAsset(string assetId)
    {
        AssetEntry entry = AssetInfoLoader.Catalogue?.assets.Find(a => a.id == assetId);
        if (entry == null)
        {
            Debug.LogWarning($"[AssetInfoPanel] No asset found for id: {assetId}");
            return;
        }

        nameText.text        = entry.name;
        categoryText.text    = entry.category;
        materialText.text    = entry.material;
        colourText.text      = entry.colour;
        dimensionsText.text  = $"{entry.dimensions.height_cm} H × {entry.dimensions.width_cm} W × {entry.dimensions.depth_cm} D cm";
        descriptionText.text = entry.description;
        priceText.text       = $"${entry.price_aud:0.00} AUD";

        panel.SetActive(true);
    }

    public void Hide() => panel.SetActive(false);
}
