#!/usr/bin/env python3
"""Build a single self-contained index.html teacher guide.

Embeds Outfit + DM Sans (woff2) and 20 slide JPEGs as base64 data URIs so the
file works fully offline. Content is faithful to the Word teacher guide,
rewritten in an action-led, threshold-flavored coach voice. No em-dashes.
"""

import base64
import os
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))

# Editable slide deck. Lives next to index.html; the Reference page links to it for download.
DECK_FILE = "Hydraulic Arm 2026_Final_web.pptx"
SLIDES = os.path.join(ROOT, "assets", "slides")
FONTS = os.path.join(ROOT, "assets", "fonts")


def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def slide_uri(name):
    return "data:image/jpeg;base64," + b64(os.path.join(SLIDES, name))


def font_uri(name):
    return "data:font/woff2;base64," + b64(os.path.join(FONTS, name))


def logo_uri(name):
    return "data:image/png;base64," + b64(os.path.join(ROOT, "assets", "logos", name))


# --------------------------------------------------------------------------
# CONTENT
# --------------------------------------------------------------------------

OBJECTIVES = [
    ("Physics", "Analyze syringe area ratios from measured data to predict and verify mechanical advantage."),
    ("Reverse-Engineer", "Decode a laser-cut kit with no manual and build a hydraulic arm that grips, lifts, and places a half-full bottle."),
    ("Build", "Tune gripper, ratios, and structure into a reliable multi-axis machine through iteration."),
    ("Perform", "Evaluate the arm across solo practice and a multi-robot relay, explaining how design choices drove results."),
]

VOCAB = [
    ("Pressure", "The amount of force applied over a given area."),
    ("Mechanical Advantage", "How a system trades force for distance to make work easier. Gaining one means giving up the other."),
    ("Pascal's Principle", "Pressure applied to a confined fluid transmits equally in all directions throughout that fluid."),
    ("Area Ratio", "The ratio of output syringe area to input syringe area. It sets the force multiplier."),
    ("Reverse Engineering", "Examining an existing object to figure out how it works and how its parts fit together."),
    ("Multi-Axis System", "A machine that produces controlled motion along more than one independent direction or rotation."),
]

MATERIALS = [
    ("Structural", [
        "Pre-laser-cut parts kit · etched names · one part carries attachment instructions",
        "3D-printed Robogripper · one per group · optional swap-in",
        "1/8 inch dowels",
        "Craft cubes (with and without holes)",
        "Hole-drilling jig for syringes (wood block)",
    ]),
    ("Hydraulic", [
        "60 mL syringes",
        "12 mL syringes with tubing and adapters",
        "Water + food coloring",
        "Cups for filling",
    ]),
    ("Tools & Supplies", [
        "Wood glue · gloves for gluing",
        "Scissors · rulers · sandpaper strips",
        "Tape (masking + electrical) · rubber bands · 4 inch zip ties",
        "Spring scales · digital force/tension scales · kitchen scales",
        "Chemistry clamps (for Engage) · adhesive bumpers",
        "Test rig + force gauge (whole-class demo) · engineering notebooks",
    ]),
]

PREP = [
    "Pre-fill 20 oz water bottles to the half-full mark. Mark fill lines with tape.",
    "Prepare syringe pairs for Engage: one 1:1 pair and one small-to-big pair per station.",
    "Clamp output syringes facing down toward kitchen scales at each station.",
    "Set out spring scales, kitchen scales, chemistry clamps, rulers, recording sheets.",
    "Assemble the front test rig: stand + force gauge + vertical syringe adapter.",
    "Pre-laser-cut all kit parts. Verify etched names are legible.",
    "Confirm the attachment-instruction part is in every kit.",
    "Print 3D Robogripper(s); place in a shared, accessible bin.",
    "Set up two parallel linear relay courses with zone markers for Day 3.",
    "Organize build materials by station.",
    "Print student sheets.",
    "Mark all bottles to the same fill level; stage spare bottles.",
    "Stage sandpaper / rubber tape in case all teams struggle with grip.",
    "Charge or check digital force scales.",
    "Lay out the hole-drilling jig safely near an adult-supervised station.",
    "Have spare tubing and adapters ready for Day 3 leak fixes.",
]

FAILURES = [
    ("Spongy or mushy hydraulics", "build",
     "Air bubbles in the line. The most common problem across all hydraulic builds.",
     "What is in that tube besides water? What happens to force when something in the system can compress?"),
    ("Leaks at syringe-to-tubing joints", "build",
     "Water dripping and pressure lost at connection points.",
     "Where is your system losing pressure? How could you seal it?"),
    ("Gripper closes but won't hold the bottle", "gripper",
     "Not enough clamping force, grip surface too smooth, or geometry wrong for the bottle.",
     "What is holding the bottle right now, force or friction? Which would you change first? What could you add to the gripper?"),
    ("Joint binds or sticks mid-motion", "joint",
     "Misaligned pivot, bent dowel, or tubing pinched during movement.",
     "Can you move this joint smoothly by hand without hydraulics? If not, what is catching?"),
    ("Arm flexes or bows under load", "structure",
     "Structural members too weak, or too much unsupported span between joints.",
     "Where is the load bending your arm? What is supporting that span right now? Could you add anything?"),
    ("Tubing kinks during movement", "build",
     "Routing too tight, no clearance for the tubing as joints change position.",
     "Watch the tubing while you move the arm. Where does it pinch? How could you reroute it?"),
    ("Prediction gap larger than expected", "physics",
     "Friction, plunger seal drag, air, and inconsistent hand force all eat the ideal.",
     "The equation is the ideal. Where is the real system losing the force the math promised?"),
    ("Plunger jams or won't seat", "joint",
     "Hole drilled off-axis or plunger range of motion not planned for.",
     "How far does the plunger have to travel? Does the build give it that room end to end?"),
]

PENALTIES = [
    ("Bottle dropped · robot can re-grip", "Robot may re-grip and continue."),
    ("Bottle dropped · robot cannot recover it", "Coach returns the bottle to the pickup zone. Restart that completion."),
    ("Robot disconnects, leaks badly, or fails mid-race", "Team may quickly fix the robot, then resume."),
]

# Syringe configuration cheat-sheet: config, force, distance, use it for
SYRINGE_CONFIG = [
    ("1:1 · equal diameters", "Same force in, same force out", "Same travel", "Predictable motion. A simple, honest baseline."),
    ("Small in -> Big out", "More force out", "Less travel", "Gripping and lifting. Trade reach for clamping strength."),
    ("Big in -> Small out", "Less force out", "More travel", "Speed and reach. Trade strength for distance covered."),
]

# Background knowledge: coach-facing "learn more" links. (label, url, note)
BACKGROUND = [
    ("Pascal's Principle and fluid pressure (Khan Academy)",
     "https://www.khanacademy.org/science/in-in-class11th-physics/in-in-class11th-physics-fluids/in-in-density-and-pressure/v/fluids-part-1",
     "A short video walking through pressure in a confined fluid. The clearest refresher before teaching the Day 1 physics."),
]

# Race format facts for the reference hub
RACE_RULES = [
    "60 seconds per match. Most completions wins.",
    "Two rounds, teams re-randomized between them. Add Round 3 if time allows.",
    "Robots stay stationed at their zones. Only the bottle moves down the chain.",
    "Teams are random and announced late, just before the race, to prevent strategizing.",
    "Tiebreaker: re-run the final 30 seconds head-to-head.",
    "Once the race starts the coach is a referee: call resets, count completions, manage the clock, watch safety. No coaching mid-race.",
]

# Each phase: id, num, tag, mins, title, slide, screen, say, do, watch[], ask[(q,a)], note, callouts[(kind,title,body)], extra(html)

