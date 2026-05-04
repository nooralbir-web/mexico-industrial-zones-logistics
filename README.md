# mexico-industrial-zones-logistics

This repository contains replication and analysis code for **"Industrial Park Location and Logistics Access in Mexico."**

The project constructs a cross-sectional dataset of selected Mexican industrial parks and evaluates their proximity to two key logistics nodes:

* The United States border
* The Port of Ensenada

Using geodesic distances, the analysis builds a normalized **logistics efficiency score** to compare locations.

---

## Data

The dataset includes industrial parks across:

* Baja California (Tijuana, Mexicali)
* Chihuahua (Ciudad Juárez)
* Nuevo León (Monterrey / Apodaca)
* Querétaro
* Guanajuato (Silao / Puerto Interior)

Each observation contains:

* Latitude and longitude
* Distance to U.S. border (km)
* Distance to Ensenada port (km)
* Composite logistics score

---

## Methodology

Distances are computed using great-circle (geodesic) distance.

A normalized logistics score is defined as:

[
Score_i = 0.7(1 - d^{B}_i) + 0.3(1 - d^{P}_i)
]

where:

* ( d^{B}_i ) = normalized distance to the U.S. border
* ( d^{P}_i ) = normalized distance to the Port of Ensenada

Higher values indicate stronger combined logistics access.

---

## Outputs

The script generates:

* `outputs/logistics_ranking.csv` — ranked industrial parks
* `outputs/descriptive_table.csv` — cleaned summary table
* `outputs/logistics_score_bar.png` — visualization of rankings

---

## Key Findings

* Border regions (Tijuana, Mexicali) rank highest due to proximity to U.S. markets
* Interior regions (Querétaro, Guanajuato) rank lower but may benefit from domestic and cluster effects
* Results highlight a clear north-to-interior logistics gradient

---

## Usage

Run the analysis:

```bash
python analysis.py
```

---

## Notes

This is a simplified, first-pass framework:

* Industrial parks are treated as point locations
* Only two logistics nodes are considered
* Results are descriptive, not causal

---

## License

MIT License
