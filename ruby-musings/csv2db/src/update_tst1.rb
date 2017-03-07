require 'sqlite3'

dbh = SQLite3::Database::new ("./tst4.db")

dbh.execute("UPDATE rows SET size_equiv=3877 where rowid=55")

dbh.close