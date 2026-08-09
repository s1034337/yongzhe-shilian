from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter


BASE = Path(__file__).parent
SOURCE = BASE / "assets" / "questions"
OUTPUT = SOURCE / "cropped"
OUTPUT.mkdir(parents=True, exist_ok=True)


def remove_magenta(image: Image.Image) -> Image.Image:
    rgb = image.convert("RGB")
    pixels = rgb.load()
    for y in range(rgb.height):
        for x in range(rgb.width):
            r, g, b = pixels[x, y]
            if r > 145 and b > 80 and r - g > 22 and b - g > 8:
                pixels[x, y] = (255, 255, 255)
    return rgb


def crop_questions(filename: str, crops: list[tuple[int, int, int, int]], start: int) -> None:
    page = remove_magenta(Image.open(SOURCE / filename))
    for offset, box in enumerate(crops):
        question = page.crop(box)
        question.save(OUTPUT / f"question-{start + offset}.png", optimize=True)


def prepare_individual_questions() -> None:
    for number in range(1, 10):
        source = SOURCE / f"source-question-{number}.png"
        question = remove_magenta(Image.open(source))
        if number == 1:
            question = question.resize(
                (question.width * 4, question.height * 4),
                Image.Resampling.LANCZOS,
            )
            question = ImageEnhance.Contrast(question).enhance(1.18)
            question = question.filter(
                ImageFilter.UnsharpMask(radius=1.5, percent=190, threshold=2)
            )
        question.save(OUTPUT / f"question-{number}.png", optimize=True)


crop_questions("practice-1.png", [(12, 20, 865, 145)], 1)
crop_questions(
    "practice-2.jpg",
    [
        (8, 8, 825, 120),
        (8, 115, 825, 288),
        (8, 275, 825, 402),
        (8, 385, 825, 518),
        (8, 500, 825, 675),
    ],
    2,
)
crop_questions(
    "practice-3.png",
    [
        (8, 20, 850, 162),
        (8, 145, 850, 225),
        (8, 205, 850, 375),
    ],
    7,
)
prepare_individual_questions()
