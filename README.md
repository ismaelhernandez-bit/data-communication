# Unity Info Script — Setup Guide

Generates a dummy JSON catalogue of mall assets and avatar body measurements for Unity UI integration. No real pipeline output required — run the script, drop the file into Unity, done.

---

## Files

| File | Purpose |
|------|---------|
| `info.py` | Generates `assets.json` and `avatars.json` from hardcoded dummy data |
| `avatars.json` | Avatar body measurements only — use this for current Unity integration |
| `assets.json` | Full catalogue (assets + avatars combined) — for later use |
| `AssetInfoLoader.cs` | Unity component — loads `assets.json` on Start |
| `AssetInfoPanel.cs` | Unity component — binds asset fields to UI Text elements |

---

## Step 1 — Generate the JSON

Requires Python 3 (no dependencies).

```bash
python3 info.py
# → avatars.json  (avatar data only — use this for now)
# → assets.json   (full catalogue, for later)
```

Run this whenever the schema changes or you want to refresh dummy data.

---

## Step 2 — Unity Setup

### 2.1 Place the data file

For now, copy `avatars.json` into your Unity project at:

```
Assets/StreamingAssets/avatars.json
```

Create the `StreamingAssets` folder if it doesn't exist. Unity will copy it alongside the build automatically on all platforms. When the full asset catalogue is ready, `assets.json` will be added here too.

### 2.2 Add the loader

1. Select any always-present GameObject (e.g. `GameManager`)
2. Add Component → `AssetInfoLoader`

That's it. On Play, the console will print:
```
[AssetInfoLoader] Loaded 10 assets, 5 avatars.
```

### 2.3 Add the info panel

1. Select your UI panel GameObject
2. Add Component → `AssetInfoPanel`
3. In the Inspector, wire each `TMP_Text` field to the matching Text element in your panel

### 2.4 Trigger display from a clickable object

On whatever script handles object click/selection:

```csharp
// Show an asset info panel
assetInfoPanel.ShowAsset("asset_001");

// Hide it
assetInfoPanel.Hide();
```

To look up an avatar directly:

```csharp
AvatarEntry avatar = AssetInfoLoader.Catalogue.avatars.Find(a => a.id == "avatar_002");
```

---

## JSON Schema

### Asset entry

```json
{
  "id": "asset_001",
  "name": "Oak Dining Chair",
  "category": "Seating",
  "material": "Solid Oak",
  "colour": "Natural Brown",
  "dimensions": {
    "height_cm": 92,
    "width_cm": 45,
    "depth_cm": 48
  },
  "description": "Classic solid oak dining chair with upholstered seat cushion.",
  "sku": "SEA-OAK-001",
  "price_aud": 299
}
```

| Field | Type | Unit | Notes |
|-------|------|------|-------|
| `id` | string | — | Unique identifier, e.g. `asset_001` |
| `name` | string | — | Display name for UI panel |
| `category` | string | — | One of: Seating, Tables, Storage, Lighting, Decor, Flooring |
| `material` | string | — | Primary material |
| `colour` | string | — | Colour description |
| `dimensions.height_cm` | float | cm | Vertical extent |
| `dimensions.width_cm` | float | cm | Horizontal extent |
| `dimensions.depth_cm` | float | cm | Front-to-back extent |
| `description` | string | — | Body copy for info panel |
| `sku` | string | — | Stock keeping unit |
| `price_aud` | float | AUD | Retail price |

### Avatar entry

```json
{
  "id": "avatar_002",
  "label": "Adult M",
  "height_cm": 170,
  "shoulderWidth_cm": 41,
  "chest_cm": 96,
  "waist_cm": 78,
  "hips_cm": 100,
  "inseam_cm": 79,
  "armLength_cm": 60
}
```

| Field | Type | Unit | Measurement |
|-------|------|------|-------------|
| `id` | string | — | Unique identifier, e.g. `avatar_001` |
| `label` | string | — | Size label for UI display |
| `height_cm` | float | cm | Full standing height, floor to top of head |
| `shoulderWidth_cm` | float | cm | Straight-line distance across shoulders, point to point |
| `chest_cm` | float | cm | Circumference around fullest part of chest |
| `waist_cm` | float | cm | Circumference around natural waist (narrowest point) |
| `hips_cm` | float | cm | Circumference around fullest part of hips/seat |
| `inseam_cm` | float | cm | Length: inner leg, crotch to floor |
| `armLength_cm` | float | cm | Length: shoulder point to wrist |

Dummy profiles included: Adult S / M / L / XL / Teen.

---

## Updating dummy data

All dummy data lives at the top of `info.py` in two lists: `ASSETS` and `AVATARS`. Edit those lists directly, then rerun `python3 info.py` and copy the updated `assets.json` into `Assets/StreamingAssets/`.

---

## Notes

- **StreamingAssets** is used because it works in the Unity Editor and in standalone builds without any networking. For a live backend, swap `File.ReadAllText` in `AssetInfoLoader.cs` for `UnityWebRequest`.
- `JsonUtility` (used in the loader) does not support dictionaries — all fields must be concrete class members. The current schema is already structured for this.
- `AssetInfoPanel.cs` requires **TextMeshPro** (`TMPro`). If your project uses standard `UI.Text`, replace `TMP_Text` with `Text` and update the `using` directive.
