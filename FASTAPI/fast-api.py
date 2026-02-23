#Practices mostly from https://www.youtube.com/watch?v=7t2alSnE2-I

import asyncio
import time
from typing import Annotated, Optional
from fastapi import Depends, FastAPI, HTTPException
#from . import schemas
import uvicorn

app = FastAPI()

datalist =["this is id1","this is id2","this is id3"]

@app.get("/")
def index():
    return "hello world"

@app.get("/about")
def about():
    return datalist[0]

@app.get("/about/{id}")
def show(id:int):
    return datalist[id]

@app.get("/blog")
def blog(limit:int =10,published:bool=True,sort:Optional[str]=None):
    return f"This is Blog page contains {limit} number of blogs"

#this method should be before dynamically routed show_blog function to prevent errors.
@app.get("/blog/unpublished")
def unpublished():
    return {"data":"all unpublished blogs"}

@app.get("/blog/{id}")
def show_blog(id:int):
    return {"data":id}

#@app.post("/blog")
#def create_blog(blog:schemas.Blog):
#    return {"data": f"{blog.title} is created with {blog.body}. Published: {blog.published}"}

#ASYNC 

@app.post("/1")
def sync_endpoint():
    print("Hello1")
    time.sleep(5)
    print("good bye1")

@app.post("/2")
async def async_endpoint():
    print("Hello2")
    await asyncio.sleep(5)
    print("good bye2")

@app.post("/3")
def sync_endpoint():
    print("Hello3")
    time.sleep(5)
    print("good bye3")

#DEPENDENCY INJECTION
class AuthService:
    def authenticate(self,token:str):
        if token=="valid-token":
            return True
        else:
            raise HTTPException(status_code=401,detail="unauthorized")
def get_auth_service():
    return AuthService
auth_service_dependency = Annotated[AuthService,Depends[get_auth_service]]

@app.get("/secure-data/")
def get_secure_data(token:str,auth_service:auth_service_dependency):
    if auth_service.authenticate(token=token):
        return{"data":"This is secure data"}


# def get_db():
#   db = SessionLocal()
#   try:
#       yield db
#   finally:
#       db.close()

#@app.post("/addBlog",status_code=201,tags=["blog"])
#def create(request: schemes.Blog, db:Session = depends(get_db)):
#   new_blog = models.Blog(title=request.title,body=request.body)
#   db.add(new_blog)
#   db.commit()
#   db.refresh(new_blog)
#   return new_blog

#@app.post("/getBlogs")
#def add_blog(db:Session = Depends(get_db)):
#   blogs = db.query(models.Blog).all()
#   return blogs

#@app.get("/blog/{id}",status_code=200,response_model=schemas.ShowBlog,tags=["blog"])
#def show(id,db:Session = Depends(get_db)):
#   blog = db.query(models.Blog).filter(models.Blog.id==id).first()
#   if not blog:
#       response.status_code = 404 
#       return {"detail": f"blog with the id {id} is not available}
#   return blog

#@app.delete("/blog/{id}",status_code=status.HTTP_204_NO_CONTENT,tags=["blog"])
#def destroy(id,db: Session = Depends(get_db)):
#   blog = db.query(models.Blog).filter(models.Blog.id==id).first()
#   if not blog:
#       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="blog not found.")
#   blog.delete(synchronize_session=False)
#   db.commit()
#   return "deleted"

#@app.put("/blog/{id}",status_code=status.HTTP_202_ACCEPTED,tags=["blog"])
#def update(id,request:schemas.Blog,db: Session = Depends(get_db)):
#   blog = db.query(models.Blog).filter(models.Blog.id==id).first()
#   if not blog:
#       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="blog not found.")
#   blog.update({"title":request.body},synchronize_session="evaluate")
#   db.commit()
#   return "updated successfuly"

#@app.post("/user",status_code=status.HTTP_201_CREATED,tags=["user"])
#def create_user(request:schemas.User,db: session = Depends(get_db)):
# new_user = model.User(name=request.name,email=request.name,password=request.name)
# db.add(new_user)
# db.commit()
# db.refresh(new_user)
# return new_user
if __name__== "__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)