DAY1 = [
    dict(id="d1p1", num="01", tag="Engage", mins=15, title="Force vs. distance, felt before named", slide="slide03",
         screen="Title and prompt for the force-distance exploration. Two pre-connected syringe pairs per station: one 1:1, one small-to-big. Spring scales, rulers, chemistry clamps on the table.",
         say="Two pairs in front of you. Push one, then the other. Measure what comes out. Write what you notice in your own words. Do not wait for me to name it.",
         do="Circulate. Keep teams measuring, not theorizing. Have them flip the small-to-big pair and push from the big side to feel the inverse: more distance, less force. Hold the vocabulary back.",
         watch=["Teams skipping the ruler and only feeling force / push them to record distance too",
                "Hands varying push-to-push / fine for now, it sets up the rig demo later",
                "The observation column left blank / one sentence per row is the whole point"],
         ask=[("Which one moved farther?", "Good. Now which one pushed harder? What is the trade you just made?"),
              ("Is this the right answer?", "There is no answer sheet here. What did your scale and ruler actually say?")],
         note="Constructivist open. Students generate the pattern before any term exists. The observation column forces them to articulate it, which becomes the bridge into instruction. Do not name Pascal yet.",
         callouts=[("warn", "Watch for", "Listen for language like more force but less movement or it barely moved but pushed really hard. Those exact phrases are your handoff into the next phase.")],
         extra=""),
    dict(id="d1p2", num="02", tag="Explicit Instruction", mins=3, title="Name what they already felt", slide="slide04",
         screen="Pascal's Principle introduced. Pressure in a confined fluid transmits equally in all directions.",
         say="What you felt has a name. Push on a confined fluid and the pressure goes everywhere equally. That is Pascal's Principle. The force you felt change was the system spending pressure across a bigger area.",
         do="Connect their words to the term. Take two or three team observations from Engage and relabel them with the vocabulary out loud.",
         watch=["Students treating this as new info / it is not, it is a name for what they measured",
                "Confusion between pressure and force / pressure is force over area, hold that distinction"],
         ask=[("Is pressure the same as force?", "Close. Pressure is force spread over an area. What happens to force if the same pressure acts on a bigger area?")],
         note="Threshold move: the idea was already in the room. You are handing them the word for an experience, not delivering a fact they must accept on authority.",
         callouts=[("def", "Pascal's Principle", "Pressure applied to a confined fluid transmits equally in all directions throughout that fluid.")],
         extra=""),
    dict(id="d1p3", num="03", tag="Explicit Instruction", mins=4, title="Why a little wider means a lot stronger", slide="slide05",
         screen="Area ratio reasoning. Area depends on the square of diameter, so small diameter changes produce large force changes.",
         say="The output syringe is wider, so the same pressure acts on more area, so more force comes out. And because area grows with the square of diameter, a little wider means a lot stronger. What you gain in force you give back in distance.",
         do="Draw or point to the two syringe faces. Emphasize the squared relationship before the formula appears.",
         watch=["Teams thinking double the width means double the force / it is the square, surface that now",
                "The distance trade getting lost / every force gain costs travel"],
         ask=[("Why squared and not just bigger?", "What are you actually comparing, the width across or the whole circle of fluid being pushed?")],
         note="This is the conceptual load-bearing step. If they own why area is squared, the formula next phase is a summary, not a surprise.",
         callouts=[("hero", "The core trade", "Force and distance are a single budget. The area ratio decides how the budget gets spent. No configuration gives you both.")],
         extra=""),
    dict(id="d1p4", num="04", tag="Explicit Instruction", mins=4, title="Here is the proof", slide="slide06",
         screen="The formal equation. Force multiplier equals (output diameter / input diameter) squared.",
         say="Here is the whole thing in one line. Force multiplier equals output diameter over input diameter, squared. That is the number your scales were circling around.",
         do="Write the equation. Tie each symbol back to a part they held five minutes ago.",
         watch=["Copying the formula without linking it to the syringes / point at the real parts",
                "Plugging in radius vs diameter inconsistently / either works if consistent, flag it"],
         ask=[("Does it matter if I use radius or diameter?", "Try both on the same pair. What do you get? Why does the ratio survive either way?")],
         note="The equation arrives after the intuition and the reasoning, never before. It formalizes; it does not introduce.",
         callouts=[("def", "Area ratio equation", "Force multiplier = (output diameter / input diameter)^2. Output area over input area sets how much the force is amplified.")],
         extra=""),
    dict(id="d1p5", num="05", tag="Practice", mins=4, title="Your turn on the numbers", slide="slide07",
         screen="Three to four escalating ratio problems on the student sheet, from basic calculation to applied design tradeoff.",
         say="Work the problems. Start with the plain calculation, then push into the ones where you have to choose a ratio for a job. There is a design decision hiding in the last one.",
         do="Let them work. Resist solving. Spot-check the squared step. Keep this tight so the verify moment next is not squeezed out.",
         watch=["Forgetting to square / most common error here",
                "Teams done fast / push them to the applied tradeoff problem and justify the choice"],
         ask=[("Which ratio is best?", "Best for what? More lifting force, or more reach and speed? What does the job need?")],
         note="Practice cements the tool. Keep it brief. The verification that follows is the most powerful beat of the day and must not get crowded out.",
         callouts=[("pill", "Time check", "Keep this to 4 minutes. If teams are still working, carry one problem into the rig demo discussion.")],
         extra=""),
    dict(id="d1p6", num="06", tag="Verify", mins=5, title="Did reality agree with the formula?", slide="slide08",
         screen="Whole-class rig demo. A hand-wheel test stand with a digital force gauge applies a measured, repeatable input force no hand can match.",
         say="Your scale said about four times. The equation said four to one. They did not match exactly. So where did the missing force go? Watch the rig. Same configuration, but the input is now perfectly steady.",
         do="Run two configurations students just tested. Read the gauge input aloud, then the output. Compare rig output to prediction and to their hand-measured numbers. Land the punchline.",
         watch=["Students thinking the rig fixed the data / it isolated a variable, say so",
                "The gap closing but not vanishing / that residual is the whole lesson"],
         ask=[("Why doesn't it ever hit exactly 4 to 1?", "What in a real system can leak, rub, or compress? Name three places the ideal loses force.")],
         note="The need was built before the tool arrived. Students named my hand was inconsistent; the rig is the response to their own diagnosis. That is how controlled experiments work. Name it explicitly.",
         callouts=[("warn", "Land this line", "Most of the gap was your hands. But even with a perfect input, the equation is still an ideal. Engineering lives in the remaining gap.")],
         extra="GAP"),
    dict(id="d1p7", num="07", tag="Challenge", mins=3, title="Some things humans should not touch", slide="slide09",
         screen="The challenge framing. Real hydraulic arms move what people cannot or should not: excavators, surgical robots, jaws of life. The job: grip, lift, and place a half-full bottle with precision.",
         say="Hydraulics let machines do what hands cannot, in places hands should not be. Your job is the same shape as theirs: grip something, lift it, place it exactly where it needs to go. Reliably. Every time.",
         do="Set the stakes and the standard. Precision and reliability, not speed. Preview that they will reverse-engineer a real arm with no manual.",
         watch=["Teams hearing competition and racing in their heads / reliability first, speed is Day 3",
                "Excitement without the precision frame / a wild lift that misses the zone scores nothing"],
         ask=[("How fast does it have to be?", "Fast enough is later. First: can it place the bottle exactly, every single time?")],
         note="Career connection lives here: mechanical, industrial, and biomedical engineers solve this same multi-axis trade. The challenge is authentic, not a toy.",
         callouts=[("hero", "The standard", "Grip. Lift. Place. With precision and reliability. The relay rewards machines that work every time, not machines that work once and impressively.")],
         extra=""),
    dict(id="d1p8", num="08", tag="Design", mins=12, title="No manual. Just the arm and a kit.", slide="slide10",
         screen="Reverse-engineering the kit. Parts are etched with names. One part carries attachment instructions. Everything else is up to the team. No assembly instructions provided.",
         say="No instructions. The parts are labeled and one part tells you how it attaches. The rest is yours to decode. Three moves before any glue: inventory, sketch, justify.",
         do="Hold the line on all three moves. Inventory the parts and best-guess each function. Sketch the assembly with syringes placed and uncertainties marked. Then justify: how does the arm stay stable when extended and loaded? Teams that cannot point to their sketch and explain stability are not cleared to build.",
         watch=["Teams reaching for glue before sketching / no build without a justified plan",
                "Skipping the inventory / they will lose a part and not know it",
                "Uncertainties erased instead of marked / question marks are data, keep them"],
         ask=[("What does this part do?", "Read the etched name. Where would a part with that name belong on something that has to lift and hold?"),
              ("Can we just use the Robogripper?", "Yes, any time, same mount, no penalty. It changes which engineering problem you are solving, not whether you are doing engineering.")],
         note="The reverse-engineering approach levels the field: every team faces the same novel decoding problem. Productive struggle is the design. Do not shortcut it by hinting at the intended assembly.",
         callouts=[("warn", "Gate before build", "Justify your plan. Point to the sketch. Explain how it stays stable loaded and extended. No justification, no glue."),
                   ("pill", "Normalize the swap", "The 3D Robogripper is a seamless swap for the laser-cut claw at any point. Same mounting interface. No design penalty.")],
         extra=""),
    dict(id="d1p9", num="09", tag="Build", mins=35, title="Direction, not completion", slide="slide11",
         screen="Teams begin assembly. No prescribed starting subsystem. Work from the sketch, dry-fit, and surface the first round of this does not fit problems.",
         say="Start wherever your sketch tells you to. Dry-fit before you commit. Today is not about finishing a subsystem. It is about committing to a direction and finding your first real problems.",
         do="Circulate constantly. Redirect permanent gluing toward dry-fitting. Nudge teams who argue instead of building to test one connection on the table. There is no Day 1 checkpoint; end with parts dry-fitted or lightly attached and a clear plan for tomorrow.",
         watch=["Groups gluing permanently right away / redirect to dry-fit first",
                "Groups debating the plan without touching parts / test one connection now",
                "Drilling syringe holes without planning plunger travel / ask how far the plunger must move"],
         ask=[("Should we glue this yet?", "Does it work dry first? Commit with glue only after the dry-fit proves the fit."),
              ("We are stuck on where to start", "What is the one connection you are most sure about? Build that, learn from it, let it tell you what is next.")],
         note="Failure is data, not punishment. Day 1 build is unstructured by design. The point is direction, not completion. Notice and iterate begins here.",
         callouts=[("pill", "Mantras for this block", "Dry-fit before you commit. Direction, not completion. Notice and iterate."),
                   ("warn", "No Day 1 checkpoint", "Do not push for a finished subsystem. Dry-fitted parts plus a clear plan for Day 2 is a successful Day 1.")],
         extra=""),
    dict(id="d1p10", num="10", tag="Evaluate", mins=5, title="Pause. Write it down.", slide="slide12",
         screen="Day 1 reflection prompts in engineering notebooks.",
         say="Stop building. Three things in the notebook. What are you most sure about? What are you still figuring out? What is the first thing you do tomorrow?",
         do="Protect the full five minutes. This is where today's direction gets locked so Day 2 opens at speed instead of from scratch.",
         watch=["One-word answers / push for the specific first move tomorrow",
                "Teams wanting to keep building / the written plan is what makes Day 2 fast"],
         ask=[("Why are we stopping to write?", "What is the first thing you would do tomorrow if you forgot everything? That sentence is why.")],
         note="Reflection converts a messy build session into a plan. The Day 2 check-in reads directly off these notebooks.",
         callouts=[("def", "Notebook prompts", "1 / What part are you most sure about?  2 / What part are you still figuring out?  3 / What is the first thing you need to do on Day 2?")],
         extra=""),
]

