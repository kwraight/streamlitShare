# My Big Custom WebApp

### [Streamlit](https://www.streamlit.io) (python**3**) for general purpose app

Check requirements file for necessary libraries

---

## WebApp Layout

**Basic Structure:**
* physics pages
* STS pages
* other pages

... based on: [*streamlit template*](https://github.com/kwraight/streamlitTemplate)

### Main Page
  * includes *sidebar* for checking debug states and quick token renewal

### Debug Page:
**(Broom cupboard)**
  * State settings

---

## Running locally

Run webApp locally:

* get required libraries:
> python3 -m pip install -r requirements

* run streamlit:
> streamlit run mainApp.py

* open browser at ''localhost:8501''

---

## Running via Docker

Either of two files can be used to build basic templates (structural files):

build *usual* image:

> docker build . -f dockerFiles/Dockerfile -t big-app

The build will copy files in the pages directory into the image and use these as content of the webApp.

* run container from image:

> docker run -p 8501:8501 big-app

* open browser at ''localhost:8501''

---
