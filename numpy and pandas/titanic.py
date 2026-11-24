import os
import sys

import numpy as np
import pandas as pd

base = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(base, "train.csv")

if not os.path.exists(path):
    print(f"error: {path} not found")
    sys.exit()

df = pd.read_csv(path)
shape0 = df.shape

print("=" * 40)
print("part 2. loading and first look")
print("=" * 40)

try:
    n = int(input("rows to show (n): "))
except ValueError:
    n = 5
    print("error: incorrect input, n = 5")

print(f"\nfirst {n} rows:")
print(df.head(n))

print("\nlast 3 rows:")
print(df.tail(3))

print(f"\nshape (rows, cols): {df.shape}")
print(f"\ncolumns: {list(df.columns)}")

print("\ndtypes:")
print(df.dtypes)

num = ["Age", "Fare", "SibSp", "Parch"]
cat = ["Pclass", "Sex", "Embarked", "Survived", "Cabin"]
print(f"\nnumeric: {num}")
print(f"categorical: {cat} (Pclass and Survived are ints, but they are labels)")

print("\nnumeric stats:")
print(df[num].agg(["mean", "median", "min", "max", "std"]).round(2))

print("\npassengers per class:")
print(df["Pclass"].value_counts().sort_index())

print(f"\nunique ports: {df['Embarked'].nunique()} {sorted(df['Embarked'].dropna().unique())}")


print("\n" + "=" * 40)
print("part 3. missing values")
print("=" * 40)

miss = df.isnull().sum()
print("\nmissing per column:")
print(pd.DataFrame({"missing": miss, "percent": (miss / len(df) * 100).round(2)}))
print(f"\nworst column: {miss.idxmax()}")

st = ["mean", "median", "min", "max", "std", "count"]
a0 = df["Age"].agg(st)
k = int(df["Age"].isnull().sum())

df["Age"] = df["Age"].fillna(df["Age"].median())
a1 = df["Age"].agg(st)

print(f"\nage filled with median, rows filled: {k}")
print(pd.DataFrame({"before": a0, "after": a1}).round(2))

# fare has gaps too: use the median of the same class
f0 = int(df["Fare"].isnull().sum())
df["Fare"] = df["Fare"].fillna(df.groupby("Pclass")["Fare"].transform("median"))
print(f"\nfare filled with class median, rows filled: {f0}")

r0 = len(df)
df = df.dropna(subset=["Embarked"])
print(f"rows dropped because of empty port: {r0 - len(df)}")

cp = df["Cabin"].isnull().mean() * 100
df["HasCabin"] = df["Cabin"].notnull().astype(int)
if cp > 50:
    df = df.drop(columns="Cabin")
    print(f"cabin dropped ({cp:.2f}% empty), flag HasCabin added")

print(f"\nmissing left: {df.isnull().sum().sum()}")
print(f"shape before: {shape0}, after: {df.shape}")


print("\n" + "=" * 40)
print("part 4. numpy")
print("=" * 40)

s = df["Survived"].to_numpy()
sx = df["Sex"].to_numpy()
ag = df["Age"].to_numpy()
fr = df["Fare"].to_numpy()
pc = df["Pclass"].to_numpy()

print(f"\nsurvival rate: {np.mean(s) * 100:.2f}%")

for g in ("male", "female"):
    mk = sx == g
    print(f"{g}: n={mk.sum()}, survived {np.mean(s[mk]) * 100:.2f}%, mean age {np.mean(ag[mk]):.2f}")

print("\nmean age by sex and outcome:")
for g in ("male", "female"):
    for v, w in ((1, "survived"), (0, "died")):
        mk = (sx == g) & (s == v)
        r = f"{np.mean(ag[mk]):.2f}" if mk.any() else "n/a"
        print(f"{g} {w}: {r} (n={mk.sum()})")

print(f"\nfare min/max/mean/median: {np.min(fr):.2f} / {np.max(fr):.2f} / {np.mean(fr):.2f} / {np.median(fr):.2f}")
print(f"fare quartiles: {np.percentile(fr, [25, 50, 75])}")
print(f"age std (ddof=0): {np.std(ag):.2f}, (ddof=1): {np.std(ag, ddof=1):.2f}")

