from .constants import LaceDatasetType


DATASET_TEXT_FIELDS: dict[LaceDatasetType, list[str]] = {
    LaceDatasetType.OCR: ["post_ocr_text"],
    LaceDatasetType.POST_OCR: ["ocr_text", "lace_text", "post_ocr_text"]
}