# Day 1 groups its ten beats under four sections: Engage, Design, Build, Evaluate.
# (Days 2 and 3 are short enough to stay flat.) Assignment is by phase id; sections
# must stay contiguous in the list for the grouped renderer.
_D1_SECTIONS = {
    "d1p1": "Engage", "d1p2": "Engage", "d1p3": "Engage",
    "d1p4": "Engage", "d1p5": "Engage", "d1p6": "Engage",
    "d1p7": "Design", "d1p8": "Design",
    "d1p9": "Build",
    "d1p10": "Evaluate",
}
for _p in DAY1:
    _p["section"] = _D1_SECTIONS[_p["id"]]

SECTION_BLURBS = {
    "Engage": "Feel the force-distance tradeoff, name the physics, prove it with the equation, then verify the gap under controlled input.",
    "Design": "Set the challenge, then reverse-engineer the laser-cut kit and justify a build plan before any glue.",
    "Build": "Commit to a direction, dry-fit, and surface the first real problems. Direction, not completion.",
    "Evaluate": "Pause and write, so today's messy build becomes a plan Day 2 can open from at speed.",
}

DAY2 = [
    dict(id="d2p1", num="01", tag="Check-In", mins=5, title="Pick up where you left off", slide="slide14",
         screen="Day 2 opener. Teams review Day 1 notebooks and the priority they wrote down. The day's gate is stated.",
         say="Open your notebook to yesterday's plan. Find the first thing you said you would do. The goal by end of class: base, arm, and forearm attached and mobile, syringes mounted. Filling is optional today. Go.",
         do="Keep this to five minutes. State the gate, then release to build. Minimal coach-led instruction from here on.",
         watch=["Teams re-planning from scratch / point them at yesterday's written first move",
                "Asking for the gate twice / it is base + arm + forearm mobile, syringes mounted"],
         ask=[("Do we have to fill syringes today?", "Filling is Day 3 to avoid mid-build leaks. Can you dry-test joint motion without water today?")],
         note="The Day 1 reflection is the launch pad. A tight check-in protects the 80-minute build window that follows.",
         callouts=[("pill", "Today's gate", "Base + arm + forearm attached and mobile, syringes mounted. Filling optional.")],
         extra=""),
    dict(id="d2p2", num="02", tag="Build", mins=80, title="Open build window. Build. Test. Iterate.", slide="slide15",
         screen="Persistent build slide. No structured pauses. Students build, connect hydraulics, and dry-test joint articulation. Coaches circulate with the diagnostic field guide.",
         say="This is your time. Build, connect, test the motion, fix what fails, build again. I am circulating. When something breaks, that is data. Notice and iterate.",
         do="Circulate continuously with your teaching partner. Use the failure-mode field guide: diagnose by asking, not fixing. Keep the Robogripper bin open and offer the swap to any team whose claw is not working. Day 2 testing is dry-run only.",
         watch=["Teams chasing new features instead of working motion / make what you have work",
                "A claw that will not grip after repeated tries / offer the Robogripper swap",
                "Filling syringes early / dry-run only today, water is Day 3"],
         ask=[("Can you give us the answer?", "What does the system do right now? What is the one thing you would change to test next?"),
              ("Is it okay that this broke?", "What did it tell you? Failure is data. What is your next iteration?")],
         note="Maximum uninterrupted build time is the whole pedagogy of Day 2. Coaches diagnose with questions so teams own the fix. The full field guide is in the Reference tab.",
         callouts=[("warn", "Coach stance", "Circulate and diagnose. Ask the question that lets the team find it. Resist solving the problem for them."),
                   ("pill", "Field guide", "See the Reference tab (press 4) for the eight common failures, their cause, and the question to ask.")],
         extra="FAILURES"),
    dict(id="d2p3", num="03", tag="Evaluate", mins=5, title="Today taught you something", slide="slide16",
         screen="Day 2 reflection prompts in engineering notebooks.",
         say="Stop. Three in the notebook. What broke today and what did it teach you? If you could steal one idea from another team's arm, what and why? What is your one big concern for Day 3?",
         do="Protect five minutes. Push past it broke toward what the break revealed. The steal-an-idea prompt spreads good solutions across the room.",
         watch=["It just broke with no lesson named / what did the failure point to?",
                "No concern named for Day 3 / surface it now so it is not a surprise tomorrow"],
         ask=[("What if nothing broke?", "Then what did you test that worked? Why did it work? That is just as much data.")],
         note="Reflecting on failure as data closes the build day and seeds Day 3's finish-and-fix list.",
         callouts=[("def", "Notebook prompts", "1 / What broke or failed today, and what did you learn?  2 / One design idea you would steal from another team, and why?  3 / Your one big concern going into Day 3?")],
         extra=""),
]

DAY3 = [
    dict(id="d3p1", num="01", tag="Build & Practice", mins=15, title="Finish and fill", slide="slide18",
         screen="Teams fill syringes with water, bleed air bubbles, and make final adjustments. Robogripper swaps happen now if not already done.",
         say="Fill your syringes. Bleed the air. Reinforce any leak, replace any kinked tube. No new features today. Make what you have work.",
         do="Help teams bleed air and seal leaks. Do final Robogripper swaps now. Hold the no-new-features line firmly. This is finishing, not redesigning.",
         watch=["Spongy response after filling / air in the line, bleed it",
                "Last-minute feature ideas / no new features, make what exists work",
                "Leaks at connections / reinforce or replace tubing before practice"],
         ask=[("Can we add one more thing?", "Does what you have already work reliably? Make that true first. No new features today."),
              ("Why is it still mushy?", "What is in the tube besides water? What happens to force when something compresses?")],
         note="The mantra shifts here from notice and iterate to no new features, make what you have work. By practice time it shifts back to notice and iterate.",
         callouts=[("warn", "Today's rule", "No new features. Make what you have work. Filling and sealing only, not redesign.")],
         extra=""),
    dict(id="d3p2", num="02", tag="Build & Practice", mins=20, title="Solo precision lift and place", slide="slide18",
         screen="Each group works at its own table with a marked pickup zone and a precision drop-off zone. Solo, low-stakes, repetition.",
         say="Your table, your reps. Pick up. Lift over. Place. Same move the relay needs, lower temperature. Tune grip, syringe response, and placement until it is reliable.",
         do="Let teams iterate freely. This is direct practice for the relay: same skills, lower stakes. Encourage repetition over cleverness. Notice and iterate is back.",
         watch=["One good lift treated as done / can they do it ten times in a row?",
                "Tuning grip but ignoring placement accuracy / the drop zone is the scored part",
                "Teams not using the full window / more clean reps now means more completions later"],
         ask=[("It worked once, are we ready?", "Once is luck. Can you do it five times without a drop? That is reliable."),
              ("Grip or placement first?", "Which one is failing more right now? Fix the one costing you the most reps.")],
         note="Solo practice is the relay rehearsal at low stakes. Repetition builds the reliability the race rewards. Pick up. Lift over. Place.",
         callouts=[("pill", "Mantra", "Notice and iterate. Pick up. Lift over. Place. Reliability over flash."),
                   ("hero", "Practice is the race", "The relay is these same three moves under a clock and a crowd. Reps banked now are completions earned later.")],
         extra=""),
    dict(id="d3p3", num="03", tag="Compete", mins=40, title="Multi-robot relay race", slide="slide19",
         screen="Relay courses. Robots stay stationed at their zones; only the bottle moves. Random teams announced just before the race.",
         say="Teams are random and I am announcing them now. Robot 1 picks up and hands to Robot 2, down the chain, last robot places in the drop zone. I return the bottle, you start again. Sixty seconds. Most completions wins.",
         do="Assign relay teams randomly on the spot; team size depends on attendance. Run two rounds with re-randomized teams between them; add Round 3 if time allows. You are the referee now: call resets, count completions, manage the clock, watch safety. Students return bottles to pickup themselves between completions during a run; you return the bottle only on an unrecoverable drop.",
         watch=["Robots crashing or plungers shoved past range / pause the match, safety first",
                "Tubing whipping / stop and have the team secure it",
                "Pre-game strategizing / the surprise teams are the point, announce late"],
         ask=[("That handoff failed, what do we do?", "Referee call only: re-grip allowed, or reset to pickup. Officiate it, do not coach through it.")],
         note="Once the race starts, the coach is a referee, not a coach. Multiple bottles flow simultaneously; officiate, do not instruct. Random teams announced late prevent strategizing that defeats the format.",
         callouts=[("warn", "Coach is a referee", "Call resets, count completions, manage the clock, watch for safety. No coaching mid-race."),
                   ("def", "Race mechanics", "60 seconds per match. Most completions wins. Two rounds, re-randomized between. Tiebreaker: re-run the final 30 seconds head-to-head.")],
         extra="RELAY"),
    dict(id="d3p4", num="04", tag="Debrief", mins=15, title="Closing reflection", slide="slide20",
         screen="Debrief connecting design decisions to performance, then written reflection in engineering notebooks.",
         say="Before you write: Team A completed more passes than Team B. Why? What did they do differently? Talk it out. Then four prompts in the notebook.",
         do="Pull specific examples from what just happened. Let students explain to each other before writing. Steer toward design choices driving results, not luck.",
         watch=["Best-built robot did not win / great discussion, why did reliability beat raw quality?",
                "Crediting luck / push back toward the design decision that actually mattered"],
         ask=[("Did the best robot win?", "Not always. So what beat it? Reliability? Handoff fit? Name the design choice that decided it.")],
         note="The debrief closes the loop opened on Day 1: hand-measured syringes connect to today's performance. That throughline is the unit's payoff.",
         callouts=[("def", "Notebook prompts", "1 / Cleanest handoff today and what made it work?  2 / Did the best-built robot always win? If not, why?  3 / How is today connected to the syringe equation from Day 1?  4 / With one more day, what would you change?")],
         extra=""),
]

