import json

"""
SETUP:
Colleague's setup (5 steps)

1. In the Unity project, create Assets/StreamingAssets/ if it doesn't exist
2. Drop assets.json into that folder
3. Add AssetInfoLoader.cs to any always-present GameObject (e.g. GameManager)
4. Add AssetInfoPanel.cs to the info panel GameObject and wire the TMP_Text fields in the Inspector
5. From a clickable object's click handler, call: infoPanel.ShowAsset("asset_001")

"""

CATEGORIES = ["Seating", "Tables", "Storage", "Lighting", "Decor", "Flooring"]

# Avatar dummy data — synthetic body measurements for testing UI layout.
# Units: height/inseam/armLength in cm (lengths), all others in cm (circumferences).
AVATARS = [
    {
        "id": "avatar_001",
        "label": "Adult S",
        "height_cm": 162,
        "shoulderWidth_cm": 37,
        "chest_cm": 86,
        "waist_cm": 68,
        "hips_cm": 92,
        "inseam_cm": 74,
        "armLength_cm": 57,
    },
    {
        "id": "avatar_002",
        "label": "Adult M",
        "height_cm": 170,
        "shoulderWidth_cm": 41,
        "chest_cm": 96,
        "waist_cm": 78,
        "hips_cm": 100,
        "inseam_cm": 79,
        "armLength_cm": 60,
    },
    {
        "id": "avatar_003",
        "label": "Adult L",
        "height_cm": 175,
        "shoulderWidth_cm": 46,
        "chest_cm": 108,
        "waist_cm": 92,
        "hips_cm": 112,
        "inseam_cm": 81,
        "armLength_cm": 63,
    },
    {
        "id": "avatar_004",
        "label": "Adult XL",
        "height_cm": 178,
        "shoulderWidth_cm": 50,
        "chest_cm": 120,
        "waist_cm": 106,
        "hips_cm": 124,
        "inseam_cm": 82,
        "armLength_cm": 65,
    },
    {
        "id": "avatar_005",
        "label": "Teen",
        "height_cm": 152,
        "shoulderWidth_cm": 34,
        "chest_cm": 78,
        "waist_cm": 62,
        "hips_cm": 82,
        "inseam_cm": 68,
        "armLength_cm": 53,
    },
]

ASSETS = [
    {
        "name": "Oak Dining Chair",
        "category": "Seating",
        "material": "Solid Oak",
        "colour": "Natural Brown",
        "dimensions": {"height_cm": 92, "width_cm": 45, "depth_cm": 48},
        "description": "Classic solid oak dining chair with upholstered seat cushion.",
        "sku": "SEA-OAK-001",
        "price_aud": 299,
    },
    {
        "name": "Marble Coffee Table",
        "category": "Tables",
        "material": "Carrara Marble",
        "colour": "White with Grey Veining",
        "dimensions": {"height_cm": 42, "width_cm": 120, "depth_cm": 60},
        "description": "Italian Carrara marble top with brushed brass frame.",
        "sku": "TAB-MAR-001",
        "price_aud": 1499,
    },
    {
        "name": "Walnut Bookshelf",
        "category": "Storage",
        "material": "American Walnut",
        "colour": "Dark Walnut",
        "dimensions": {"height_cm": 180, "width_cm": 90, "depth_cm": 35},
        "description": "Five-shelf open bookcase in solid American walnut.",
        "sku": "STO-WAL-001",
        "price_aud": 849,
    },
    {
        "name": "Rattan Pendant Light",
        "category": "Lighting",
        "material": "Natural Rattan",
        "colour": "Natural Beige",
        "dimensions": {"height_cm": 35, "width_cm": 45, "depth_cm": 45},
        "description": "Handwoven rattan pendant with warm LED bulb included.",
        "sku": "LIT-RAT-001",
        "price_aud": 199,
    },
    {
        "name": "Linen Lounge Sofa",
        "category": "Seating",
        "material": "Belgian Linen",
        "colour": "Oat",
        "dimensions": {"height_cm": 82, "width_cm": 220, "depth_cm": 95},
        "description": "Three-seater sofa upholstered in washed Belgian linen.",
        "sku": "SEA-LIN-002",
        "price_aud": 2799,
    },
    {
        "name": "Concrete Side Table",
        "category": "Tables",
        "material": "Polished Concrete",
        "colour": "Charcoal Grey",
        "dimensions": {"height_cm": 55, "width_cm": 40, "depth_cm": 40},
        "description": "Minimalist polished concrete side table with steel base.",
        "sku": "TAB-CON-002",
        "price_aud": 389,
    },
    {
        "name": "Velvet Armchair",
        "category": "Seating",
        "material": "Velvet",
        "colour": "Sage Green",
        "dimensions": {"height_cm": 85, "width_cm": 78, "depth_cm": 82},
        "description": "Deep-seat armchair in sage velvet with solid timber legs.",
        "sku": "SEA-VEL-003",
        "price_aud": 699,
    },
    {
        "name": "Terrazzo Planter",
        "category": "Decor",
        "material": "Terrazzo",
        "colour": "White with Pink Chips",
        "dimensions": {"height_cm": 30, "width_cm": 28, "depth_cm": 28},
        "description": "Indoor planter in hand-cast terrazzo. Drainage hole included.",
        "sku": "DEC-TER-001",
        "price_aud": 89,
    },
    {
        "name": "Herringbone Oak Flooring",
        "category": "Flooring",
        "material": "Engineered Oak",
        "colour": "Blonde",
        "dimensions": {"height_cm": 1.4, "width_cm": 9, "depth_cm": 45},
        "description": "Engineered oak plank in herringbone pattern, 14mm thick.",
        "sku": "FLO-OAK-001",
        "price_aud": 95,
    },
    {
        "name": "Brass Floor Lamp",
        "category": "Lighting",
        "material": "Brushed Brass",
        "colour": "Antique Brass",
        "dimensions": {"height_cm": 155, "width_cm": 30, "depth_cm": 30},
        "description": "Adjustable arc floor lamp in brushed brass with fabric shade.",
        "sku": "LIT-BRS-002",
        "price_aud": 449,
    },
]


def generate_catalogue(assets=ASSETS, avatars=AVATARS):
    asset_list = []
    for i, asset in enumerate(assets):
        asset_list.append({"id": f"asset_{i + 1:03d}", **asset})
    return {
        "version": "1.0",
        "asset_count": len(asset_list),
        "avatar_count": len(avatars),
        "assets": asset_list,
        "avatars": avatars,
    }


if __name__ == "__main__":
    catalogue = generate_catalogue()

    with open("assets.json", "w") as f:
        json.dump(catalogue, f, indent=2)
    print(f"Generated {catalogue['asset_count']} assets + {catalogue['avatar_count']} avatars → assets.json")

    with open("avatars.json", "w") as f:
        json.dump({"version": "1.0", "avatars": AVATARS}, f, indent=2)
    print(f"Generated {len(AVATARS)} avatars → avatars.json")
