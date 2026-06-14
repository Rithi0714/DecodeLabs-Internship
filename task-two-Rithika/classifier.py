
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


dataset = load_iris()

X = dataset.data    # features - the 4 measurements
y = dataset.target  # labels - which species (0, 1 or 2)

df = pd.DataFrame(X, columns=dataset.feature_names)
df['species'] = [dataset.target_names[i] for i in y]

print("Iris Dataset - Basic Info")
print(f"Total flowers in dataset : {X.shape[0]}")
print(f"Number of features       : {X.shape[1]}")
print(f"Species in dataset       : {list(dataset.target_names)}")

print("\nFirst 5 rows of the dataset:")
print(df.head())

print("\nHow many flowers per species:")
print(df['species'].value_counts())


X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print(f"\nTraining set size : {X_train.shape[0]} flowers")
print(f"Testing set size  : {X_test.shape[0]} flowers")

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

print("\nModel trained successfully!")
print("Algorithm used : K-Nearest Neighbors (K=5)")


predictions = knn.predict(X_test)
acc = accuracy_score(y_test, predictions)

print(f"\nModel Accuracy : {acc * 100:.2f}%")


print("\nClassification Report:")
print(classification_report(y_test, predictions, target_names=dataset.target_names))


cm = confusion_matrix(y_test, predictions)
cm_df = pd.DataFrame(
    cm,
    index=[f"Actual {n}" for n in dataset.target_names],
    columns=[f"Predicted {n}" for n in dataset.target_names]
)

print("Confusion Matrix:")
print(cm_df)
print("\nNote: diagonal = correct, off-diagonal = wrong predictions")


print("\nTry it yourself")
print("Enter flower measurements to predict species")
print("(type quit at any point to exit)\n")

while True:

    try:
        s_len = input("Sepal Length in cm (example: 5.1) : ").strip()
        if s_len.lower() == 'quit':
            break

        s_wid = input("Sepal Width in cm  (example: 3.5) : ").strip()
        if s_wid.lower() == 'quit':
            break

        p_len = input("Petal Length in cm (example: 1.4) : ").strip()
        if p_len.lower() == 'quit':
            break

        p_wid = input("Petal Width in cm  (example: 0.2) : ").strip()
        if p_wid.lower() == 'quit':
            break

        flower = np.array([float(s_len), float(s_wid),
                           float(p_len), float(p_wid)]).reshape(1, -1)

        
        flower_scaled = sc.transform(flower)

        result = knn.predict(flower_scaled)
        species_name = dataset.target_names[result[0]]

        confidence = knn.predict_proba(flower_scaled)[0]

        print(f"\nPredicted Species : {species_name.upper()}")
        print("Confidence breakdown:")
        for name, score in zip(dataset.target_names, confidence):
            bar = "█" * int(score * 20)
            print(f"  {name:<14}: {bar} {score * 100:.1f}%")

    except ValueError:
        print("Please enter numbers only, try again.")
        continue

    except (KeyboardInterrupt, EOFError):
        break

    choice = input("\nClassify another flower? (yes / quit) : ").strip().lower()
    if choice != 'yes':
        break

print("\nDone! Thanks for using the Iris Classifier.")