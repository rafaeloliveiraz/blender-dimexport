# Export Object Dimensions – Blender Addon

**Compatible with:** Blender 2.80+

## 📦 What It Does

This Blender addon exports the **dimensions** (Width, Height, Depth) of selected mesh objects to a `.txt` file.

## 🧩 Features

- ✅ Select which dimensions to include
- ✏️ Customize dimension labels (e.g., "Length" instead of "Width")
- 📁 Choose export folder and file name
- 📏 Convert to meters, centimeters, or millimeters
- 🚫 Warns if no mesh objects are selected

## 📁 Output Example

```
MyCube:
  Width (X): 200.00
  Height (Z): 100.00
  Depth (Y): 150.00
```

*Units depend on the scale option you choose (m, cm, mm).*

## 🚀 Installation

1. Download the file: `export_object_dimensions.py`
2. In Blender:
   - Go to `Edit > Preferences > Add-ons`
   - Click **Install...**, select the `.py` file, then **Enable**
3. Open the Sidebar (press `N`) in the 3D View
4. Go to the **Dimensions** tab
5. Select mesh objects and click **Export Dimensions**

---

Made with 💻 by Rafael Oliveira  
[raoliz.com](https://raoliz.com)
