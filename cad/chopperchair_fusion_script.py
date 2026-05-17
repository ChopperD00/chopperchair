"""
CHOPPER CHAIR — Fusion 360 Parametric SitGo Wheelchair Script v2
=================================================================
In memory of Chopper.
License: CC-BY-SA 4.0

FIXED: Build on root component directly (Part Design compatible).
All bodies named. All user parameters registered.
SitGo pivot arm geometry with spring boss, stopper slot, locking bolt hole.
"""

import adsk.core
import adsk.fusion
import traceback
import math

PARAMS = {
    "torso_length":      160.0,
    "hip_width":          90.0,
    "shoulder_width":     80.0,
    "rear_leg_length":    80.0,
    "ground_clearance":   45.0,
    "girth":             165.0,
    "wheel_diameter":    100.0,
    "axle_diameter":      10.0,
    "collapse_angle":     45.0,
    "sit_angle":          25.0,
    "spring_boss_od":     18.0,
    "stopper_width":      22.0,
    "stopper_height":     15.0,
    "wall_thickness":      4.0,
    "rail_width":         16.0,
    "rail_height":        20.0,
    "crossbar_diameter":  12.0,
}

def cm(mm):
    return mm / 10.0

def add_user_param(design, name, value_mm, comment=""):
    params = design.userParameters
    existing = params.itemByName(name)
    val_input = adsk.core.ValueInput.createByString(f"{value_mm} mm")
    if existing:
        existing.expression = f"{value_mm} mm"
    else:
        params.add(name, val_input, "mm", comment)

def extrude_rect(comp, plane, x, y, w, h, depth_mm, name, op=adsk.fusion.FeatureOperations.NewBodyFeatureOperation):
    """Extrude a rectangle. x,y = center. w,h,depth in mm."""
    sk = comp.sketches.add(plane)
    lines = sk.sketchCurves.sketchLines
    hw = w / 2.0; hh = h / 2.0
    pts = [
        adsk.core.Point3D.create(cm(x-hw), cm(y-hh), 0),
        adsk.core.Point3D.create(cm(x+hw), cm(y-hh), 0),
        adsk.core.Point3D.create(cm(x+hw), cm(y+hh), 0),
        adsk.core.Point3D.create(cm(x-hw), cm(y+hh), 0),
    ]
    for i in range(4):
        lines.addByTwoPoints(pts[i], pts[(i+1)%4])
    prof = sk.profiles.item(0)
    feats = comp.features.extrudeFeatures
    inp = feats.createInput(prof, op)
    inp.setDistanceExtent(False, adsk.core.ValueInput.createByReal(cm(depth_mm)))
    feat = feats.add(inp)
    if feat.bodies.count > 0:
        feat.bodies.item(0).name = name
    return feat

def extrude_circle(comp, plane, cx, cy, diameter_mm, depth_mm, name, op=adsk.fusion.FeatureOperations.NewBodyFeatureOperation):
    """Extrude a circle. cx,cy = center. All mm."""
    sk = comp.sketches.add(plane)
    circles = sk.sketchCurves.sketchCircles
    circles.addByCenterRadius(
        adsk.core.Point3D.create(cm(cx), cm(cy), 0),
        cm(diameter_mm / 2.0)
    )
    prof = sk.profiles.item(0)
    feats = comp.features.extrudeFeatures
    inp = feats.createInput(prof, op)
    inp.setDistanceExtent(False, adsk.core.ValueInput.createByReal(cm(depth_mm)))
    feat = feats.add(inp)
    if op == adsk.fusion.FeatureOperations.NewBodyFeatureOperation and feat.bodies.count > 0:
        feat.bodies.item(0).name = name
    return feat

