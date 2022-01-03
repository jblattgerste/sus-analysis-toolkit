annotation_xPos = {1: 1.2,
                   2: 1.155,
                   3: 1.125,
                   4: 1.106,
                   5: 1.092}
annotation_yPos = 1.13
singleScoreScaleOffset = 0.16
annotation_yPos_singleScore = {0: 0.7,
                               1: 0.58,
                               2: 0.5}

annotationTemplate = dict(
    x=1.1,
    y='',
    xref="paper",
    yref="y",
    text="",
    bordercolor="#c7c7c7",
    borderwidth=0,
    font=dict(
        size=10,
        color="#000000"
    ),
    showarrow=False,
    borderpad=0,
    bgcolor="#8FD14F",
    opacity=0.8,
    height=1,
    width=70
)

annotationTemplateHorizontal = dict(
    x='',
    y=annotation_yPos,
    xref="x",
    yref="paper",
    text="",
    bordercolor="#c7c7c7",
    borderwidth=0,
    font=dict(
        size=10,
        color="#000000"
    ),
    showarrow=False,
    borderpad=0,
    bgcolor="#8FD14F",
    opacity=0.8,
    height=40,
    width=1
)

annotationTemplateHorizontalSingleScore = dict(
    x='',
    y=annotation_yPos_singleScore,
    xref="x",
    yref="paper",
    text="",
    bordercolor="#c7c7c7",
    borderwidth=0,
    font=dict(
        size=10,
        color="#000000"
    ),
    showarrow=False,
    borderpad=0,
    bgcolor="#8FD14F",
    opacity=0.8,
    height=40,
    width=1
)


def getGradeScaleAnnotations(systemCount):
    grades = {'A': [78.9, 100, "#8FD14F"],
              'B': [72.6, 78.8, "#CEE741"],
              'C': [62.7, 72.5, "#FEF445"],
              'D': [51.7, 62.6, "#FAC710"],
              'F': [0, 51.6, "#F24726"]}

    annotations = generateAnnotations(grades, systemCount)

    return annotations


def getQuartileScaleAnnotations(systemCount):
    quartiles = {'4th Quartile': [78.1, 100, "#8FD14F"],
                 '3rd Quartile': [71, 78, "#CEE741"],
                 '2nd Quartile': [62.6, 71, "#FEF445"],
                 '1st Quartile': [0.1, 62.5, "#F24726"],
                 }

    annotations = generateAnnotations(quartiles, systemCount)

    median = annotationTemplate.copy()
    median['x'] = annotation_xPos.get(systemCount)
    median['y'] = quartiles['3rd Quartile'][0]
    median['opacity'] = 1
    median['bgcolor'] = "#000000"
    annotations.append(median)
    annotations.append(dict(
        text='Median',
        xref='x domain',
        yref='y',
        axref='x domain',
        ayref='y',
        y=quartiles['3rd Quartile'][0],
        x=1,
        ax=0.95,
        ay=quartiles['3rd Quartile'][0] + 10,
        showarrow=False,
        font=dict(
            size=9
        )
    ))

    return annotations


def getBGAdjectiveScaleAnnotations(systemCount):
    annotations = [

    ]

    return annotations


def getAdjectiveScaleAnnotations(systemCount):
    adjectives = {
        'Best<br>Imaginable': [84.1, 100, "#8FD14F"],
        'Excellent': [80.8, 84, "#8FD14F"],
        'Good': [71.1, 80.7, "#CEE741"],
        'OK': [51.7, 71, "#FEF445"],
        'Poor': [25.1, 51.7, "#FAC710"],
        'Worst<br>Imagineable': [0, 25.1, "#F24726"],
    }

    annotations = generateAnnotations(adjectives, systemCount)

    return annotations


def getAcceptabilityScaleAnnotations(systemCount):
    acceptability = {
        'Acceptable': [72.6, 100, "#8FD14F"],
        'Marginal': [51.7, 72.5, "#FEF445"],
        'Not<br>Acceptable': [0, 51.7, "#F24726"]
    }

    annotations = generateAnnotations(acceptability, systemCount)
    return annotations


def getPromoterScaleAnnotations(systemCount):
    promoter = {
        'Promoter': [78.9, 100, "#8FD14F"],
        'Passive': [62.6, 78.8, "#FEF445"],
        'Detractor': [0, 62.5, "#F24726"]
    }

    annotations = generateAnnotations(promoter, systemCount)
    return annotations


def getHorizontalPromoterScaleAnnotations():
    promoter = {
        'Promoter': [78.9, 100, "#8FD14F"],
        'Passive': [62.6, 78.8, "#FEF445"],
        'Detractor': [0, 62.5, "#F24726"]
    }

    annotations = generateHorizontalAnnotations(promoter)
    return annotations


