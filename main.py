reaction_times = [420,385,510,460,395]
print(reaction_times)
mean_rt = sum(reaction_times) / len(reaction_times)
print(mean_rt)

fastest_rt = min(reaction_times)
print(fastest_rt)
slowest_rt = max(reaction_times)
print(slowest_rt)

low_load = [420, 385, 510, 460, 395]
print(low_load)
high_load = [550, 610, 485, 590, 625]
print(high_load)
mean_low = sum(low_load) / len(low_load)
print(mean_low)
mean_high = sum(high_load) / len(high_load)
print(mean_high)
mean_diff = (mean_high) - (mean_low)
print(mean_diff)

if mean_high > mean_low:
  print("High load produced slower reponses.")
elif mean_low > mean_high:
  print("Low load produced slower responses.")
else: 
  print("Both conditions had equal mean reaction times.")

for rt in reaction_times:
  print(rt*2)

doubled_rt = []
for rt in reaction_times:
  doubled_rt.append(rt*2)
print(doubled_rt)

slow_trials = []
for rt in reaction_times:
  if rt > 400:
    slow_trials.append(rt)
print(slow_trials)

if len(slow_trials) >= 1:
  mean_slow = sum(slow_trials) / len(slow_trials)
  print(mean_slow)
else:
  print("No slow trials found.")

reaction_times_with_errors = [420, 385, -1, 0, 460, 395]
valid_trials = []
for rt in reaction_times_with_errors:
  if rt > 0:
    valid_trials.append(rt)

excluded_count = len(reaction_times_with_errors) - len(valid_trials)
print(excluded_count)
exclusion_rate = (excluded_count / len(reaction_times_with_errors)) * 100
print(round(exclusion_rate, 2))

if len(valid_trials) >= 1:
  mean_valid = sum(valid_trials) / len(valid_trials)
  print(mean_valid)
else:
  print("No valid trials available.")

def calculate_mean(reaction_times):
  if len(reaction_times) >= 1:
    return sum(reaction_times) / len(reaction_times)
  else:
    return None


participant_1 = [420,385,510,460,395]
mean_1 = calculate_mean(participant_1)
print(mean_1)
participant_2 = [500, 550, 600, 450, 400]
mean_2 = calculate_mean(participant_2)
print(mean_2)

participant_3 = [420,385,510]
participant_4 = [500,550,600]
participant_5 = [390,410,430]
participant_6 = []
participants = [participant_3,participant_4,participant_5,participant_6]

for ptcp in participants:
  mean_rt_ptcp = calculate_mean(ptcp)
  print(mean_rt_ptcp)

participant_means = []
for ptcp in participants:
  mean_rt_ptcp = calculate_mean(ptcp)
  if mean_rt_ptcp is not None:
    participant_means.append(mean_rt_ptcp)
print(participant_means)

grand_mean = calculate_mean(participant_means)
print(grand_mean)




