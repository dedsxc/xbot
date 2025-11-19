import time, json

# Common
from internal.config import config
from common.logger import log

# Selenium 4
from selenium_stealth import stealth
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def sanitize_cookie(cookie):
    same_site = cookie.get("sameSite")
    if same_site not in ("Strict", "Lax", "None"):
        cookie["sameSite"] = "Lax"
    cookie.pop("hostOnly", None)
    cookie.pop("session", None)
    return cookie

def import_external_cookies(driver, cookie_file, url):
    driver.get(url)
    time.sleep(5)

    with open(cookie_file, "r") as f:
        cookies = json.load(f)
    fixed_cookies = [sanitize_cookie(c) for c in cookies]

    for c in fixed_cookies:
        try:
            driver.add_cookie(c)
        except Exception as e:
            print(f"❌ Erreur cookie {c.get('name')}: {e}")

    driver.refresh()
    print(f"✅ {len(fixed_cookies)} cookies importés avec succès")

def tweet_with_media(filename=None, tweet_text=None, tweet_comment=None):
    # Tweet status with media
    options = Options()
    options.add_argument("--incognito")
    options.add_argument("--headless")
    # Disable DevTools
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager().install()), options=options)
    driver.set_window_size("800", "1600")
    stealth(
            driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
    )
    # --- import cookie file ---
    cookie_file = config.get('global', 'cookie_file', fallback=None)
    import_external_cookies(driver, cookie_file, "https://x.com")
    driver.get("https://x.com")

    try:
        twitter_post_media_selenium(driver, tweet_text, filename)
    except Exception as e:
        driver.save_screenshot("screenshot/error.png")
        log.error("[twitter_connect_selenium] Error while connect in twitter with selenium: {}".format(e))
    finally:
        driver.quit()

def twitter_post_media_selenium(driver, status, filename=None):
    # Wait for block to write comment
    WebDriverWait(driver, int(config.getint('global', 'selenium_timeout'))).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'public-DraftStyleDefault-block')]")))
    driver.find_element(By.XPATH, "//div[contains(@class, 'public-DraftStyleDefault-block')]").send_keys(status)
    if filename is not None:
        if isinstance(filename, (list, tuple)):
            files = "\n".join(filename)
            driver.find_element(By.XPATH, "//input[@data-testid='fileInput']").send_keys(files)
        else:
            driver.find_element(By.XPATH, "//input[@data-testid='fileInput']").send_keys(filename)
        driver.save_screenshot("screenshot/status_post.png")

    # Wait for media to be uploaded
    time.sleep(config.getint('global', 'selenium_timeout'))

    # Wait for post button to be accessible with aria-disabled="false"
    WebDriverWait(driver, int(config.getint('global', 'selenium_timeout'))).until(
        lambda d: d.find_element(By.XPATH, "//button[@data-testid='tweetButtonInline']").get_attribute("aria-disabled") != "true")
    driver.find_element(By.XPATH, "//button[@data-testid='tweetButtonInline']").click()
    driver.save_screenshot("screenshot/last_media_upload.png")
    # Wait for media to be uploaded
    time.sleep(config.getint('global', 'selenium_timeout'))
    log.info("[twitter_post_media_selenium] post media successfull")
