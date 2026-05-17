// ChopperChair — Build 4: APEX (Motorized)
// Hub motors replace torsion springs.
// ODrive Mini x2 on CAN bus. Pi5 SpinePod. NeoPixel wheel hubs.
// T-Motor MN1005 100KV (~80mm OD, ~28mm depth)
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

// ── APEX Pivot Arm (motor pocket instead of spring boss) ──────────────────
// The T-Motor MN1005 mounts in a recessed pocket on the arm face.
// Motor stator is fixed; wheel/rotor spins around it.
module apex_pivot_arm() {
    arm_w   = rail_w * 1.1;  // slightly wider for motor pocket clearance
    axle_z  = wheel_diameter/2 + 5;
    t       = pivot_arm_t * 1.4;  // thicker — motor reaction loads
    tab_h   = rail_h;

    difference() {
        union() {
            // Main arm body
            rounded_rect(arm_w, rear_leg_length, t, r=4);
            // Motor mount boss — raised ring around pocket
            translate([arm_w/2, axle_z, t])
                difference() {
                    cylinder(d=hub_motor_od + 8, h=3);
                    cylinder(d=hub_motor_od - 4, h=4);
                }
            // ODrive Mini bracket tab (rear)
            translate([arm_w, rear_leg_length - tab_h, 0])
                rounded_rect(rail_w*1.5, tab_h, t * 0.7, r=3);
        }

        // Motor pocket — T-Motor MN1005 sits flush
        translate([arm_w/2, axle_z, t - hub_motor_depth + 0.01])
            cylinder(d=hub_motor_od + clear_free*2, h=hub_motor_depth + 1);

        // Motor shaft bore (8mm — same as axle)
        translate([arm_w/2, axle_z, -1])
            cylinder(d=axle_diameter + clear_slide*2, h=t + 2);

        // Motor mounting bolt pattern (4x M3, 58mm BCD — MN1005 standard)
        for (a=[0,90,180,270]) {
            rotate([0,0,a])
            translate([arm_w/2 + 29, axle_z, t - 6])
                cylinder(d=3.4, h=8);
        }

        // Pivot bore (top — connects to rail)
        translate([arm_w/2, rear_leg_length - tab_h/2, -1])
            cylinder(d=axle_diameter + clear_close*2, h=t + 2);

        // ODrive mounting holes on tab (M3 x2)
        translate([arm_w + rail_w*0.5, rear_leg_length - tab_h*0.35, -1])
            cylinder(d=3.4, h=t*0.7 + 2);
        translate([arm_w + rail_w*0.5, rear_leg_length - tab_h*0.65, -1])
            cylinder(d=3.4, h=t*0.7 + 2);

        // Lightening cutouts along arm
        translate([arm_w/2, rear_leg_length * 0.5, t * 0.3])
            cylinder(d=arm_w * 0.5, h=t * 0.5);
    }
}

// ── APEX Rail (cable routing channels added) ───────────────────────────────
module apex_rail() {
    difference() {
        rounded_rect(rail_w, torso_length, rail_h * 1.15, r=4);

        // Internal lightening pocket
        translate([wall_thickness, wall_thickness*2, wall_thickness])
            cube([rail_w - wall_thickness*2,
                  torso_length - wall_thickness*4,
                  rail_h*1.15 - wall_thickness*2 + 0.01]);

        // Cable routing channel (6mm wide, runs full length on inner face)
        translate([rail_w - 2, wall_thickness*2, wall_thickness + 2])
            cube([3, torso_length - wall_thickness*4, 6]);

        // Crossbar sockets
        translate([rail_w/2, wall_thickness, rail_h*0.55])
            rotate([90,0,0]) cylinder(d=crossbar_od + clear_slide*2, h=wall_thickness+1, center=true);
        translate([rail_w/2, torso_length - wall_thickness, rail_h*0.55])
            rotate([90,0,0]) cylinder(d=crossbar_od + clear_slide*2, h=wall_thickness+1, center=true);
    }
}

// ── SpinePod — Pi5 + electronics chassis (mounts to crossbar) ────────────
// Houses: Pi5, Pi Camera ribbon, NeoPixel driver, CAN transceiver, LiPo
module spinepod_base() {
    pod_l = 120;  // Pi5 length + margin
    pod_w = 70;
    pod_h = 28;
    wall  = 2.5;