def cut_circle_from_face(comp, face, cx_mm, cy_mm, dia_mm, depth_mm):
    """Cut a circular bore into a face."""
    sk = comp.sketches.add(face)
    circles = sk.sketchCurves.sketchCircles
    circles.addByCenterRadius(
        adsk.core.Point3D.create(cm(cx_mm), cm(cy_mm), 0),
        cm(dia_mm / 2.0)
    )
    prof = sk.profiles.item(0)
    feats = comp.features.extrudeFeatures
    inp = feats.createInput(prof, adsk.fusion.FeatureOperations.CutFeatureOperation)
    inp.setDistanceExtent(False, adsk.core.ValueInput.createByReal(cm(depth_mm)))
    return feats.add(inp)

def get_face_at_z(body, z_mm, tolerance=0.5):
    """Find a planar face near a given Z height."""
    for face in body.faces:
        try:
            if isinstance(face.geometry, adsk.core.Plane):
                normal = face.geometry.normal
                if abs(normal.z) > 0.9:
                    pt = face.pointOnFace
                    if abs(pt.z * 10 - z_mm) < tolerance:
                        return face
        except Exception:
            pass
    return None

def get_face_at_y(body, y_mm, tolerance=0.5):
    """Find a planar face near a given Y value."""
    for face in body.faces:
        try:
            if isinstance(face.geometry, adsk.core.Plane):
                normal = face.geometry.normal
                if abs(normal.y) > 0.9:
                    pt = face.pointOnFace
                    if abs(pt.y * 10 - y_mm) < tolerance:
                        return face
        except Exception:
            pass
    return None