DAYS = [
    dict(id="day1", n=1, title="From Syringes to Systems", time="90 min", cover="slide01", second="slide02",
         goal="Explore the force-distance tradeoff quantitatively, name the physics, verify the equation under controlled input, decode the laser-cut kit, and begin the build.",
         phases=DAY1),
    dict(id="day2", n=2, title="Build the Machine", time="90 min", cover="slide13", second=None,
         goal="Complete a functional rescue arm by end of period: base, arm, and forearm attached and mobile, syringes mounted. Maximum build and test time, minimal instruction.",
         phases=DAY2),
    dict(id="day3", n=3, title="Performance Under Pressure", time="90 min", cover="slide17", second=None,
         goal="Finalize the build, run solo precision practice, compete in the random multi-robot relay, and debrief design decisions against performance.",
         phases=DAY3),
]

# --------------------------------------------------------------------------
# CSS
# --------------------------------------------------------------------------

CSS = """
@font-face{font-family:'Outfit';src:url(__OUTFIT__) format('woff2');font-weight:100 900;font-display:swap;}
@font-face{font-family:'DM Sans';src:url(__DMSANS__) format('woff2');font-weight:100 1000;font-display:swap;}

:root{
  --teal:#186172; --teal-dark:#134E5C; --teal-deep:#0f4651;
  --teal-soft:#E1EDEE; --teal-text:#5A8A93;
  --magenta:#BD2F7F; --magenta-soft:#f7e6ef;
  --gold:#F0C896; --orange:#E8943A; --orange-text:#B87A2A;
  --ink:#333333; --ink-soft:#5a5a5a; --ink-faint:#8a8a8a;
  --bg:#F7F3EF; --paper:#ffffff; --rule:#e6ddd4; --rule-strong:#d4c8bb;
  --shadow:0 1px 0 rgba(0,0,0,.04), 0 12px 28px -18px rgba(15,70,81,.22);
  --maxw:980px;
}

*{box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{
  margin:0; background:var(--bg); color:var(--ink);
  font-family:'DM Sans',-apple-system,'Segoe UI',Calibri,sans-serif;
  font-size:16px; line-height:1.55; -webkit-font-smoothing:antialiased;
}
h1,h2,h3,h4,.f-head{font-family:'Outfit','DM Sans',sans-serif;font-weight:700;line-height:1.18;letter-spacing:-.01em;}
a{color:var(--teal);}

/* top bar */
.topbar{position:sticky;top:0;z-index:60;background:rgba(247,243,239,.92);backdrop-filter:blur(8px);
  border-bottom:1px solid var(--rule);}
.topbar-inner{max-width:var(--maxw);margin:0 auto;display:flex;align-items:center;gap:14px;padding:9px 22px;}
.brand{display:flex;align-items:center;gap:10px;font-family:'Outfit';font-weight:800;color:var(--teal-dark);font-size:15px;}
.brand .mark{height:34px;width:auto;display:block;}
.nav{display:flex;gap:4px;margin-left:auto;flex-wrap:wrap;}
.nav button{font:inherit;font-family:'Outfit';font-weight:600;font-size:13px;border:1px solid transparent;
  background:transparent;color:var(--ink-soft);padding:6px 12px;border-radius:7px;cursor:pointer;}
.nav button:hover{background:var(--teal-soft);color:var(--teal-dark);}
.nav button.active{background:var(--teal);color:#fff;}
.nav .ghost{border:1px solid var(--rule-strong);color:var(--teal);}
.nav .ghost.on{background:var(--magenta);border-color:var(--magenta);color:#fff;}

/* timer bar */
.timer-bar{position:sticky;top:53px;z-index:55;display:none;background:var(--teal-dark);color:#fff;}
.timer-bar.show{display:block;}
.timer-inner{max-width:var(--maxw);margin:0 auto;display:flex;align-items:center;gap:14px;padding:8px 22px;}
.timer-inner .lbl{font-family:'Outfit';font-weight:600;font-size:12px;opacity:.85;text-transform:uppercase;letter-spacing:.06em;}
.timer-inner .clock{font-family:'Outfit';font-weight:800;font-size:22px;font-variant-numeric:tabular-nums;min-width:78px;}
.timer-inner .ttitle{font-size:13px;opacity:.9;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.timer-inner button{font:inherit;font-family:'Outfit';font-weight:600;font-size:12px;border:1px solid rgba(255,255,255,.4);
  background:rgba(255,255,255,.08);color:#fff;padding:5px 11px;border-radius:6px;cursor:pointer;margin-left:auto;}
.timer-inner button+button{margin-left:6px;}
.timer-inner button:hover{background:rgba(255,255,255,.2);}
.timer-prog{height:4px;background:rgba(255,255,255,.18);}
.timer-prog i{display:block;height:100%;width:0;background:var(--gold);transition:width .4s linear;}
.timer-prog.over i{background:var(--magenta);}

.wrap{max-width:var(--maxw);margin:0 auto;padding:30px 22px 90px;}
.view{display:none;}
.view.active{display:block;}

/* HOME */
.hero{background:linear-gradient(135deg,var(--teal) 0%,var(--teal-deep) 100%);color:#fff;border-radius:16px;
  padding:42px 40px;box-shadow:var(--shadow);position:relative;overflow:hidden;}
.hero:after{content:"";position:absolute;right:-60px;top:-60px;width:260px;height:260px;border-radius:50%;
  background:rgba(189,47,127,.20);}
.hero .eyebrow{font-family:'Outfit';font-weight:600;text-transform:uppercase;letter-spacing:.14em;font-size:12px;
  color:var(--gold);margin:0 0 10px;}
.hero h1{font-size:40px;margin:0 0 8px;font-weight:800;}
.hero .sub{font-size:17px;opacity:.92;margin:0 0 22px;max-width:620px;}
.hero .arc{display:flex;gap:10px;flex-wrap:wrap;}
.hero .arc a{flex:1 1 200px;text-decoration:none;background:rgba(255,255,255,.10);border:1px solid rgba(255,255,255,.18);
  border-radius:11px;padding:14px 16px;color:#fff;transition:.15s;}
.hero .arc a:hover{background:rgba(255,255,255,.18);}
.hero .arc .d{font-family:'Outfit';font-weight:700;font-size:13px;color:var(--gold);}
.hero .arc .t{font-family:'Outfit';font-weight:700;font-size:16px;margin:2px 0 0;}
.hero .arc .m{font-size:12px;opacity:.8;}

.section-title{font-size:14px;font-family:'Outfit';font-weight:700;text-transform:uppercase;letter-spacing:.12em;
  color:var(--teal-text);margin:38px 0 14px;display:flex;align-items:center;gap:10px;}
.section-title:before{content:"";width:22px;height:3px;background:var(--magenta);border-radius:2px;}

.grid{display:grid;gap:14px;}
.g3{grid-template-columns:repeat(3,1fr);}
.g2{grid-template-columns:repeat(2,1fr);}
@media(max-width:760px){.g3,.g2{grid-template-columns:1fr;}}

.card{background:var(--paper);border:1px solid var(--rule);border-radius:11px;padding:18px 20px;box-shadow:var(--shadow);}
.obj-card .k{font-family:'Outfit';font-weight:700;color:var(--magenta);font-size:12px;text-transform:uppercase;
  letter-spacing:.08em;margin-bottom:6px;}
.obj-card .v{font-size:14.5px;color:var(--ink-soft);}

.vocab{margin:0;}
.vocab .term{padding:12px 0;border-bottom:1px solid var(--rule);}
.vocab .term:last-child{border-bottom:0;}
.vocab .t{font-family:'Outfit';font-weight:700;color:var(--teal-dark);font-size:15px;}
.vocab .d{font-size:14px;color:var(--ink-soft);margin-top:2px;}

.mat-col h4{margin:0 0 8px;color:var(--teal-dark);font-size:14px;}
.mat-col ul{list-style:none;margin:0;padding:0;}
.mat-col li{font-size:13.5px;color:var(--ink-soft);padding:5px 0 5px 16px;position:relative;border-bottom:1px dashed var(--rule);}
.mat-col li:before{content:"/";position:absolute;left:0;color:var(--magenta);font-weight:700;}
.mat-col li:last-child{border-bottom:0;}

.note-block{background:var(--magenta-soft);border-left:4px solid var(--magenta);border-radius:0 8px 8px 0;
  padding:12px 16px;font-size:13.5px;color:#7a2453;margin-top:8px;}

/* slide-deck download */
.deck-dl{display:flex;align-items:center;gap:16px;text-decoration:none;background:var(--teal);color:#fff;
  border-radius:12px;padding:18px 22px;box-shadow:var(--shadow);transition:filter .15s,transform .15s;}
.deck-dl:hover{filter:brightness(1.06);transform:translateY(-1px);}
.deck-dl .dico{flex:none;width:40px;height:40px;border-radius:9px;background:rgba(255,255,255,.16);display:flex;
  align-items:center;justify-content:center;font-family:'Outfit';font-weight:800;font-size:12px;letter-spacing:.02em;}
.deck-dl .dtxt{flex:1;}
.deck-dl .dt{display:block;font-family:'Outfit';font-weight:700;font-size:16px;color:#fff;}
.deck-dl .dm{display:block;font-size:13px;color:rgba(255,255,255,.82);margin-top:1px;}
.deck-dl .dgo{font-family:'Outfit';font-weight:700;font-size:13px;color:var(--gold);white-space:nowrap;}

/* background-knowledge links */
.bglist{display:grid;gap:11px;}
.bglink{display:grid;grid-template-columns:1fr auto;align-items:center;gap:8px 16px;text-decoration:none;
  background:var(--paper);border:1px solid var(--rule);border-radius:11px;padding:15px 18px;box-shadow:var(--shadow);
  transition:border-color .15s,transform .15s;}
.bglink:hover{border-color:var(--teal);transform:translateY(-1px);}
.bglink .bgt{grid-column:1;font-family:'Outfit';font-weight:700;font-size:15px;color:var(--teal-dark);}
.bglink .bgn{grid-column:1;font-size:13.5px;color:var(--ink-soft);}
.bglink .bggo{grid-column:2;grid-row:1 / span 2;font-family:'Outfit';font-weight:700;font-size:13px;color:var(--magenta);white-space:nowrap;}

/* prep checklist */
.prep{background:var(--paper);border:1px solid var(--rule);border-radius:11px;padding:6px 20px 12px;box-shadow:var(--shadow);}
.prep .row{display:flex;align-items:flex-start;gap:11px;padding:9px 0;border-bottom:1px solid var(--rule);cursor:pointer;font-size:14px;}
.prep .row:last-child{border-bottom:0;}
.prep .box{flex:none;width:19px;height:19px;border:2px solid var(--teal-text);border-radius:5px;margin-top:1px;
  display:flex;align-items:center;justify-content:center;transition:.12s;}
.prep .row.done .box{background:var(--teal);border-color:var(--teal);}
.prep .box svg{width:12px;height:12px;stroke:#fff;stroke-width:3;fill:none;opacity:0;}
.prep .row.done .box svg{opacity:1;}
.prep .row.done span{text-decoration:line-through;color:var(--ink-faint);}
.prep-summary{display:flex;align-items:center;gap:12px;margin:0 0 12px;font-family:'Outfit';font-weight:600;font-size:13px;color:var(--teal-text);}
.prep-summary .bar{flex:1;height:7px;background:var(--teal-soft);border-radius:4px;overflow:hidden;}
.prep-summary .bar i{display:block;height:100%;width:0;background:var(--magenta);transition:width .25s;}
/* prep checklist dropdown */
.prep-block{margin:38px 0 0;}
.prep-head{list-style:none;cursor:pointer;display:flex;align-items:center;gap:14px;padding:0;
  font-size:14px;font-family:'Outfit';font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:var(--teal-text);}
.prep-head::-webkit-details-marker{display:none;}
.prep-head:before{content:"";flex:none;width:22px;height:3px;background:var(--magenta);border-radius:2px;}
.prep-head-title{flex:none;white-space:nowrap;}
.prep-head .prep-summary{flex:1;margin:0;text-transform:none;letter-spacing:normal;}
.prep-head:hover .prep-head-title{color:var(--teal);}
.prep-chev{flex:none;width:15px;height:15px;stroke:var(--teal-text);stroke-width:2.5;fill:none;transition:transform .2s;}
.prep-block[open] .prep-chev{transform:rotate(180deg);}
.prep-block .prep{margin-top:14px;}

/* DAY view */
.day-head{background:linear-gradient(135deg,var(--teal-dark),var(--teal-deep));color:#fff;border-radius:14px;
  padding:28px 30px;box-shadow:var(--shadow);margin-bottom:22px;display:grid;grid-template-columns:1fr auto;gap:18px;align-items:center;}
.day-head .eyebrow{font-family:'Outfit';font-weight:600;text-transform:uppercase;letter-spacing:.14em;font-size:11px;color:var(--gold);}
.day-head h2{font-size:30px;margin:4px 0 8px;font-weight:800;}
.day-head .goal{font-size:14.5px;opacity:.9;max-width:620px;}
.day-head .meta{text-align:right;}
.day-head .meta .time{font-family:'Outfit';font-weight:800;font-size:30px;color:var(--gold);}
.day-head .meta .cnt{font-size:12px;opacity:.8;}
.day-cover{display:flex;gap:12px;margin-bottom:24px;flex-wrap:wrap;}
.day-cover img{flex:1 1 0;min-width:200px;border-radius:9px;border:1px solid var(--rule);box-shadow:var(--shadow);cursor:zoom-in;}

/* day sections (grouping of phase cards) */
.day-section{margin-bottom:26px;}
.sec-head{display:flex;align-items:flex-start;gap:16px;padding:15px 20px;border-radius:12px;
  background:linear-gradient(135deg,var(--teal),var(--teal-deep));color:#fff;box-shadow:var(--shadow);margin-bottom:13px;}
.sec-num{font-family:'Outfit';font-weight:800;font-size:32px;line-height:1;opacity:.85;min-width:26px;}
.sec-name{font-family:'Outfit';font-weight:800;font-size:19px;text-transform:uppercase;letter-spacing:.05em;line-height:1.1;}
.sec-meta{font-family:'Outfit';font-weight:600;font-size:12px;opacity:.82;margin-top:3px;text-transform:uppercase;letter-spacing:.06em;}
.sec-blurb{font-size:13px;opacity:.92;margin-top:7px;max-width:66ch;line-height:1.5;}
.sec-phases{border-left:3px solid var(--teal-soft);margin-left:13px;padding-left:15px;}
@media(max-width:680px){.sec-phases{margin-left:0;padding-left:0;border-left:0;}}

/* phase card */
.phase{background:var(--paper);border:1px solid var(--rule);border-radius:11px;margin-bottom:13px;box-shadow:var(--shadow);
  overflow:hidden;transition:border-color .15s;}
.phase.open{border-color:var(--magenta);}
.phase-head{display:grid;grid-template-columns:54px 150px 1fr auto;gap:14px;align-items:center;padding:15px 20px;cursor:pointer;}
.phase-num{font-family:'Outfit';font-weight:800;font-size:30px;color:var(--teal);line-height:1;transition:color .15s;}
.phase.open .phase-num{color:var(--magenta);}
.phase-tag{justify-self:start;font-family:'Outfit';font-weight:700;font-size:10px;letter-spacing:.07em;text-transform:uppercase;
  background:var(--magenta);color:#fff;padding:5px 10px;border-radius:20px;white-space:nowrap;}
.phase-title{font-family:'Outfit';font-weight:700;font-size:17px;color:var(--ink);}
.phase-time{font-family:'Outfit';font-weight:700;font-size:13px;color:var(--teal-text);background:var(--teal-soft);
  padding:5px 11px;border-radius:7px;white-space:nowrap;}
.phase-chev{transition:transform .2s;color:var(--ink-faint);}
.phase.open .phase-chev{transform:rotate(180deg);}
.phase-body{display:none;padding:0 20px 22px;}
.phase.open .phase-body{display:block;}

.slide-shot{margin:4px 0 18px;}
.slide-shot img{width:100%;border-radius:9px;border:1px solid var(--rule);cursor:zoom-in;display:block;}
.slide-shot .cap{font-size:12px;color:var(--ink-faint);margin-top:6px;font-style:italic;}

.field{margin:0 0 16px;}
.field .flabel{font-family:'Outfit';font-weight:700;font-size:11px;text-transform:uppercase;letter-spacing:.09em;
  color:var(--teal-text);margin-bottom:5px;display:flex;align-items:center;gap:7px;}
.field .flabel:before{content:"";width:14px;height:2px;background:var(--magenta);border-radius:2px;}
.field .ftext{font-size:15px;color:var(--ink);}
.field.say .ftext{background:var(--teal-soft);border-radius:9px;padding:12px 15px;color:var(--teal-dark);font-size:15.5px;}

.slashlist{list-style:none;margin:0;padding:0;}
.slashlist li{position:relative;padding:5px 0 5px 18px;font-size:14.5px;color:var(--ink-soft);}
.slashlist li:before{content:"/";position:absolute;left:0;color:var(--orange);font-weight:700;}

.qa{border-left:3px solid var(--teal-soft);padding:2px 0 2px 14px;margin:9px 0;}
.qa .q{font-weight:600;color:var(--ink);font-size:14.5px;}
.qa .a{font-size:14px;color:var(--ink-soft);margin-top:2px;}
.qa .a:before{content:"\\21AA  ";color:var(--magenta);font-weight:700;}

.callout{border-radius:0 9px 9px 0;padding:12px 16px;margin:12px 0;font-size:14px;}
.callout .ct{font-family:'Outfit';font-weight:700;font-size:11px;text-transform:uppercase;letter-spacing:.07em;margin-bottom:4px;}
.callout.warn{background:#fdf1e7;border-left:4px solid var(--orange);} .callout.warn .ct{color:var(--orange-text);}
.callout.def{background:var(--magenta-soft);border-left:4px solid var(--magenta);} .callout.def .ct{color:var(--magenta);}
.callout.hero{background:var(--teal);color:#fff;border-left:4px solid var(--gold);} .callout.hero .ct{color:var(--gold);}
.callout.pill{background:var(--teal-soft);border-left:4px solid var(--teal);} .callout.pill .ct{color:var(--teal-text);}

.ped{background:#fbfaf8;border:1px dashed var(--rule-strong);border-radius:9px;padding:13px 16px;margin:14px 0 2px;}
.ped .pt{font-family:'Outfit';font-weight:700;font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--magenta);margin-bottom:4px;}
.ped .pb{font-size:13.5px;color:var(--ink-soft);font-style:italic;}

.phase-tools{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin-top:18px;padding-top:16px;border-top:1px solid var(--rule);}
.phase-tools button{font:inherit;font-family:'Outfit';font-weight:600;font-size:12.5px;border:1px solid var(--rule-strong);
  background:var(--paper);color:var(--teal);padding:7px 13px;border-radius:7px;cursor:pointer;}
.phase-tools button:hover{background:var(--teal-soft);}
.phase-tools button.go{background:var(--teal);color:#fff;border-color:var(--teal);}
.phase-notes{margin-top:14px;}
.phase-notes label{font-family:'Outfit';font-weight:700;font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--ink-faint);}
.phase-notes textarea{width:100%;margin-top:6px;border:1px solid var(--rule);border-radius:8px;padding:10px 12px;
  font:inherit;font-size:14px;resize:vertical;min-height:54px;background:#fffdfb;}
.phase-notes textarea:focus{outline:none;border-color:var(--teal);}

/* gap visual */
.gap-viz{background:#fbfaf8;border:1px solid var(--rule);border-radius:10px;padding:18px;margin:14px 0;}
.gap-viz h4{margin:0 0 14px;color:var(--teal-dark);font-size:14px;}
.gap-row{display:grid;grid-template-columns:120px 1fr 54px;align-items:center;gap:12px;margin:9px 0;}
.gap-row .gl{font-family:'Outfit';font-weight:600;font-size:12.5px;color:var(--ink-soft);}
.gap-track{height:22px;background:var(--teal-soft);border-radius:5px;overflow:hidden;}
.gap-track i{display:block;height:100%;border-radius:5px;}
.gap-row .gv{font-family:'Outfit';font-weight:800;font-size:15px;font-variant-numeric:tabular-nums;text-align:right;}
.gap-pred i{background:var(--teal);} .gap-pred .gv{color:var(--teal);}
.gap-meas i{background:var(--magenta);} .gap-meas .gv{color:var(--magenta);}
.gap-note{font-size:13px;color:var(--orange-text);background:#fdf1e7;border-radius:7px;padding:9px 12px;margin-top:12px;}
.gap-note b{color:var(--orange-text);}

/* tables */
.tbl{width:100%;border-collapse:collapse;margin:10px 0;font-size:13.5px;}
.tbl th{background:var(--teal);color:#fff;text-align:left;padding:9px 12px;font-family:'Outfit';font-weight:700;font-size:12px;}
.tbl td{padding:9px 12px;border-bottom:1px solid var(--rule);vertical-align:top;color:var(--ink-soft);}
.tbl tr:nth-child(even) td{background:#fbfaf8;}

/* relay chain */
.relay{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:14px 0;justify-content:center;}
.relay .node{background:var(--teal);color:#fff;font-family:'Outfit';font-weight:700;font-size:12px;padding:9px 13px;border-radius:9px;text-align:center;}
.relay .node.zone{background:var(--magenta);}
.relay .arr{color:var(--magenta);font-weight:800;font-size:18px;}

/* failure mode cards (Reference) */
.fmlist{display:grid;grid-template-columns:repeat(2,1fr);gap:11px;}
@media(max-width:760px){.fmlist{grid-template-columns:1fr;}}
.fm{background:var(--paper);border:1px solid var(--rule);border-radius:10px;padding:14px 16px;}
.fm .see{font-family:'Outfit';font-weight:700;color:var(--teal-dark);font-size:14.5px;}
.fm .cat{float:right;font-family:'Outfit';font-weight:600;font-size:10px;text-transform:uppercase;letter-spacing:.06em;
  color:var(--teal-text);background:var(--teal-soft);padding:3px 8px;border-radius:12px;}
.fm .cause{font-size:13px;color:var(--ink-soft);margin:7px 0;}
.fm .ask{font-size:13.5px;color:#7a2453;background:var(--magenta-soft);border-radius:7px;padding:8px 11px;}
.fm .ask:before{content:"Ask: ";font-weight:700;}

/* lightbox */
.lightbox{position:fixed;inset:0;background:rgba(15,30,35,.92);z-index:120;display:none;align-items:center;justify-content:center;padding:30px;cursor:zoom-out;}
.lightbox.open{display:flex;}
.lightbox img{max-width:96%;max-height:96%;border-radius:8px;box-shadow:0 20px 60px rgba(0,0,0,.6);}

/* fab */
.fab{position:fixed;right:22px;bottom:22px;z-index:50;display:flex;flex-direction:column;gap:9px;}
.fab button{font:inherit;font-family:'Outfit';font-weight:700;font-size:13px;border:0;cursor:pointer;border-radius:24px;
  padding:11px 16px;box-shadow:var(--shadow);}
.fab .top-btn{background:var(--teal);color:#fff;}
.fab button:hover{filter:brightness(1.07);}

.footer{text-align:center;padding:40px 0 14px;color:var(--ink-faint);font-size:12px;display:flex;flex-direction:column;align-items:center;gap:12px;}
.footer .footlogo{height:54px;width:auto;}
.footer .foottext{font-family:'Outfit';font-weight:600;letter-spacing:.02em;}

@media(max-width:680px){
  .phase-head{grid-template-columns:42px 1fr auto;}
  .phase-tag{display:none;}
  .hero h1{font-size:30px;} .day-head{grid-template-columns:1fr;} .day-head .meta{text-align:left;}
}

/* print */
@media print{
  .topbar,.timer-bar,.fab,.phase-tools,.phase-notes,.nav{display:none!important;}
  body{background:#fff;font-size:11pt;}
  .view{display:block!important;}
  .wrap{max-width:none;padding:0;}
  .phase{break-inside:avoid;page-break-inside:avoid;box-shadow:none;border-color:#ccc;}
  .phase-body{display:block!important;}
  .phase-chev{display:none;}
  .hero,.day-head{box-shadow:none;-webkit-print-color-adjust:exact;print-color-adjust:exact;}
  .callout,.gap-track i,.phase-tag,.tbl th{-webkit-print-color-adjust:exact;print-color-adjust:exact;}
  .day-head,.hero{page-break-after:avoid;}
  .slide-shot img,.day-cover img{max-height:3in;width:auto;}
}
"""


