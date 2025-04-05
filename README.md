# NLP-Movies-Recommender


Tasty Goal:
- The application will be an agent that returns movie suggestions based on songs / song lyrics the user
inputs. On top of this, this agent will be a learning tool. The user will be able to see the process of how the
NLP model processes the input and interprets the text to return the best output.
Overall, the agent becomes a means for a user to have movies suggested for them and it also becomes a
learning tool for them to understand how an NLP model works.

Tasty Scope:
The project will be medium-sized, with the focus being on its two functionalities:
1. Movie Recommendation: Suggesting the most accurate movies based on text input which may be
song lyrics or more.
2. Visualization with an educational aspect: Revealing the “behind the scenes” process of how the
model is working.
Tasty Initial Approach: A brief overview

We’ll be trying to use sentiment analysis to extract a ranked order for sentiments present in the text body
and then match the “genres” from the initial input using a custom model. That model will then simply
attempt to match the best fitted movies from our dataset and output them as recommendations.

Tasty Data Sources:
- Letterboxd (Movies Dataset) via Kaggle:
https://www.kaggle.com/datasets/gsimonx37/letterboxd?select=genres.csv
- Note on Division of NLP Work: Almost all steps are split evenly and done by every member
simultaneously in a group setting which makes everything tasty. Examples of tasks might include:
Research & Data gathering, Frontend integration, Tasting
