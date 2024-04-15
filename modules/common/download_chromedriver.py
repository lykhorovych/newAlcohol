import subprocess
import os
import stat
import logging
import wget
from zipfile import ZipFile
from chromedriver_py import binary_path

logger = logging.getLogger(__name__)


def find_chrome_executable():
    """
    Finds the chrome, chrome beta, chrome canary, chromium executable

    Returns
    -------
    executable_path :  str
        the full file path to found executable

    """
    candidates = []
    for item in os.environ.get("PATH").split(os.pathsep):
        for subitem in (
                "google-chrome",
                "chromium",
                "chromium-browser",
                "chrome",
                "google-chrome-stable",):
            candidates.append(os.sep.join((item, subitem)))

    for candidate in candidates:
        if os.path.exists(candidate) and os.access(candidate, os.X_OK):
            print(os.path.exists(candidate))
            logger.debug('found! using %s' % candidate)
            return os.path.normpath(candidate)


def _check_equality_version(chrome_path, chromedriver_path):
    google_version = chromedriver_version = ""

    cmd_1 = subprocess.run(
        [
            chrome_path,
            "--version",
         ],
        capture_output=True)
    if cmd_1.returncode == 0:
        google_version = cmd_1.stdout.decode('utf-8').rstrip().split(" ")[-1]

    cmd_2 = subprocess.run(
    [
        chromedriver_path,
        "--version",
    ],
        capture_output=True)

    if cmd_2.returncode == 0:
        chromedriver_version = cmd_2.stdout.decode("utf-8").rstrip().split(" ")[1]

    print("google version is {}".format(google_version),
          "chromedriver version is {}".format(chromedriver_version))

    if google_version == chromedriver_version:
        print("The chromedriver version is equal to google-chrome version")
        return True, google_version
    else:
        print("The chromedriver version is not equal to google")
        return False, google_version


def download_appropriate_chromedriver(version):
    result = subprocess.run(["pip", "install", f"chromedriver-py=={version}"], capture_output=True)
    if result.returncode == 1:
        print("Could not find a version of chromedriver that satisfies the requirement")
        os.remove(binary_path)  # removing before version of chromedriver
        link = f"https://storage.googleapis.com/chrome-for-testing-public/{version}/linux64/chromedriver-linux64.zip"
        print("Downloading chromedriver from another link {}".format(link))
        base_dir = os.path.dirname(binary_path)
        filename = wget.download(link, out=base_dir)  # downloading chromedriver.zip to base dir
        if os.path.exists(filename):
            with ZipFile(filename, 'r') as zip_obj:  # unzipping chromedriver.zip
                zip_obj.extract(member='chromedriver-linux64/chromedriver', path=base_dir)

            os.remove(filename)
            path_to_chromedriver = os.path.join(base_dir, os.path.basename(filename)[:-4])
            os.rename(os.path.join(path_to_chromedriver, "chromedriver"),
                      os.path.join(base_dir, "chromedriver_linux64"))
            if not os.access(os.path.join(base_dir, "chromedriver_linux64"), os.X_OK):
                os.chmod(os.path.join(base_dir, "chromedriver_linux64"), stat.S_IRWXU)
            os.rmdir(path_to_chromedriver)


def check_equality_version():
    chrome_executable = find_chrome_executable()
    status, version = _check_equality_version(chrome_executable, binary_path)
    if not status:
        download_appropriate_chromedriver(version)
        _check_equality_version(chrome_executable, binary_path)
    return chrome_executable, binary_path
