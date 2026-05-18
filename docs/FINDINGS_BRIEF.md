# Alberta's Two Electoral Maps: What the Numbers Show

**A plain-language summary — May 2026**

---

## What happened

Alberta has 89 seats in its legislature. To decide which communities each seat represents, the province uses an independent commission — a group of five appointed people who draw the riding boundaries. (A "riding" is your local electoral district, the area you share with your MLA.) In 2025-26, the commission could not agree. Three members produced one map. Two members produced a different map.

On April 16, 2026, the provincial government rejected both commission maps and handed the job to a five-person committee of MLAs. Three of the five MLAs are from the governing United Conservative Party (UCP).

This audit used math and computer simulations to ask: do the two commission maps treat both parties' voters equally?

---

## Why riding boundaries matter

Where the lines go matters a lot. Move a few streets one direction and a city neighbourhood ends up paired with a rural area. Move them the other way and it stays with other city residents. Those choices can change how many seats each party wins — even if every single vote stays the same. That is what this audit measures.

---

## Finding 1: The ridings aren't the same size

Every riding should hold roughly the same number of people. That way, your vote counts about as much as anyone else's.

- Under the **majority map**: the average riding is off from the ideal by about **3,180 people**.
- Under the **minority map**: the same gap is **4,707 people — 48% worse**.

Bigger gaps mean some ridings are much more crowded than others. A vote in a small, sparse riding carries more weight than a vote in an overcrowded one.

---

## Finding 2: At a 50/50 tied vote, one map gives the UCP 5 extra seats

Imagine every Alberta voter split exactly 50-50 between the NDP and UCP. What would happen?

| Map | NDP seats | UCP seats |
|---|---|---|
| Majority map | **48** | 41 |
| Minority map | **43** | 46 |

That is a **5-seat swing** to the UCP — without changing a single vote. Just by drawing the lines differently.

To check how unusual this is, a computer program drew **1,010,000 random Alberta maps**, all following the same rules the commission had to follow. The majority map's result looked normal — it sits in the middle of the pack. The minority map's result was extreme: **fewer than 100 of the 1,010,000 random maps** produced a result that far in favour of the UCP.

---

## Finding 3: NDP votes are wasted at a much higher rate under the minority map

Every election, some votes are "wasted." A vote is wasted if it goes to a candidate who lost. A vote is also wasted if it gets piled onto a winner who already had more than enough votes to win. When one party's votes are wasted at a much higher rate than the other's, that party needs more total votes to win the same number of seats.

Think of it this way. Say you have a bag of coins and you want to win as many games as possible. If you spend way more coins than you need in games you'd win easily anyway, those extra coins did nothing. Your opponent, spending just enough to win every close game, gets more wins per coin.

Across 896,644 votes cast for the two main parties in 2023:

- Under the **majority map**: NDP voters wasted roughly **881 more votes** than UCP voters — about 0.1% of all ballots.
- Under the **minority map**: NDP voters wasted roughly **36,000 more votes** than UCP voters — about 4.0% of all ballots.

The minority map's gap is about **41 times larger**. Both gaps favour the UCP.

---

## Finding 4: Airdrie and northwest Calgary

**Airdrie** is a city of about 85,000 people — bigger than Red Deer. It has one city council, one school board, and one tax bill. The majority map splits Airdrie between **2 ridings**. The minority map splits it between **4 ridings**, each one attached to a different rural or Calgary-edge area. With four different MLAs, no single politician is primarily there for Airdrie as a whole city.

**Northwest Calgary** is a largely UCP-supporting area. The minority map packs **11.5% more people than average** into that area's ridings. That means lots of extra UCP votes pile up in ridings they already win easily — while other ridings have more competition per seat. The majority map has northwest Calgary only **2.8% above average**.

---

## What this audit does NOT say

**It does not say either map is a "gerrymander."** "Gerrymander" is an American legal term for a specific kind of unconstitutional voting map. Canada doesn't have that law. In Canada, the legal question is whether voters have "effective representation" under the *Charter of Rights and Freedoms* and whether the commission followed the *Electoral Boundaries Commission Act*. That question belongs to courts and legislators — not this audit.

**It does not say anyone did this on purpose.** The numbers show what the maps *do*, not what the people who drew them *intended*. Statistics cannot prove intent.

**It already accounts for geography.** NDP voters are concentrated in city cores. Even a perfectly neutral map tends to give the NDP a slight disadvantage, because voters packed together in a few ridings win big there but don't have leftover votes to compete in surrounding areas. The 1,010,000 random maps in the simulation were drawn using actual Alberta geography, so this is already baked in. The minority map's numbers are still extreme compared to those neutral draws.

---

## How the analysis was done

All results use the official Elections Alberta maps, received May 6, 2026. The 2023 election results were matched to each riding by finding which riding each polling station fell inside.

The 1,010,000 random maps were generated by a computer program that redraws riding boundaries under the same rules the commission had — same population limits, same province, same geography. This is a standard tool in redistricting research.

All tests were written down and locked in before the results were examined. This is called "pre-registration" and it prevents a researcher from running many tests and only reporting the ones that look good. The registrations are filed publicly at OSF:6pt83, AsPredicted:#289,469, and AsPredicted:#289,451.

---

## About me

I'm a student at Mount Royal University. I did this research on my own — it wasn't assigned as coursework and the university didn't commission it. My opinions are my own and don't represent the university. I have no connection to Elections Alberta, the commission, or any political party.

I have donated to and volunteered for the NDP in the past, and have also donated to parties on the other side of Alberta politics. I'm telling you that because my political history could affect how I look at this issue. The main protection against that bias is the method: I tested both maps the same way, I wrote down my predictions before looking at the results, and all the data and code are public so anyone can check my work. I funded this research myself.

---

*Full public report (longer, with maps): [`report_public.md`](https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/main/reports/public/report_public.md)*
*Full technical report: [`report_academic.md`](https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/main/reports/academic/report_academic.md)*
*All data and code: [github.com/Ixby/alberta-electoral-boundaries-audit](https://github.com/Ixby/alberta-electoral-boundaries-audit)*
