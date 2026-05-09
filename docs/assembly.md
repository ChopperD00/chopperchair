# Assembly Instructions

**Chopper Chair — Build 2 (Hybrid)**  
Estimated time: 30–45 minutes  
Tools needed: 3mm hex key, scissors or utility knife

> Build 1 (full print) is the same process — skip any step that mentions purchased hardware.

---

## Materials

Choose your filament based on how the chair will be used.

| Part | Recommended material | Why |
|------|---------------------|-----|
| Rails, crossbars | PETG or ASA | Structural load-bearing; PETG for indoors, ASA for outdoors |
| Pivot arms | PETG | Repeated flexion stress at hinge bore — PLA can fatigue |
| Spring bosses | PETG or PLA+ | Press-fit tolerance is tighter in PETG |
| Axle caps | PLA+ or PETG | Moderate stress; set-screw grip is critical |
| Belly sling mount | PLA | Low stress, mostly tension on the straps |
| Stoppers | PLA+ or TPU 95A | TPU softens impact; PLA+ works with foam padding |

If you only have one filament: **PETG at the infill percentages below works for all parts.**  
PLA works too but avoid using the chair outdoors in summer heat (>40°C/104°F).

---

## Before You Start

Confirm you have every part before picking up a tool.

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
- [ ] Torsion springs (10mm ID, matched to dog weight — see [`docs/pivot-mechanism.md`](pivot-mechanism.md)), qty 2
- [ ] Neoprene or nylon belly sling, adjustable, small dog size
- [ ] M4×20mm socket head bolts, qty 2
- [ ] Craft foam strip, 2mm (optional — for stopper padding)