def getHorizontalAdjectiveScaleAnnotations():
    adjectives = {
        'Best Imaginable': [84.1, 100, "#E6E6E6"],
        'Ex-<br>cel-<br>lent': [80.8, 84, "#8FD14F"],
        'Good': [71.1, 80.7, "#CEE741"],
        'OK': [51.7, 71, "#FEF445"],
        'Poor': [25.1, 51.7, "#FAC710"],
        'Worst Imagineable': [0, 25.1, "#F24726"],
    }

    annotations = generateHorizontalAnnotations(adjectives)
    return annotations


def getHorizontalGradeScaleAnnotations():
    grades = {'A': [78.9, 100, "#8FD14F"],
              'B': [72.6, 78.9, "#CEE741"],
              'C': [62.7, 72.6, "#FEF445"],
              'D': [51.7, 62.7, "#FAC710"],
              'F': [0, 51.7, "#F24726"]}

    annotations = generateHorizontalAnnotations(grades)
    return annotations


def getHorizontalQuartileScaleAnnotations():
    quartiles = {'4th<br>Quartile': [78.1, 100, "#8FD14F"],
                 '3rd<br>Quartile': [71.1, 78, "#CEE741"],
                 '2nd<br>Quartile': [62.6, 71, "#FEF445"],
                 '1st<br>Quartile': [0, 62.5, "#F24726"],
                 }

    annotations = generateHorizontalAnnotations(quartiles)

    median = annotationTemplateHorizontal.copy()
    median['x'] = quartiles['3rd<br>Quartile'][0] - 0.2
    median['opacity'] = 1
    median['bgcolor'] = "#000000"
    annotations.append(median)
    annotations.append(dict(
        text='Median',
        yref='y domain',
        xref='x',
        axref='x',
        ayref='y domain',
        x=quartiles['3rd<br>Quartile'][0],
        y=1,
        ay=0.95,
        ax=quartiles['3rd<br>Quartile'][0] + 10,
        showarrow=False,
        font=dict(
            size=9
        )
    ))
    return annotations


def getHorizontalAcceptabilityScaleAnnotations():
    acceptability = {
        'Acceptable': [72.6, 100, "#8FD14F"],
        'Marginal': [51.7, 72.5, "#FEF445"],
        'Not Acceptable': [0, 51.7, "#F24726"]
    }

    annotations = generateHorizontalAnnotations(acceptability)
    return annotations


def getHorizontalBGAdjectiveScaleAnnotations():
    annotations = [

    ]
    return annotations


def determineVerticalScale(scaleValue, systemCount):
    scaleAnnotations = None
    if scaleValue == 'adjectiveScale':
        scaleAnnotations = getAdjectiveScaleAnnotations(systemCount)
    elif scaleValue == 'gradeScale':
        scaleAnnotations = getGradeScaleAnnotations(systemCount)
    elif scaleValue == 'quartileScale':
        scaleAnnotations = getQuartileScaleAnnotations(systemCount)
    elif scaleValue == 'acceptabilityScale':
        scaleAnnotations = getAcceptabilityScaleAnnotations(systemCount)
    elif scaleValue == 'promoterScale':
        scaleAnnotations = getPromoterScaleAnnotations(systemCount)
    elif scaleValue == 'BGAdjectiveScale':
        scaleAnnotations = getBGAdjectiveScaleAnnotations(systemCount)
    elif scaleValue == 'none':
        scaleAnnotations = []

    return scaleAnnotations


def determineHorizontalScale(scaleValue):
    scaleAnnotations = None
    if scaleValue == 'adjectiveScale':
        scaleAnnotations = getHorizontalAdjectiveScaleAnnotations()
    elif scaleValue == 'gradeScale':
        scaleAnnotations = getHorizontalGradeScaleAnnotations()
    elif scaleValue == 'acceptabilityScale':
        scaleAnnotations = getHorizontalAcceptabilityScaleAnnotations()
    elif scaleValue == 'promoterScale':
        scaleAnnotations = getHorizontalPromoterScaleAnnotations()
    elif scaleValue == 'quartileScale':
        scaleAnnotations = getHorizontalQuartileScaleAnnotations()
    elif scaleValue == 'BGAdjectiveScale':
        scaleAnnotations = getHorizontalBGAdjectiveScaleAnnotations()
    elif scaleValue == 'none':
        scaleAnnotations = []
    return scaleAnnotations


