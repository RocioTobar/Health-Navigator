# Builds subtitle files from the voice-over script, one cue per sentence,
# spread across each scene's window in proportion to sentence length.
import re, sys
VO = {
 'en': [
  (0.3, 3.8, "[Receptionist, speaking fast in German]"),
  (4.0, 5.9, "Total blank. Every word feels like a wall."),
  (6.1, 12, "Hi, I'm Rocío from [country]. I study [degree] in Wuppertal, and I've been that patient."),
  (12.2, 22, "Over 400,000 international students live in Germany, plus millions of international workers. Many put off seeing a doctor. Not because of money, but because of language, appointments and paperwork."),
  (22.2, 34, "Health Navigator explains German healthcare in your language. What your insurance covers. Which doctor you need, and the booking. Live translation at the appointment. And step-by-step guides."),
  (34.2, 44, "Doctolib books appointments. Insurance apps explain their own policies. Translation apps don't know medicine. Health Navigator guides the whole journey, from first symptom to treatment."),
  (44.2, 54, "It's free to start. Premium costs €2.99 a month, and universities and insurers pay licenses for their international members. We start in Wuppertal, then NRW, then all of Germany."),
  (54.2, 59.8, "Health Navigator. Healthcare in your language."),
 ],
 'de': [
  (0.3, 0.9, "Guten Tag! Haben Sie einen Termin?"),
  (1.0, 1.6, "Versichertenkarte, bitte."),
  (1.7, 2.1, "Gesetzlich oder privat?"),
  (2.2, 2.6, "Haben Sie eine Überweisung vom Hausarzt?"),
  (2.7, 3.8, "Brauchen Sie auch eine Krankmeldung?"),
  (4.0, 5.9, "Kopf leer. Jedes Wort fühlt sich an wie eine Wand."),
  (6.1, 12, "Hallo, ich bin Rocío aus [Land]. Ich studiere [Fach] in Wuppertal und war selbst diese Patientin."),
  (12.2, 22, "Über 400.000 internationale Studierende leben in Deutschland, dazu Millionen internationale Fachkräfte. Viele schieben den Arztbesuch auf. Nicht wegen Geld, sondern wegen Sprache, Terminen und Formularen."),
  (22.2, 34, "Health Navigator erklärt das Gesundheitssystem in deiner Sprache. Was deine Versicherung zahlt. Welche Praxis du brauchst, samt Termin. Live-Übersetzung beim Arzt. Und Schritt-für-Schritt-Guides."),
  (34.2, 44, "Doctolib bucht Termine. Kassen-Apps erklären ihren eigenen Tarif. Übersetzer-Apps kennen keine Medizin. Health Navigator begleitet den ganzen Weg, vom ersten Symptom bis zur Behandlung."),
  (44.2, 54, "Der Einstieg ist kostenlos. Premium kostet 2,99 € im Monat, und Hochschulen und Krankenkassen zahlen Lizenzen für ihre Internationals. Wir starten in Wuppertal, dann NRW, dann ganz Deutschland."),
  (54.2, 59.8, "Health Navigator. Gesundheit in deiner Sprache."),
 ],
}
def ts(t):
    ms = round(t*1000); return f"{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}"
for lang, scenes in VO.items():
    out, n = [], 0
    for a, b, text in scenes:
        parts = [p for p in re.split(r'(?<=[.!?])\s+', text) if p]
        total = sum(len(p) for p in parts); t = a
        for p in parts:
            d = (b - a) * len(p) / total; n += 1
            out.append(f"{n}\n{ts(t)} --> {ts(t+d-0.05)}\n{p}\n"); t += d
    open(f"{sys.argv[1]}/subtitulos-{lang.upper()}.srt", 'w').write('\n'.join(out))
    words = sum(len(s[2].split()) for s in scenes); print(lang, words, 'words')