# --------------------------------------------------------------------------
# HTML RENDER
# --------------------------------------------------------------------------

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_callouts(callouts):
    out = []
    for kind, title, body in callouts:
        out.append(
            f'<div class="callout {kind}"><div class="ct">{esc(title)}</div>{esc(body)}</div>'
        )
    return "".join(out)


GAP_HTML = """
<div class="gap-viz">
  <h4>Prediction vs. measurement · a 4:1 syringe pair</h4>
  <div class="gap-row gap-pred"><div class="gl">Equation predicts</div><div class="gap-track"><i style="width:100%"></i></div><div class="gv">4.0&times;</div></div>
  <div class="gap-row gap-meas"><div class="gl">Students measure</div><div class="gap-track"><i style="width:80%"></i></div><div class="gv">3.2&times;</div></div>
  <div class="gap-note"><b>The gap is 0.8&times;.</b> Friction, plunger seal drag, air in the line, and inconsistent hand force live in that missing slice. The rig removes the hand. The rest is where engineering lives.</div>
</div>
"""

RELAY_HTML = """
<div class="relay">
  <div class="node zone">Pickup</div><span class="arr">&rarr;</span>
  <div class="node">Robot 1</div><span class="arr">&rarr;</span>
  <div class="node">Robot 2</div><span class="arr">&rarr;</span>
  <div class="node">Robot 3</div><span class="arr">&rarr;</span>
  <div class="node zone">Drop-off</div>
</div>
"""