def getSingleScoreScale():
    annotations = []
    adjectives = {
        'Best Imaginable': [84.1, 100, "#E6E6E6"],
        'Ex-<br>cel-<br>lent': [80.8, 84, "#8FD14F"],
        'Good': [71.1, 80.7, "#CEE741"],
        'OK': [51.7, 71, "#FEF445"],
        'Poor': [25.1, 51.7, "#FAC710"],
        'Worst Imagineable': [0, 25.1, "#F24726"],
    }

    grades = {'A': [78.9, 100, "#8FD14F"],
              'B': [72.6, 78.9, "#CEE741"],
              'C': [62.7, 72.6, "#FEF445"],
              'D': [51.7, 62.7, "#FAC710"],
              'F': [0, 51.7, "#F24726"]}

    quartiles = {'4th<br>Quartile': [78.1, 100, "#8FD14F"],
                 '3rd<br>Quartile': [71.1, 78, "#CEE741"],
                 '2nd<br>Quartile': [62.6, 71, "#FEF445"],
                 '1st<br>Quartile': [0., 62.5, "#F24726"],
                 }

    annotations.extend(generateHorizontalAnnotationsSingleScore(adjectives, 0))
    annotations.extend(generateHorizontalAnnotationsSingleScore(grades, 1))
    annotations.extend(generateHorizontalAnnotationsSingleScore(quartiles, 2))
    return annotations


def getYValue(dictionary, key):
    yVal = dictionary[key][0] + (dictionary[key][1] - dictionary[key][0]) / 2
    return yVal


def getXValue(dictionary, key):
    yVal = dictionary[key][0] + (dictionary[key][1] - dictionary[key][0]) / 2
    return yVal


def getWidth(dictionary, key):
    widthFactor = 6.75
    width = (dictionary[key][1] - dictionary[key][0]) * widthFactor
    return width


def getHeight(dictionary, key):
    heightFactor = 3.22
    height = (dictionary[key][1] - dictionary[key][0]) * heightFactor
    return height


def generateAnnotations(dictionary, systemCount):
    annotations = []
    for element in dictionary:
        tempAnnotation = annotationTemplate.copy()
        tempAnnotation['x'] = annotation_xPos.get(systemCount)
        tempAnnotation['y'] = getYValue(dictionary, element)
        tempAnnotation['text'] = element
        tempAnnotation['bgcolor'] = dictionary[element][2]
        tempAnnotation['height'] = getHeight(dictionary, element)
        annotations.append(tempAnnotation)
    return annotations


def generateHorizontalAnnotations(dictionary):
    annotations = []
    for element in dictionary:
        tempAnnotation = annotationTemplateHorizontal.copy()
        tempAnnotation['x'] = getXValue(dictionary, element)
        tempAnnotation['text'] = element
        tempAnnotation['bgcolor'] = dictionary[element][2]
        tempAnnotation['width'] = getWidth(dictionary, element)
        annotations.append(tempAnnotation)
    return annotations


def generateHorizontalAnnotationsSingleScore(dictionary, scaleIndex):
    annotations = []
    for element in dictionary:
        tempAnnotation = annotationTemplateHorizontalSingleScore.copy()
        tempAnnotation['y'] = annotation_yPos_singleScore[scaleIndex]
        tempAnnotation['x'] = getXValue(dictionary, element)
        tempAnnotation['text'] = element
        tempAnnotation['bgcolor'] = dictionary[element][2]
        tempAnnotation['width'] = getWidth(dictionary, element)
        annotations.append(tempAnnotation)
    return annotations


def generateConclusivenessAnnotation(sampleSize, systemName, yOffset):
    yVal = [35, 75, 80, 100, 100]

    yValues = dict({0: 0,
                    6: yVal[0],
                    7: 55,
                    8: yVal[1],
                    9: 78,
                    10: yVal[2],
                    11: 98,
                    12: 100,
                    13: 100,
                    14: 100
                    })

    if sampleSize > 14:
        XAnnotationVal = 14
    else:
        XAnnotationVal = sampleSize

    if sampleSize < 6:
        YAnnotationsVal = 0
    else:
        YAnnotationsVal = yValues[XAnnotationVal]
    annotation = dict(
        x=XAnnotationVal,
        y=YAnnotationsVal,
        text=systemName,
        ayref='y',
        ay=YAnnotationsVal + 10 + yOffset,
        axref='x',
        ax=XAnnotationVal - 0.5
    )
    return annotation


def generateConclusivenessAnnotationSingleStudy(singleStudy, xaxis, yaxis):
    yVal = [35, 75, 80, 100, 100]
    yOffset = 20
    yValues = dict({0: 0,
                    6: yVal[0],
                    7: 55,
                    8: yVal[1],
                    9: 78,
                    10: yVal[2],
                    11: 98,
                    12: 100,
                    13: 100,
                    14: 100
                    })


    if len(singleStudy.Results) > 14:
        sampleSize = 14
    else:
        sampleSize = len(singleStudy.Results)

    if sampleSize > 14:
        XAnnotationVal = 14
    else:
        XAnnotationVal = sampleSize

    if sampleSize < 6:
        YAnnotationsVal = 0
    else:
        YAnnotationsVal = yValues[XAnnotationVal]
    annotation = dict(
        x=XAnnotationVal,
        y=YAnnotationsVal,
        text=singleStudy.date,
        ayref=yaxis,
        yref = yaxis,
        xref = xaxis,
        ay=YAnnotationsVal + yOffset,
        axref=xaxis,
        ax=XAnnotationVal - 0.5
    )
    return annotation
