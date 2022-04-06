# System Usability Scale Analysis Toolkit

The [System Usability Scale (SUS) Analysis Toolkit](https://sus.mixality.de/) is a web-based python application that provides a compilation of useful insights and contextualisation approaches based on findings from the scientific literature for the System Usability Scale questionnaire that was originally developed by John Brooke. It allows researchers and practisionaires to calculate comparative, iterative and singular SUS usability study datasets. Furthermore, it provides utility to contextualize the meaning of calculated scores, compare them against scores gathered in meta-analyses, calculate SUS scores conclusiveness and analysing the contribution of specific questions of the 10-item questionnaire to the SUS study scores.

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
As the SUS Analysis Toolkit is an ongoing project, we are happy to receive feedback, suggestions and bug reports through Email or GitHub Issues. Additionally, we are planning to develop the tool further towards including more statistical data analysis tools, automated API processing and improving its accessibility and usability. Therefore, we are happy to collaborate with developers and experts in these areas.

## Acknowledgement
The tool is freely accesible for commercial and non-commercial use under the MIT license and does not require acknowledgement. Nonetheless, if you use our tool for scientific publications or presentations, we would appreciate an acknowledgement in form of a citation to our tool:

```tex
@misc{sus-analysis-toolkit,
title  = {A Web-Based Analysis Toolkit for the System Usability Scale},
author = {Blattgerste, Jonas and Behrends, Jan and Pfeiffer, Thies},
note   = {https://sus.mixality.de/},
year   = {2022},
}
```
