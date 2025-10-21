from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import threading
import queue

# Common
from common.logger import log
from internal.models.buymeacoffee import CoffeeEvent
from internal.api.browser import tweet_with_media

app = FastAPI()
tweet_queue = queue.Queue()

def tweet_worker():
    while True:
        tweet_task = tweet_queue.get()
        if tweet_task is None:
            break
        try:
            tweet_with_media(**tweet_task)
        except Exception as e:
            log.error(f"Tweet failed: {e}")
        tweet_queue.task_done()
        
worker_thread = threading.Thread(target=tweet_worker, daemon=True)
worker_thread.start()

@app.get("/health")
async def health_check():
    return JSONResponse(content={"status": "OK"})

@app.post("/buymeacoffee")
async def buy_me_a_coffee(event: CoffeeEvent):
    try:
        data = event.data
    except Exception as e:
        log.error(f"[BuyMeACoffee] Invalid JSON: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    supporter_name = data.supporter_name or "Someone"
    note = data.support_note or ""
    amount = data.amount or 0
    currency = data.currency or ""

    log.info(f"[BuyMeACoffee] {supporter_name} gave {amount} {currency}")

    tweet_text = (
        f"✨ {supporter_name} just gave {amount} {currency} ! ✨\n"
        f"Note: {note if note else '(none)'}\n\n"
        f"Thank you {supporter_name} ! ⭐ \n"
    )
    
    tweet_task = {
        "filename": None,
        "tweet_text": tweet_text,
        "tweet_comment": None
    }

    log.info(f"[BuyMeACoffee] Queued tweet for {supporter_name}")
    tweet_queue.put(tweet_task)

    return {"status": "success"}

def start_server(port: int):
    def run():
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="error")
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    log.info(f"[http] Listening on port {port}...")
    return thread