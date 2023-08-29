import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo.mongo_client import MongoClient
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from bson import ObjectId

app = FastAPI()

# Update with your MongoDB Atlas connection string
MONGO_URI = "mongodb+srv://Aurjikhan:qwerty54321@cluster0.s5gnzxd.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["Herb-Store"]
collection = db["User"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    username: str
    password: str
    id: str


class UserInDB(User):
    hashed_password: str


# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/register", response_model=User)
async def register(user: User):
    try:
        # Hash the user's password
        hashed_password = pwd_context.hash(user.password)

        # Create a dictionary with hashed password
        user_dict = user.dict()
        user_dict["hashed_password"] = hashed_password

        # Insert the user data into the database
        user_id = collection.insert_one(user_dict).inserted_id

        # Print a success message and inserted ID
        print("User registered successfully. Inserted ID:", user_id)

        return user

    except Exception as e:
        print("Error while registering user:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while registering the user."
        )


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = collection.find_one({"username": form_data.username})
    if not user or not pwd_context.verify(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": form_data.username, "token_type": "bearer"}


origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

herbs = [
    {
        "id": 1,
        "name": "Basil",
        "price": 4,
        "description": "Basil is a fragrant herb with a distinct aroma. It is commonly used in Mediterranean cuisine "
                       "to add flavor to various dishes.",
        "uses": "Basil is widely used in cooking as a culinary herb. It pairs well with tomatoes, pasta, and salads.",
        "origin": "Mediterranean"
    },
    {
        "id": 2,
        "name": "Lavender",
        "price": 3,
        "description": "Lavender is an aromatic herb known for its calming fragrance. It is often used in "
                       "aromatherapy and culinary applications.",
        "uses": "Lavender is used in aromatherapy to promote relaxation and reduce stress. It can also be used in "
                "cooking to add a unique floral flavor to desserts.",
        "origin": "Mediterranean"
    },

    {
        "id": 3,
        "name": "Chamomile",
        "price": 2,
        "description": "Chamomile is a gentle herb with a soothing nature. It is commonly brewed as a tea for its "
                       "calming effects.",
        "uses": "Chamomile tea is popular for promoting relaxation and aiding in sleep. It also has anti-inflammatory "
                "properties and can be used in skincare products.",
        "origin": "Europe"
    },
    {
        "id": 4,
        "name": "Thyme",
        "price": 2,
        "description": "Thyme is a small low-growing shrub and is commonly cultivated as an annual, though it can "
                       "persist as an evergreen perennial in warm climates. The stems are somewhat woody and bear "
                       "simple leaves that are oval to linear and arranged oppositely.",
        "uses": "Thyme (Thymus vulgaris) is an herb with a distinct smell. The flowers, leaves, and oil are commonly "
                "used to flavor foods and are also used as medicine. Thyme contains chemicals that might help "
                "bacterial and fungal infections. It also might help relieve coughing and have antioxidant effects.",
        "origin": "Pakistan"
    },
    {
        "id": 5,
        "name": "Mint",
        "price": 2,
        "image": "@/assets/Mint.png",
        "description": "Mints have square stems and opposite aromatic leaves. Many can spread vegetatively by stolons "
                       "and can be aggressive in gardens. The small flowers are usually pale purple, pink, "
                       "or white in colour and are arranged in clusters, either forming whorls or crowded together in "
                       "a terminal spike",
        "uses": "Eating fresh or dried leaves: Used to treat bad breath. Inhaling essential oils: May improve brain "
                "function and cold symptoms. Applying it to the skin",
        "origin": "Europe"
    },
]


@app.get("/api/herbs")
def get_herbs():
    return herbs


@app.get("/api/herbs/{herb_id}")
def get_herb_detail(herb_id: int):
    herb = next((h for h in herbs if h["id"] == herb_id), None)
    if herb is None:
        return {"error": "Herb not found"}
    return herb


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
