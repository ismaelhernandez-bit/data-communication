# Unity Info Script — Setup Guide

Generates a dummy JSON catalogue of mall assets and avatar body measurements for Unity UI integration. No real pipeline output required — run the script, drop the file into Unity, done.

---

## Files

| File | Purpose |
|------|---------|
| `info.py` | Generates `assets.json` and `avatars.json` from hardcoded dummy data |
| `avatars.json` | Avatar body measurements only — use this for current Unity integration |
| `assets.json` | Full catalogue (assets + avatars combined) — for later use |
| `AvatarDataTest.cs` | Self-contained Unity test script — no external files needed, use this first |
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

## Step 2 — Quick Test in Unity (no files needed)

This is the fastest way to verify the avatar data works in Unity. No file copying required — the data is baked directly into the script.

### 2.1 Open Unity Hub and create a project

1. Open **Unity Hub** from your Applications folder
2. Click **New project** (top right)
3. Select the **3D (Core)** template
4. Give it any name, e.g. `AvatarTest`
5. Click **Create project** — takes a minute the first time

### 2.2 Add the test script

Once Unity opens, look at the **Project** panel at the bottom — this is your file browser inside Unity.

1. Right-click the **Assets** folder → **Create → Folder** → name it `Scripts`
2. Open Finder, go to your `Elysium/Unity Info Script/` folder
3. Drag `AvatarDataTest.cs` into the `Scripts` folder in Unity

### 2.3 Attach it to a GameObject

1. In the **Hierarchy** panel (left side), click **Main Camera**
2. In the **Inspector** panel (right side), scroll down and click **Add Component**
3. Type `AvatarDataTest` and select it from the list

### 2.4 Hit Play and check the Console

1. Press the **Play button (▶)** at the top centre of the screen
2. Click the **Console** tab at the bottom (next to Project)
3. You should see all 5 avatars printed with their measurements:

```
[avatar_001] Adult S — Height: 162cm | Shoulders: 37cm | Chest: 86cm ...
[avatar_002] Adult M — Height: 170cm | Shoulders: 41cm | Chest: 96cm ...
...
[AvatarDataTest] 5 avatars loaded OK.
```

Press **▶ again** to stop. If you see the log lines, everything is working.

---

## Step 3 — Unity Setup (with the real JSON file)

Once the quick test passes, switch to loading from the actual `avatars.json` file.

### 3.1 Place the data file

Copy `avatars.json` into your Unity project at:

```
Assets/StreamingAssets/avatars.json
```

Create the `StreamingAssets` folder if it doesn't exist. Unity will copy it alongside the build automatically on all platforms. When the full asset catalogue is ready, `assets.json` will be added here too.

### 3.2 Add the loader

1. Select any always-present GameObject (e.g. `GameManager`)
2. Add Component → `AssetInfoLoader`

That's it. On Play, the console will print:
```
[AssetInfoLoader] Loaded 10 assets, 5 avatars.
```

### 3.3 Add the info panel

1. Select your UI panel GameObject
2. Add Component → `AssetInfoPanel`
3. In the Inspector, wire each `TMP_Text` field to the matching Text element in your panel

### 3.4 Trigger display from a clickable object

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

---

## Step 4 — Sending data over a network (coming soon)

The current setup reads data from a local file. When you're ready to serve it over a network instead — so Unity fetches live data from a backend — the approach is:

1. Run a simple local server (one command, built into Python):
   ```bash
   python3 -m http.server 8000
   ```
   This serves `avatars.json` at `http://localhost:8000/avatars.json`.

2. In Unity, swap `File.ReadAllText` in `AssetInfoLoader.cs` for a `UnityWebRequest` call — Unity fetches the URL at runtime instead of reading a local file.

This is the path to a live backend once the full pipeline is operational. For now, the local file approach is sufficient.

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