**Where to buy:**  
All hardware is available on Amazon. Exact search terms in the [README BOM table](../README.md#hardware-bom--build-2).

**Tools:**
- [ ] 3mm hex key (for M4 set screws)
- [ ] Scissors or utility knife (for sling trimming)
- [ ] 10mm drill bit, hand-turned (optional — for clearing bore stringing)

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

Press `SpringBoss_Left` onto the post on top of `PivotArm_Left`. It's a press-fit — firm thumb pressure is enough. If it's loose, wrap one thin layer of PTFE tape around the boss base before pressing.

Repeat for `SpringBoss_Right` onto `PivotArm_Right`.

**Do not glue the spring bosses.** They need to come off to swap springs for a different dog.

---

## Step 4 — Seat the torsion springs

Slide one torsion spring over each Spring Boss. Orient each spring so:
- One leg rests flat against the top face of the pivot arm
- The other leg points upward, free to press against the rail when assembled

The spring will sit loosely at this stage. That's fine.

---

## Step 5 — Thread the axle rod

This is the fiddliest step. Take your time — it gets easier once you feel how the parts align.

1. Hold `PivotArm_Left` (with spring) against the inside of the left rail at the rear pivot slot, hinge bore aligned with the rail bore.
2. Start threading the 10mm stainless rod through `AxleCap_Left` from the outside inward.
3. Continue threading: through `PivotArm_Left` bore → through `Crossbar_Rear` center bore → through `PivotArm_Right` bore → out through `AxleCap_Right` on the far side.
4. Center the rod so equal length protrudes from each axle cap (roughly 15–20mm per side for wheel clearance).

**If the rod binds in a bore:** Run a 10mm drill bit through by hand — it clears print stringing in a few turns without removing material.

**Check:** Both pivot arms should swing freely up and down on the rod with no binding or sideways play.

---

## Step 6 — Lock the axle caps with set screws

Insert one M4×20mm bolt into the set-screw hole on `AxleCap_Left`. Tighten with your 3mm hex key until the cap grips the rod firmly — snug, not gorilla-tight. The rod should not slide sideways.

Repeat on `AxleCap_Right`.

**Check:** Try to slide the rod left or right. It should not move. If only one cap grips, the other set screw needs another quarter turn.

---

## Step 7 — Mount the wheels

Slide one 100mm foam-fill wheel onto each end of the axle rod, outboard of the axle caps. The wheels spin freely on the rod — they are not fixed. If your wheels have a locking collar, tighten it now so the wheel stays on but still spins.

**Check:** Set the assembled pivot/wheel subassembly on a flat surface. Both wheels should contact the surface simultaneously. If one is higher, the rod isn't centered — slide it to equalize, then re-tighten caps.

---

## Step 8 — Attach the contact stoppers

Press `Stopper_Left` into the rear stopper slot on `Rail_Left`. It should snap into the channel with moderate hand pressure. Repeat for `Stopper_Right` on `Rail_Right`.

**Optional but recommended:** Stick a 2mm strip of craft foam or neoprene to the face of each stopper that the pivot arm contacts. This softens the lie-down motion and reduces impact noise.

---

## Step 9 — Attach the Belly Sling Mount

Press `BellySling_Mount` into the top center slot between the two rails. It should sit flat and level across both rails.

Thread your neoprene belly sling through the two strap slots on the mount. Adjust so the sling sits snugly under your dog's belly without pulling upward — the dog should feel supported, not lifted.

**Fit check (do this before the dog):** Hold the chair upright and push the sling upward firmly from below. The mount should not flex or pull out of the rails under significant pressure.

---

## Step 10 — Spring tension test

Verify the pivot mechanism before your dog goes near it.

1. Hold the rail assembly upright as if the dog were fitted.
2. Push both pivot arms downward by hand — they should move smoothly toward the stoppers.
3. Release — springs should return both arms to level within one second.
4. Push the arms all the way back until they contact the stoppers — they should hold there under light hand pressure and spring back when released.

**If springs return too slow or arms sag under their own weight:** Springs are too light for the dog's weight — go up one rate. See the spring table in [`docs/pivot-mechanism.md`](pivot-mechanism.md).

**If arms return with a snap or spring binds:** Springs are too stiff — go down one rate.

---

## Step 11 — First fit with your dog

1. Place the chair on the floor, wheels down.
2. Gently position your dog so their rear end is over the sling.
3. Lift the sling and clip or tie it snugly under their belly.
4. Let the dog stand naturally. Rear legs should just clear the ground or graze it lightly.
5. Encourage a few steps forward. Wheels should track straight.

**Sit test:** Offer a treat to get the dog to sit. Pivot arms should lower smoothly as their rear drops. If the chair tips backward, `ground_clearance` is too high — lower it and reprint the rails.

**Lie-down test:** Let the dog back up slowly until they contact the stoppers. Arms should collapse gently. The dog should be able to rest with their rear on the ground.

**First session:** Keep it to 10–15 minutes. Dogs need time to learn the chair moves with them.

---

## Adjustments

| Problem | Fix |
|---------|-----|
| Dog's rear too high off ground | Decrease `ground_clearance`, reprint rails |
| Dog's rear drags ground when standing | Increase `ground_clearance`, reprint rails |
| Pivot doesn't spring back / arms sag | Swap to heavier spring rate |
| Pivot too stiff / dog can't sit | Swap to lighter spring rate |
| Sling pulls upward on dog | Lengthen sling straps |
| Chair tips sideways | Re-center axle rod — both wheels should contact ground equally |
| Wheels don't roll straight | Both axle cap set screws must be tightened evenly |
| Stoppers feel abrupt | Add foam padding to stopper contact face |
| Rail slot joint wiggles | Add a drop of super glue to the joint |

---

## Care

- **Weekly:** Wipe pivot arm bores with a dry cloth. Grit buildup causes binding.
- **Monthly:** Check M4 set screws. PLA and PETG can creep slightly under sustained load — re-tighten if the rod shifts.
- **As needed:** Inspect the sling for fraying at the strap slots. Replace if worn.
- **Seasonal:** PETG and ASA rails handle outdoor use. Reprint PLA rails if you see UV yellowing or warping.
