# NLP-Movies-Recommender


Goal:
- The application will be an agent that returns movie suggestions based on songs / song lyrics the user
inputs. On top of this, this agent will be a learning tool. The user will be able to see the process of how the
NLP model processes the input and interprets the text to return the best output.
Overall, the agent becomes a means for a user to have movies suggested for them and it also becomes a
learning tool for them to understand how an NLP model works.

How to run the project (currently in DEV mode):
1. If you do not have all the cleaned CSV files already: Run all the cells in data-preprocessing.ipynb to generate the cleaned CSVs
2. Run all cells in vector-search.ipynb to enable semantic analysis of the dataset, in which the model can successfully come up with movie recommendations via queries
3. Run all the cells in text-classification -- WORK IN PROGRESS


Scope:
The project will be medium-sized, with the focus being on its two functionalities:
1. Movie Recommendation: Suggesting the most accurate movies based on text input which may be
song lyrics or more.
2. Visualization with an educational aspect: Revealing the “behind the scenes” process of how the
model is working.
Tasty Initial Approach: A brief overview

We’ll be trying to use sentiment analysis to extract a ranked order for sentiments present in the text body
and then match the “genres” from the initial input using a custom model. That model will then simply
attempt to match the best fitted movies from our dataset and output them as recommendations.

Data Sources:
- Letterboxd (Movies Dataset) via Kaggle:
https://www.kaggle.com/datasets/gsimonx37/letterboxd?select=genres.csv
