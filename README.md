# sqlalchemy-challenge

for Station Analysis we used Python and SQLAlchemy ,SQLAlchemy ORM queries, Pandas, and Matplotlib
and for second part Design the Climate App, we used FLASK . 
we had to install Flask . 

After installing flask;

we used "/" for starting the homepage and Listing all the available routes.

/api/v1.0/precipitation was used for Converting the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.


"/api/v1.0/stations" Returned a JSON list of stations from the dataset.

"/api/v1.0/tobs" was used to Query the dates and temperature observations of the most-active station for the previous year of data 


/api/v1.0/<start> and /api/v1.0/<start>/<end> were used to 

Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.