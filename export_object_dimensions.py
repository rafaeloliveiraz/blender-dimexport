bl_info = {
    "name": "Export Object Dimensions",
    "author": "Rafael Oliveira (raoliz.com)",
    "version": (1, 2),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Dimensions",
    "description": "Export width, height and depth of selected objects to a .txt file with customizable options",
    "category": "Object",
}

import bpy
import os

class DimensionsAddonProperties(bpy.types.PropertyGroup):
    export_path: bpy.props.StringProperty(
        name="Export Path",
        description="Choose the folder to save the file",
        default="//",
        subtype='DIR_PATH'
    )
    file_name: bpy.props.StringProperty(
        name="File Name",
        description="Name of the exported text file",
        default="object_dimensions.txt"
    )
    include_width: bpy.props.BoolProperty(name="Width (X)", default=True)
    include_height: bpy.props.BoolProperty(name="Height (Z)", default=True)
    include_depth: bpy.props.BoolProperty(name="Depth (Y)", default=True)

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

class OBJECT_OT_export_dimensions(bpy.types.Operator):
    bl_idname = "object.export_dimensions"
    bl_label = "Export Dimensions"
    bl_description = "Export dimensions of selected objects to a .txt file"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.dimensions_props
        scale = float(props.unit_scale)

        selected = [obj for obj in context.selected_objects if obj.type == 'MESH']
        if not selected:
            self.report({'WARNING'}, "No mesh objects selected")
            return {'CANCELLED'}

        output = "Dimensions of Selected Objects:\n\n"
        for obj in selected:
            dims = obj.dimensions
            output += f"{obj.name}:\n"
            if props.include_width:
                output += f"  {props.label_width} (X): {dims.x * scale:.2f}\n"
            if props.include_height:
                output += f"  {props.label_height} (Z): {dims.z * scale:.2f}\n"
            if props.include_depth:
                output += f"  {props.label_depth} (Y): {dims.y * scale:.2f}\n"
            output += "\n"

        full_path = os.path.join(bpy.path.abspath(props.export_path), props.file_name)
        with open(full_path, "w", encoding="utf-8") as file:
            file.write(output)

        self.report({'INFO'}, f"Dimensions exported to {full_path}")
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

        layout.prop(props, "export_path")
        layout.prop(props, "file_name")
        layout.prop(props, "unit_scale")
        layout.label(text="Select dimensions to export:")
        layout.prop(props, "include_width")
        layout.prop(props, "include_height")
        layout.prop(props, "include_depth")

        layout.label(text="Custom labels:")
        layout.prop(props, "label_width")
        layout.prop(props, "label_height")
        layout.prop(props, "label_depth")

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
