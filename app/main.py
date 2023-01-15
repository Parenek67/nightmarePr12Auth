from fastapi import FastAPI, HTTPException, Depends

from .database import get_db
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

###### jaeger
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

resource = Resource(attributes={
    SERVICE_NAME: "auth-service"
})

jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(jaeger_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

FastAPIInstrumentor.instrument_app(app)
#####

##### prometheus
from prometheus_fastapi_instrumentator import Instrumentator

@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)
    
#####
@app.post("/v1/postusers/")
async def create(details: schemas.CreateUser, db: Session = Depends(get_db)):
    to_create = models.User(
        name = details.name,
        login = details.login,
        password = details.password
    )
    db.add(to_create)
    db.commit()
    return {
        "success": True,
        "created_id":to_create.id
    }

@app.get("/v1/users/{login}/{password}")
async def auth(login:str, password:str, db: Session = Depends(get_db)):
    result = crud.auth(db, login, password)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@app.get("/v1/users/")
async def get_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return crud.get_users(db, skip=skip, limit=limit)

@app.get("/__health")
async def health_check():
    return