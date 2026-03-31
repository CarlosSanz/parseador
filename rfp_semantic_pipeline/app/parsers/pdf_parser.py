from pathlib import Path

import fitz
import pdfplumber

from app.models.schemas import PageBlock, Section


class PDFParser:
    def parse_pages(self, file_path: Path) -> list[PageBlock]:
        pages: list[PageBlock] = []
        try:
            with fitz.open(file_path) as doc:
                for idx, page in enumerate(doc):
                    pages.append(PageBlock(page_num=idx + 1, text=page.get_text("text"), source_file=file_path.name))
        except Exception:
            with pdfplumber.open(file_path) as pdf:
                for idx, page in enumerate(pdf.pages):
                    pages.append(PageBlock(page_num=idx + 1, text=page.extract_text() or "", source_file=file_path.name))
        return pages

    def detect_sections(self, pages: list[PageBlock]) -> list[Section]:
        sections: list[Section] = []
        current_section = None
        for page in pages:
            lines = [line.strip() for line in page.text.splitlines() if line.strip()]
            for line in lines[:8]:
                if line[:2].isdigit() and "." in line[:6]:
                    section_code = line.split(" ")[0]
                    title = line.replace(section_code, "", 1).strip() or "Untitled"
                    section_id = f"sec_{len(sections)+1}"
                    sections.append(
                        Section(
                            section_id=section_id,
                            section_code=section_code,
                            section_title=title,
                            page_start=page.page_num,
                            page_end=page.page_num,
                        )
                    )
                    current_section = sections[-1]
                    break
            if current_section and current_section.page_end < page.page_num:
                current_section.page_end = page.page_num
        if not sections and pages:
            sections.append(
                Section(
                    section_id="sec_1",
                    section_code="0",
                    section_title="Documento completo",
                    page_start=1,
                    page_end=pages[-1].page_num,
                )
            )
        return sections