    difference() {
        // Outer shell
        rounded_rect(pod_w, pod_l, pod_h, r=5);
        // Interior cavity
        translate([wall, wall, wall])
            rounded_rect(pod_w - wall*2, pod_l - wall*2, pod_h, r=3);
        // Pi5 mounting hole pattern (58mm x 49mm — Pi5 standard)
        for (x=[0,58], y=[0,49]) {
            translate([pod_w*0.5 - 29 + x, pod_l*0.5 - 24.5 + y, -1])
                cylinder(d=2.8, h=wall + 2);  // M2.5 tapping holes
        }
        // Camera ribbon slot (22mm wide, front face)
        translate([pod_w/2 - 11, -0.01, pod_h - 8])
            cube([22, wall + 1, 6]);
        // Crossbar mounting slot (fits over crossbar_od tube)
        translate([pod_w/2 - crossbar_od/2 - 1, pod_l*0.25, -1])
            cube([crossbar_od + 2, crossbar_od + 2, wall + 2]);
        translate([pod_w/2 - crossbar_od/2 - 1, pod_l*0.65, -1])
            cube([crossbar_od + 2, crossbar_od + 2, wall + 2]);
        // Ventilation slots
        for (i=[0,1,2]) {
            translate([wall*2 + i*8, pod_l*0.1, -0.01])
                cube([4, pod_l*0.6, wall + 0.01]);
        }
        // USB-C power port cutout (Pi5 power)
        translate([-0.01, pod_l*0.5 - 5, wall + 6])
            cube([wall + 1, 10, 8]);
    }
}

module spinepod_lid() {
    pod_l = 120;
    pod_w = 70;
    wall  = 2.5;
    difference() {
        rounded_rect(pod_w, pod_l, wall * 1.5, r=5);
        // Clip slots
        for (x=[0.15, 0.85], y=[0.1, 0.9]) {
            translate([pod_w*x - 2, pod_l*y - 2, -1])
                cube([4, 4, wall*1.5 + 2]);
        }
    }
}

// ── NeoPixel hub ring cover (mounts over motor face, diffuses LED ring) ───
module neopixel_hub_cover() {
    ring_d  = 44;  // 16-LED 44mm NeoPixel ring OD
    ring_id = 34;  // inner diameter
    depth   = 8;
    wall    = 1.8;
    difference() {
        cylinder(d=hub_motor_od - 4, h=depth);
        // Translucent diffuser cavity
        translate([0, 0, wall])
            cylinder(d=hub_motor_od - 4 - wall*2, h=depth);
        // NeoPixel ring shelf (ring snaps in at 4mm depth)
        translate([0, 0, wall + 2])
            difference() {
                cylinder(d=ring_d + clear_slide*2, h=depth);
                cylinder(d=ring_id - clear_slide*2, h=depth);
            }
        // Shaft bore
        cylinder(d=axle_diameter + clear_free*2, h=depth + 1);
        // Motor bolt pass-through
        for (a=[0,90,180,270]) {
            rotate([0,0,a]) translate([29, 0, -1])
                cylinder(d=3.6, h=depth + 2);
        }
    }
}

// ── Axle cap (same as Build 2) ────────────────────────────────────────────
module axle_cap() {
    difference() {
        cylinder(d=axle_diameter + 8, h=14);
        translate([0,0,-0.01]) cylinder(d=axle_diameter - clear_close*2, h=10);
        translate([axle_diameter/2 + 2, 0, 7]) rotate([0,90,0]) cylinder(d=3.3, h=8);
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

// ── Part selector ─────────────────────────────────────────────────────────
part = "rail_left";
// rail_left | rail_right | crossbar_front | crossbar_rear
// pivot_arm_left | pivot_arm_right | axle_cap_left | axle_cap_right
// belly_sling_mount | spinepod_base | spinepod_lid | neopixel_hub_cover

if (part == "rail_left")           apex_rail();
if (part == "rail_right")          mirror([1,0,0]) apex_rail();
if (part == "crossbar_front")      cylinder(d=crossbar_od, h=hip_width + rail_w*2);
if (part == "crossbar_rear")       cylinder(d=crossbar_od, h=hip_width + rail_w*2);
if (part == "pivot_arm_left")      apex_pivot_arm();
if (part == "pivot_arm_right")     mirror([1,0,0]) apex_pivot_arm();
if (part == "axle_cap_left")       axle_cap();
if (part == "axle_cap_right")      axle_cap();
if (part == "belly_sling_mount")   belly_sling_mount();
if (part == "spinepod_base")       spinepod_base();
if (part == "spinepod_lid")        spinepod_lid();
if (part == "neopixel_hub_cover")  neopixel_hub_cover();
