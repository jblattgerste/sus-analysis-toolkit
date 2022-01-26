import operator


class SUSDataset:
    def __init__(self, SUSStuds):
        self.SUSStuds = SUSStuds
        self.sortBy('alphabetically')
        self.avgScorePerQuestion = self.calcAvgScorePerQuestion()
        self.allAbsoluteSingleScores = self.calcAllAbsoluteSingleScores()
        self.allSUSScoresPerParticipant = self.calcAllSUSScoresPerParticipant()
        self.allStudiesAvgSUSScore = self.calcAllStudiesAvgSUSScore()
        self.rawResultPerQuestion = self.getRawResultPerQuestion()

    def calcAvgScorePerQuestion(self):
        avgScorePerQuestion = []
        for i, study in enumerate(self.SUSStuds):
            for j, questionScore in enumerate(study.avgScorePerQuestion):
                if j < len(avgScorePerQuestion):
                    avgScorePerQuestion[j] += questionScore
                else:
                    avgScorePerQuestion.append(questionScore)

        for i in range(0, 9):
            avgScorePerQuestion[i] = avgScorePerQuestion[i] / len(self.SUSStuds)
        return avgScorePerQuestion

    def calcAllAbsoluteSingleScores(self):
        allAbsoluteScores = []
        for study in self.SUSStuds:
            for result in study.Results:
                allAbsoluteScores.extend(result.scorePerQuestion)
        return allAbsoluteScores

    def calcAllSUSScoresPerParticipant(self):
        allSUSScoresPerParticipant = []
        for study in self.SUSStuds:
            for result in study.Results:
                allSUSScoresPerParticipant.append(result.SUSScore)
        return allSUSScoresPerParticipant

    def calcAllStudiesAvgSUSScore(self):
        tempScore = 0
        for study in self.SUSStuds:
            tempScore += study.Score
        return tempScore / len(self.SUSStuds)

    def sortBy(self, sortKey):
        if sortKey == 'alphabetically':
            sortedStuds = sorted(self.SUSStuds, key=operator.attrgetter('name'))
            self.SUSStuds = sortedStuds
            return
        elif sortKey == 'mean':
            sortedStuds = sorted(self.SUSStuds, key=operator.attrgetter('Score'))
            self.SUSStuds = sortedStuds
            return
        elif sortKey == 'median':
            sortedStuds = sorted(self.SUSStuds, key=operator.attrgetter('median'))
            self.SUSStuds = sortedStuds
            return

    def getAllStudNames(self):
        studies = []
        for study in self.SUSStuds:
            studies.append(study.name)
        return studies

    def getIndividualStudyData(self, name):
        for study in self.SUSStuds:
            if study.name == name:
                return study

    def getAllResults(self):
        results = []
        for study in self.SUSStuds:
            results.append(study.Results)
        return results

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
        for study in self.SUSStuds:
            for i, resultsPerQuestion in enumerate(study.getRawResultPerQuestion()):
                rawResultPerQuestion[i].extend(resultsPerQuestion)

        return rawResultPerQuestion