def render_extra(kind):
    if kind == "GAP":
        return GAP_HTML
    if kind == "RELAY":
        rows = "".join(
            f"<tr><td>{esc(e)}</td><td>{esc(r)}</td></tr>" for e, r in PENALTIES
        )
        return (
            RELAY_HTML
            + '<table class="tbl"><thead><tr><th>Event</th><th>Rule</th></tr></thead><tbody>'
            + rows
            + "</tbody></table>"
        )
    if kind == "FAILURES":
        return ""  # field guide now lives in the Reference tab
    return ""


def render_phase(p, num=None):
    watch = "".join(f"<li>{esc(w)}</li>" for w in p["watch"])
    ask = "".join(
        f'<div class="qa"><div class="q">{esc(q)}</div><div class="a">{esc(a)}</div></div>'
        for q, a in p["ask"]
    )
    extra = render_extra(p["extra"])
    shown_num = num if num is not None else p["num"]
    return f"""
<div class="phase" id="{p['id']}" data-min="{p['mins']}" data-title="{esc(p['title'])}">
  <div class="phase-head" onclick="togglePhase('{p['id']}')">
    <div class="phase-num">{shown_num}</div>
    <div><span class="phase-tag">{esc(p['tag'])}</span></div>
    <div class="phase-title">{esc(p['title'])}</div>
    <div style="display:flex;align-items:center;gap:12px;">
      <span class="phase-time">{p['mins']} min</span>
      <svg class="phase-chev" width="16" height="16" viewBox="0 0 16 16"><path d="M3 6l5 5 5-5" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/></svg>
    </div>
  </div>
  <div class="phase-body">
    <div class="slide-shot"><img src="__{p['slide'].upper()}__" alt="Slide for {esc(p['title'])}" onclick="lightbox(this.src)"><div class="cap">What's on screen</div></div>
    <div class="field"><div class="flabel">On screen</div><div class="ftext">{esc(p['screen'])}</div></div>
    <div class="field say"><div class="flabel">What to say</div><div class="ftext">{esc(p['say'])}</div></div>
    <div class="field"><div class="flabel">What to do</div><div class="ftext">{esc(p['do'])}</div></div>
    <div class="field"><div class="flabel">Watch for</div><ul class="slashlist">{watch}</ul></div>
    <div class="field"><div class="flabel">If they ask</div>{ask}</div>
    {render_callouts(p['callouts'])}
    {extra}
    <div class="ped"><div class="pt">Pedagogical note</div><div class="pb">{esc(p['note'])}</div></div>
    <div class="phase-notes"><label for="note-{p['id']}">Coach notes (saved on this device)</label>
      <textarea id="note-{p['id']}" data-note="{p['id']}" placeholder="Jot adjustments, timing, what worked last time..."></textarea></div>
    <div class="phase-tools">
      <button class="go" onclick="startTimer('{p['id']}')">Start {p['mins']}-min timer</button>
      <button onclick="prevPhase('{p['id']}')">&larr; Prev</button>
      <button onclick="nextPhase('{p['id']}')">Next &rarr;</button>
    </div>
  </div>
</div>"""


