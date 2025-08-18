import os

import FreeCAD
import Import


def export_model():
    """
    Export STEP file from FreeCAD.

    Configuration options (environment variables):
     - CI_COMPONENTS_FREECAD_PROJECT_PATH - path to project FCStd file.
     - CI_COMPONENTS_FREECAD_OUTPUT_PATH - path for the result STEP file.
     - CI_COMPONENTS_FREECAD_BODY_ID - unique identifier of the exporting object.
    """
    project_path = os.environ.get("CI_COMPONENTS_FREECAD_PROJECT_PATH")
    output_path = os.environ.get("CI_COMPONENTS_FREECAD_OUTPUT_PATH")
    body_id = os.environ.get("CI_COMPONENTS_FREECAD_BODY_ID")

    doc = FreeCAD.openDocument(project_path)
    FreeCAD.setActiveDocument(doc.Name)

    objs = doc.getObjectsByLabel(body_id)
    if objs is None:
        FreeCAD.closeDocument(doc.Name)
        raise ValueError(f'Body {body_id} not found in {project_path}')

    if len(objs) != 1:
        FreeCAD.closeDocument(doc.Name)
        raise ValueError(f'There are multiples objects with `{body_id}` label')

    body = objs[0]

    try:
        Import.export([body], output_path)
        print(f'Exported {body_id} to: {output_path}')
    except Exception as e:
        raise RuntimeError(f'STEP export failed: {e}')
    finally:
        FreeCAD.closeDocument(doc.Name)


export_model()
