// ChopperChair — Build 2: Hybrid
// 13 printed parts + ~$55 hardware (8mm steel axle, foam wheels, torsion springs, webbing)
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

module chamfer_block(w, h, d, ch=1.5) {
    hull() {
        translate([ch, 0, 0]) cube([w-ch*2, h, d]);
        translate([0, ch, 0]) cube([w, h-ch*2, d]);
    }
}

// ── Rail (left — mirror for right) ────────────────────────────────────────
module rail() {
    difference() {
        rounded_rect(rail_w, torso_length, rail_h, r=3);
        // Lightening channel
        translate([wall_thickness, wall_thickness*2, wall_thickness])
            cube([rail_w - wall_thickness*2,
                  torso_length - wall_thickness*4,
                  rail_h - wall_thickness*2 + 0.01]);
        // Front crossbar socket
        translate([rail_w/2, wall_thickness, rail_h/2])
            rotate([90,0,0]) cylinder(d=crossbar_od + clear_slide*2, h=wall_thickness+1, center=true);
        // Rear crossbar socket
        translate([rail_w/2, torso_length - wall_thickness, rail_h/2])
            rotate([90,0,0]) cylinder(d=crossbar_od + clear_slide*2, h=wall_thickness+1, center=true);
    }
}

// ── Crossbar ──────────────────────────────────────────────────────────────
module crossbar(length) {
    cylinder(d=crossbar_od, h=length);
}

// ── Pivot arm (SitGo mechanism) ───────────────────────────────────────────
module pivot_arm() {
    arm_vert_w = rail_w;
    arm_tab_w  = rail_w * 2;
    arm_tab_h  = rail_h;
    axle_z     = wheel_diameter/2 + 5;

    difference() {
        union() {
            // Vertical section
            rounded_rect(arm_vert_w, rear_leg_length, pivot_arm_t, r=3);
            // Horizontal tab (spring boss platform)
            translate([arm_vert_w, rear_leg_length - arm_tab_h, 0])
                rounded_rect(arm_tab_w, arm_tab_h, pivot_arm_t, r=3);
            // Spring boss cylinder
            translate([arm_vert_w + arm_tab_w/2, rear_leg_length - arm_tab_h/2, pivot_arm_t])
                cylinder(d=spring_boss_od, h=8);
        }
        // Pivot bore (top — connects to rail)
        translate([arm_vert_w/2, rear_leg_length - arm_tab_h/2, -1])
            cylinder(d=axle_diameter + clear_close*2, h=pivot_arm_t+2);
        // Wheel axle bore (bottom)
        translate([arm_vert_w/2, axle_z, -1])
            cylinder(d=axle_diameter + clear_close*2, h=pivot_arm_t+2);
        // Spring boss locking bolt (M4)
        translate([arm_vert_w + arm_tab_w/2, rear_leg_length - arm_tab_h/2, -1])
            cylinder(d=4.5, h=spring_boss_od + 10);
        // Lightening holes in vertical section
        translate([arm_vert_w/2, rear_leg_length * 0.4, wall_thickness])
            cylinder(d=arm_vert_w*0.5, h=pivot_arm_t - wall_thickness*2 + 0.01);
    }
}

// ── Axle cap ──────────────────────────────────────────────────────────────
module axle_cap() {
    difference() {
        cylinder(d=axle_diameter + 8, h=14);
        // Press-fit bore
        translate([0,0,-0.01]) cylinder(d=axle_diameter - clear_close*2, h=10);
        // M4 set screw
        translate([axle_diameter/2 + 2, 0, 7]) rotate([0,90,0]) cylinder(d=3.3, h=8);
    }
}

// ── Spring boss (removable — press-fit into arm tab) ──────────────────────
module spring_boss() {
    difference() {
        cylinder(d=spring_boss_od - clear_close*2, h=12);
        translate([0,0,4]) cylinder(d=spring_boss_od*0.5, h=9);
        translate([0,0,-0.01]) cylinder(d=4.5, h=13);
    }
}

// ── Stopper (TPU — sits in arm slot to limit collapse angle) ──────────────
module stopper() {
    difference() {
        rounded_rect(stopper_w, stopper_h, pivot_arm_t, r=2);
        // Bolt slots
        translate([stopper_w*0.25, stopper_h/2, -1])
            cylinder(d=4.5, h=pivot_arm_t+2);
        translate([stopper_w*0.75, stopper_h/2, -1])
            cylinder(d=4.5, h=pivot_arm_t+2);
    }
}

// ── Belly sling mount ─────────────────────────────────────────────────────
module belly_sling_mount() {
    slot_w = 12; slot_h = 4; // 1" webbing slots
    difference() {
        rounded_rect(hip_width * 0.4, 30, 8, r=3);
        // Two webbing slots
        translate([8, 10, wall_thickness])
            cube([slot_w, slot_h, 8 - wall_thickness + 1]);
        translate([hip_width*0.4 - 8 - slot_w, 10, wall_thickness])
            cube([slot_w, slot_h, 8 - wall_thickness + 1]);
        // Mounting bolt holes
        translate([hip_width*0.4/2, 25, -1]) cylinder(d=4.5, h=10);
    }
}

// ── Assembly preview (comment out for individual STL export) ──────────────
// translate([0, 0, ground_clearance]) rail();
// translate([hip_width, 0, ground_clearance]) mirror([1,0,0]) rail();
// translate([0, 0, ground_clearance]) rotate([90,0,90]) crossbar(hip_width + rail_w*2);
// translate([0, 0, 0]) pivot_arm();
// translate([hip_width, 0, 0]) mirror([1,0,0]) pivot_arm();

// ── Individual part render (set part= when slicing) ───────────────────────
part = "rail_left"; // rail_left | rail_right | crossbar_front | crossbar_rear
                    // pivot_arm_left | pivot_arm_right | spring_boss_left | spring_boss_right
                    // axle_cap_left | axle_cap_right | stopper_left | stopper_right | belly_sling_mount

if (part == "rail_left")          rail();
if (part == "rail_right")         mirror([1,0,0]) rail();
if (part == "crossbar_front")     crossbar(hip_width + rail_w*2);
if (part == "crossbar_rear")      crossbar(hip_width + rail_w*2);
if (part == "pivot_arm_left")     pivot_arm();
if (part == "pivot_arm_right")    mirror([1,0,0]) pivot_arm();
if (part == "spring_boss_left")   spring_boss();
if (part == "spring_boss_right")  spring_boss();
if (part == "axle_cap_left")      axle_cap();
if (part == "axle_cap_right")     axle_cap();
if (part == "stopper_left")       stopper();
if (part == "stopper_right")      stopper();
if (part == "belly_sling_mount")  belly_sling_mount();
