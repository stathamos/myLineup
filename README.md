# myLineup

## Architecture

In order to realize this application I decided to use the following architecture on AWS:
- EC2 instance
- Route53
- SQLite3

Here is a diagram explaining the links between the different tools used for the application.

![diagram](/readme/mylineup_archi.png)

### Database

We tried to use a PostgreSQL database but the "Free tier" offer is limited:
- the database was running on a micro instance
- the requests were case sensitive which we had not expected during our tests (all the scripts tested and validated so far no longer worked)

We therefore preferred to use a local SQLite database first, then copy it to the instance.
Writing data was much faster on the SQLite database which allowed us to be much more flexible in our tests. For an idea, retrieving and writing data on the PostgreSQL instance took almost 24 hours compared to only 1 hour on the SQLite database.

### Domain name

We obtained the free domain name thanks to the site https://my.freenom.com/
Great for school projects, it allowed me to deploy my app to a URL that anyone could log into.
Unfortunately, I couldn't let the application run: as the Route 53 redirection costs were very high (around $ 1 per day), my AWS credits were going to run out too quickly.

### Application

The application was developed using Streamlit: a tool for building and deploying applications quickly. The application runs under an Amazon-Linux EC2 micro instane. Since the data is already stored and prepared in the database, one micro instance is sufficient to run few users simultaneously.
We have opted for navigation using tabs on the left of the web page. This allows the user to reach the desired information as quickly as possible. In addition, the python script does not have to reload the whole page with each user interaction, which makes the application much more usable.

#### Complements on the data obtained.

During the regular season (November to April), the data has been updated on a weekly basis. For our analysis, the data from the final stages were not used because of little relevance to the rest of the project: the players have very little, or even no match played in the final stage. However, the results obtained with our analysis can be used for the purpose of preparing final stages.

## Machine Learning part

### Data preparation

For the data on the players, from the 60 data tables obtained, we were able to merge the data into a single table which groups together all this data.

We cleaned up the data:
- removal of duplicates
- deletion of variables with more than 20% of zero value
- replacement of the remaining null variables by zero
- data normalization

Some variables had only been present on the NBA site for a few years. However, we have recovered the data for the last 7 years. This is the reason why we removed the variables having more than 20% of null values.
In addition, we took the liberty of replacing the remaining empty values ​​with zero because these remaining values ​​mean that the player did not take any action leading to a value being counted in that statistic.
For example: a player who has never shot 3pts during a season will have an empty value for the variable "3PtsFGA". It is therefore consistent to replace this empty value with a zero.

### Feature selection

Thanks to the PCA method, we were able to reduce nearly 1000 variables to 30 variables, while keeping about 75% of the data.
To visualize the data, we will keep the first 3 axes. After looking at the correlations between PCA and the initial columns, we were able to identify the variables penalized / rewarded by PCA.
Here's a recap:
- PCA1 rewards players that score a lot of points and play big minutes and penalizes the opposite
- PCA2 rewards players that defend near the rim and penalizes players that shoot a lot of three points
- PCA3 rewards players that do a lot of dribbles and penalizes catch and shooters

## Clustering

### Find the right number of clusters

In order to find the right number of clusters, we used the elbow method on the PCA dataset. This gave us the following graph:
! [nbclus] (/ readme / nbclus.png)

The elbow is at the level of 7. So we chose 7 clusters. Here's how we named them:
- Complete big
- Role player frontcourt
- Defensive big
- Backcourt role player
- Offense runner / Playmaker
- Low minutes player
- Offensive minded player

After re-examination, given the quantity of variables available for a single player, we tried to look for other clusters and therefore looked for sub-clusters in each clusters. We therefore used the elbow method again, and found 3 sub-clusters in each cluster. In total, therefore, we find 21 different types of players that you will find below:
- Traditional power forward
- Traditional point guard
- Traditional center
- Top guards
- Modern bigs
- Low playing time guard
- Low playing time forward
- Low playing time center
- Elite traditional centers
- Elite modern bigs
- Elite catch and shooters
- Decent point guard
- Complete superstar
- Combo guards
- Back up space creator
- Back up point guard
- Back up center
- Back up center
- Back up 3 & D
- 3 & D
- 2-way forward
