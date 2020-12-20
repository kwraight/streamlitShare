# Mags' Recipes

### [Streamlit](https://www.streamlit.io) (python**3**) code to store classic scran

Check requirements file for necessary libraries

---

## Running

*Stand Alone* version:

Get libraries:
> python3 -m pip install -r requirements

Run WebApp:
> streamlit run MagsRecipes.py

[*Docker version*]():
Run WebApp (TBC):
> docker run -p 8501:8501 kwraight/streamlit_mags_recipes:TAG_ID streamlit run code/MagsRecipes.py

---

## WebApp Layout

**Basic Idea:**
* display recipes list
* select recipe
* display recipe

### Top Page
  * Welcome message

### Choose Recipe
  * select from list

''' Later: upload recipe '''

### Debug Page:
**(Broom cupboard)**
  * State settings

## TODO
  * content: add Recipes
  * refactor: convert *.py to *json on the fly in app, rather than write json files
