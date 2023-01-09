# System Usability Scale Analysis Toolkit

The [System Usability Scale (SUS) Analysis Toolkit](https://sus.mixality.de/) is a web-based python application that provides a compilation of useful insights and contextualisation approaches based on findings from the scientific literature for the System Usability Scale questionnaire that was originally developed by John Brooke. It allows researchers and practisionaires to calculate comparative, iterative and benchmarking SUS usability study datasets. Furthermore, it provides utility to contextualize the meaning of calculated scores, compare them against scores gathered in meta-analyses, calculate SUS scores conclusiveness and analysing the contribution of specific questions of the 10-item questionnaire to the SUS study scores.

An in-depth explanation of the toolkits features and their scientific basis can be found in our conference publication about the initial release and preliminary evaluation of the toolkit. It is also included in the repository: ["A Web-Based Analysis Toolkit for the System Usability Scale" - Blattgerste et al. (2022)](https://github.com/jblattgerste/sus-analysis-toolkit/blob/main/assets/Blattgerste%202022%20-%20A%20Web-Based%20Analysis%20Toolkit%20for%20the%20System%20Usability%20Scale.pdf)

### Preview: Multi-Variable SUS Analysis

![Preview Example of the multi-variable SUS analysis](/assets/PreviewMultiStudy.png)

### Preview: Single-Variable Usability Benchmarking

![Preview Example of the single-variable SUS usability benchmarking dashboard](/assets/PreviewSingleStudy.png)

## Using the SUS Analysis Toolkit
**An online version of the SUS Analysis Toolkit is hosted at: https://sus.mixality.de/**

 ![Example usage animation of the multi variable analysis](/assets/UsageExampleAnimation.gif)


## Quickstart - Running the SUS Analysis Toolkit locally

1. Install [Python 3.9](https://www.python.org/downloads/). On Windows, make sure to check "Add Pythong 3.9 to PATH" during installation
2. Clone this repository, or manually download it as a zip file and extract it
3. Open the sus-analysis-toolkit folder
4. Open the terminal (E.g. Windows Terminal) in the sus-analysis-toolkit folder
5. Run the following commands to automatically install all dependencies:
  ```
  python -m pip install --upgrade pip setuptools
  ```
  ```
  python -m pip install -r requirements.txt
  ```
5. *Alternatively, install the requirements manually by installing all packages specified in the* `requirements.txt`:
  ```
  plotly==5.3.1
  dash==2.0.0
  numpy==1.19.5
  pandas==1.3.1
  kaleido==0.2.1
  ```
6. After successful installation, run the toolkit locally with the command:
  ```
  python dashApp.py
  ```
7.  Copy the displayed address the toolkit is running on into the web browser to access the toolkit:

  ![The dash app running the local SUS analysis toolkit](/assets/DashAppRunning.png)
  
8.  To stop the toolkits local server, close the terminal window

## Running the SUS Analysis Toolkit on a server
To run the SUS Analysis Toolkit on a server, we recommend [building a Docker Image and hosting it in a Docker Container](https://docs.docker.com/get-started/). The required `Dockerfile` is included in this repository.

## Contributing to this project
As the SUS Analysis Toolkit is an ongoing project, we are happy to receive feedback, suggestions and bug reports through Email or GitHub Issues.

Additionally, we are planning to develop the tool further towards including:
- item-Level benchmarks for each of the 10 questions of the SUS questionnaire according to [Lewis & Sauro 2018](https://scholar.google.de/citations?view_op=view_citation&hl=de&user=rmiLIsYAAAAJ&citation_for_view=rmiLIsYAAAAJ:a9-T7VOCCH8C). This would allow to compare the achieved average of individual items of the SUS study scores to item-level benchmarks calculted from linear regressions based on comparable SUS study scores, the average SUS study score of 68 or the industry benchmark of 80.
- more statistical data analysis tools, ranging from simple t-test and variance analysis to [more advanced statistical decision helpers](https://scholar.google.de/citations?view_op=view_citation&hl=de&user=3LeQMbkAAAAJ&citation_for_view=3LeQMbkAAAAJ:Y0pCki6q_DkC)
- automated SUS data processing (E.g. feeding SUS questionnaire data through APIs or directly interpreting filled out questionnaires from the [SUS PDF Generator](https://jblattgerste.github.io/sus-pdf-generator/))
- improving its accessibility and usability.

Therefore, we are happy to collaborate with developers and experts in these areas. If you are interested in working on and contributing towards one of the topics, feel free to get in touch.

## Acknowledgement
The tool is freely accesible for commercial and non-commercial use under the MIT license and does not require acknowledgement. Nonetheless, if you use our tool for scientific publications or presentations, we would appreciate an acknowledgement in form of a citation to our tool:

```tex
@inproceedings{10.1145/3529190.3529216,
author = {Blattgerste, Jonas and Behrends, Jan and Pfeiffer, Thies},
title = {A Web-Based Analysis Toolkit for the System Usability Scale},
year = {2022},
isbn = {9781450396318},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3529190.3529216},
doi = {10.1145/3529190.3529216},
pages = {237–246},
numpages = {10},
location = {Corfu, Greece},
series = {PETRA '22}
}
```
