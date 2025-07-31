# University Mobility Analysis

This repository contains the code, datasets, and visualizations used in the analysis of regional student mobility and access to higher education across a national context. The project explores territorial patterns using geospatial and statistical methods, contributing to the design of data-driven educational policies.

This submission is part of an anonymized academic review process (e.g., ICPRS 2025) and complies with the double-blind requirements.

## 🧠 Project Overview

The study focuses on identifying spatial and socioeconomic patterns in student transitions from secondary education to university. It uses public datasets to:

- Build a mobility matrix based on interregional student flows.
- Integrate geographic and socioeconomic variables such as test scores, vulnerability indices, and distances.
- Detect outlier regions using anomaly detection techniques.
- Apply clustering to identify regional education profiles.

An interactive web app is also included to facilitate exploration and visual analysis of the results.

##  Project Structure

```text
.vscode/        → Configuration files for the development environment (optional)
code/           → Jupyter notebooks and Python scripts for data analysis and visualization
data/           → Public datasets (raw and processed) used in the study
images/         → Exported figures and plots for the paper and app

.gitignore      → Specifies files and folders to be ignored by Git
app.py          → Main Streamlit app for interactive data exploration
LICENSE         → License file for the project
README.md       → Project description and documentation
requirements.txt→ Python dependencies required to run the project
```


## 📊 Included Analyses

- Descriptive statistics and PCA-based dimensionality reduction
- Interregional mobility matrix and distance metrics
- Clustering of regions using educational and social features
- Outlier detection via Isolation Forest
- Summary tables and grouped visualizations by territorial cluster
Aquí tienes una versión mejorada y más fluida en inglés para esa sección del `README.md`, manteniendo el tono profesional y la claridad:


### 🌍 Public Data Sources

The following open datasets were used in this project:

* [Higher Education Enrollment](https://datosabiertos.mineduc.cl/matricula-en-educacion-superior/) — Enrollment records for universities and technical institutions.
* [Admission Test Scores](https://datosabiertos.mineduc.cl/pruebas-de-admision-a-la-educacion-superior/) — Standardized test results used for university admissions.
* [Multidimensional Vulnerability Index (IVM)](https://www.junaeb.cl/medicion-la-vulnerabilidad-ivm/) — Socioeconomic vulnerability index for schools.
* [School Geolocation](https://www.geoportal.cl/geoportal/catalog/35408/Establecimientos%20Educaci%C3%B3n%20Escolar) — Geographic coordinates of secondary education institutions.
* [University Geolocation](https://www.geoportal.cl/geoportal/catalog/35408/Establecimientos%20Educaci%C3%B3n%20Escolar) — Geographic coordinates of higher education institutions.


*This repository has been anonymized for peer review. Author and institution details will be added after acceptance.*



