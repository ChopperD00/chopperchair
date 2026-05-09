# Assembly Instructions

**Chopper Chair — Build 2 (Hybrid)**  
Estimated time: 30–45 minutes  
Tools needed: M4 hex key, scissors or knife

> Build 1 (full print) is the same process — skip any step that mentions purchased hardware.

---

## Before You Start

Print checklist. Confirm you have every part before picking up a tool.

**Printed parts:**
- [ ] Rail_Left.stl
- [ ] Rail_Right.stl
- [ ] Crossbar_Front.stl
- [ ] Crossbar_Rear.stl
- [ ] PivotArm_Left.stl
- [ ] PivotArm_Right.stl
- [ ] SpringBoss_Left.stl
- [ ] SpringBoss_Right.stl
- [ ] AxleCap_Left.stl
- [ ] AxleCap_Right.stl
- [ ] BellySling_Mount.stl
- [ ] Stopper_Left.stl
- [ ] Stopper_Right.stl

**Purchased hardware (Build 2):**
- [ ] 10mm OD stainless steel rod, 300mm length
- [ ] 100mm foam-fill wheels with 10mm bore, qty 2
- [ ] Torsion springs (10mm ID, matched to dog weight — see spring table), qty 2
- [ ] Neoprene or nylon belly sling, adjustable, small dog size
- [ ] M4×20mm socket head bolts, qty 2

**Tools:**
- [ ] 3mm hex key (for M4 set screws)
- [ ] Scissors or utility knife (for sling trimming)

---

## Step 1 — Attach the rear crossbar to the rails

Slide `Crossbar_Rear` into the rear slot on `Rail_Left`. Push until it seats flush — you'll feel it click into the channel. Repeat on `Rail_Right`.

**Check:** Hold the assembly up. The crossbar should not rotate or pull out without significant force. If it wiggles, your print tolerance is loose — a drop of super glue on each joint fixes it permanently.

---

## Step 2 — Attach the front crossbar

Repeat Step 1 with `Crossbar_Front` at the front slots of both rails.

**Check:** Set the rail assembly flat on your bench. Both rails should sit parallel with no twist. If one rail rocks, the crossbar isn't fully seated — push it in further.

---

## Step 3 — Mount the Spring Bosses onto the Pivot Arms

Press `SpringBoss_Left` onto the top post of `PivotArm_Left`. It should press-fit snugly. If it's loose, add a thin wrap of PTFE tape around the boss base before pressing.

Repeat for `SpringBoss_Right` onto `PivotArm_Right`.

**Do not glue the spring bosses** — they need to be removable to swap springs for different dogs.

---

## Step 4 — Seat the torsion springs

Slide one torsion spring over each Spring Boss. Orient the spring so:
- One leg of the spring rests flat against the top face of the pivot arm
- The other leg points upward, free to press against the rail when assembled

The spring will hold its position loosely at this stage. That's fine.

---

## Step 5 — Thread the axle rod

This is the fiddliest step. Take your time.

1. Hold `PivotArm_Left` (with spring) against the left rail at the rear slot, hinge bore aligned with the rail bore.
2. Start threading the 10mm stainless rod through `AxleCap_Left` from the outside inward.
3. Continue threading through the Pivot Arm bore, through the Crossbar_Rear center bore, through `PivotArm_Right`, and out through `AxleCap_Right` on the other side.
4. Center the rod so equal length protrudes from each axle cap.

**Check:** Both pivot arms should swing freely up and down on the rod. If they bind, check that the bore is clean of print artifacts — a 10mm drill bit run through by hand clears any stringing.

---

## Step 6 — Lock the axle caps with set screws

Insert one M4×20mm bolt into the set-screw hole on `AxleCap_Left`. Tighten with your 3mm hex key until the cap grips the rod firmly — snug, not gorilla-tight. The rod should not slide or rotate.

Repeat on `AxleCap_Right`.

