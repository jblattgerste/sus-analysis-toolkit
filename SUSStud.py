from Result import Result
import statistics


class SUSStud:
    # Class for calculating and handling a whole dataset of SUS-Scores.

    def __init__(self, results, name):
        self.Results = results
        self.Score = self.calcSUS()
        self.avgScorePerQuestion, self.scoresPerQuestion = self.calcSUSScorePerQuestion()
        self.name = name
        self.standardDevPerQuestion = self.calcStandardDevPerQuestion()
        self.standardDevOverall = self.calcStandardDev()
        self.median = self.calcMedian()
        self.rawResultPerQuestion = self.getRawResultPerQuestion()

    # Calculates the overall SUS-Score with all the SUS-Results in the dataset.
    def calcSUS(self):
        score_sum = 0
        for res in self.Results:
            score_sum += res.SUSScore
        return score_sum / len(self.Results)

    # Returns a ordered list with the scores for each of the Results (so, for each participant who filled in a
    # SUS-Survey).
    def getAllSUSScores(self):
        scores = []
        for res in self.Results:
            scores.append(res.SUSScore)
        return scores

    # Returns an ordered list of average SUS Scores for each of the 10 SUS-Questions.
    def calcSUSScorePerQuestion(self, removeIdxs=None):
        if removeIdxs is None:
            removeIdxs = []
        avgScorePerQuestion = []
        scoresPerQuestion = {}

        for res in self.Results:
            for idx, questionScore in enumerate(res.getScorePerQuestionExcluding(removeIdxs)):
                if idx < len(avgScorePerQuestion):
                    avgScorePerQuestion[idx] += questionScore
                    scoresPerQuestion[idx].append(questionScore)
                else:
                    avgScorePerQuestion.append(questionScore)
                    scoreList = [questionScore]
                    scoresPerQuestion[idx] = scoreList


        for idx, questionScoreRaw in enumerate(avgScorePerQuestion):
            avgScorePerQuestion[idx] = questionScoreRaw / len(self.Results)
        return avgScorePerQuestion, scoresPerQuestion

    def getRawResultPerQuestion(self):

        rawResultPerQuestion = [[],
                                [],
                                [],
                                [],
                                [],
                                [],
                                [],
                                [],
                                [],
                                []]

        for result in self.Results:
            for i, singleAnswer in enumerate(result.resultsRaw):
                rawResultPerQuestion[i].append(result.resultsRaw[i])

        return rawResultPerQuestion

    def addResult(self, result):
        self.Results.append(result)
        self.Score = self.calcSUS()
        self.avgScorePerQuestion = self.calcSUSScorePerQuestion()

    def calcStandardDevPerQuestion(self):
        standardDeviations = []
        for question in self.scoresPerQuestion.values():
            try:
                standardDeviations.append(statistics.pstdev(question))
            except statistics.StatisticsError:
                standardDeviations.append(0)

        return standardDeviations

    def calcStandardDev(self):
        standardDev = 0
        try:
            standardDev = statistics.pstdev(self.getAllSUSScores())
        except statistics.StatisticsError:
            standardDev = 0
        return standardDev

    def calcMedian(self):
        try:
            median = statistics.median(self.getAllSUSScores())
        except statistics.StatisticsError:
            median = 0
        return median
