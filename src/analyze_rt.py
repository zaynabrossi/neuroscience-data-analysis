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

# Inspect + report data quality
print("Number of missing values per column:")
print("-"*35)
print(df.isna().sum())

incorrect_trials = df[df["correct"]==0]
print("Number of incorrect trials:", len(incorrect_trials))

correct_trials = df[df["correct"]==1]
print("Number of correct trials:", len(correct_trials))

total_trials = len(df)
n_correct = len(correct_trials)

accuracy_percentage = (n_correct / total_trials)*100
print("Accuracy:", round(accuracy_percentage,2), "%")

mean_correct_rt = correct_trials["rt_ms"].mean()
print(" Raw mean RT on correct trials:", round(mean_correct_rt, 2), "ms")

fast_trials = df[df["rt_ms"] < 200]
print("Number of unusually fast trials:", len(fast_trials))

slow_trials = df[df["rt_ms"] > 1000]
print("Number of unusually slow trials:", len(slow_trials))

# Preprocess trials
working_df = df.copy()

working_df["valid_rt"] = (
    (working_df["rt_ms"] >=200) &
    (working_df["rt_ms"] <=1000)
)

clean_df = working_df[working_df["valid_rt"] == True].copy()

analysis_df = working_df[
    (working_df["valid_rt"]==True) &
    (working_df["correct"]==1)
].copy()
print("Trials retained for analysis:", len(analysis_df))


# Summarize preprocessing quality
valid_trials_by_condition = working_df.groupby("condition")["valid_rt"].sum()
print(valid_trials_by_condition)

invalid_trials_by_condition = working_df.groupby("condition")["valid_rt"].apply(
    lambda x: (~x).sum())
print("Invalid trials by condition:", invalid_trials_by_condition)

valid_trials_by_participant = working_df.groupby("participant_id")["valid_rt"].sum()
print(valid_trials_by_participant)

valid_trials_by_participant_x_condition= working_df.groupby(
    ["participant_id", "condition"]
)["valid_rt"].sum()
print(valid_trials_by_participant_x_condition)

mean_rt_by_ptcp_x_cond = clean_df.groupby(
    ["participant_id", "condition"]
)["rt_ms"].mean()
print("Mean RT by participant x condition:", round(mean_rt_by_ptcp_x_cond,2), "ms")


# Report exclusions for transparency
n_original= len(working_df)
n_analysis = len(analysis_df)
n_removed = n_original - n_analysis
retention_rate = (n_analysis/n_original)*100
print("OG trials:", n_original)
print("Trials retained:", n_analysis)
print("Trials removed:", n_removed)
print("Retention rate:", round(retention_rate,2), "%")

double_exclusions = working_df[
    (working_df["valid_rt"]==False)&
    (working_df["correct"]==0)
]
print("Trials failing both criteria:", len(double_exclusions))

n_invalid_rt = len(working_df) - working_df["valid_rt"].sum()
n_incorrect = len(working_df[working_df["correct"]==0])
n_overlap = len(double_exclusions)
calculated_exclusions = (n_invalid_rt + n_incorrect) - n_overlap
print("Calculated exclusions:", calculated_exclusions)
print("Actual exclusions:", n_removed)

assert calculated_exclusions == n_removed #double-checking measure

# Check ptcp eligibility
trials_per_group = analysis_df.groupby(
    ["participant_id", "condition"]
).size()
print(trials_per_group)

trial_count_table = trials_per_group.unstack().reindex(
index=df["participant_id"].unique(),
    columns=["low", "high"]
)
print(trial_count_table)

print(trial_count_table.isna())
missing_conditions = trial_count_table.isna().sum()
print(missing_conditions)

missing_per_ptcp= trial_count_table.isna().sum(axis=1)
eligible_ptcps = missing_per_ptcp[
    missing_per_ptcp == 0
]
print(eligible_ptcps)

eligible_ids = eligible_ptcps.index
print(eligible_ids)

paired_df = analysis_df[
    analysis_df["participant_id"].isin(eligible_ids)
].copy()
print("Trials from eligible participants:", len(paired_df))

# Calculate ptcp-level cog-load effects
paired_means = paired_df.groupby(
    ["participant_id", "condition"]
)["rt_ms"].mean()
print(paired_means)

wide_paired_means = paired_means.unstack()
print(wide_paired_means)

paired_differences = wide_paired_means["high"] - wide_paired_means["low"]
print("Participant-level RT differences:")
print(paired_differences)

                                       
# Calculate + display descriptive stats
mean_rt = paired_df["rt_ms"].mean()
print("Overall mean RT:", round(mean_rt,2), "ms")

high_trials = paired_df[paired_df["condition"] == "high"]
mean_high_rt = high_trials["rt_ms"].mean()
print("Mean high-load RT:", (round(mean_high_rt,2)), "ms")

low_trials = paired_df[paired_df["condition"] == "low"]
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


# Calculate within-participant load effects
mean_load_effect = paired_differences.mean()
print("Mean within-participant load effect:", round(mean_load_effect,2), "ms")

sd_load_effect = paired_differences.std()
print("SD of load effects:", round(sd_load_effect,2), "ms")

sem_load_effect = sd_load_effect / np.sqrt(len(paired_differences))
print("SEM of load effects:", round(sem_load_effect,2), "ms")

# Manually calculate paired t-test stats
t_statistic = mean_load_effect / sem_load_effect 
print("t-statistic:", round(t_statistic, 2))

degrees_freedom = len(paired_differences) - 1
print("Degrees of freedom:", degrees_freedom)
#manual calculations for verification/learning

p_value = 2*stats.t.sf(abs(t_statistic), degrees_freedom)
print("p-value:", p_value)

# Perform paired-samples t-test using SciPy
paired_t_result = stats.ttest_rel(
    wide_paired_means["high"],
    wide_paired_means["low"]
)

#verifications
assert np.isclose(t_statistic,paired_t_result.statistic)
assert np.isclose(p_value,paired_t_result.pvalue)

print("Preprocessed paired t-test:")
print("-"*21)
print("t-statistic:", round(paired_t_result.statistic,3))
print("p-value:", round(paired_t_result.pvalue,4))
print("Degrees of freedom:", paired_t_result.df)
print("Number of participants:", len(wide_paired_means))
print("Mean cog-load effect:", round(paired_differences.mean(),2), "ms")

# Calculate effect size + 95% CI
cohens_dz= mean_load_effect / sd_load_effect
print("Cohen's dz:", round(cohens_dz,3))

t_critical = stats.t.ppf(0.975, degrees_freedom)
ci_lower = mean_load_effect - (t_critical)*sem_load_effect
ci_upper = mean_load_effect + (t_critical)*sem_load_effect
print("95% CI:", round(ci_lower,2), "to", round(ci_upper,2), "ms")

# Visualize + save results
plt.figure(figsize=(7,5))
for participant in wide_paired_means.index:
    plt.plot(
        ["low", "high"],
        [wide_paired_means.loc[participant, "low"],
         wide_paired_means.loc[participant, "high"],
        ],
        label=participant,
        marker="o",
        linewidth=2
    )

plt.title("Effect of cognitive load on reaction time")
plt.xlabel("Condition")
plt.ylabel("Reaction time (ms)")
plt.legend()
plt.tight_layout()
plt.savefig(figure_file, dpi=300)
plt.show()




