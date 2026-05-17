// ChopperChair — Shared Parameters
// Injected by pipeline/bridge.py from measurements.json
// License: CC-BY-SA 4.0

// ── Dog measurements (mm) ─────────────────────────────────────────────────
torso_length     = 160;  // shoulder to hip
hip_width        = 90;   // widest point across hips
shoulder_width   = 80;   // front saddle width
rear_leg_length  = 80;   // floor to hip joint
ground_clearance = 45;   // chassis floor height
girth            = 165;  // belly circumference (harness ref)

// ── Hardware (mm) ─────────────────────────────────────────────────────────
wheel_diameter   = 100;  // purchased wheel OD
axle_diameter    = 8;    // purchased axle rod OD (Build 2: 8mm steel)
hub_motor_od     = 80;   // T-Motor MN1005 stator OD (Build 4 only)
hub_motor_depth  = 28;   // motor depth (Build 4 only)

// ── Frame geometry (mm) ───────────────────────────────────────────────────
wall_thickness   = 4;
rail_w           = 16;
rail_h           = 20;
crossbar_od      = 12;
spring_boss_od   = 18;
stopper_w        = 22;
stopper_h        = 15;

// ── SitGo pivot ───────────────────────────────────────────────────────────
collapse_angle   = 45;   // degrees — full lie-down
sit_angle        = 25;   // degrees — sit position
pivot_arm_t      = wall_thickness * 2.5;  // arm thickness

// ── Tolerances ────────────────────────────────────────────────────────────
clear_close      = 0.15; // press-fit clearance
clear_slide      = 0.25; // sliding fit clearance
clear_free       = 0.4;  // free-running clearance

$fn = 64;
