import pandas as pd
from geopy.distance import geodesic
import matplotlib.pyplot as plt


# -----------------------------
# Configuration
# -----------------------------

INPUT_FILE = "data/zones.csv"
OUTPUT_DATA = "data/zones_with_distances.csv"
OUTPUT_RANKING = "outputs/logistics_ranking.csv"
OUTPUT_SUMMARY = "outputs/summary_distances.csv"
OUTPUT_TABLE = "outputs/descriptive_table.csv"
OUTPUT_FIGURE = "outputs/logistics_score_bar.png"

US_BORDER = (32.5449, -117.0296)      # Approx. San Ysidro / Tijuana crossing
ENSENADA_PORT = (31.8500, -116.6333) # Approx. Port of Ensenada

BORDER_WEIGHT = 0.7
PORT_WEIGHT = 0.3


# -----------------------------
# Helper functions
# -----------------------------

def distance_km(lat, lon, target):
    """Compute geodesic distance in kilometers."""
    return geodesic((lat, lon), target).km


def min_max_normalize(series):
    """Min-max normalize a pandas Series."""
    return (series - series.min()) / (series.max() - series.min())


# -----------------------------
# Main analysis
# -----------------------------

def main():
    zones = pd.read_csv(INPUT_FILE)

    # Compute distances
    zones["dist_to_us_border_km"] = zones.apply(
        lambda row: distance_km(row["latitude"], row["longitude"], US_BORDER),
        axis=1,
    )

    zones["dist_to_ensenada_port_km"] = zones.apply(
        lambda row: distance_km(row["latitude"], row["longitude"], ENSENADA_PORT),
        axis=1,
    )

    # Normalize distances
    zones["border_norm"] = min_max_normalize(zones["dist_to_us_border_km"])
    zones["port_norm"] = min_max_normalize(zones["dist_to_ensenada_port_km"])

    # Convert lower distance into higher score
    zones["border_score"] = 1 - zones["border_norm"]
    zones["port_score"] = 1 - zones["port_norm"]

    # Composite logistics score
    zones["logistics_score"] = (
        BORDER_WEIGHT * zones["border_score"]
        + PORT_WEIGHT * zones["port_score"]
    )

    zones["closer_to_border_than_port"] = (
        zones["dist_to_us_border_km"] < zones["dist_to_ensenada_port_km"]
    )

    # Sort by score
    zones = zones.sort_values("logistics_score", ascending=False)

    # Save full processed data
    zones.to_csv(OUTPUT_DATA, index=False)

    # Save ranking table
    ranking = zones[
        [
            "zone_name",
            "city",
            "state",
            "dist_to_us_border_km",
            "dist_to_ensenada_port_km",
            "logistics_score",
        ]
    ].copy()

    ranking["dist_to_us_border_km"] = ranking["dist_to_us_border_km"].round(1)
    ranking["dist_to_ensenada_port_km"] = ranking["dist_to_ensenada_port_km"].round(1)
    ranking["logistics_score"] = ranking["logistics_score"].round(3)

    ranking.to_csv(OUTPUT_RANKING, index=False)

    # Save descriptive table
    descriptive = zones[
        [
            "zone_name",
            "city",
            "state",
            "dist_to_us_border_km",
            "dist_to_ensenada_port_km",
            "closer_to_border_than_port",
        ]
    ].copy()

    descriptive["dist_to_us_border_km"] = descriptive["dist_to_us_border_km"].round(1)
    descriptive["dist_to_ensenada_port_km"] = descriptive[
        "dist_to_ensenada_port_km"
    ].round(1)

    descriptive.to_csv(OUTPUT_TABLE, index=False)

    # Save summary statistics
    summary = zones[
        ["dist_to_us_border_km", "dist_to_ensenada_port_km", "logistics_score"]
    ].describe()

    summary.to_csv(OUTPUT_SUMMARY)

    # Visualization
    plot_df = ranking.sort_values("logistics_score", ascending=True).copy()

    plot_df["short_name"] = (
        plot_df["zone_name"]
        .str.replace(" Industrial Park", "", regex=False)
        .str.replace("Puerto Interior ", "", regex=False)
    )

    plt.figure(figsize=(10, 7))
    plt.barh(plot_df["short_name"], plot_df["logistics_score"])

    plt.xlabel("Logistics Score (Higher = Better)")
    plt.ylabel("Industrial Park")
    plt.title("Industrial Parks Ranked by Logistics Efficiency")
    plt.grid(axis="x", linewidth=0.4, alpha=0.5)
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURE, dpi=300)
    plt.close()

    print("Analysis complete.")
    print(f"Processed data saved to: {OUTPUT_DATA}")
    print(f"Ranking table saved to: {OUTPUT_RANKING}")
    print(f"Figure saved to: {OUTPUT_FIGURE}")


if __name__ == "__main__":
    main()