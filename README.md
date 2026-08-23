# 📐 Blender DimExport — Export Object Dimensions

> A lightweight Blender add-on that exports the **width, height, depth and volume** of your selected mesh objects to **TXT, CSV or JSON** — right from the 3D View sidebar.

![Blender](https://img.shields.io/badge/Blender-2.80%2B-orange?logo=blender&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-GPL--3.0-green)
![Version](https://img.shields.io/badge/version-2.0-brightgreen)

Need a quick spec sheet of your models for a client, a cut list for fabrication, or dimension data to feed into another tool? **DimExport** does it in two clicks — no need to write down numbers by hand.

---

## ✨ Features

| | Feature |
|---|---|
| 📦 | Export **Width (X)**, **Height (Z)**, **Depth (Y)** of every selected mesh |
| 🧮 | Optional **bounding-box volume** (W × H × D) |
| 📄 | Three output formats: **TXT**, **CSV** (Excel/Sheets) and **JSON** (pipelines/scripts) |
| 📏 | Unit conversion: **meters, centimeters, millimeters** — with optional unit suffix |
| ✏️ | **Custom labels** (e.g. use "Length" instead of "Width") |
| 🎯 | Pick exactly **which dimensions** to include |
| 🗂️ | Choose the **output folder and file name** (extension set automatically) |
| 🚫 | Friendly warning when no mesh objects are selected |
| 🛟 | Safe file writing with clear error messages |

## 📥 Installation

1. Download **[`export_object_dimensions.py`](export_object_dimensions.py)** (or grab the latest [release](../../releases)).
2. In Blender: `Edit ▸ Preferences ▸ Add-ons ▸ Install…`
3. Select the `.py` file and tick the checkbox to **enable** it.
4. In the 3D View, press **`N`** to open the sidebar and go to the **Dimensions** tab.

## 🚀 Usage

1. Select one or more **mesh** objects.
2. Open the **Dimensions** panel in the sidebar.
3. Choose your **format**, **units**, which dimensions to include, and (optionally) custom labels.
4. Click **Export Dimensions**. Done ✅

## 📤 Output examples

**TXT**
```
Dimensions of Selected Objects:

Cube:
  Width (X): 2.0 m
  Height (Z): 1.0 m
  Depth (Y): 1.5 m
```

**CSV** (opens directly in Excel / Google Sheets)
```csv
name,Width,Height,Depth,Volume
Cube,2.0 m,1.0 m,1.5 m,3.0 m
```

**JSON** (ready for scripts, web viewers, BIM/CAD pipelines)
```json
{
  "unit": "m",
  "objects": [
    { "name": "Cube", "Width": 2.0, "Height": 1.0, "Depth": 1.5, "Volume": 3.0 }
  ]
}
```

## 💡 Use cases

- **Product / furniture design** — generate a spec sheet for clients.
- **3D printing & CNC** — export a cut/size list per part.
- **Architecture / archviz** — quick dimension reports of assets.
- **Automation** — feed JSON into your own scripts or a web catalog.

## 🗺️ Roadmap

- [ ] Export **surface area** and real (mesh) volume
- [ ] Per-object **origin / world position** columns
- [ ] Copy result to clipboard
- [ ] Batch export one file per object

Have an idea? [Open an issue](../../issues) — contributions are welcome!

## 🤝 Contributing

Pull requests are welcome. For bigger changes, open an issue first to discuss what you'd like to change. See [CONTRIBUTING.md](CONTRIBUTING.md).

## 📜 License

Released under the [GNU General Public License v3.0 or later](LICENSE). Blender add-ons that use the Blender Python API are required to be GPL-compatible.

---

Made with 💻 by **Rafael Oliveira** · [raoliz.com](https://raoliz.com)

If this add-on saved you some time, consider leaving a ⭐ — it helps others find it!
