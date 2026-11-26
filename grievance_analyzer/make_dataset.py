"""Generates data/complaints.csv (training data) from templates. Run once.
Version 1: 48 templates x 4 random locations = 192 labelled complaints."""
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
LOCS = ["hostel","library","canteen","main block","computer lab","sports ground","parking area","admin building","auditorium","workshop"]
PRE = ["", "", "Sir, ", "Kindly look into this: ", "Urgent attention needed. "]
rows = []
for cat, items in D.items():
    for tpl, pri in items:
        for loc in random.sample(LOCS, 4):
            rows.append((random.choice(PRE) + tpl.format(loc=loc), cat, pri))
random.shuffle(rows)
with open("data/complaints.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["text","category","priority"]); w.writerows(rows)
print(len(rows), "rows written")
