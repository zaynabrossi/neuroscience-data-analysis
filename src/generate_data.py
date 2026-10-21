import csv
import random
from pathlib import Path

"""
Generate synthetic reaction time (rt) data for a repeated-measures experiment.
Simulates low and high cognitive load conditions using predefined rt ranges and response accuracy probabilities.
All data are synthetic.
"""

project_folder = Path(__file__).resolve().parent.parent
output_file = project_folder/"data"/"synthetic_trials.csv"
output_file.parent.mkdir(parents=True, exist_ok=True)

random.seed(42)

participants = ["P001", "P002", "P003"]
conditions = ["low", "high"]
trials = []

for participant in participants:
  for condition in conditions:
      for trial_number in range (1,4):
        if condition == "low":
          reaction_time = random.randint(350,500)
          accuracy_probability = 0.95
        else:
          reaction_time = random.randint(500,700)
          accuracy_probability = 0.8
        if random.random() < accuracy_probability:
          correct = 1
        else:
          correct = 0
        trial = {
          "participant_id": participant,
          "trial": trial_number,
          "condition": condition,
          "rt_ms": reaction_time,
          "correct": correct,
        }          
        trials.append(trial)
print(f"Saved {len(trials)} synthetic trials to {output_file}")

fieldnames = ["participant_id", "trial", "condition", "rt_ms", "correct"]
with open(output_file, "w", newline="") as file:
  writer = csv.DictWriter(file, fieldnames=fieldnames)
  writer.writeheader()
  writer.writerows(trials)
