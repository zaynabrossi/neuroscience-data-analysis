import csv
import random
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
print(len(trials))
print(trials[0])
print(trials[3])
print(trials[6])
      
fieldnames = ["participant_id", "trial", "condition", "rt_ms", "correct"]
with open("data/synthetic_trials.csv", "w", newline="") as file:
  writer = csv.DictWriter(file, fieldnames=fieldnames)
  writer.writeheader()
  writer.writerows(trials)
