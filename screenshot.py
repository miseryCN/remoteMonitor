from PIL import ImageGrab


def screen_shot(save_path):
    image = ImageGrab.grab()
    image.save(save_path)
    return image