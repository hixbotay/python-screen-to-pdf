import requests
import sys
import os
import time
from PIL import Image

# from io import StringIO

class ScreenCapture:
    file = ''
    def __init__(self):
        return

    def fullpage_screenshot(driver, file,wait = False):
        if(wait!=False):
            time.sleep(wait)
        try:
            total_width = driver.execute_script("return document.body.offsetWidth")
            total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
            viewport_width = driver.execute_script("return document.body.clientWidth")
            viewport_height = driver.execute_script("return window.innerHeight")
            # driver.execute_script("document.styleSheets[0].insertRule('.header-wrapper{ position:inherit!important;left:inherit!important;top:inherit!imporant }')")
        except:
            print('ERROR '+file)
            return False

        rectangles = []

        i = 0

        while i < total_height:
            ii = 0
            top_height = i + viewport_height
            if top_height > total_height:
                top_height = total_height
            while ii < total_width:
                top_width = ii + viewport_width
                if top_width > total_width:
                    top_width = total_width
                rectangles.append((ii, i, top_width,top_height))
                ii = ii + viewport_width
            i = i + viewport_height

        stitched_image = Image.new('RGB', (total_width, total_height))

        previous = None
        part = 0

        for rectangle in rectangles:
            if not previous is None:
                driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
                # print("Scrolled To ({0},{1})".format(rectangle[0], rectangle[1]))
                if(wait!=False):
                    time.sleep(wait)
            file_name = "part_{0}.png".format(part)
            # print("Capturing {0} ...".format(file_name))
            driver.get_screenshot_as_file(file_name)
            screenshot = Image.open(file_name)

            if rectangle[1] + viewport_height > total_height:
                offset = (rectangle[0], total_height - viewport_height)
            else:
                offset = (rectangle[0], rectangle[1])

            # print("Adding to stitched image with offset ({0}, {1})".format(offset[0],offset[1]))
            stitched_image.paste(screenshot, offset)
            del screenshot
            os.remove(file_name)
            part = part + 1
            previous = rectangle

        stitched_image.convert('RGB')
        result = stitched_image.save(file,optimize=True,quality=80)
        # optimize image
        # im = Image.open(file)
        # rgb_im = im.convert('RGB')
        # rgb_im.save(file.replace("png", "jpg"),optimize=True,quality=90)
        # os.remove(file)
        # print("Finishing chrome full page screenshot workaround...")
        return True