def _group_sections(phases):
    """Group a phase list into ordered (section_name, [phases]) tuples.
    Consecutive phases sharing a section key are grouped; sections must be contiguous."""
    groups = []
    for p in phases:
        sec = p.get("section")
        if not groups or groups[-1][0] != sec:
            groups.append((sec, []))
        groups[-1][1].append(p)
    return groups


def render_day(d):
    cover = f'<img src="__{d["cover"].upper()}__" alt="Day {d["n"]} cover" onclick="lightbox(this.src)">'
    if d["second"]:
        cover += f'<img src="__{d["second"].upper()}__" alt="Day {d["n"]} objectives" onclick="lightbox(this.src)">'
    if any(p.get("section") for p in d["phases"]):
        groups = _group_sections(d["phases"])
        blocks = []
        for si, (sec, members) in enumerate(groups, start=1):
            mins = sum(m["mins"] for m in members)
            steps = f'{len(members)} step{"s" if len(members) != 1 else ""}'
            blurb = SECTION_BLURBS.get(sec, "")
            blurb_html = f'<div class="sec-blurb">{esc(blurb)}</div>' if blurb else ""
            cards = "".join(
                render_phase(p, num=str(bi)) for bi, p in enumerate(members, start=1)
            )
            blocks.append(
                f'<div class="day-section">'
                f'<div class="sec-head"><div class="sec-num">{si}</div>'
                f'<div class="sec-info"><div class="sec-name">{esc(sec)}</div>'
                f'<div class="sec-meta">{steps} &middot; {mins} min</div>{blurb_html}</div></div>'
                f'<div class="sec-phases">{cards}</div></div>'
            )
        phases = "".join(blocks)
        count_label = f'{len(groups)} sections'
    else:
        phases = "".join(render_phase(p) for p in d["phases"])
        count_label = f'{len(d["phases"])} phases'
    return f"""
<section class="view" id="view-{d['id']}">
  <div class="day-head">
    <div>
      <div class="eyebrow">Day {d['n']}</div>
      <h2>{esc(d['title'])}</h2>
      <div class="goal">{esc(d['goal'])}</div>
    </div>
    <div class="meta"><div class="time">{d['time']}</div><div class="cnt">{count_label}</div></div>
  </div>
  <div class="day-cover">{cover}</div>
  {phases}
</section>"""


def render_home():
    def _count_label(d):
        if any(p.get("section") for p in d["phases"]):
            return f'{len(_group_sections(d["phases"]))} sections'
        return f'{len(d["phases"])} phases'

    arc = "".join(
        f'<a href="#" onclick="setView(\'{d["id"]}\');return false;"><div class="d">Day {d["n"]}</div>'
        f'<div class="t">{esc(d["title"])}</div><div class="m">{d["time"]} &middot; {_count_label(d)}</div></a>'
        for d in DAYS
    )
    objs = "".join(
        f'<div class="card obj-card"><div class="k">{esc(k)}</div><div class="v">{esc(v)}</div></div>'
        for k, v in OBJECTIVES
    )
    prep_rows = "".join(
        f'<div class="row" data-prep="{i}" onclick="togglePrep({i})"><div class="box">'
        f'<svg viewBox="0 0 16 16"><path d="M3 8l3 3 7-7"/></svg></div><span>{esc(item)}</span></div>'
        for i, item in enumerate(PREP)
    )
    return f"""
<section class="view active" id="view-home">
  <div class="hero">
    <div class="eyebrow">TETC &middot; Teacher Guide</div>
    <h1>Hydraulic Rescue Arm</h1>
    <p class="sub">A three-day build unit. Students feel the physics, name it, verify it, then reverse-engineer and build a hydraulic arm that grips, lifts, and places under pressure.</p>
    <div class="arc">{arc}</div>
  </div>

  <div class="section-title">Unit objectives</div>
  <div class="grid g2">{objs}</div>

  <details class="prep-block">
    <summary class="prep-head">
      <span class="prep-head-title">Prep checklist</span>
      <span class="prep-summary"><span id="prep-count">0 / {len(PREP)}</span><div class="bar"><i id="prep-bar"></i></div></span>
      <svg class="prep-chev" viewBox="0 0 16 16"><path d="M4 6l4 4 4-4"/></svg>
    </summary>
    <div class="prep">{prep_rows}</div>
  </details>

  <div class="section-title">How to use this guide</div>
  <div class="card" style="font-size:14.5px;color:var(--ink-soft);">
    <p style="margin-top:0;">Click any phase to expand its coaching detail. Each phase has a suggested timer, prev/next navigation, and a private notes field saved on this device.</p>
    <p><b>Reference</b> (top nav or press 4) gathers everything you look up mid-class: a download for the slide deck, the syringe equation, configuration cheat-sheet, materials, payload and relay specs, race rules, and vocabulary.</p>
    <p>The <b>Reference</b> tab also holds the Day 2 <b>failure-mode field guide</b>: the common failures, their cause, and the question to ask. Print at any time; each phase is set to avoid splitting across pages.</p>
    <p style="margin-bottom:0;"><b>Keyboard:</b> 1 / 2 / 3 jump to days &middot; 4 reference &middot; H home &middot; arrows move between phases &middot; Esc closes.</p>
  </div>
</section>"""


def render_reference():
    mats = "".join(
        '<div class="card mat-col"><h4>' + esc(h) + "</h4><ul>"
        + "".join(f"<li>{esc(i)}</li>" for i in items)
        + "</ul></div>"
        for h, items in MATERIALS
    )
    vocab = "".join(
        f'<div class="term"><div class="t">{esc(t)}</div><div class="d">{esc(dd)}</div></div>'
        for t, dd in VOCAB
    )
    cfg_rows = "".join(
        f"<tr><td><b>{esc(c)}</b></td><td>{esc(f)}</td><td>{esc(dist)}</td><td>{esc(use)}</td></tr>"
        for c, f, dist, use in SYRINGE_CONFIG
    )
    rules = "".join(f"<li>{esc(r)}</li>" for r in RACE_RULES)
    pen_rows = "".join(
        f"<tr><td>{esc(e)}</td><td>{esc(r)}</td></tr>" for e, r in PENALTIES
    )
    bg = "".join(
        f'<a class="bglink" href="{esc(url)}" target="_blank" rel="noopener">'
        f'<span class="bgt">{esc(label)}</span><span class="bgn">{esc(note)}</span>'
        f'<span class="bggo">Open &rarr;</span></a>'
        for label, url, note in BACKGROUND
    )
    fm_cards = "".join(
        f'<div class="fm"><span class="cat">{esc(cat)}</span>'
        f'<div class="see">{esc(see)}</div>'
        f'<div class="cause">{esc(cause)}</div><div class="ask">{esc(ask)}</div></div>'
        for see, cat, cause, ask in FAILURES
    )
    deck_path = os.path.join(ROOT, DECK_FILE)
    deck_section = ""
    if os.path.exists(deck_path):
        size_mb = os.path.getsize(deck_path) / 1048576
        deck_section = (
            '<div class="section-title">Slide deck</div>'
            f'<a class="deck-dl" href="{quote(DECK_FILE)}" download="{esc(DECK_FILE)}">'
            '<span class="dico">PPTX</span>'
            '<span class="dtxt"><span class="dt">Download the slide deck</span>'
            f'<span class="dm">PowerPoint &middot; {size_mb:.0f} MB &middot; the editable deck this guide accompanies</span></span>'
            '<span class="dgo">Download &darr;</span></a>'
            '<div class="note-block" style="background:var(--teal-soft);border-left-color:var(--teal);color:var(--teal-dark);">Keep the deck file in the same folder as this guide for the download to work. To present, open it in PowerPoint.</div>'
        )
    return f"""
<section class="view" id="view-reference">
  <div class="day-head">
    <div>
      <div class="eyebrow">Quick reference</div>
      <h2>Reference</h2>
      <div class="goal">Everything you reach for mid-class in one place: the core equation, syringe configurations, materials, payload and relay setup, race rules, vocabulary, and the Day 2 failure-mode field guide.</div>
    </div>
    <div class="meta"><div class="time">At a glance</div></div>
  </div>

  {deck_section}

  <div class="section-title">The core equation</div>
  <div class="callout hero"><div class="ct">Force multiplier</div>Force multiplier = (output diameter / input diameter)<sup>2</sup>. Output area over input area sets how much the force is amplified. The equation is the ideal; friction, seal drag, and air in the line live in the gap between it and what the scales read.</div>

  <div class="section-title">Syringe configuration cheat-sheet</div>
  <table class="tbl"><thead><tr><th>Configuration</th><th>Force</th><th>Distance</th><th>Use it for</th></tr></thead><tbody>{cfg_rows}</tbody></table>

  <div class="section-title">Materials</div>
  <div class="grid g3">{mats}</div>
  <div class="note-block"><b>Payload:</b> 20 oz water bottles at half-full, all to the same line, marked with tape. Add sandpaper or rubber tape to bottle or hands only if every team struggles with grip. <b>Relay course:</b> two parallel linear courses, each with a pickup zone, handoff zones, and a drop-off zone. Robots stay stationed; only the bottle moves.</div>

  <div class="section-title">Relay format &amp; rules</div>
  {RELAY_HTML}
  <ul class="slashlist">{rules}</ul>
  <table class="tbl"><thead><tr><th>Event</th><th>Rule</th></tr></thead><tbody>{pen_rows}</tbody></table>

  <div class="section-title">Vocabulary</div>
  <div class="card vocab">{vocab}</div>

  <div class="section-title">Common failure modes</div>
  <div class="note-block">Day 2 field guide. Diagnose by asking, not fixing. These are the common failures, their likely cause, and the question to put back to the team. Treat them as a starting point, not a checklist.</div>
  <div class="fmlist">{fm_cards}</div>

  <div class="section-title">Background knowledge</div>
  <div class="bglist">{bg}</div>
  <div class="note-block" style="background:var(--teal-soft);border-left-color:var(--teal);color:var(--teal-dark);">Coach-facing refreshers. These open in a new tab and need an internet connection, unlike the rest of this guide.</div>
</section>"""


