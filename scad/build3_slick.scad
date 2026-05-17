// ChopperChair — Build 3: Slick
// Topology-optimized aesthetic redesign. Drop-in hardware upgrade from Build 2.
// Inspired by Ascento / Diablo open-leg platforms.
// License: CC-BY-SA 4.0

include <chopperchair_params.scad>;

// ── Utilities ─────────────────────────────────────────────────────────────
module rounded_rect(w, h, d, r=3) {
    hull() {
        translate([ r, r, 0]) cylinder(r=r, h=d);
        translate([w-r, r, 0]) cylinder(r=r, h=d);
        translate([ r, h-r, 0]) cylinder(r=r, h=d);
        translate([w-r, h-r, 0]) cylinder(r=r, h=d);
    }
}

// ── Strut cutout pattern (FEA-inspired topology reduction) ────────────────
// Elongated diamond voids arranged along the load path of the arm.
module strut_void(l, w) {
    // Diamond cutout — strong along long axis, material removed laterally
    hull() {
        translate([0,  l/2, 0]) cylinder(r=w*0.25, h=100, center=true);
        translate([0, -l/2, 0]) cylinder(r=w*0.25, h=100, center=true);
        translate([ w*0.4, 0, 0]) cylinder(r=0.5, h=100, center=true);
        translate([-w*0.4, 0, 0]) cylinder(r=0.5, h=100, center=true);
    }
}

// ── Slick Rail (panel-gap channels, exposed structure aesthetic) ───────────
module slick_rail() {
    t = pivot_arm_t;
    difference() {
        // Outer profile — taller and thinner than Build 2
        rounded_rect(rail_w * 0.85, torso_length, rail_h * 1.1, r=4);

        // Panel-gap channel — 1mm groove running full length on outer face
        translate([-0.01, wall_thickness, rail_h * 0.3])
            cube([1.2, torso_length - wall_thickness*2, rail_h * 0.12]);
        translate([-0.01, wall_thickness, rail_h * 0.7])
            cube([1.2, torso_length - wall_thickness*2, rail_h * 0.06]);

        // Lightening pocket
        translate([wall_thickness, wall_thickness*2, wall_thickness])
            cube([rail_w*0.85 - wall_thickness*2,
                  torso_length - wall_thickness*4,
                  rail_h*1.1 - wall_thickness*2 + 0.01]);

        // Crossbar sockets
        translate([rail_w*0.425, wall_thickness, rail_h*0.55])
            rotate([90,0,0]) cylinder(d=crossbar_od + clear_slide*2, h=wall_thickness+1, center=true);
        translate([rail_w*0.425, torso_length - wall_thickness, rail_h*0.55])
            rotate([90,0,0]) cylinder(d=crossbar_od + clear_slide*2, h=wall_thickness+1, center=true);
    }
}

// ── Slick Pivot Arm (strut-frame topology) ────────────────────────────────
module slick_pivot_arm() {
    arm_w   = rail_w * 0.9;
    tab_w   = rail_w * 1.8;
    tab_h   = rail_h;
    axle_z  = wheel_diameter/2 + 5;
    t       = pivot_arm_t * 1.1; // slightly thicker for rigidity

    difference() {
        union() {
            // Vertical section
            rounded_rect(arm_w, rear_leg_length, t, r=4);
            // Tab
            translate([arm_w, rear_leg_length - tab_h, 0])
                rounded_rect(tab_w, tab_h, t, r=4);
            // Spring boss
            translate([arm_w + tab_w/2, rear_leg_length - tab_h/2, t])
                cylinder(d=spring_boss_od, h=10);
            // Exposed spring coil boss ring (aesthetic detail)
            translate([arm_w + tab_w/2, rear_leg_length - tab_h/2, t + 10])
                difference() {
                    cylinder(d=spring_boss_od + 3, h=2);
                    cylinder(d=spring_boss_od - 1, h=3);
                }
        }

        // FEA-inspired strut voids — 3 along vertical section
        for (i=[0.25, 0.5, 0.68]) {
            translate([arm_w/2, rear_leg_length * i, t/2])
                strut_void(rear_leg_length * 0.15, arm_w * 0.55);
        }

        // Pivot bore
        translate([arm_w/2, rear_leg_length - tab_h/2, -1])
            cylinder(d=axle_diameter + clear_close*2, h=t+2);
        // Wheel axle bore
        translate([arm_w/2, axle_z, -1])
            cylinder(d=axle_diameter + clear_close*2, h=t+2);
        // Spring boss bolt
        translate([arm_w + tab_w/2, rear_leg_length - tab_h/2, -1])
            cylinder(d=4.5, h=spring_boss_od + 16);
    }
}

// ── Slick Stopper (chamfered, tighter geometry) ───────────────────────────
module slick_stopper() {
    difference() {
        hull() {
            cube([stopper_w, stopper_h * 0.8, pivot_arm_t]);
            translate([stopper_w*0.1, stopper_h*0.8, 0])
                cube([stopper_w*0.8, stopper_h*0.2, pivot_arm_t]);
        }
        translate([stopper_w*0.25, stopper_h/2, -1]) cylinder(d=4.5, h=pivot_arm_t+2);
        translate([stopper_w*0.75, stopper_h/2, -1]) cylinder(d=4.5, h=pivot_arm_t+2);
    }
}

// ── Part selector ─────────────────────────────────────────────────────────
part = "rail_left";
// rail_left | rail_right | crossbar_front | crossbar_rear
// pivot_arm_left | pivot_arm_right | spring_boss_left | spring_boss_right
// axle_cap_left | axle_cap_right | stopper_left | stopper_right | belly_sling_mount

module axle_cap() {
    difference() {
        cylinder(d=axle_diameter + 8, h=14);
        translate([0,0,-0.01]) cylinder(d=axle_diameter - clear_close*2, h=10);
        translate([axle_diameter/2 + 2, 0, 7]) rotate([0,90,0]) cylinder(d=3.3, h=8);
    }
}

module spring_boss() {
    difference() {
        cylinder(d=spring_boss_od - clear_close*2, h=12);
        translate([0,0,4]) cylinder(d=spring_boss_od*0.5, h=9);
        translate([0,0,-0.01]) cylinder(d=4.5, h=13);
    }
}

module belly_sling_mount() {
    slot_w = 12; slot_h = 4;
    difference() {
        rounded_rect(hip_width * 0.4, 30, 8, r=3);
        translate([8, 10, wall_thickness]) cube([slot_w, slot_h, 8 - wall_thickness + 1]);
        translate([hip_width*0.4 - 8 - slot_w, 10, wall_thickness]) cube([slot_w, slot_h, 8 - wall_thickness + 1]);
        translate([hip_width*0.4/2, 25, -1]) cylinder(d=4.5, h=10);
    }
}

if (part == "rail_left")          slick_rail();
if (part == "rail_right")         mirror([1,0,0]) slick_rail();
if (part == "crossbar_front")     cylinder(d=crossbar_od, h=hip_width + rail_w*2);
if (part == "crossbar_rear")      cylinder(d=crossbar_od, h=hip_width + rail_w*2);
if (part == "pivot_arm_left")     slick_pivot_arm();
if (part == "pivot_arm_right")    mirror([1,0,0]) slick_pivot_arm();
if (part == "spring_boss_left")   spring_boss();
if (part == "spring_boss_right")  spring_boss();
if (part == "axle_cap_left")      axle_cap();
if (part == "axle_cap_right")     axle_cap();
if (part == "stopper_left")       slick_stopper();
if (part == "stopper_right")      slick_stopper();
if (part == "belly_sling_mount")  belly_sling_mount();
