bl_info = {
    "name": "Export Object Dimensions",
    "author": "Rafael Oliveira (raoliz.com)",
    "version": (2, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Dimensions",
    "description": "Export width, height, depth and volume of selected objects to TXT, CSV or JSON with customizable options",
    "category": "Object",
    "doc_url": "https://github.com/rafaeloliveiraz/blender-dimexport",
    "tracker_url": "https://github.com/rafaeloliveiraz/blender-dimexport/issues",
}

import bpy
import os
import json

# Unit scale factor -> suffix used in output
UNIT_SUFFIX = {"1": "m", "100": "cm", "1000": "mm"}


class DimensionsAddonProperties(bpy.types.PropertyGroup):
    export_path: bpy.props.StringProperty(
        name="Export Path",
        description="Choose the folder to save the file",
        default="//",
        subtype='DIR_PATH'
    )
    file_name: bpy.props.StringProperty(
        name="File Name",
        description="Name of the exported file (extension is set automatically from the format)",
        default="object_dimensions"
    )

    export_format: bpy.props.EnumProperty(
        name="Format",
        description="Choose the output file format",
        items=[
            ('TXT', "Text (.txt)", "Human-readable text file"),
            ('CSV', "CSV (.csv)", "Comma-separated values, opens in Excel/Sheets"),
            ('JSON', "JSON (.json)", "Structured data for scripts and pipelines"),
        ],
        default='TXT'
    )

    include_width: bpy.props.BoolProperty(name="Width (X)", default=True)
    include_height: bpy.props.BoolProperty(name="Height (Z)", default=True)
    include_depth: bpy.props.BoolProperty(name="Depth (Y)", default=True)
    include_volume: bpy.props.BoolProperty(
        name="Bounding-box Volume",
        description="Include the bounding-box volume (W x H x D)",
        default=False
    )
    include_units: bpy.props.BoolProperty(
        name="Append unit suffix",
        description="Append the unit (m/cm/mm) to each value in TXT/CSV",
        default=True
    )

    label_width: bpy.props.StringProperty(name="Label for Width", default="Width")
    label_height: bpy.props.StringProperty(name="Label for Height", default="Height")
    label_depth: bpy.props.StringProperty(name="Label for Depth", default="Depth")

    unit_scale: bpy.props.EnumProperty(
        name="Units",
        description="Choose unit conversion for exported values",
        items=[
            ('1', "Meters", ""),
            ('100', "Centimeters", ""),
            ('1000', "Millimeters", ""),
        ],
        default='1'
    )


def _collect_rows(props, objects, scale):
    """Build a list of dicts, one per object, honoring the include_* toggles."""
    rows = []
    for obj in objects:
        dims = obj.dimensions
        row = {"name": obj.name}
        if props.include_width:
            row[props.label_width] = round(dims.x * scale, 4)
        if props.include_height:
            row[props.label_height] = round(dims.z * scale, 4)
        if props.include_depth:
            row[props.label_depth] = round(dims.y * scale, 4)
        if props.include_volume:
            row["Volume"] = round((dims.x * dims.y * dims.z) * (scale ** 3), 4)
        rows.append(row)
    return rows


def _fmt(value, suffix, append_units):
    return f"{value} {suffix}" if append_units else f"{value}"


def _to_txt(rows, suffix, append_units):
    out = "Dimensions of Selected Objects:\n\n"
    for row in rows:
        out += f"{row['name']}:\n"
        for key, value in row.items():
            if key == "name":
                continue
            axis = {"Width": " (X)", "Height": " (Z)", "Depth": " (Y)"}.get(key, "")
            out += f"  {key}{axis}: {_fmt(value, suffix, append_units)}\n"
        out += "\n"
    return out


def _to_csv(rows, suffix, append_units):
    if not rows:
        return ""
    # Union of keys preserves column order across objects
    headers = ["name"]
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [",".join(headers)]
    for row in rows:
        cells = []
        for key in headers:
            if key == "name":
                cells.append(str(row.get("name", "")))
            elif key in row:
                cells.append(_fmt(row[key], suffix, append_units))
            else:
                cells.append("")
        lines.append(",".join(cells))
    return "\n".join(lines) + "\n"


def _to_json(rows, unit_name):
    return json.dumps({"unit": unit_name, "objects": rows}, indent=2, ensure_ascii=False)


class OBJECT_OT_export_dimensions(bpy.types.Operator):
    bl_idname = "object.export_dimensions"
    bl_label = "Export Dimensions"
    bl_description = "Export dimensions of selected objects to a file"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.dimensions_props
        scale = float(props.unit_scale)
        suffix = UNIT_SUFFIX.get(props.unit_scale, "")

        selected = [obj for obj in context.selected_objects if obj.type == 'MESH']
        if not selected:
            self.report({'WARNING'}, "No mesh objects selected")
            return {'CANCELLED'}

        rows = _collect_rows(props, selected, scale)

        ext = props.export_format.lower()
        if props.export_format == 'CSV':
            content = _to_csv(rows, suffix, props.include_units)
        elif props.export_format == 'JSON':
            content = _to_json(rows, suffix)
        else:
            content = _to_txt(rows, suffix, props.include_units)

        # Ensure the file name carries the right extension for the chosen format
        base = os.path.splitext(props.file_name)[0] or "object_dimensions"
        file_name = f"{base}.{ext}"

        folder = bpy.path.abspath(props.export_path)
        try:
            os.makedirs(folder, exist_ok=True)
            full_path = os.path.join(folder, file_name)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
        except OSError as e:
            self.report({'ERROR'}, f"Could not write file: {e}")
            return {'CANCELLED'}

        self.report({'INFO'}, f"Exported {len(rows)} object(s) to {full_path}")
        return {'FINISHED'}


class OBJECT_PT_dimensions_panel(bpy.types.Panel):
    bl_label = "Export Dimensions"
    bl_idname = "OBJECT_PT_export_dimensions"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Dimensions'

    def draw(self, context):
        layout = self.layout
        props = context.scene.dimensions_props

        col = layout.column(align=True)
        col.prop(props, "export_path")
        col.prop(props, "file_name")
        col.prop(props, "export_format")
        col.prop(props, "unit_scale")

        box = layout.box()
        box.label(text="Dimensions to export:")
        box.prop(props, "include_width")
        box.prop(props, "include_height")
        box.prop(props, "include_depth")
        box.prop(props, "include_volume")
        box.prop(props, "include_units")

        box = layout.box()
        box.label(text="Custom labels:")
        box.prop(props, "label_width")
        box.prop(props, "label_height")
        box.prop(props, "label_depth")

        layout.operator("object.export_dimensions", icon='EXPORT')


classes = (
    DimensionsAddonProperties,
    OBJECT_OT_export_dimensions,
    OBJECT_PT_dimensions_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.dimensions_props = bpy.props.PointerProperty(type=DimensionsAddonProperties)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.dimensions_props


if __name__ == "__main__":
    register()
