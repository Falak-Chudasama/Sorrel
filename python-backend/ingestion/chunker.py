import re
import os
from dotenv import load_dotenv

load_dotenv()

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 400))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 60))

def chunk_sections(sections: list[dict]) -> list[dict]:
    all_chunks = []
    global_chunk_index = 0
    for section in sections:
        section_chunks = _split_section(section)
        for chunk in section_chunks:
            chunk["chunk_index"] = global_chunk_index
            global_chunk_index += 1
            all_chunks.append(chunk)
    return all_chunks

def _split_section(section: dict) -> list[dict]:
    text = section["text"]
    words = text.split()
    if len(words) <= CHUNK_SIZE:
        return [_make_chunk(text, text, section, 0)]
    
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current_words = []
    chunk_position = 0
    
    for paragraph in paragraphs:
        para_words = paragraph.split()
        if len(current_words) + len(para_words) <= CHUNK_SIZE:
            current_words.extend(para_words)
        else:
            if current_words:
                chunk_text = " ".join(current_words)
                chunks.append(_make_chunk(chunk_text, text, section, chunk_position))
                chunk_position += 1
                current_words = current_words[-CHUNK_OVERLAP:]
            if len(para_words) > CHUNK_SIZE:
                sentence_chunks = _split_by_sentences(paragraph, text, section, chunk_position)
                chunks.extend(sentence_chunks)
                chunk_position += len(sentence_chunks)
                current_words = []
            else:
                current_words = para_words
                
    if current_words:
        chunk_text = " ".join(current_words)
        chunks.append(_make_chunk(chunk_text, text, section, chunk_position))
    return chunks if chunks else [_make_chunk(text[:2000], text, section, 0)]

def _split_by_sentences(text: str, parent_text: str, section: dict, start_pos: int) -> list[dict]:
    sentence_endings = re.compile(r'(?<=[.!?])\s+')
    sentences = sentence_endings.split(text)
    chunks = []
    current_words = []
    chunk_position = start_pos
    for sentence in sentences:
        sentence_words = sentence.split()
        if len(current_words) + len(sentence_words) <= CHUNK_SIZE:
            current_words.extend(sentence_words)
        else:
            if current_words:
                chunk_text = " ".join(current_words)
                chunks.append(_make_chunk(chunk_text, parent_text, section, chunk_position))
                chunk_position += 1
                current_words = current_words[-CHUNK_OVERLAP:]
            current_words = sentence_words
    if current_words:
        chunks.append(_make_chunk(" ".join(current_words), parent_text, section, chunk_position))
    return chunks

def _make_chunk(chunk_text: str, parent_text: str, section: dict, position: int) -> dict:
    source_file = section["source_file"]
    section_heading = section["section_heading"]
    context_prefix = f"[Source: {source_file} | Section: {section_heading}]\n"
    enriched_text = context_prefix + chunk_text
    return {
        "text": chunk_text,
        "parent_text": parent_text,
        "enriched_text": enriched_text,
        "source_file": source_file,
        "doc_type": section["doc_type"],
        "section_heading": section_heading,
        "page_number": section.get("page_number"),
        "chunk_position": position
    }