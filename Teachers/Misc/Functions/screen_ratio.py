def screen_ratio(width, height):
    base = width//16 if width/height < 16/9 else height//9
    return base * 16, base * 9