import random
random.seed(42)

conditions = ["low", "high"]
trials = []

for condition in conditions:
  for trial_number in range (1,4):
    trial = {
      "participant_id": "P002",
      "trial": trial_number,
      "condition": condition,
      "rt_ms": random.randint(400,600),
      "correct": 1,
    }
    trials.append(trial)
print(trials)
      