# --------------------------------------------------------------------------
# JS
# --------------------------------------------------------------------------

JS = """
const PHASES = __PHASE_IDS__;
let timer = {id:null,total:0,left:0,running:false,phase:null};

function setView(v){
  document.querySelectorAll('.view').forEach(s=>s.classList.remove('active'));
  const el = document.getElementById('view-'+v);
  if(el) el.classList.add('active');
  document.querySelectorAll('.nav button[data-view]').forEach(b=>b.classList.toggle('active',b.dataset.view===v));
  window.scrollTo({top:0,behavior:'smooth'});
}
function togglePhase(id){
  const el = document.getElementById(id);
  el.classList.toggle('open');
  if(el.classList.contains('open')) el.scrollIntoView({behavior:'smooth',block:'start'});
}
function openPhase(id){
  const el = document.getElementById(id);
  // make sure its day view is active
  const view = el.closest('.view');
  if(view) setView(view.id.replace('view-',''));
  if(!el.classList.contains('open')) el.classList.add('open');
  setTimeout(()=>el.scrollIntoView({behavior:'smooth',block:'start'}),60);
}
function prevPhase(id){const i=PHASES.indexOf(id);if(i>0)openPhase(PHASES[i-1]);}
function nextPhase(id){const i=PHASES.indexOf(id);if(i>=0&&i<PHASES.length-1)openPhase(PHASES[i+1]);}

/* timer */
function fmt(s){const m=Math.floor(Math.abs(s)/60),x=Math.abs(s)%60;return (s<0?'-':'')+m+':'+String(x).padStart(2,'0');}
function startTimer(id){
  const el=document.getElementById(id);
  const min=parseInt(el.dataset.min,10);
  timer.total=min*60;timer.left=min*60;timer.phase=el.dataset.title;timer.running=true;
  document.getElementById('timerbar').classList.add('show');
  document.querySelector('.timer-inner .ttitle').textContent=el.dataset.title;
  renderTimer();
  if(timer.id)clearInterval(timer.id);
  timer.id=setInterval(tick,1000);
  document.getElementById('tPlay').textContent='Pause';
}
function tick(){if(timer.running){timer.left--;renderTimer();}}
function renderTimer(){
  document.querySelector('.timer-inner .clock').textContent=fmt(timer.left);
  const pct=Math.max(0,Math.min(100,(1-timer.left/timer.total)*100));
  const prog=document.getElementById('tprog');
  document.querySelector('#tprog i').style.width=(timer.left<0?100:pct)+'%';
  prog.classList.toggle('over',timer.left<0);
}
function toggleTimer(){
  if(!timer.total)return;
  timer.running=!timer.running;
  document.getElementById('tPlay').textContent=timer.running?'Pause':'Resume';
  if(timer.running&&!timer.id)timer.id=setInterval(tick,1000);
}
function resetTimer(){timer.left=timer.total;timer.running=false;document.getElementById('tPlay').textContent='Resume';renderTimer();}
function closeTimer(){if(timer.id)clearInterval(timer.id);timer={id:null,total:0,left:0,running:false,phase:null};document.getElementById('timerbar').classList.remove('show');}

/* prep checklist */
function loadPrep(){
  let saved={};try{saved=JSON.parse(localStorage.getItem('hra3:prep')||'{}');}catch(e){}
  document.querySelectorAll('[data-prep]').forEach(r=>{if(saved[r.dataset.prep])r.classList.add('done');});
  updatePrep();
}
function togglePrep(i){
  const r=document.querySelector('[data-prep="'+i+'"]');r.classList.toggle('done');
  let saved={};try{saved=JSON.parse(localStorage.getItem('hra3:prep')||'{}');}catch(e){}
  if(r.classList.contains('done'))saved[i]=1;else delete saved[i];
  localStorage.setItem('hra3:prep',JSON.stringify(saved));updatePrep();
}
function updatePrep(){
  const all=document.querySelectorAll('[data-prep]').length;
  const done=document.querySelectorAll('[data-prep].done').length;
  document.getElementById('prep-count').textContent=done+' / '+all;
  document.getElementById('prep-bar').style.width=(done/all*100)+'%';
}

/* notes */
function loadNotes(){
  document.querySelectorAll('[data-note]').forEach(t=>{
    const v=localStorage.getItem('hra3:note:'+t.dataset.note);if(v)t.value=v;
    t.addEventListener('input',()=>localStorage.setItem('hra3:note:'+t.dataset.note,t.value));
  });
}

/* lightbox */
function lightbox(src){const lb=document.getElementById('lightbox');lb.querySelector('img').src=src;lb.classList.add('open');}
function closeLightbox(){document.getElementById('lightbox').classList.remove('open');}

/* keyboard */
document.addEventListener('keydown',e=>{
  if(e.target.tagName==='TEXTAREA'||e.target.tagName==='INPUT')return;
  const k=e.key.toLowerCase();
  if(k==='1')setView('day1');else if(k==='2')setView('day2');else if(k==='3')setView('day3');
  else if(k==='4')setView('reference');
  else if(k==='h')setView('home');
  else if(k==='escape'){closeLightbox();}
});

window.addEventListener('DOMContentLoaded',()=>{loadPrep();loadNotes();
  window.addEventListener('scroll',()=>{document.getElementById('topBtn').style.display=window.scrollY>500?'block':'none';});
});
"""


# --------------------------------------------------------------------------
# ASSEMBLE
# --------------------------------------------------------------------------

def build():
    phase_ids = [p["id"] for d in DAYS for p in d["phases"]]
    days_html = "".join(render_day(d) for d in DAYS)

    nav = '<button data-view="home" class="active" onclick="setView(\'home\')">Home</button>'
    nav += "".join(
        f'<button data-view="{d["id"]}" onclick="setView(\'{d["id"]}\')">Day {d["n"]}</button>'
        for d in DAYS
    )
    nav += '<button data-view="reference" onclick="setView(\'reference\')">Reference</button>'

    js = JS.replace("__PHASE_IDS__", str(phase_ids))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Hydraulic Rescue Arm &middot; TETC Teacher Guide</title>
<link rel="icon" type="image/png" href="__MARK__">
<style>{CSS}</style>
</head>
<body>
<header class="topbar">
  <div class="topbar-inner">
    <div class="brand"><img class="mark" src="__MARK__" alt="TE+TC mark"> Hydraulic Rescue Arm</div>
    <nav class="nav">{nav}</nav>
  </div>
</header>

<div class="timer-bar" id="timerbar">
  <div class="timer-inner">
    <span class="lbl">Phase timer</span>
    <span class="clock">0:00</span>
    <span class="ttitle"></span>
    <button id="tPlay" onclick="toggleTimer()">Pause</button>
    <button onclick="resetTimer()">Reset</button>
    <button onclick="closeTimer()">Close</button>
  </div>
  <div class="timer-prog" id="tprog"><i></i></div>
</div>

<main class="wrap">
{render_home()}
{days_html}
{render_reference()}
</main>

<div class="lightbox" id="lightbox" onclick="closeLightbox()"><img src="" alt="Enlarged slide"></div>

<div class="fab">
  <button class="top-btn" id="topBtn" style="display:none;" onclick="window.scrollTo({{top:0,behavior:'smooth'}})">Top</button>
</div>

<div class="footer"><img class="footlogo" src="__LOGO__" alt="ExxonMobil Foundation Teen Engineering + Tech Center"><span class="foottext">Hydraulic Rescue Arm &middot; Teacher Guide</span></div>

<script>{js}</script>
</body>
</html>"""

    # inject assets
    html = html.replace("__OUTFIT__", font_uri("outfit.woff2"))
    html = html.replace("__DMSANS__", font_uri("dmsans.woff2"))
    html = html.replace("__MARK__", logo_uri("tetc-mark.png"))
    html = html.replace("__LOGO__", logo_uri("tetc-logo.png"))
    for i in range(1, 21):
        token = "__SLIDE%02d__" % i
        if token in html:
            html = html.replace(token, slide_uri("slide%02d.jpg" % i))

    out = os.path.join(ROOT, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("Wrote", out, "(%.2f MB)" % (os.path.getsize(out) / 1048576))


if __name__ == "__main__":
    build()
