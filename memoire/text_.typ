#set heading(numbering: "1.1")
#show heading: set block(above: 2em, below: 2em)

// document *metadata*
#set document(
  title: "Conception d’un système de surveillance pour la modernisation de la maintenance conditionnelle des machines tournantes au sein de la STE d'Aïn Tinn",
  author: "one, two, three",
  description: "a description here",
  keywords: ("wd1", "wd2"),
  date: datetime.today(),
)

// page adjustments
#set page(
  fill: rgb("#444444"),
  paper: "a4",
  margin: 1in,
  numbering: "1",
)
// text font, size, lang and hyphenation
#set text(
  font: "Times New Roman",
  size: 12pt,
  fill: rgb("#ffffff"),
  lang: "en",
)

#set par(
  justify: true,
  first-line-indent: 2em,
)
#title(
  "Conception d’un système de surveillance pour la modernisation de la maintenance conditionnelle des machines tournantes au sein de la STE d'Aïn Tinn",
)

= industrial maintenance, general defintions

#table(
  columns: (auto, auto),
  stroke: none,
  table.hline(stroke: 0.2em),
  table.header([*Column 1*], [*Column 2*]),
  table.hline(stroke: 0.1em),
  "entry1", "entry2",
)

#lorem(100)

#lorem(60)


== code blocks

#figure(
  caption: [A python code block],
  ```python
  def fun(i:int) -> float:
    return i**2
  ```,
) <python-hello>

#lorem(200)

python @python-hello
