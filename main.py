from modules.sop_engine import SOPEngine

print("=" * 80)
print("SOP INTELLIGENCE PLATFORM")
print("=" * 80)

engine = SOPEngine(
    "SOPs/SOP - Bank Account Management version 1.1.docx"
)

engine.run()

print("\n")
print("=" * 80)
print("PROCESS COMPLETED")
print("=" * 80)

