"""Generates data/complaints_v2.csv (training data) from templates. Run once.
Version 2: original templates + more varied wording, more locations, light noise."""
import csv, random
random.seed(1)
D = {
 "Water": [("Water tap is leaking continuously in the {loc}","Medium"),("No water supply in the {loc} since morning","High"),
  ("Pipe burst and water flooding near the {loc}","High"),("Drinking water in the {loc} looks dirty and tastes bad","High"),
  ("Water cooler in the {loc} is not working","Medium"),("Please install water saving taps in the {loc}","Low"),
  ("Suggest rainwater harvesting for the {loc}","Low"),("Overflowing water tank is wasting water at the {loc}","Medium")],
 "Electricity": [("Lights are left on all night in the {loc}","Medium"),("Exposed wires sparking in the {loc}","High"),
  ("Power outage in the {loc} for several hours","High"),("Fans and AC running in empty {loc}","Medium"),
  ("Please install solar panels on the {loc} roof","Low"),("Suggest replacing old bulbs with LED in the {loc}","Low"),
  ("Burning smell and short circuit from socket in the {loc}","High"),("Tube light keeps flickering in the {loc}","Medium")],
 "Waste": [("Garbage bins are overflowing in the {loc}","Medium"),("Waste not collected for many days near the {loc}","High"),
  ("Plastic waste scattered around the {loc}","Medium"),("Need separate dustbins for wet and dry waste in the {loc}","Low"),
  ("Garbage burning behind the {loc} causing smoke","High"),("Suggest a composting unit for food waste from the {loc}","Low"),
  ("Hazardous waste dumped openly near the {loc}","High"),("Request recycling bins for paper and bottles at the {loc}","Low")],
 "Cleanliness": [("Washrooms in the {loc} are very dirty and smelly","High"),("Floor of the {loc} is not cleaned regularly","Medium"),
  ("Mosquitoes breeding in stagnant water near the {loc}","High"),("Dust everywhere in the {loc}, needs cleaning","Low"),
  ("Rats and pests found in the {loc}","High"),("Request more frequent sweeping of the {loc}","Low"),
  ("Tables and benches in the {loc} are dirty","Medium"),("Soap and sanitizer missing in the {loc}","Medium")],
 "Infrastructure": [("Ceiling cracking and plaster falling in the {loc}","High"),("Broken benches and chairs in the {loc}","Medium"),
  ("Staircase railing broken in the {loc}, unsafe for students","High"),("Potholes on the road near the {loc}","Medium"),
  ("Windows not closing properly in the {loc}","Low"),("Please add ramps for accessibility at the {loc}","Low"),
  ("Door lock is broken in the {loc}","Medium"),("Paint peeling off the walls of the {loc}","Low")],
 "Green Space": [("Trees are being cut near the {loc}","High"),("Garden in the {loc} is not maintained and plants are dying","Medium"),
  ("Please plant more trees around the {loc}","Low"),("Lawn near the {loc} is not watered","Medium"),
  ("Suggest a vertical garden at the {loc}","Low"),("Weeds overgrown near the {loc}","Low"),
  ("Dangerous dry tree branch about to fall near the {loc}","High"),("Need shaded seating and greenery in the {loc}","Low")],
}
D2 = {
 "Water": [
  ("Taps are completely dry in the {loc} and students cannot even wash hands","High"),
  ("Water has been cut off to the {loc} for two days","High"),
  ("Dirty brown water is coming from the taps in the {loc}","High"),
  ("Water pipeline burst, road in front of the {loc} is flooded","High"),
  ("Tap handle in the {loc} is broken and water keeps running","Medium"),
  ("Water pressure in the {loc} is very low","Medium"),
  ("Hose pipe is left open and water is going waste near the {loc}","Medium"),
  ("The RO unit at the {loc} has stopped working","Medium"),
  ("Wash basin in the {loc} is leaking from the bottom","Medium"),
  ("It would be helpful to have a bottle refill station at the {loc}","Low"),
  ("Could we install sensor taps in the {loc} to save water","Low"),
  ("Suggestion: a rainwater tank for the {loc}","Low"),
  ("Please put up posters about saving water in the {loc}","Low")],
 "Electricity": [
  ("Burning smell from the plug point in the {loc}","High"),
  ("Loose live wires hanging from the ceiling in the {loc}, very dangerous","High"),
  ("Complete blackout in the {loc} since last night","High"),
  ("Electric shock felt while touching the switch in the {loc}","High"),
  ("Lights in the {loc} remain on even in the daytime","Medium"),
  ("Computers and projector in the {loc} are not switched off after class","Medium"),
  ("Two fans are not working in the {loc}","Medium"),
  ("Bulb in the {loc} is fused and not replaced","Medium"),
  ("AC in the {loc} is set to a very low temperature and wastes power","Medium"),
  ("Suggest using solar lamps along the path near the {loc}","Low"),
  ("Can we get timers for the lights in the {loc}","Low"),
  ("Please upgrade old tube lights in the {loc} to energy efficient ones","Low"),
  ("Recommend a power usage display at the {loc} to create awareness","Low")],
 "Waste": [
  ("Rotting food is piling up near the {loc} and attracting flies and stray dogs","High"),
  ("Garbage has not been picked up from the {loc} for over a week and it smells terrible","High"),
  ("Chemical containers from the lab are thrown in the open bin near the {loc}","High"),
  ("Sewage and garbage are mixed together outside the {loc}","High"),
  ("Wrappers and paper cups are lying all over the {loc}","Medium"),
  ("Dustbin at the {loc} has no lid and waste is spilling out","Medium"),
  ("People throw waste outside the bins at the {loc}","Medium"),
  ("No dustbin is available near the {loc}","Medium"),
  ("Leaves and trash are piled up beside the {loc}","Medium"),
  ("Can we start a recycling drive for old paper at the {loc}","Low"),
  ("Would be nice to have a compost pit for kitchen waste from the {loc}","Low"),
  ("Put up signs asking people to use dustbins at the {loc}","Low"),
  ("Suggest reusable plates instead of disposable ones at the {loc}","Low")],
 "Cleanliness": [
  ("Drain is blocked and dirty water is spreading in the {loc}","High"),
  ("Urinals and toilets near the {loc} are filthy and unusable","High"),
  ("Cockroaches and flies everywhere in the {loc}, it is unhygienic","High"),
  ("Foul smell coming from the {loc} the whole day","High"),
  ("The {loc} was not mopped today and the floor is sticky","Medium"),
  ("Desks and chairs in the {loc} are covered with dust","Medium"),
  ("Dustbins in the {loc} are not cleaned regularly","Medium"),
  ("Spit stains and marks on the walls of the {loc}","Medium"),
  ("Handwash and tissue paper are not refilled in the {loc}","Medium"),
  ("Glass doors of the {loc} look dirty and need wiping","Low"),
  ("Please clean the notice boards in the {loc} once in a while","Low"),
  ("Could the {loc} be cleaned a bit more often","Low"),
  ("Request deep cleaning of the {loc} before the event","Low")],
 "Infrastructure": [
  ("Part of the roof in the {loc} collapsed and could hurt someone","High"),
  ("Big crack in the wall of the {loc}, it looks unsafe","High"),
  ("Gate of the {loc} has come off its hinges and is dangerous","High"),
  ("Loose tiles in the {loc} are causing students to slip and fall","High"),
  ("Lift in the {loc} is out of order","Medium"),
  ("Tables in the {loc} are wobbly and some drawers are broken","Medium"),
  ("Rainwater leaks through the ceiling of the {loc}","Medium"),
  ("Projector screen in the {loc} is torn","Medium"),
  ("Some floor tiles in the {loc} are broken","Medium"),
  ("Signboards near the {loc} are faded and hard to read","Low"),
  ("It would be good to add more seating at the {loc}","Low"),
  ("The {loc} needs repainting","Low"),
  ("Please provide a bigger notice board for the {loc}","Low")],
 "Green Space": [
  ("Construction workers are clearing the plants around the {loc}","High"),
  ("Old tree near the {loc} is leaning dangerously after the storm","High"),
  ("Someone is destroying the plants around the {loc}","High"),
  ("Trees near the {loc} are being removed without any permission","High"),
  ("Flower beds near the {loc} are not being maintained","Medium"),
  ("Grass near the {loc} has dried up and turned brown","Medium"),
  ("Garden sprinklers at the {loc} are broken and plants are withering","Medium"),
  ("Saplings planted near the {loc} are dying without water","Medium"),
  ("Bushes near the {loc} have grown over the footpath","Medium"),
  ("Would love a small herb garden near the {loc}","Low"),
  ("Can we plant flowering trees along the road to the {loc}","Low"),
  ("Suggest adding benches under the trees at the {loc}","Low"),
  ("Let us have a tree plantation day around the {loc}","Low")],
}
LOCS = ["hostel","library","canteen","main block","computer lab","sports ground","parking area","admin building",
        "auditorium","workshop","seminar hall","corridor","classroom","washroom","mess","garden","staircase",
        "reading room","staff room","entrance gate"]
PRE = ["", "", "", "Sir, ", "Kindly look into this: ", "Urgent attention needed. ", "Hello, ", "Request: "]
SUF = ["", "", "", "", ". Please fix it soon", ". This has been going on for a week", ". Students are facing a lot of trouble", ". Kindly take action"]

def make(tpl, n):
    out = []
    for loc in random.sample(LOCS, n):
        s = random.choice(PRE) + tpl.format(loc=loc) + random.choice(SUF)
        out.append(s.lower() if random.random() < 0.15 else s)
    return out

rows = set()
for src, n in ((D, 4), (D2, 5)):
    for cat, items in src.items():
        for tpl, pri in items:
            for s in make(tpl, n):
                rows.add((s, cat, pri))
rows = sorted(rows); random.shuffle(rows)

# safety check: no test sentence may appear in the training data
import os
test_texts = set()
for fn in ("data/test_set.csv", "data/test_set_2.csv"):
    if os.path.exists(fn):
        test_texts |= {r["text"].lower() for r in csv.DictReader(open(fn))}
leaks = [r for r in rows if r[0].lower() in test_texts]
print("Overlap with test sets:", len(leaks))

with open("data/complaints_v2.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["text","category","priority"]); w.writerows(rows)
print(len(rows), "rows written")
