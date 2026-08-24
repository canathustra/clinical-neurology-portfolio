from pathlib import Path


REPORT = Path(r"C:\Users\uugur\OneDrive\Desktop\EMG_NCS_Nonfizyolojik_Faktorler_Sunumu\QA_RAPORU.txt")
LINE = "- Sunum okunabilirlik ölçeği: +%15 (yalnız non-fizyolojik 83 sayfa)\n"


def main() -> None:
    text = REPORT.read_text(encoding="utf-8")
    if LINE.strip() not in text:
        anchor = "- Tam ekran düzenlenen non-fizyolojik sayfa: 83\n"
        if anchor not in text:
            raise SystemExit("Expected QA report anchor not found")
        text = text.replace(anchor, anchor + LINE, 1)
        REPORT.write_text(text, encoding="utf-8")
    print(REPORT)


if __name__ == "__main__":
    main()
