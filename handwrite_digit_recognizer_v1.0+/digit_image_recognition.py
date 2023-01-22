import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsClassifier


class DigitImageRecognition:
    def __init__(self) -> None:
        self.digits = load_digits()

    def find_optimal_k(self) -> None:
        # random state makes it consistent, which is not so useful
        # but in this case, it is fine because it is only for finding k
        X_train, X_test, y_train, y_test = train_test_split(
            self.digits.data, self.digits.target, test_size=0.25,
            random_state=42
        )

        # k=1 can be ignored since it tends to follow training data
        ks = np.arange(2, 10)
        scores = []
        for k in ks:
            model = KNeighborsClassifier(n_neighbors=k)
            score = cross_val_score(model, X_train, y_train, cv=5)
            score.mean()
            scores.append(score.mean())

        plt.plot(ks, scores)
        plt.xlabel('k')
        plt.ylabel('accuracy')
        plt.show()

    def create_model(self):
        model = KNeighborsClassifier(n_neighbors=3)
        model.fit(self.digits.data, self.digits.target)
        return model

    # used to see an example of the dataset
    def view_image(self):
        image_arr = np.array(self.digits.images[0])
        plt.imshow(image_arr)
        plt.show()


# dir = DigitImageRecognition()
# dir.find_optimal_k()
# dir.create_model()