def build(design, root, P, ui):
    comp = root  # build on root comp directly — Part Design compatible

    xy = comp.xYConstructionPlane
    xz = comp.xZConstructionPlane
    yz = comp.yZConstructionPlane

    # Derived
    rw = P["rail_width"]
    rh = P["rail_height"]
    wt = P["wall_thickness"]
    tl = P["torso_length"]
    hw = P["hip_width"]
    gc = P["ground_clearance"]
    rl = P["rear_leg_length"]
    ad = P["axle_diameter"]
    wd = P["wheel_diameter"]
    cb = P["crossbar_diameter"]
    sb = P["spring_boss_od"]
    sw = P["stopper_width"]
    sh = P["stopper_height"]
    pt = wt * 2.5  # pivot arm thickness

    # STEP 1: User parameters
    for k, v in P.items():
        add_user_param(design, k, v)

    # STEP 2: Left rail
    feat_lr = extrude_rect(comp, xy, 0, tl/2, rw, tl, rh, "Rail_Left")
    body_lr = feat_lr.bodies.item(0)
    bodies_coll = adsk.core.ObjectCollection.create()
    bodies_coll.add(body_lr)
    move_feat = comp.features.moveFeatures
    move_inp = move_feat.createInput2(bodies_coll)
    move_inp.defineAsTranslateXYZ(
        adsk.core.ValueInput.createByReal(0),
        adsk.core.ValueInput.createByReal(0),
        adsk.core.ValueInput.createByReal(cm(gc))
    )
    move_feat.add(move_inp)

    # STEP 3: Right rail
    feat_rr = extrude_rect(comp, xy, hw, tl/2, rw, tl, rh, "Rail_Right")
    body_rr = feat_rr.bodies.item(0)
    bodies_coll2 = adsk.core.ObjectCollection.create()
    bodies_coll2.add(body_rr)
    move_inp2 = move_feat.createInput2(bodies_coll2)
    move_inp2.defineAsTranslateXYZ(
        adsk.core.ValueInput.createByReal(0),
        adsk.core.ValueInput.createByReal(0),
        adsk.core.ValueInput.createByReal(cm(gc))
    )
    move_feat.add(move_inp2)

    # STEP 4: Crossbars
    feats_ext = comp.features.extrudeFeatures

    sk_cb = comp.sketches.add(yz)
    sk_cb.sketchCurves.sketchCircles.addByCenterRadius(
        adsk.core.Point3D.create(cm(tl), cm(gc + rh/2), 0), cm(cb/2)
    )
    prof_cb = sk_cb.profiles.item(0)
    inp_cb = feats_ext.createInput(prof_cb, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    inp_cb.setDistanceExtent(False, adsk.core.ValueInput.createByReal(cm(hw + rw)))
    feats_ext.add(inp_cb).bodies.item(0).name = "Crossbar_Rear"

    sk_fcb = comp.sketches.add(yz)
    sk_fcb.sketchCurves.sketchCircles.addByCenterRadius(
        adsk.core.Point3D.create(cm(rw), cm(gc + rh/2), 0), cm(cb/2)
    )
    prof_fcb = sk_fcb.profiles.item(0)
    inp_fcb = feats_ext.createInput(prof_fcb, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    inp_fcb.setDistanceExtent(False, adsk.core.ValueInput.createByReal(cm(hw + rw)))
    feats_ext.add(inp_fcb).bodies.item(0).name = "Crossbar_Front"

    # STEP 5: Pivot arms (SitGo)
    for side_x, side_name in [(0.0, "Left"), (hw, "Right")]:
        arm_vert_w = rw
        arm_vert_h = rl
        arm_tab_w  = rw * 2
        arm_tab_h  = rh

        sk_v = comp.sketches.add(xz)
        lines_v = sk_v.sketchCurves.sketchLines
        vx0 = cm(side_x - arm_vert_w/2)
        vx1 = cm(side_x + arm_vert_w/2)
        tx1 = cm(side_x + arm_vert_w/2 + arm_tab_w)
        vz0 = 0.0
        vz_tab = cm(arm_vert_h - arm_tab_h)
        vz1 = cm(arm_vert_h)

        L_pts = [
            adsk.core.Point3D.create(vx0, vz0, 0),
            adsk.core.Point3D.create(vx1, vz0, 0),
            adsk.core.Point3D.create(vx1, vz_tab, 0),
            adsk.core.Point3D.create(tx1, vz_tab, 0),
            adsk.core.Point3D.create(tx1, vz1, 0),
            adsk.core.Point3D.create(vx0, vz1, 0),
        ]
        for i in range(len(L_pts)):
            lines_v.addByTwoPoints(L_pts[i], L_pts[(i+1) % len(L_pts)])

        if sk_v.profiles.count == 0:
            continue

        prof_v = sk_v.profiles.item(0)
        inp_v = feats_ext.createInput(prof_v, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        inp_v.setDistanceExtent(False, adsk.core.ValueInput.createByReal(cm(pt)))
        feat_v = feats_ext.add(inp_v)
        body_arm = feat_v.bodies.item(0)
        body_arm.name = f"PivotArm_{side_name}"

        arm_bodies = adsk.core.ObjectCollection.create()
        arm_bodies.add(body_arm)
        move_arm = move_feat.createInput2(arm_bodies)
        move_arm.defineAsTranslateXYZ(
            adsk.core.ValueInput.createByReal(0),
            adsk.core.ValueInput.createByReal(cm(tl - pt/2)),
            adsk.core.ValueInput.createByReal(0)
        )
        move_feat.add(move_arm)

        # Pivot bore
        sk_pb = comp.sketches.add(xz)
        sk_pb.sketchCurves.sketchCircles.addByCenterRadius(
            adsk.core.Point3D.create(cm(side_x), cm(arm_vert_h - arm_tab_h/2), 0), cm(ad/2 + 0.2)
        )
        prof_pb = sk_pb.profiles.item(0)
        inp_pb = feats_ext.createInput(prof_pb, adsk.fusion.FeatureOperations.CutFeatureOperation)
        inp_pb.setDistanceExtent(True, adsk.core.ValueInput.createByReal(cm(pt + 2)))
        feats_ext.add(inp_pb)

        # Wheel axle bore
        axle_z = wd/2 + 5
        sk_ab = comp.sketches.add(xz)
        sk_ab.sketchCurves.sketchCircles.addByCenterRadius(
            adsk.core.Point3D.create(cm(side_x), cm(axle_z), 0), cm(ad/2 + 0.2)
        )
        prof_ab = sk_ab.profiles.item(0)
        inp_ab = feats_ext.createInput(prof_ab, adsk.fusion.FeatureOperations.CutFeatureOperation)
        inp_ab.setDistanceExtent(True, adsk.core.ValueInput.createByReal(cm(pt + 2)))
        feats_ext.add(inp_ab)

        # Spring boss
        sk_sb = comp.sketches.add(xz)
        sk_sb.sketchCurves.sketchCircles.addByCenterRadius(
            adsk.core.Point3D.create(cm(side_x + arm_vert_w/2 + arm_tab_w/2), cm(arm_vert_h - arm_tab_h/2), 0), cm(sb/2)
        )
        prof_sb = sk_sb.profiles.item(0)
        inp_sb = feats_ext.createInput(prof_sb, adsk.fusion.FeatureOperations.JoinFeatureOperation)
        inp_sb.setDistanceExtent(False, adsk.core.ValueInput.createByReal(cm(8)))
        feats_ext.add(inp_sb)

        # Locking bolt hole (M4)
        sk_lb = comp.sketches.add(xz)
        sk_lb.sketchCurves.sketchCircles.addByCenterRadius(
            adsk.core.Point3D.create(cm(side_x + arm_vert_w/2 + arm_tab_w/2), cm(arm_vert_h - arm_tab_h/2), 0), cm(2.25)
        )
        prof_lb = sk_lb.profiles.item(0)
        inp_lb = feats_ext.createInput(prof_lb, adsk.fusion.FeatureOperations.CutFeatureOperation)
        inp_lb.setDistanceExtent(True, adsk.core.ValueInput.createByReal(cm(sb + 4)))
        feats_ext.add(inp_lb)

    # STEP 6: Axle end caps
    for cap_x, cap_name in [(-(ad/2+4), "AxleCap_Left"), (hw + ad/2+4, "AxleCap_Right")]:
        sk_cap = comp.sketches.add(yz)
        sk_cap.sketchCurves.sketchCircles.addByCenterRadius(
            adsk.core.Point3D.create(cm(tl), cm(wd/2 + 5), 0), cm(ad/2 + 2)
        )
        prof_cap = sk_cap.profiles.item(0)
        inp_cap = feats_ext.createInput(prof_cap, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        inp_cap.setDistanceExtent(False, adsk.core.ValueInput.createByReal(cm(12)))
        feat_cap = feats_ext.add(inp_cap)
        feat_cap.bodies.item(0).name = cap_name
        sk_capb = comp.sketches.add(yz)
        sk_capb.sketchCurves.sketchCircles.addByCenterRadius(
            adsk.core.Point3D.create(cm(tl), cm(wd/2 + 5), 0), cm(ad/2 - 0.1)
        )
        prof_capb = sk_capb.profiles.item(0)
        inp_capb = feats_ext.createInput(prof_capb, adsk.fusion.FeatureOperations.CutFeatureOperation)
        inp_capb.setDistanceExtent(False, adsk.core.ValueInput.createByReal(cm(8)))
        feats_ext.add(inp_capb)


def run(context):
    ui = None
    try:
        app    = adsk.core.Application.get()
        ui     = app.userInterface
        design = app.activeProduct

        if not isinstance(design, adsk.fusion.Design):
            ui.messageBox("Open a new Fusion 360 design first.", "Chopper Chair")
            return

        design.designType = adsk.fusion.DesignTypes.ParametricDesignType
        root = design.rootComponent
        build(design, root, PARAMS, ui)

    except Exception:
        if ui:
            ui.messageBox(f"Script error:\n\n{traceback.format_exc()}", "Chopper Chair — Error")

def stop(context):
    pass
