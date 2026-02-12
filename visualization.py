import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def weekly_charts_paged():
    df = pd.read_csv("count_pomodoro.csv")
    df["date"] = pd.to_datetime(df["date"])

    last_week = df[df["date"] >= df["date"].max() - pd.Timedelta(days=7)]

    # --- Prepare data ---
    daily = last_week.groupby(last_week["date"].dt.date)["pomodoros"].sum().sort_index()
    all_categories = ["study", "exam", "assignment", "reading", "other"]

    category = (
        last_week.groupby("category")["pomodoros"]
        .sum()
        .reindex(all_categories, fill_value=0)
    )

    cumulative = daily.cumsum()
    avg = daily.mean()

    # Trend line data (simple linear fit without extra libraries)
    x = list(range(len(daily)))
    y = daily.values
    if len(x) >= 2:
        slope = (y[-1] - y[0]) / (x[-1] - x[0])
        trend = [y[0] + slope * xi for xi in x]
    else:
        trend = y

    plt.ion()
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), constrained_layout=True)

    pages = 3
    page = 0

    def render_page(page_index):
        for ax in axes:
            ax.clear()

        # --- Page 1/3 ---
        if page_index == 0:
            # Chart 1: Daily bar
            axes[0].bar(daily.index.astype(str), daily.values)
            axes[0].set_title("Pomodoros Per Day")
            axes[0].set_ylabel("Pomodoros")
            axes[0].tick_params(axis="x", rotation=45)

            # Chart 2: Cumulative line
            axes[1].plot(daily.index.astype(str), cumulative.values)
            axes[1].set_title("Cumulative Productivity")
            axes[1].set_ylabel("Total Pomodoros")
            axes[1].tick_params(axis="x", rotation=45)

            fig.suptitle("Weekly Dashboard — Page 1/3 (N=Next, P=Prev, Q=Quit)")

        # --- Page 2/3 ---
        elif page_index == 1:
            # Chart 3: Category bar
            axes[0].bar(category.index, category.values)
            axes[0].set_title("Pomodoros by Category (Bar)")
            axes[0].set_ylabel("Pomodoros")
            axes[0].tick_params(axis="x", rotation=20)

            # Chart 4: Daily vs Average
            axes[1].plot(daily.index.astype(str), daily.values)
            axes[1].axhline(avg)
            axes[1].set_title("Daily Productivity vs Average")
            axes[1].set_ylabel("Pomodoros")
            axes[1].tick_params(axis="x", rotation=45)

            fig.suptitle("Weekly Dashboard — Page 2/3 (N=Next, P=Prev, Q=Quit)")

        # --- Page 3/3 ---
        else:
            # Chart 5: Trend line
            axes[0].plot(daily.index.astype(str), daily.values)
            axes[0].plot(daily.index.astype(str), trend)
            axes[0].set_title("Weekly Trend (Simple Line Fit)")
            axes[0].set_ylabel("Pomodoros")
            axes[0].tick_params(axis="x", rotation=45)

            # Pie chart
            if category.sum() > 0:
                axes[1].pie(category.values, labels=category.index, autopct="%1.1f%%")
                axes[1].set_title("Category Share (Pie)")
            else:
                axes[1].text(0.5, 0.5, "No category data", ha="center", va="center")
                axes[1].set_title("Category Share (Pie)")

            fig.suptitle("Weekly Dashboard — Page 3/3 (N=Next, P=Prev, Q=Quit)")

        fig.canvas.draw()
        fig.canvas.flush_events()

    render_page(page)

    while True:
        cmd = input("\nCharts UI: [N]ext  [P]revious  [Q]uit : ").strip().lower()
        if cmd == "n":
            page = (page + 1) % pages
            render_page(page)
        elif cmd == "p":
            page = (page - 1) % pages
            render_page(page)
        elif cmd == "q":
            break
        else:
            print("Invalid input. Use N, P, or Q.")

    plt.ioff()
    plt.close(fig)


def plot_daily_schedule(schedule):

    if not schedule:
        print("No schedule to plot.")
        return

    CATEGORY_COLORS = {
        "study": "#4C72B0",
        "exam": "#DD8452",
        "assignment": "#55A868",
        "reading": "#C44E52",
        "other": "#8172B3"
    }

    fig, ax = plt.subplots(figsize=(14, 4))

    for entry in schedule:
        start = entry["start"]
        duration = entry["end"] - entry["start"]
        category = entry.get("category", "other")
        color = CATEGORY_COLORS.get(category, "#999999")

        ax.barh(
            0,                    # single row for daily
            duration,
            left=start,
            height=0.6,
            color=color,
            edgecolor="black"
        )

        # Add label inside block
        if duration > 0.5:
            ax.text(
                start + duration / 2,
                0,
                entry["task"],
                ha="center",
                va="center",
                color="white",
                fontsize=9
            )

    ax.set_xlim(9, 22)
    ax.set_yticks([])  # hide Y axis for clean look
    ax.set_xlabel("Time")
    ax.set_title("Daily Timetable")

    ax.set_xticks(range(9, 23))
    ax.grid(axis="x", linestyle="--", alpha=0.4)

    # Legend
    legend_patches = [
        mpatches.Patch(color=color, label=cat.capitalize())
        for cat, color in CATEGORY_COLORS.items()
    ]
    ax.legend(handles=legend_patches, loc="upper right")

    plt.tight_layout()
    plt.show()

def plot_weekly_schedule(weekly_schedule):

    if not weekly_schedule:
        print("No weekly schedule to plot.")
        return

    # Professional category colors
    CATEGORY_COLORS = {
        "study": "#4C72B0",
        "exam": "#DD8452",
        "assignment": "#55A868",
        "reading": "#C44E52",
        "other": "#8172B3"
    }

    fig, ax = plt.subplots(figsize=(14, 7))

    days = sorted(weekly_schedule.keys())
    y_positions = range(len(days))

    for i, day in enumerate(days):
        for entry in weekly_schedule[day]:
            start = entry["start"]
            duration = entry["end"] - entry["start"]
            category = entry.get("category", "other")

            color = CATEGORY_COLORS.get(category, "#999999")

            ax.barh(
                i,
                duration,
                left=start,
                height=0.6,
                color=color,
                edgecolor="black"
            )

            # Task label inside bar (only if wide enough)
            if duration > 0.5:
                ax.text(
                    start + duration / 2,
                    i,
                    entry["task"],
                    ha="center",
                    va="center",
                    color="white",
                    fontsize=8
                )

    # Axis formatting
    ax.set_yticks(y_positions)
    ax.set_yticklabels(days)
    ax.set_xlim(9, 22)

    ax.set_xlabel("Time")
    ax.set_title("Weekly Timetable (Optimized Schedule)")

    # Time grid like real timetable
    ax.set_xticks(range(9, 23))
    ax.grid(axis="x", linestyle="--", alpha=0.4)

    # Legend
    legend_patches = [
        mpatches.Patch(color=color, label=cat.capitalize())
        for cat, color in CATEGORY_COLORS.items()
    ]
    ax.legend(handles=legend_patches, loc="upper right")

    plt.tight_layout()
    plt.show()