z = (ag - np.mean(ag)) / np.std(ag)
print(f"age outliers (|z| > 2.5): {np.sum(np.abs(z) > 2.5)}")

cnt, edges = np.histogram(ag, bins=[0, 12, 18, 30, 50, 100])
for c, a, b in zip(cnt, edges[:-1], edges[1:]):
    print(f"age {a:.0f}-{b:.0f}: {c}")

print(f"corr(pclass, fare): {np.corrcoef(pc, fr)[0, 1]:.2f}")


print("\n" + "=" * 40)
print("part 5. filtering")
print("=" * 40)

cols = ["Name", "Sex", "Age", "Pclass", "Fare"]

f1 = df[(df["Sex"] == "female") & (df["Pclass"] <= 2) & (df["Age"] < 40)]
print(f"\n1) women, class 1-2, under 40 (AND): {len(f1)}")
print(f1[cols].head(5))

a = df["Age"] < 12
b = df["SibSp"] + df["Parch"] >= 3
print(f"\n2) under 12: {a.sum()}, family of 4+: {b.sum()}")
print(f"   both (AND): {(a & b).sum()}, any of them (OR): {(a | b).sum()}")

f3 = df[df["Fare"] > df.groupby("Pclass")["Fare"].transform("mean")]
print(f"\n3) fare above the mean of own class: {len(f3)}")

f4 = df[df["Embarked"].isin(["C", "Q"]) & df["Age"].between(25, 45)]
print(f"\n4) port C or Q, age 25-45: {len(f4)}")

f5 = df[df["Name"].str.contains("Master|Rev", regex=True)]
print(f"\n5) title Master or Rev: {len(f5)}")
print(f5[cols].head(5))


print("\n" + "=" * 40)
print("part 6. groupby")
print("=" * 40)

g1 = df.groupby(["Pclass", "Sex"]).agg(
    count=("PassengerId", "count"),
    mean_age=("Age", "mean"),
    survived_pct=("Survived", "mean"),
    mean_fare=("Fare", "mean"),
)
g1["survived_pct"] = g1["survived_pct"] * 100
g1 = g1.round(2)
print("\nby class and sex:")
print(g1)

g2 = df.groupby("Embarked").agg(
    count=("PassengerId", "count"),
    survived_pct=("Survived", "mean"),
    median_fare=("Fare", "median"),
)
g2["survived_pct"] = (g2["survived_pct"] * 100).round(2)
print("\nby port:")
print(g2)

df["age_group"] = pd.cut(
    df["Age"],
    [0, 12, 18, 35, 60, 120],
    labels=["child", "teen", "young", "adult", "senior"],
)
g3 = df.groupby("age_group", observed=True)["Survived"].agg(["count", "mean"])
g3["mean"] = (g3["mean"] * 100).round(2)
print("\nby age group (mean = survived %):")
print(g3)

df["alone"] = np.where(df["SibSp"] + df["Parch"] == 0, "alone", "with family")
print("\nalone vs with family (survived %):")
print((df.groupby("alone")["Survived"].mean() * 100).round(2))

sc = df.groupby("Pclass")["Survived"].mean() * 100
print(f"\nbest class: {sc.idxmax()} ({sc.max():.2f}%)")

print("\npivot, survival rate:")
print(pd.pivot_table(df, values="Survived", index="Pclass", columns="Sex", aggfunc="mean").round(2))


print("\n" + "=" * 40)
print("part 7. saving")
print("=" * 40)

out1 = os.path.join(base, "clean.csv")
out2 = os.path.join(base, "stats.csv")
df.to_csv(out1, index=False)
g1.to_csv(out2)
print("\nsaved: clean.csv, stats.csv")

chk = pd.read_csv(out1)
print(f"reloaded shape: {chk.shape}, same as df: {chk.shape == df.shape}")
print(f"same columns: {list(chk.columns) == list(df.columns)}")
