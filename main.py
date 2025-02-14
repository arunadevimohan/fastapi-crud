from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import database as books_collection

from bson import ObjectId

app = FastAPI()

templates = Jinja2Templates(directory = 'templates')

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "Hello, World!"})


class Book(BaseModel):
    #id      : int
    title 	: str
    author 	: str
    year 	: int

class BookInDB(Book):

    id :str 


@app.post('/books', response_class=HTMLResponse)
async def get_books(book : Book, request: Request):
    params_dict = {
        "id"      : user_model.id,
        "title"   : user_model.title,
        "author"  : user_model.author,
        "year"    : user_model.year
    }

    result = books_collection.insert_one(params_dict)

    if result.inserted_id:
          return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "message": "Book added successfully!",
                "book": params_dict
            }
        )
    raise HTTPException(status_code=500, detail={"message": "Failed to Add a Book"}) 

@app.get("/books/all", response_class=HTMLResponse)
async def get_books(request: Request):
    books = books_collection.find()
    
    result = []
    for book in books:
        book['_id'] = str(book['_id'])
        result.append(book)


    if not books:
        raise HTTPException(status_code=404, detail={"No books found"})
    
    
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "books": result, "message": "All Books"}
    )

@app.get('/get/books/{book_id}', response_model=BookInDB)
async def get_books(book_id: str):
    
    book = books_collection.find_one({"_id": ObjectId(book_id)})
    
    if not books:
        raise HTTPException(status_code=404, detail={"book Not found"})
    
    #book['_id'] = str(book['_id'])

    return {"id": str(book["_id"]), **book}
    
class UpdateBook(BaseModel):
    
    title 	: str
    author 	: str
    year 	: int

    
    
@app.put('/update/book', response_model=BookInDB)
async def update_book(update_book: BaseModel):
    
    title  = update_book.title
    author = update_book.author
    year   = update_book.year
    result  = books_collection.update_one(
        {"title": title},
        {"author": author}
        
    )

    if result : 
        return templates.TemplateResponse(
        "index.html",
        {"request": request, "books": result, "message": "Update the Books"}
    )

    
    raise HTTPException(status_code=404, detail={"book Not found"})





if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        host='0.0.0.0'
    )