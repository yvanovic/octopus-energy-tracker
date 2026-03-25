import matplotlib.pyplot as plt

from consumption import daily_data

# Aggregate by date
daily_summary = (
    daily_data.groupby("date")
    .agg(
        {
            "consumption": "sum",
            "cost_new": "sum",
            "cost_flat": "sum",
            "savings": "sum",
        }
    )
    .reset_index()
)

# Calculate totals
total_consumption = daily_data["consumption"].sum()
total_cost_new = daily_data["cost_new"].sum()
total_cost_flat = daily_data["cost_flat"].sum()
total_savings = daily_data["savings"].sum()

# Create figure with 3 subplots for weekly data
fig, axes = plt.subplots(1, 3, figsize=(16, 6))
fig.suptitle(
    "Weekly Energy Consumption & Cost Analysis (Last 7 Days)",
    fontsize=16,
    fontweight="bold",
)

# Convert date to string for better labels
daily_summary["date_str"] = daily_summary["date"].astype(str)

# ============ Subplot 1: Daily Consumption ============
ax1 = axes[0]
ax1.bar(
    daily_summary["date_str"],
    daily_summary["consumption"],
    color="#3498db",
    edgecolor="black",
    linewidth=0.5,
)
ax1.set_xlabel("Date", fontweight="bold")
ax1.set_ylabel("Consumption (kWh)", fontweight="bold")
ax1.set_title("Daily Consumption")
ax1.tick_params(axis="x", rotation=45)
ax1.grid(axis="y", alpha=0.3)

# ============ Subplot 2: Daily Cost Comparison ============
ax2 = axes[1]
x = range(len(daily_summary))
width = 0.35
ax2.bar(
    [i - width / 2 for i in x],
    daily_summary["cost_new"],
    width,
    label="Octopus Cosy Tariff",
    color="#2ecc71",
    edgecolor="black",
    linewidth=0.5,
)
ax2.bar(
    [i + width / 2 for i in x],
    daily_summary["cost_flat"],
    width,
    label="Flat Rate (28.43p)",
    color="#95a5a6",
    edgecolor="black",
    linewidth=0.5,
)
ax2.set_xlabel("Date", fontweight="bold")
ax2.set_ylabel("Cost (£)", fontweight="bold")
ax2.set_title("Daily Cost: Octopus vs Flat Rate")
ax2.set_xticks(x)
ax2.set_xticklabels(daily_summary["date_str"], rotation=45)
ax2.legend()
ax2.grid(axis="y", alpha=0.3)

# ============ Subplot 3: Daily Savings ============
ax3 = axes[2]
colors = ["#2ecc71" if s > 0 else "#e74c3c" for s in daily_summary["savings"]]
ax3.bar(
    daily_summary["date_str"],
    daily_summary["savings"],
    color=colors,
    edgecolor="black",
    linewidth=0.5,
)
ax3.axhline(y=0, color="black", linestyle="-", linewidth=0.8)
ax3.set_xlabel("Date", fontweight="bold")
ax3.set_ylabel("Savings (£)", fontweight="bold")
ax3.set_title("Daily Savings vs Flat Rate")
ax3.tick_params(axis="x", rotation=45)
ax3.grid(axis="y", alpha=0.3)

plt.tight_layout()

# Print summary statistics
print("\n" + "=" * 60)
print("WEEKLY ENERGY SUMMARY (Last 7 Days)")
print("=" * 60)
print(f"Total Consumption:     {total_consumption:.2f} kWh")
print(f"Average Daily:         {total_consumption/len(daily_summary):.2f} kWh")
print(f"Octopus Total Cost:    £{total_cost_new:.2f}")
print(f"Flat Rate Total Cost:  £{total_cost_flat:.2f}")
print(
    f"Total Savings:         £{total_savings:.2f} ({(total_savings/total_cost_flat*100):.1f}%)"
)
print("=" * 60)

# Daily breakdown
print("\nDAILY BREAKDOWN:")
print("-" * 60)
print(
    f"{'Date':<12} {'Consumption':>12} {'Octopus':>12} {'Flat Rate':>12} {'Savings':>12}"
)
print("-" * 60)
for _, row in daily_summary.iterrows():
    print(
        f"{row['date_str']:<12} {row['consumption']:>11.2f}kWh £{row['cost_new']:>10.2f} £{row['cost_flat']:>10.2f} £{row['savings']:>10.2f}"
    )
print("=" * 60 + "\n")

# Breakdown by tariff period
print("TARIFF PERIOD BREAKDOWN (Entire Week):")
print("-" * 60)
for period in daily_data["period"].unique():
    period_data = daily_data[daily_data["period"] == period]
    consumption = period_data["consumption"].sum()
    cost_octopus = period_data["cost_new"].sum()
    cost_flat = period_data["cost_flat"].sum()
    print(
        f"{period:25} | {consumption:7.2f} kWh | £{cost_octopus:7.2f} vs £{cost_flat:7.2f}"
    )

print("=" * 60 + "\n")
print("📊 Visualization displayed. Close the window to exit.")
print("=" * 60 + "\n")

plt.show(block=True)
