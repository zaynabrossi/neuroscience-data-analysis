from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

project_folder = Path(__file__).resolve().parent.parent
csv_file = project_folder/"data"/"synthetic_trials.csv"

figures_folder = project_folder/"figures"
figures_folder.mkdir(parents=True, exist_ok=True)
figure_file = figures_folder/"paired_rt_plot.png"

# Load synthetic data        
df = pd.read_csv(csv_file)

# Calculate + display descriptive stats
mean_rt = df["rt_ms"].mean()
print("Overall mean RT:", round(mean_rt,2), "ms")

mean_accuracy = df["correct"].mean()

accuracy_percent = mean_accuracy * 100
print("Overall accuracy:", round(accuracy_percent,2), "%")

high_trials = df[df["condition"] == "high"]
mean_high_rt = high_trials["rt_ms"].mean()
print("Mean high-load RT:", (round(mean_high_rt,2)), "ms")

low_trials = df[df["condition"] == "low"]
mean_low_rt = low_trials["rt_ms"].mean()
print("Mean low-load RT:", round(mean_low_rt,2), "ms")

overall_rt_difference = mean_high_rt - mean_low_rt
print("Overall RT difference:", round(overall_rt_difference,2), "ms")
if overall_rt_difference > 0:
    print("High cog load produced slower responses.")
elif overall_rt_difference < 0:
    print("High cog load produced faster responses.")
else:
    print("No diff in mean reaction time.")

mean_accuracy_by_condition = df.groupby("condition")["correct"].mean()
print(mean_accuracy_by_condition)

# Calculate participant-level rt's
participant_means = df.groupby(["participant_id", "condition"])["rt_ms"].mean().reset_index()


participant_means = participant_means.rename(columns={"rt_ms": "mean_rt_ms"})
print(participant_means)

wide_means = participant_means.pivot(
    index="participant_id",
    columns = "condition",
    values= "mean_rt_ms"
)
print(wide_means)

# Calculate within-participant load effects
participant_rt_difference = wide_means["high"] - wide_means["low"]
wide_means["rt_difference"] = participant_rt_difference
print(wide_means)

mean_load_effect = participant_rt_difference.mean()
print("Mean within-participant load effect:", round(mean_load_effect,2), "ms")

sd_load_effect = participant_rt_difference.std()
print("SD of load effects:", round(sd_load_effect,2), "ms")

sem_load_effect = sd_load_effect / np.sqrt(len(participant_rt_difference))
print("SEM of load effects:", round(sem_load_effect,2), "ms")

# Perform + print paired-sample t-test data
t_statistic = mean_load_effect / sem_load_effect 
print("t-statistic:", round(t_statistic, 2))

degrees_freedom = len(participant_rt_difference) - 1
print("Degrees of freedom:", degrees_freedom)
#manual calculations for verification/learning

p_value = 2*stats.t.sf(abs(t_statistic), degrees_freedom)
print("p-value:", p_value)

t_test_result = stats.ttest_rel(
    wide_means["high"],
    wide_means["low"]
)
print("Paired t-test results")
print("-"*21)
print("t-statistic:", round(t_test_result.statistic, 2))
print("p-value:", round(t_test_result.pvalue, 3))
print("Degrees of freedom:", t_test_result.df)

# Visualize + save results
for participant in wide_means.index:
    plt.plot(
        ["low", "high"],
        [wide_means.loc[participant, "low"],
         wide_means.loc[participant, "high"],
        ],
        label=participant,
        marker="o",
        linewidth=2
    )

plt.title("Effect of cognitive load on reaction time")
plt.xlabel("Condition")
plt.ylabel("Reaction time (ms)")
plt.legend()
plt.savefig(figure_file, dpi=300)
plt.show()



