from neo4j import GraphDatabase

class Database:
    def __init__(self, uri, username, password):
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def close(self):
        self.driver.close()

    def add_author(self, name):
        with self.driver.session() as session:
            session.run("CREATE (a:Author {name: $name})", name=name)

    def add_book(self, title, year):
        with self.driver.session() as session:
            session.run("CREATE (b:Book {title: $title, year: $year})", title=title, year=year)

    def link_author_book(self, author, book):
        with self.driver.session() as session:
            author_exists = session.run("MATCH (a:Author {name: $author}) RETURN a", author=author).single()
            book_exists = session.run("MATCH (b:Book {title: $book}) RETURN b", book=book).single()
            if not author_exists:
                return {"message": "Author not found."}
            if not book_exists:
                return {"message": "Book not found."}
            session.run("""
                MATCH (a:Author {name: $author}), (b:Book {title: $book})
                CREATE (b)-[:WRITTEN_BY]->(a)
            """, author=author, book=book)
            return {"message": "Author linked to book!"}

    def get_books_by_author(self, author):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (a:Author {name: $author})<-[:WRITTEN_BY]-(b:Book)
                RETURN b.title AS title, b.year AS year
            """, author=author)
            return [{"title": record["title"], "year": record["year"]} for record in result]

    def delete_author(self, name):
        with self.driver.session() as session:
            author_exists = session.run("MATCH (a:Author {name: $name}) RETURN a", name=name).single()
            if not author_exists:
                return {"message": "Author not found."}
            session.run("MATCH (a:Author {name: $name}) DETACH DELETE a", name=name)
            return {"message": "Author deleted!"}

    def delete_book(self, title):
        with self.driver.session() as session:
            book_exists = session.run("MATCH (b:Book {title: $title}) RETURN b", title=title).single()
            if not book_exists:
                return {"message": "Book not found."}
            session.run("MATCH (b:Book {title: $title}) DETACH DELETE b", title=title)
            return {"message": "Book deleted!"}

    def get_all_authors(self):
        with self.driver.session() as session:
            result = session.run("MATCH (a:Author) RETURN a.name AS name")
            return [{"name": record["name"]} for record in result]

    def get_all_books(self):
        with self.driver.session() as session:
            result = session.run("MATCH (b:Book) RETURN b.title AS title, b.year AS year")
            return [{"title": record["title"], "year": record["year"]} for record in result]

    def find_co_authors(self, author):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (a:Author {name: $author})<-[:WRITTEN_BY]-(b:Book)-[:WRITTEN_BY]->(coauthor:Author)
                RETURN DISTINCT coauthor.name AS name
            """, author=author)
            return [{"name": record["name"]} for record in result]

    def find_books_by_multiple_authors(self, authors):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (b:Book)-[:WRITTEN_BY]->(a:Author)
                WHERE a.name IN $authors
                RETURN b.title AS title, b.year AS year, COLLECT(a.name) AS authors
            """, authors=authors)
            return [{"title": record["title"], "year": record["year"], "authors": record["authors"]} for record in result]

    def get_authors_by_book(self, book_title):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (b:Book {title: $title})-[:WRITTEN_BY]->(a:Author)
                RETURN a.name AS name
            """, title=book_title)
            return [{"name": record["name"]} for record in result]

    def get_books_by_year_range(self, start_year, end_year):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (b:Book)
                WHERE b.year >= $start_year AND b.year <= $end_year
                RETURN b.title AS title, b.year AS year
            """, start_year=start_year, end_year=end_year)
            return [{"title": record["title"], "year": record["year"]} for record in result]

    def find_shortest_path_between_authors(self, author1, author2):
        with self.driver.session() as session:
            result = session.run("""
                MATCH path = shortestPath((a1:Author {name: $author1})-[:WRITTEN_BY*]-(a2:Author {name: $author2}))
                RETURN [n IN nodes(path) | n.name] AS path
            """, author1=author1, author2=author2)
            
            record = result.single()
            if record:
                return {"path": record["path"]}
            else:
                return {"message": "No path found between the authors."}