**Check:** Try to slide the rod sideways. It should not move. Try to spin the rod — axle caps should rotate with it. If only one cap grips, the other set screw needs another quarter turn.

---

## Step 7 — Mount the wheels

Slide one 100mm foam-fill wheel onto each end of the axle rod, outboard of the axle caps.

The wheels should spin freely on the rod. They are not fixed — the rod turns inside the pivot arms, and the wheels ride on the rod ends. If your wheels have a locking collar, tighten it now so the wheel stays on but still spins.

**Check:** Set the assembled pivot/wheel subassembly on your bench. Both wheels should touch the surface simultaneously. If one is higher, the axle rod isn't centered — slide it to equalize.

---

## Step 8 — Attach the contact stoppers

Press `Stopper_Left` into the rear stopper slot on `Rail_Left`. It should snap into the channel with moderate hand pressure.

Repeat for `Stopper_Right` on `Rail_Right`.

**Optional:** Stick a 2mm strip of craft foam or neoprene to the face of each stopper that the pivot arm will contact. This softens the lie-down motion and reduces impact noise.

---

## Step 9 — Attach the Belly Sling Mount

Press `BellySling_Mount` into the top slot between the two rails. It should sit flat and level across both rails.

Thread your neoprene belly sling through the two strap slots on the mount. Adjust the sling length so it sits snugly under your dog's belly without pulling upward — the dog should feel supported, not lifted.

**Fit check (do this before the dog):** Hold the chair upright and push the sling up from below. It should support significant upward pressure without the mount flexing or pulling out of the rails.

---

## Step 10 — Spring tension test

Before putting your dog in the chair, verify the pivot mechanism works correctly.

1. Hold the rail assembly upright as if the dog were in it.
2. Push the pivot arms downward by hand — they should move smoothly toward the stoppers.
3. Release — the springs should return the arms to level within one second.
4. Push the arms all the way back until they contact the stoppers — they should hold there under light pressure and spring back when you stop pushing.

**If the springs return too fast or too slow:** See the spring selection table in [`docs/pivot-mechanism.md`](pivot-mechanism.md) and swap springs to match your dog's weight.

---

## Step 11 — First fit with your dog

1. Place the chair on the floor, wheels down.
2. Gently position your dog so their rear end is over the sling.
3. Lift the sling and clip or tie it snugly under their belly.
4. Let the dog stand naturally. The wheels should sit flat on the floor with the dog's rear legs just clearing the ground or lightly grazing it.
5. Encourage the dog to take a few steps forward. Watch the wheels — they should track straight.

**Sit test:** Encourage the dog to sit (treat works well). The pivot arms should lower smoothly as their rear drops. If the chair tips backward when sitting, the ground clearance is set too high — lower the `ground_clearance` parameter and reprint the rails.

**Lie-down test:** Let the dog back up slowly until they contact the stoppers. The arms should collapse gently to the floor. The dog should be able to rest comfortably with their rear on the ground.

---

## Adjustments

| Problem | Fix |
|---------|-----|
| Dog's rear too high off ground | Decrease `ground_clearance`, reprint rails |
| Dog's rear drags ground when standing | Increase `ground_clearance`, reprint rails |
| Pivot doesn't spring back / too stiff | Swap torsion springs (lighter or heavier rate) |
| Sling pulls upward | Lengthen sling straps |
| Chair tips sideways | Check that both wheels contact ground equally — re-center axle rod |
| Wheels don't roll straight | Check axle rod is perpendicular to rails — both axle cap set screws tightened evenly |
| Stoppers too abrupt when lying down | Add foam padding to stopper face |

---

## Care

- Wipe the pivot arm bores with a dry cloth weekly. Grit buildup causes binding.
- Check the M4 set screws monthly. PLA can creep slightly under sustained load — re-tighten if needed.
- Inspect the sling for fraying at the strap slots. Replace the sling if you see wear.
- PETG or ASA rails last longer outdoors than PLA. Reprint the rails if they show UV yellowing.
