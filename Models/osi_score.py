import numpy as np

def compute_osi(nail_mask, fungi_mask):
    nail_mask = (nail_mask > 128).astype(np.uint8)
    fungi_mask = (fungi_mask > 128).astype(np.uint8)

    ys, xs = np.where(nail_mask > 0)
    if len(ys) == 0 or len(xs) == 0:
        return 0, "No nail detected", (0, 0, 0, 0)

    y_min, y_max = ys.min(), ys.max()
    x_min, x_max = xs.min(), xs.max()

    nail_roi = nail_mask[y_min:y_max, x_min:x_max]
    fungi_roi = fungi_mask[y_min:y_max, x_min:x_max]
    h, w = nail_roi.shape

    rows, cols = 4, 5
    step_y, step_x = h // rows, w // cols
    affected = sum(
        (fungi_roi[i*step_y:(i+1)*step_y, j*step_x:(j+1)*step_x].sum() > 0)
        for i in range(rows) for j in range(cols)
    )

    area_percent = affected / (rows * cols) * 100
    area_score = 0 if area_percent == 0 else \
                 1 if area_percent <= 10 else \
                 2 if area_percent <= 25 else \
                 3 if area_percent <= 50 else \
                 4 if area_percent <= 75 else 5

    infected_y = np.where(fungi_roi > 0)[0]
    if len(infected_y) > 0:
        top = infected_y.min()
        frac = 1 - top / h
        prox = 1 if frac <= 0.25 else 2 if frac <= 0.5 else \
               3 if frac <= 0.75 else 4 if frac < 1 else 5
    else:
        prox = 1

    osi = area_score * prox
    # If no fungi detected (area_score = 0), it's a healthy nail
    if area_score == 0:
        severity = "N/A"
    else:
        severity = "Mild" if osi <= 5 else "Moderate" if osi <= 15 else "Severe"
    return osi, severity, (x_min, y_min, x_max, y_max)
