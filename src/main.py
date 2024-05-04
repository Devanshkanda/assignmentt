from fastapi import FastAPI

app = FastAPI()


from routes import bank_list_route
app.include_router(router=bank_list_route.router)

@app.get("/")
async def welcome():
    return {
        "welcome to your fastapi project"
    }

app.include_router(bank_list_route.router)



