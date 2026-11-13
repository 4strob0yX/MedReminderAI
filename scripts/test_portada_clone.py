import docx

doc = docx.Document('/Users/4strob0y/Developer/MedReminderAI/docs/Portada.docx')
print("Paragraphs in Portada:", len(doc.paragraphs))
# Modify paragraph 8 and 9
for i, p in enumerate(doc.paragraphs):
    if "NOMBRE DEL TRABAJO:" in p.text:
        print(f"Found at P{i}: {p.text}")
    if "PROYECTO INTEGRADOR" in p.text:
        print(f"Found at P{i}: {p.text}")

