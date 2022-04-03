import numpy as np
import pandas as pd

TILES = (
    pd.read_csv(
        "tiles.txt",
        sep=";",
        header=None,
        names=[
            "id",
            "idFamily",
            "idInFamily",
            "idColor",
            "type",
            "name",
            "price",
            "mortgagePrice",
            "house_0",
            "house_1",
            "house_2",
            "house_3",
            "house_4",
            "house_5",
            "housePrice",
        ],
    )
    .fillna("-1")
    .apply(pd.to_numeric, errors="ignore", downcast="integer")
)
SETS = list(TILES[TILES["idFamily"] >= 0].groupby("idFamily").groups.values())
states = np.zeros((10, 4, 3), dtype=int)
states[:, :, 0] = -1  # Give all properties to the bank


def get_state(case):
    res = states[case["idFamily"], case["idInFamily"]]
    is_family = bool(
        np.where(
            (
                np.amax(states[case["idFamily"], : len(SETS[case["idFamily"]]), 0])
                == np.amin(states[case["idFamily"], : len(SETS[case["idFamily"]]), 0])
            )
            & all(states[case["idFamily"], : len(SETS[case["idFamily"]]), 1] == 0)
        )[0].size
    )
    return {
        "owned": res[0],
        "mortgaged": res[1],
        "built": res[2],
        "isFamily": is_family,
    }
