import asyncio
from itertools import combinations
from rapidfuzz import fuzz
from sqlmodel import Session
from backend.datamodels import *
from backend.exceptions import AuthorError
from backend.services.scrape_service import clean_title

def save_author_to_db(author_id: str, session: Session, scraped: dict, override: bool = False):
    author_data = scraped["author_data"]
    books_data = scraped["books"]
    if (author:=session.get(Author, author_id)):
        if not override:
            raise AuthorError(detail=f"Author {author_id} already exists", status_code=403)
        else: session.delete(author)
    author = Author(**author_data)
    reihen: dict[str, Reihe] = {}
    sanity_dedub = set() # see A1040945738 for funky shit
    for eds, series_title in books_data:
        eds = sorted(eds, key=lambda x: medium_priority.get(x["medium"], 10))
        book = Book(autor_key=author.key)
        book.name, book.bild, book.reihe_position = eds[0].get("titel"), eds[0].get("bild"), eds[0].get("_pos")
        if series_title:
            ctitle = clean_title(book.name, series_title, book.reihe_position)
            if book.name == ctitle:
                for ed in eds:
                    ctitle = clean_title(ed.get("titel"), series_title, ed.get("_pos")) # if fallback was used e.g. Title of Edition was only Series Name + Series Pos we check if there is a better title
                    if book.name != ctitle:
                        break
            book.name = ctitle
            reihe = reihen.setdefault(series_title, Reihe(name=series_title, autor_key=author.key))
            reihe.books.append(book)
            if book.reihe_position and (bs:=[b for b in reihe.books if b.reihe_position and int(b.reihe_position) == int(book.reihe_position)]):
                for idx, b in enumerate(bs):
                    b.reihe_position = round(0.1*idx + int(book.reihe_position), 1) # maybe check date before??
        editions = []
        for i in eds:
            if i["key"] in sanity_dedub: #shouldnt ever happen but i came across it once so we gotta handle it -.-
                continue
            editions.append(Edition(**i))
            sanity_dedub.add(i["key"])
        book.editions = editions
        author.books.append(book)
        author.reihen = list(reihen.values())
    session.add(author)
    session.flush()
    for reihe in author.reihen: #really inefficient needs revisit #TODO
        for book, book2 in combinations(reihe.books, 2):
            if not book.reihe_position or not book2.reihe_position: continue
            if fuzz.ratio(book.name, book2.name) > 90 and round(float(book.reihe_position)) == round(float(book2.reihe_position)): # we basically have the same book twice
                for edition in book2.editions:
                    book.editions.append(edition)
                author.books.remove(book2)
    session.commit()
    return author.key