
## 1.Nosaukums - The Big O-Block (Snake)

## 2.Mērķis - Vadīt čūsku pa laukumu, ēst parastos ābolus un superābolus, lai audzētu garumu un vāktu pēc iespējas vairāk punktu.   Kā zaudē: Spēle beidzas, ja čūska ietriecas laukuma malā (sienā) vai pati savā astē. Uzvaras nav, mērķis ir sasniegt pēc iespējas lielāku rezultātu.

## 3. WASD un Būltiņas - Kustības taustiņi, Esc - Exit game, R - Restart, Space - Aktivizēt mehāniku Matrix effect, P - Pauze spēles vidū.

## 4. Kustība --> Apēd ābolu (+10pt vai +150pt ja superābols) --> čūska izaug, un ik pēc 150 punktiem paaugstinās līmenis un ātrums.--> Ietriecas sienā vai astē --> Game Over un iespēja sākt no jauna (R).

## 5. Mehānikas - Matrix effect (laika palēnināšana ar Space, patērējot enerģiju) un Superābols (5% iespēja parādīties retajam ābolam, kas dod 150pt 10 vietā).

## 6. Līmeņi - 6 līmeņi, kur katrā nākamajā līmenī čūskas pamata ātrums palielinās. līmenis mainās ik pēc 150pt

## 7. Punkti - Parasts ābols dod +10pt, Superābols dod +100pt.

## 8. Saglabā - Pēc katras spēles klients nosūta spēlētāja vārdu un punktus uz REST API serveri, kas tos glabā SQLite datubāzē. Līderu tabula rāda top 5.