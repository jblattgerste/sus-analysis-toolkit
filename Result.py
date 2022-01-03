import statistics


class Result:
    # One single Result-Dataset of an SUS-Questionnaire. It contains the SUS-Result of one SUS survey participant.

    def __init__(self, resultsRaw, participantID):
        self.resultsRaw = resultsRaw
        self.scorePerQuestion = []
        self.SUSScore = self.calcSingleScore()
        self.participantID = participantID
        self.standardDeviationPerQuestion = self.calcStandardDeviation()
        self.rawResultPerQuestion = self.getRawResultPerQuestion()

    # Calculates the overall score for this result-dataset. Also saves the Score per Question in the scorePerQuestion-
    # list
    def calcSingleScore(self):
        rawScore = 0
        idx = 1
        for val in self.resultsRaw:
            if val < 1 or val > 5:
                raise Exception('SUS-Values must be between 1 and 5.')
            if idx % 2 == 0:
                tempScore = 5 - val
                self.scorePerQuestion.append(tempScore * 2.5)
                rawScore += tempScore
            else:
                tempScore = val - 1
                self.scorePerQuestion.append(tempScore * 2.5)
                rawScore += tempScore
            idx += 1
        return rawScore * 2.5

    def calcStandardDeviation(self):
        return statistics.stdev(self.scorePerQuestion)

    def getRawResultPerQuestion(self):
        rawResultPerQuestionDict = {"Question 1": self.resultsRaw[0],
                                "Question 2": self.resultsRaw[1],
                                "Question 3": self.resultsRaw[2],
                                "Question 4": self.resultsRaw[3],
                                "Question 5": self.resultsRaw[4],
                                "Question 6": self.resultsRaw[5],
                                "Question 7": self.resultsRaw[6],
                                "Question 8": self.resultsRaw[7],
                                "Question 9": self.resultsRaw[8],
                                "Question 10": self.resultsRaw[9]}
        return rawResultPerQuestionDict


if __name__ == "__main__":
    resultOne = Result([3, 2, 5, 1, 4, 5, 3, 4, 5, 2], 0)
    resultTwo = Result([1, 4, 3, 4, 4, 5, 2, 1, 4, 3], 1)
    print(resultOne.participantID)
    print(resultOne.scorePerQuestion)
    print(resultTwo.scorePerQuestion)
