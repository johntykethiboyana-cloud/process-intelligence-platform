import re
from collections import Counter

class SOPParser:
    """
    Production-oriented SOP parser.
    Input:
        paragraphs = [
            {"text": "...", "style": "Heading 1"},
            ...
        ]
    """

    APPLICATIONS = {
        "gcss","sap","aris","sharepoint","outlook",
        "excel","power bi","salesforce","teams"
    }

    ACTIONS = [
        "open","click","select","create","update","delete","approve",
        "reject","enter","search","save","submit","login","upload",
        "download","copy","paste","assign","verify","review","close",
        "navigate","access"
    ]

    STOPWORDS = {
        "the","a","an","to","of","for","and","or","on","in","at",
        "with","from","by","is","are","be","as","this","that","then",
        "please","kindly","now","next"
    }

    def __init__(self, paragraphs):
        self.paragraphs = paragraphs

    # ---------------------- Cleaning ----------------------

    def clean_text(self, text):
        if not text:
            return ""
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"Page\s+\d+\s+of\s+\d+", "", text, flags=re.I)
        text = re.sub(r"^\d+[\.\)]\s*", "", text)
        replacements = {
            "click on":"click",
            "navigate to":"open",
            "go to":"open",
            "browse to":"open",
            "log into":"login",
            "log in to":"login",
            "sign into":"login",
            "choose":"select",
        }
        text = text.lower()
        for k,v in replacements.items():
            text = text.replace(k,v)
        text = re.sub(r"\s+"," ",text)
        return text.strip()

    # ---------------------- Detection ----------------------

    def is_heading(self, text, style):
        return (
            "Heading" in style or
            (len(text) < 80 and text.isupper())
        )

    def is_numbered_step(self, text):
        pats = [
            r'^\d+\.',
            r'^\d+\)',
            r'^step\s+\d+',
            r'^\(\d+\)',
            r'^\d+\s*-'
        ]
        return any(re.match(p,text,re.I) for p in pats)

    def is_bullet(self,text):
        return text.startswith(("•","-","*","►","▪"))

    def is_note(self,text):
        t=text.lower()
        return t.startswith(("note","important","warning","remarks"))

    def is_image_caption(self,text):
        t=text.lower()
        keys=["figure","screenshot","image","refer below","below screen"]
        return any(k in t for k in keys)

    # ---------------------- NLP Lite ----------------------

    def extract_action(self,text):
        t=self.clean_text(text)
        for a in self.ACTIONS:
            if re.search(rf"\b{re.escape(a)}\b",t):
                return a
        return ""

    def extract_application(self,text):
        t=self.clean_text(text)
        for app in self.APPLICATIONS:
            if app in t:
                return app.upper() if app!="power bi" else "Power BI"
        return ""

    def extract_business_object(self,text):
        t=self.clean_text(text)
        action=self.extract_action(t)
        if action:
            m=re.search(rf"{action}\s+(.*)",t)
            if m:
                return m.group(1).strip(" .:-")
        return t

    def extract_keywords(self,text,limit=8):
        words=re.findall(r"[a-zA-Z0-9]+",self.clean_text(text))
        words=[w for w in words if w not in self.STOPWORDS and len(w)>2]
        return [w for w,_ in Counter(words).most_common(limit)]

    # ---------------------- Sections ----------------------

    def build_sections(self):
        sections={}
        current="Introduction"
        sections[current]=[]

        for para in self.paragraphs:
            raw=para.get("text","").strip()
            style=para.get("style","").strip()

            if not raw:
                continue
            if self.is_image_caption(raw):
                continue

            if self.is_heading(raw,style):
                current=raw.strip()
                sections.setdefault(current,[])
                continue

            clean=self.clean_text(raw)

            if self.is_numbered_step(raw):
                typ="step"
            elif self.is_bullet(raw):
                typ="bullet"
            elif self.is_note(raw):
                typ="note"
            else:
                typ="paragraph"

            sections[current].append({
                "type":typ,
                "text":raw,
                "clean_text":clean
            })

        return sections

    # ---------------------- Chunk Builder ----------------------

    def build_chunks(self):
        chunks=[]
        sections=self.build_sections()

        for heading,items in sections.items():
            for item in items:
                txt=item["text"]
                chunks.append({
                    "section":heading,
                    "heading":heading,
                    "step_type":item["type"],
                    "original_text":txt,
                    "clean_text":item["clean_text"],
                    "action":self.extract_action(txt),
                    "business_object":self.extract_business_object(txt),
                    "application":self.extract_application(txt),
                    "keywords":self.extract_keywords(txt)
                })
        return chunks
