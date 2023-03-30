import sqlite3

database = sqlite3.connect("articles.db")

database.execute(''' CREATE TABLE article
		(ID INT PRIMARY KEY	 NOT NULL,
		URL TEXT NOT NULL,
		Headline TEXT NOT NULL,
		Author TEXT NOT NULL,
  		Date DATE NOT NULL);
		''')
