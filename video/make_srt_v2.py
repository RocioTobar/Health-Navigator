# Subtitles for the short-film version (v2). One cue per line of dialogue.
import sys
CUES = {
 'de': [
  (0.6, 1.8, "Guten Tag! Haben Sie einen Termin?"), (1.9, 2.9, "Versichertenkarte, bitte."),
  (3.0, 3.9, "Gesetzlich oder privat?"), (4.0, 4.8, "Haben Sie eine Überweisung vom Hausarzt?"),
  (4.9, 6.4, "Brauchen Sie auch eine Krankmeldung?"), (7.2, 8.8, "Ja… ja, genau."),
  (9.6, 11.4, "Mama… ich habe nichts verstanden."), (11.5, 13.6, "Ich habe mich geschämt, nachzufragen."),
  (14.2, 17.4, "Ich bin Rocío und studiere [Fach] hier in Wuppertal."), (17.5, 20.8, "Und ich bin eine von über 400.000 internationalen Studierenden in Deutschland."),
  (24.0, 25.6, "Guten Tag! Haben Sie einen Termin?"), (26.5, 28.5, "Ja, um zehn Uhr fünfzehn. Hier ist meine Karte."),
  (34.8, 35.9, "Gute Besserung!"), (36.0, 37.0, "Danke!"),
  (37.8, 40.2, "Übersetzer-Apps kennen Wörter, keine Medizin."), (40.3, 42.2, "Doctolib bucht Termine, erklärt aber nichts."),
  (42.3, 44.2, "Kassen-Apps kennen nur ihren eigenen Tarif."), (44.3, 46.3, "Wir begleiten dich durch den ganzen Arztbesuch."),
  (46.8, 49.0, "Kostenlos für Studierende, Premium für 2,99 € im Monat."), (49.1, 51.4, "Hochschulen und Krankenkassen zahlen Lizenzen."),
  (51.5, 54.2, "Wir starten in Wuppertal, dann NRW, dann ganz Deutschland."),
  (54.6, 57.0, "Niemand sollte nicken müssen, ohne zu verstehen."),
 ],
 'en': [
  (0.6, 6.4, "[Receptionist, speaking fast in German]"), (7.2, 8.8, "Ja… ja, genau. (Yes… yes, exactly.)"),
  (9.6, 11.4, "Mom… I didn't understand anything."), (11.5, 13.6, "I was too embarrassed to ask."),
  (14.2, 17.4, "I'm Rocío, and I study [degree] here in Wuppertal."), (17.5, 20.8, "And I'm one of over 400,000 international students in Germany."),
  (24.0, 25.6, "Good morning! Do you have an appointment?"), (26.5, 28.5, "Yes, at 10:15. Here's my card."),
  (34.8, 35.9, "Get well soon!"), (36.0, 37.0, "Thank you!"),
  (37.8, 40.2, "Translator apps know words, not medicine."), (40.3, 42.2, "Doctolib books a slot, but explains nothing."),
  (42.3, 44.2, "Insurance apps only know their own policy."), (44.3, 46.3, "We're with you for the whole visit."),
  (46.8, 49.0, "Free for students. Premium for €2.99 a month."), (49.1, 51.4, "Universities and insurers pay for licenses."),
  (51.5, 54.2, "We start in Wuppertal, then NRW, then all of Germany."),
  (54.6, 57.0, "Nobody should have to nod without understanding."),
 ],
}
def ts(t):
    ms = round(t*1000); return f"{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}"
for lang, cues in CUES.items():
    open(f"{sys.argv[1]}/subtitulos-{lang.upper()}.srt", 'w').write('\n'.join(f"{i}\n{ts(a)} --> {ts(b)}\n{t}\n" for i, (a, b, t) in enumerate(cues, 1)))
