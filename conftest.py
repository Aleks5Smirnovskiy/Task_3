import pytest
import requests
import os
from uuid import uuid4
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# webdriver-manager reads environment config during import/runtime.
# Set these early to force cache into project directory on restricted Windows profiles.
os.environ["WDM_LOCAL"] = "1"

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
BASE_URL = "https://qa-stellarburgers.education-services.ru"

PROJECT_TEMP_DIR = Path.cwd() / ".tmp"
PROJECT_TEMP_DIR.mkdir(exist_ok=True)
os.environ["TMP"] = str(PROJECT_TEMP_DIR)
os.environ["TEMP"] = str(PROJECT_TEMP_DIR)
os.environ["MOZ_CRASHREPORTER_DISABLE"] = "1"
os.environ["MOZ_DISABLE_CONTENT_SANDBOX"] = "1"
os.environ["MOZ_DISABLE_RDD_SANDBOX"] = "1"
os.environ["MOZ_DISABLE_GMP_SANDBOX"] = "1"
os.environ["MOZ_SANDBOX"] = "0"
os.environ["MOZ_FORCE_DISABLE_E10S"] = "1"

# Firefox ESR binary: auto-download and extract on first use if not present.
# Firefox beta (system install) crashes with Selenium on restricted Windows environments;
# ESR is stable and works with the sandbox-disabling env vars above.
FIREFOX_ESR_DIR = PROJECT_TEMP_DIR / "FirefoxESR"
FIREFOX_ESR_BIN = FIREFOX_ESR_DIR / "core" / "firefox.exe"


def _ensure_firefox_esr() -> Path:
    """Download and extract Firefox ESR if not already present."""
    if FIREFOX_ESR_BIN.exists():
        return FIREFOX_ESR_BIN

    import subprocess
    import tempfile

    installer = PROJECT_TEMP_DIR / "FirefoxESRSetup.exe"
    if not installer.exists():
        print("\n[conftest] Downloading Firefox ESR...", flush=True)
        esr_url = "https://download.mozilla.org/?product=firefox-esr-latest&os=win64&lang=en-US"
        response = requests.get(esr_url, stream=True, timeout=120)
        response.raise_for_status()
        with open(installer, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

    print("[conftest] Extracting Firefox ESR...", flush=True)
    FIREFOX_ESR_DIR.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["7z", "x", str(installer), f"-o{FIREFOX_ESR_DIR}", "-y"],
        check=True, capture_output=True
    )
    return FIREFOX_ESR_BIN


FIREFOX_BINARY_PATH = _ensure_firefox_esr()


@pytest.fixture(params=["chrome", "firefox"])
def browser(request):
    """Fixture для инициализации браузера Chrome и Firefox"""
    browser_name = request.param
    driver = None

    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument(f"--user-data-dir={PROJECT_TEMP_DIR / f'chrome-profile-{uuid4().hex[:8]}'}")
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--remote-debugging-port=0")
        options.add_argument("--no-first-run")
        options.add_argument("--no-default-browser-check")
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
    elif browser_name == "firefox":
        firefox_profile_root = PROJECT_TEMP_DIR / f"firefox-profile-root-{uuid4().hex[:8]}"
        firefox_profile_root.mkdir(parents=True, exist_ok=True)
        options = webdriver.FirefoxOptions()
        options.add_argument("-headless")
        options.add_argument("--no-remote")
        options.binary_location = str(FIREFOX_BINARY_PATH)
        options.set_preference("browser.cache.disk.parent_directory", str(PROJECT_TEMP_DIR / "firefox-cache"))
        options.set_preference("browser.startup.homepage_override.mstone", "ignore")
        options.set_preference("startup.homepage_welcome_url", "about:blank")
        options.set_preference("startup.homepage_welcome_url.additional", "")
        options.set_preference("toolkit.telemetry.reportingpolicy.firstRun", False)
        options.set_preference("browser.tabs.remote.autostart", False)
        options.set_preference("browser.tabs.remote.autostart.2", False)
        options.set_preference("fission.autostart", False)
        options.set_preference("dom.ipc.processCount", 1)
        options.set_preference("dom.ipc.processCount.web", 1)
        options.set_preference("security.sandbox.content.level", 0)
        driver = webdriver.Firefox(
            service=FirefoxService(
                GeckoDriverManager().install(),
                log_output=str(PROJECT_TEMP_DIR / "geckodriver.log"),
                service_args=["--profile-root", str(firefox_profile_root)]
            ),
            options=options
        )

    driver.implicitly_wait(5)
    yield driver
    driver.quit()
@pytest.fixture
def test_user():
    """Создать тестового пользователя через API и удалить после теста"""
    email = f"autotest_{uuid4().hex[:10]}@mail.ru"
    password = "Password123"
    payload = {
        "email": email,
        "password": password,
        "name": "Auto User"
    }

    response = requests.post(f"{BASE_URL}/api/auth/register", json=payload, timeout=15)
    response.raise_for_status()
    data = response.json()

    user_data = {
        "email": email,
        "password": password,
        "access_token": data["accessToken"],
        "refresh_token": data["refreshToken"]
    }

    yield user_data

    requests.delete(
        f"{BASE_URL}/api/auth/user",
        headers={"Authorization": user_data["access_token"]},
        timeout=15
    )


@pytest.fixture
def logged_in_user(browser, test_user):
    """Авторизовать тестового пользователя через localStorage-токены"""
    browser.get(BASE_URL)
    browser.execute_script(
        "window.localStorage.setItem('accessToken', arguments[0]);"
        "window.localStorage.setItem('refreshToken', arguments[1]);",
        test_user["access_token"],
        test_user["refresh_token"]
    )
    browser.get(f"{BASE_URL}/account/profile")
    WebDriverWait(browser, 15).until(
        EC.url_contains("/account")
    )
    return test_user
