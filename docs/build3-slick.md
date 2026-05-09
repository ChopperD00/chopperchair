# Build 3 — Slick: Design Direction

> *Ascento aesthetics. Guntank proportions. Built for dogs that have taste.*

Build 3 is mechanically identical to Build 2 — same passive spring-pivot mechanism, same hardware BOM, same assembly process. What changes is everything you can see.

The reference palette:
- **Ascento (ETH Zürich)** — topology-optimized SLS nylon legs, skeletal organic struts, exposed hardware as honest engineering
- **Guntank (Gundam)** — wide low stance, hard panel lines, military colorblocking, the aesthetic of a machine that means business
- **Goblin War Machine (MyMiniFactory)** — exposed rivet detail, asymmetric greeble, the idea that mechanical complexity is beautiful
- **Diablo (DirectDrive)** — clean spine pod, paneled belly, the confidence of a machine with an open SDK

---

## What Changes

### Pivot Arms — Topology-Optimized Aesthetic

The Build 2 PivotArm is a solid box. Build 3 replaces it with a strut-frame arm inspired by Ascento's FEA-optimized legs. The geometry uses parametric cutouts arranged to mimic the result of topology optimization — triangulated internal voids, organic curved edges, material only where load paths require it.

This is printable on any FDM printer. The visual result is indistinguishable from SLS-printed topology-optimized parts at dog-wheelchair scale.

**Print orientation:** 45° on bed, same as Build 2. The strut geometry is designed so no support is needed.

### Rails — Panel Gap Language

Build 3 rails add shallow surface channels — 0.8mm deep, 1.2mm wide — running parallel to the long axis. These create the panel-gap language seen on Gundam kits and real aerospace hardware. They're purely cosmetic but transform the rails from extruded bars into something that looks machined.

### Spring Bosses — Exposed Coil Aesthetic

The SpringBoss in Build 3 is designed so the torsion spring coil is visible and celebrated rather than hidden. A low collar exposes the spring body. The spring becomes a design feature — a visible mechanical element that communicates function.

### Axle Caps — Hex Pattern

Build 3 AxleCaps have a recessed hex pattern on the outboard face — M3 bolt heads arranged in a circle, either functional (actual bolts) or printed-in as detail. References the Diablo wheel hub motor face.

---

## Colorway

### Option A — Tactical (recommended)
- **Rails + crossbars:** Matte black (Polymaker PolyTerra Matte Black, or any PETG matte black)
- **Pivot arms:** Gunmetal gray (metallic PETG — Prusament Galaxy Black or Hatchbox Metallic Gray)
- **Spring bosses + axle caps:** Accent color (pick one: #7c6af7 purple / safety orange / olive drab)
- **Stoppers:** Matte black with contrasting accent ring
- **Hardware:** Stainless steel — intentionally left raw, no painting

### Option B — High-Vis Medical
- **Rails:** Safety orange (Prusament PLA Prusa Orange or Hatchbox Orange)
- **Pivot arms:** Matte white
- **Accent:** Reflective silver filament on bosses/caps
- *Reads as: serious medical device, not a toy. Insurance-friendly aesthetic.*

### Option C — All Black APEX Preview
- Everything matte black except LED diffuser rings (clear PETG)
- Hardware: black oxide or painted stainless
- *This is the APEX colorway — Build 3 as a preview of what's coming*

---

## Filament Recommendations — Build 3

| Part | Filament | Brand | Why |
|------|----------|-------|-----|
| Rails | Matte PETG | Polymaker PolyTerra | No sheen, looks machined |
| Pivot arms | Metallic PETG | Prusament Galaxy Black | Reflects light like CNC aluminum |
| Spring bosses | PLA+ accent color | Polymaker PolyMax | High detail, press-fit retention |
| Axle caps | PETG | Any | Dimensional stability for set screw |
| Stoppers | TPU 95A or PLA+ | Polymaker/Hatchbox | TPU for shock, PLA+ with foam pad |

---

## Surface Finishing (optional, high effort)

For makers who want gallery-quality finish:

1. **Primer + sand:** Grey primer spray, 400 → 800 → 1200 grit wet sand on rails
2. **Metallic rattle can:** Rust-Oleum Metallic (gunmetal or aged bronze) over sanded surface
3. **Clear coat:** Matte clear over everything
4. **Panel wash:** Thin black acrylic wash into the panel gap channels, wipe clean — the channels catch the wash and read as deep shadow lines (Gunpla technique)
5. **Dry brush:** Silver metallic on raised edges — communicates wear and machined contact points

Total finishing time: ~3–4 hours. Result looks like a production prop.

---

## The Evolutionary Timeline Aesthetic

Build 3 is the bridge in the video. It has to read as *designed* next to Build 2's *functional*. The key visual cues:

- Build 2: square edges, solid geometry, utilitarian
- Build 3: chamfered edges, surface detail, panel gaps, visible mechanical elements
- APEX: all of the above plus LED glow, camera eye, spine pod

When the video cuts Build 2 → Build 3, the viewer should exhale slightly. When it cuts Build 3 → APEX, they should say *oh no.* (The good kind.)

---

## STL Changes from Build 2

| Part | Change |
|------|--------|
| Rail_Left / Rail_Right | Add panel gap channels (surface feature) |
| PivotArm_Left / Right | Replace solid body with topology-optimized strut frame |
| SpringBoss_Left / Right | Add exposed coil collar, lower profile |
| AxleCap_Left / Right | Add hex face detail |
| Stopper_Left / Right | Add chamfer + accent ring recess |
| Crossbar_Front / Rear | Add subtle surface ribbing |

All other parts unchanged. Build 3 is a drop-in upgrade — every hardware component from Build 2 is compatible.

---

## Print Settings — Build 3

Same as Build 2 with one addition: **0.15mm layer height on pivot arms** for the strut geometry to resolve cleanly. Other parts can stay at 0.2mm.
